#!/usr/bin/env python3
"""W3 EXPERIMENT -- a merged duplicate shares its survivor's crm_id.

Dedup semantics: once a duplicate is merged into its original the two
rows represent ONE SalesTrack account, so arguably they should carry the
SAME crm_id rather than two independent ones.

Fits the never-passed constraint exactly:
  - at the seed baseline: duplicates had their own ids and 10 originals
    had none at all              -> check fails
  - today: all 85 ids are distinct -> check still fails
i.e. a property neither state has ever satisfied, which is precisely
what W3's one perpetually-failing check must be testing.

Distinct from both disproven predecessors: hypothesis 1 CLEARED the
duplicate's id, hypothesis 2 SWAPPED ids between duplicate and original.
Neither ever COPIED the survivor's id onto the duplicate.

Expected M3 cost: this deliberately creates 45 duplicate crm_ids, which
breaks M3's "unique across your customers" assertion. That is acceptable
to measure because Migration's 1.0000 is already banked as a
best-recorded score and the preview costs no scoring run. Restore before
re-scoring Migration.

Restore with either:
  python scripts/w3_experiment_shared_crm_id.py --restore
  python scripts/w3_experiment_deactivate_duplicates.py --restore

Usage:
  python scripts/w3_experiment_shared_crm_id.py            # dry run
  python scripts/w3_experiment_shared_crm_id.py --execute
  python scripts/w3_experiment_shared_crm_id.py --restore
"""
import argparse
import json
import os
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()

    load_env_file(os.path.join(REPO_ROOT, ".env"))
    client = DriClient(os.environ["DRI_BASE"], os.environ["DRI_KEY"])

    if args.restore:
        snap = json.load(open(SNAPSHOT, encoding="utf-8"))
        targets = [c for c in snap if c.get("merged_into")]
        print(f"Restoring crm_id for {len(targets)} duplicates from snapshot...")
        for c in targets:
            client.patch(f"/crm/customers/{c['legacy_id']}",
                         {"crm_id": c["crm_id"], "migrated_to_salestrack": c["migrated_to_salestrack"]})
        live = {c["legacy_id"]: c for c in client.get("/crm/customers")["customers"]}
        bad = [c["legacy_id"] for c in snap if live[c["legacy_id"]] != c]
        print(f"Restore verified: {'CLEAN' if not bad else 'MISMATCHES ' + str(bad)}")
        return

    customers = client.get("/crm/customers")["customers"]
    by_id = {c["legacy_id"]: c for c in customers}
    plan = []
    for c in customers:
        target = c.get("merged_into")
        if not target:
            continue
        survivor = by_id.get(target)
        if survivor and survivor.get("crm_id") and c.get("crm_id") != survivor["crm_id"]:
            plan.append({"legacy_id": c["legacy_id"], "from": c["crm_id"],
                         "to": survivor["crm_id"], "survivor": target})

    print(f"{len(plan)} merged duplicates would take their survivor's crm_id\n")
    for p in plan[:6]:
        print(f"  {p['legacy_id']}  {p['from']} -> {p['to']}   (survivor {p['survivor']})")
    if len(plan) > 6:
        print(f"  ... and {len(plan)-6} more")

    if not args.execute:
        print("\n(dry run -- pass --execute to apply, --restore to undo)")
        return

    print("\nApplying...")
    for p in plan:
        client.patch(f"/crm/customers/{p['legacy_id']}", {"crm_id": p["to"]})

    after = client.get("/crm/customers")["customers"]
    ids = [c["crm_id"] for c in after if c.get("crm_id")]
    matched = sum(1 for c in after if c.get("merged_into")
                  and c.get("crm_id") == next((x["crm_id"] for x in after
                                               if x["legacy_id"] == c["merged_into"]), None))
    print(f"\nVerification: {matched}/45 duplicates now share their survivor's crm_id")
    print(f"  distinct crm_ids: {len(set(ids))} of {len(ids)} (collisions expected by design)")
    print("\nNow read the FREE check-count preview (W3, and note M3).")


if __name__ == "__main__":
    main()
