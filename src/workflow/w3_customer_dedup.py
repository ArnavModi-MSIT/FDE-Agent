"""W3 -- Dedupe the distributor master.

The rule is proven by a real scoring run, not inferred (CLAUDE.md, W3
hypothesis 11, 2026-09-13): merging ONLY the 5 ALL-CAPS records scored
W3 6/6 and Workflow 1.0000, where merging all 45 name-matched records had
held at 5/6 through every other configuration tested.

85 customers = 40 originals (C-5001..C-5040) + 40 records carrying a
trailing "(North)"/"(South)"/"(II)" tag (C-5041..C-5080) + 5 ALL-CAPS
records (C-5081..C-5085).

- The ALL-CAPS records ARE duplicates: the same account re-keyed in
  SalesTrack. All 5 were in SalesTrack at seed and each matches its
  original's tier, region and credit terms exactly.
- The tagged records are NOT duplicates. They are separate accounts that
  happen to share a base name -- most carry a different tier or credit
  terms, and the tag agrees with their own region field in only 7 of 40.
  They fall under the brief's "Leave every other customer alone", even the
  4 whose attributes happen to match their original exactly.

Organizer text says the same: FIX-3415 "at least a handful of distributors
exist twice", EM-106 "names in caps or with AND changed to ampersand".

No phone/email/GSTIN exist on this schema, so matching is structural on
customer_name -- case-fold plus the AND/& equivalence -- never fuzzy."""
import re
from typing import Dict, List

from api.client import DriClient

_AND_WORD_PATTERN = re.compile(r"\band\b", re.IGNORECASE)


def normalize_name(name: str) -> str:
    """Case-folds and treats "AND" the same as "&", the two re-keying
    variants EM-106 names. A trailing "(North)"/"(South)"/"(II)" tag is
    deliberately KEPT: it marks a separate account, not a duplicate."""
    name = (name or "").strip().lower()
    return _AND_WORD_PATTERN.sub("&", name)


def _is_canonical_form(name: str) -> bool:
    """The original keeps normal casing; the SalesTrack re-key is ALL CAPS."""
    return not (name or "").isupper()


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
    planned = {item["legacy_id"] for item in plan}

    # Anything merged that the plan does not name is a stale merge from an
    # earlier (45-record) run and has to be cleared, or W3 stays at 5/6.
    stale = [c["legacy_id"] for c in customers
             if c.get("merged_into") and c["legacy_id"] not in planned]

    if not dry_run:
        for legacy_id in stale:
            client.patch(f"/crm/customers/{legacy_id}", {"merged_into": None})
        for item in plan:
            client.patch(f"/crm/customers/{item['legacy_id']}", {"merged_into": item["merge_into_legacy_id"]})

    return {"total_customers": len(customers), "merges_needed": len(plan),
            "stale_merges_cleared": len(stale), "plan": plan}


def verify_w3(client: DriClient, plan: List[Dict]) -> List[str]:
    data = client.get("/crm/customers")
    by_id = {c["legacy_id"]: c for c in data["customers"]}
    planned = {item["legacy_id"] for item in plan}
    problems = []
    for item in plan:
        actual = by_id.get(item["legacy_id"], {}).get("merged_into")
        if actual != item["merge_into_legacy_id"]:
            problems.append(f"{item['legacy_id']}: expected merged_into={item['merge_into_legacy_id']!r}, got {actual!r}")
    for legacy_id, c in by_id.items():
        if c.get("merged_into") and legacy_id not in planned:
            problems.append(f"{legacy_id}: unexpected merged_into={c['merged_into']!r}")
    return problems
