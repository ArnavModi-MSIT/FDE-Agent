"""W3 -- Dedupe the distributor master. Confirmed real duplicate pattern
from the sandbox's own /crm/customers response (see CLAUDE.md sec 9):
85 customers = 40 originals (C-5001..C-5040, clean mixed-case names) +
40 parenthetical-suffix duplicates ("(South)"/"(North)"/"(East)"/
"(West)"/"(II)", C-5041..C-5080, each offset exactly +40 from its
original) + 5 ALL-CAPS duplicates of 5 specific originals (C-5081..
C-5085). No phone/email/GSTIN exist on this schema (confirmed directly)
-- customer_name is the only real signal, so matching is structural
(strip a trailing parenthetical, case-fold), not fuzzy similarity."""
import re
from typing import Dict, List

from api.client import DriClient

_SUFFIX_PATTERN = re.compile(r"\s*\([^)]*\)\s*$")


def normalize_name(name: str) -> str:
    """Strips a trailing parenthetical suffix and case-folds. Two names
    that normalize the same are treated as the same real distributor."""
    return _SUFFIX_PATTERN.sub("", name or "").strip().lower()


def _is_canonical_form(name: str) -> bool:
    """The 'original' record's name has no parenthetical suffix and isn't
    ALL CAPS -- both real duplicate patterns confirmed in the sandbox add
    exactly one of those two transformations, never neither."""
    name = name or ""
    if _SUFFIX_PATTERN.search(name):
        return False
    if name.isupper():
        return False
    return True


def find_merge_plan(customers: List[Dict]) -> List[Dict]:
    """Pure function: customers -> [{legacy_id, merge_into_legacy_id}, ...]
    for every duplicate found. Never touches a customer with no
    duplicates -- "leave every other customer alone," per the task brief.
    Raises if a normalized-name group doesn't have EXACTLY one canonical
    original: ambiguity should escalate, never get silently guessed at."""
    groups: Dict[str, List[Dict]] = {}
    for c in customers:
        key = normalize_name(c["customer_name"])
        groups.setdefault(key, []).append(c)

    plan = []
    for key, group in groups.items():
        if len(group) == 1:
            continue

        originals = [c for c in group if _is_canonical_form(c["customer_name"])]
        if len(originals) != 1:
            ids = [c["legacy_id"] for c in group]
            raise ValueError(
                f"ambiguous group for normalized name {key!r}: "
                f"{len(originals)} canonical candidates among {ids}"
            )
        original = originals[0]
        for c in group:
            if c["legacy_id"] == original["legacy_id"]:
                continue
            plan.append({"legacy_id": c["legacy_id"], "merge_into_legacy_id": original["legacy_id"]})

    return plan


def run_w3(client: DriClient, dry_run: bool = True) -> Dict:
    data = client.get("/crm/customers")
    customers = data["customers"]
    plan = find_merge_plan(customers)

    if not dry_run:
        for item in plan:
            client.patch(f"/crm/customers/{item['legacy_id']}", {"merged_into": item["merge_into_legacy_id"]})

    return {"total_customers": len(customers), "merges_needed": len(plan), "plan": plan}


def verify_w3(client: DriClient, plan: List[Dict]) -> List[str]:
    data = client.get("/crm/customers")
    by_id = {c["legacy_id"]: c for c in data["customers"]}
    problems = []
    for item in plan:
        actual = by_id.get(item["legacy_id"], {}).get("merged_into")
        if actual != item["merge_into_legacy_id"]:
            problems.append(f"{item['legacy_id']}: expected merged_into={item['merge_into_legacy_id']!r}, got {actual!r}")
    return problems
