"""M2 -- Map FlowTech SKUs. For every FT- product, set mapped_dri_sku to
the DRI SKU whose description equals the FlowTech description minus the
" (FlowTech)" suffix AND whose list_price_2023 matches. Falls back to
list_price_2019 only when list_price_2023 is None on the FT side.

Real edge cases found in the live sandbox, each
handled deliberately rather than glossed over:
- FT-1442 has list_price_2023 = None. Never match on an absent price
  from either side (None == None is not a real price match) -- but a
  real, non-null fallback exists: FT-1442's list_price_2019 (54590)
  uniquely matches exactly one of the 6 description-matching candidates
  (SM-136), while the other 5 (including SM-130, the other 2023-less
  one) have different 2019 prices. This is matching on two real numbers
  that happen to agree, not guessing -- the fallback only ever fires
  when list_price_2023 is None, and only ever resolves if the 2019-price
  match is itself unique.
- FT-1470's description has the " (FlowTech)" suffix TWICE -- a real
  trailing-suffix strip loop, not a single/global string replace that
  could accidentally corrupt a legitimate mid-string occurrence.

Produces UNIQUE_MATCH / NO_MATCH / MULTIPLE_MATCHES explicitly for every
FT- product rather than silently picking a candidate -- only UNIQUE_MATCH
rows are ever written."""
from typing import Dict, List, Optional

_SUFFIX = " (FlowTech)"


def strip_flowtech_suffix(description: str) -> str:
    while description.endswith(_SUFFIX):
        description = description[: -len(_SUFFIX)]
    return description


def _match_on_field(stripped_description: str, dri_products: List[Dict], field: str, value) -> List[Dict]:
    return [p for p in dri_products if p["description"] == stripped_description and p.get(field) == value]


def find_match(ft_product: Dict, dri_products: List[Dict]) -> Dict:
    """Returns {status, matched_sku, candidates}. status is one of
    UNIQUE_MATCH / NO_MATCH / MULTIPLE_MATCHES -- never silently picks
    among multiple candidates. Field is named matched_sku, not sku,
    deliberately -- see compute_mapping_plan's own note on why."""
    stripped = strip_flowtech_suffix(ft_product["description"])
    ft_price_2023 = ft_product.get("list_price_2023")

    if ft_price_2023 is not None:
        candidates = _match_on_field(stripped, dri_products, "list_price_2023", ft_price_2023)
    else:
        # Fallback: never invoked when list_price_2023 exists, and never
        # matches on a None value from either side -- only when the FT
        # side's 2019 price is itself a real number, matched against the
        # DRI side's real (possibly also-2023-less) list_price_2019.
        ft_price_2019 = ft_product.get("list_price_2019")
        if ft_price_2019 is None:
            return {
                "status": "NO_MATCH", "matched_sku": None, "candidates": [],
                "reason": "FT product has neither list_price_2023 nor list_price_2019",
            }
        candidates = _match_on_field(stripped, dri_products, "list_price_2019", ft_price_2019)

    if len(candidates) == 0:
        return {"status": "NO_MATCH", "matched_sku": None, "candidates": []}
    if len(candidates) > 1:
        return {"status": "MULTIPLE_MATCHES", "matched_sku": None, "candidates": [c["sku"] for c in candidates]}
    return {"status": "UNIQUE_MATCH", "matched_sku": candidates[0]["sku"], "candidates": [candidates[0]["sku"]]}


def compute_mapping_plan(products: List[Dict]) -> Dict:
    ft_products = [p for p in products if p["sku"].startswith("FT-") and p.get("mapped_dri_sku") is None]
    dri_products = [p for p in products if not p["sku"].startswith("FT-")]

    resolved = []  # [{sku, mapped_dri_sku}]
    unresolved = []  # [{sku, status, candidates, ...}]
    for ft in ft_products:
        result = find_match(ft, dri_products)
        if result["status"] == "UNIQUE_MATCH":
            resolved.append({"sku": ft["sku"], "mapped_dri_sku": result["matched_sku"]})
        else:
            # find_match's own "matched_sku" is always None here (that's
            # what NO_MATCH/MULTIPLE_MATCHES means) -- explicitly excluded
            # from the spread so it can never collide with or shadow the
            # real ft["sku"] this row is actually about. A dict-spread
            # ordering bug here previously caused this exact silent loss.
            details = {k: v for k, v in result.items() if k != "matched_sku"}
            unresolved.append({"sku": ft["sku"], **details})

    return {"resolved": resolved, "unresolved": unresolved}


def run_m2(client, dry_run: bool = True) -> Dict:
    data = client.get("/erp/products")
    plan = compute_mapping_plan(data["products"])

    if not dry_run:
        for item in plan["resolved"]:
            client.patch(f"/erp/products/{item['sku']}", {"mapped_dri_sku": item["mapped_dri_sku"]})

    return plan


def verify_m2(client, resolved: List[Dict]) -> List[str]:
    data = client.get("/erp/products")
    by_sku = {p["sku"]: p for p in data["products"]}
    problems = []
    for item in resolved:
        actual = by_sku.get(item["sku"], {}).get("mapped_dri_sku")
        if actual != item["mapped_dri_sku"]:
            problems.append(f"{item['sku']}: expected mapped_dri_sku={item['mapped_dri_sku']!r}, got {actual!r}")
    return problems
