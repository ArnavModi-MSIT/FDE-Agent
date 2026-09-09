#!/usr/bin/env python3
"""W3 EXPERIMENT -- the last untried `merged_into` configurations.

Context: W3 is 5/6. Exactly one check has NEVER passed (not at the 1/6
seed baseline, not now), so it tests something we have never done. Only
three fields are writable (`crm_id`, `migrated_to_salestrack`,
`merged_into`); the first two have both been tested and disproven
(deactivating duplicates; giving the original the real SalesTrack id).
That leaves `merged_into` shapes we have never produced.

Every one of the 45 merges has always pointed straight at the group's
canonical original. The only structurally different arrangements left
live in the 5 three-way groups (original + suffix duplicate + ALL-CAPS
duplicate):

  --mode chain    ALL-CAPS record merges into its SUFFIX sibling instead
                  of the original, forming original <- suffix <- CAPS.
  --mode uncaps   ALL-CAPS records are left unmerged entirely (tests the
                  reading that only the suffix records are duplicates and
                  we have been over-merging 5 rows).

Both touch only 5 rows, and only the `merged_into` field. Reversible
with --restore, which rewrites `merged_into` for all 85 customers from
the pre-experiment snapshot.

Read the FREE check-count preview after running; it costs no scoring run.

Usage:
  python scripts/w3_experiment_threeway_variants.py --mode chain
  python scripts/w3_experiment_threeway_variants.py --mode chain --execute
  python scripts/w3_experiment_threeway_variants.py --restore
"""
import argparse
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(REPO_ROOT, "src")
for path in (REPO_ROOT, SRC_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

from api.client import DriClient  # noqa: E402
from common.env import load_env_file  # noqa: E402

SNAPSHOT = os.path.join(
    REPO_ROOT, "submissions", "state_snapshots", "crm_customers_before_w3_experiment.json"
)
_SUFFIX = re.compile(r"\s*\([^)]*\)\s*$")


def _norm(name):
    return _SUFFIX.sub("", name or "").strip().lower()


def build_plan(customers, mode):
    """[{legacy_id, new_merged_into}] for the ALL-CAPS record of each
    three-way group. Only ever touches those 5 rows."""
    groups = {}
    for c in customers:
        groups.setdefault(_norm(c["customer_name"]), []).append(c)

    plan = []
    for _, g in groups.items():
        if len(g) < 3:
            continue
        caps = [c for c in g if (c["customer_name"] or "").isupper()]
        if len(caps) != 1:
            continue
        caps = caps[0]
        siblings = [c for c in g if c is not caps and c.get("merged_into")]
        if len(siblings) != 1:
            continue
        plan.append({
            "legacy_id": caps["legacy_id"],
            "name": caps["customer_name"],
            "new_merged_into": siblings[0]["legacy_id"] if mode == "chain" else None,
            "current": caps.get("merged_into"),
        })
    return plan


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["chain", "uncaps"], default="chain")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()

    load_env_file(os.path.join(REPO_ROOT, ".env"))
    client = DriClient(os.environ["DRI_BASE"], os.environ["DRI_KEY"])

    if args.restore:
        snap = json.load(open(SNAPSHOT, encoding="utf-8"))
        print(f"Restoring merged_into for all {len(snap)} customers...")
        for c in snap:
            client.patch(f"/crm/customers/{c['legacy_id']}", {"merged_into": c["merged_into"]})
        live = {c["legacy_id"]: c for c in client.get("/crm/customers")["customers"]}
        bad = [c["legacy_id"] for c in snap if live[c["legacy_id"]]["merged_into"] != c["merged_into"]]
        print(f"Restore verified: {'CLEAN' if not bad else 'MISMATCHES ' + str(bad)}")
        return

    customers = client.get("/crm/customers")["customers"]
    plan = build_plan(customers, args.mode)
    print(f"mode={args.mode}: {len(plan)} ALL-CAPS records would change\n")
    for p in plan:
        print(f"  {p['legacy_id']} {p['name']:34s} merged_into {p['current']} -> {p['new_merged_into']}")

    if not args.execute:
        print("\n(dry run -- pass --execute to apply, --restore to undo)")
        return

    for p in plan:
        client.patch(f"/crm/customers/{p['legacy_id']}", {"merged_into": p["new_merged_into"]})

    after = client.get("/crm/customers")["customers"]
    print(f"\nVerification: {sum(1 for c in after if c.get('merged_into'))} customers now have merged_into set")
    print("Now read the FREE check-count preview (W3).")


if __name__ == "__main__":
    main()
