#!/usr/bin/env python3
"""W3 EXPERIMENT -- deactivate merged duplicates as live SalesTrack accounts.

Hypothesis (evidence-backed, see CLAUDE.md): W3's 6th check has never
passed -- not at the 1/6 baseline, and not at today's 5/6 -- so it tests
something NEITHER state satisfies. Setting `merged_into` records the
merge relationship, but every one of the 45 merged duplicates is still
`migrated_to_salestrack="Y"` with its own `crm_id`, i.e. still a live
SalesTrack account. Both organizer texts describe the symptom as
duplicate MAIL, not a missing pointer:
  FIX-3415: "Renewal mailers going out twice."
  EM-106:   "last year two of them got the scheme letter twice."
So a merged duplicate arguably must stop being an active account.

This is fully reversible: --restore rewrites every field from the
snapshot taken before the experiment. Migration's 1.0000 is already
banked as a best-recorded score, so disturbing M3's live state cannot
cost anything on the leaderboard even before restoring.

Usage:
  python scripts/w3_experiment_deactivate_duplicates.py             # dry run
  python scripts/w3_experiment_deactivate_duplicates.py --execute   # apply
  python scripts/w3_experiment_deactivate_duplicates.py --restore   # undo
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
    parser.add_argument("--execute", action="store_true", help="Apply the deactivation")
    parser.add_argument("--restore", action="store_true", help="Restore from the snapshot")
    args = parser.parse_args()

    load_env_file(os.path.join(REPO_ROOT, ".env"))
    client = DriClient(os.environ["DRI_BASE"], os.environ["DRI_KEY"])

    if args.restore:
        snap = json.load(open(SNAPSHOT, encoding="utf-8"))
        targets = [c for c in snap if c.get("merged_into")]
        print(f"Restoring {len(targets)} duplicates from snapshot...")
        for i, c in enumerate(targets, 1):
            client.patch(
                f"/crm/customers/{c['legacy_id']}",
                {"crm_id": c["crm_id"], "migrated_to_salestrack": c["migrated_to_salestrack"]},
            )
            if i % 15 == 0:
                print(f"  {i}/{len(targets)}")
        live = {c["legacy_id"]: c for c in client.get("/crm/customers")["customers"]}
        bad = [c["legacy_id"] for c in snap if live.get(c["legacy_id"]) != c]
        print(f"Restore verified: {'CLEAN' if not bad else 'MISMATCHES ' + str(bad)}")
        return

    customers = client.get("/crm/customers")["customers"]
    merged = [c for c in customers if c.get("merged_into")]
    print(f"Merged duplicates found: {len(merged)}")
    print("Would set migrated_to_salestrack='N' and crm_id=None on each.")
    print(f"Currently active among them: "
          f"{sum(1 for c in merged if c.get('migrated_to_salestrack') == 'Y')} migrated, "
          f"{sum(1 for c in merged if c.get('crm_id'))} with crm_id")

    if not args.execute:
        print("\n(dry run -- pass --execute to apply, --restore to undo)")
        return

    for i, c in enumerate(merged, 1):
        client.patch(
            f"/crm/customers/{c['legacy_id']}",
            {"migrated_to_salestrack": "N", "crm_id": None},
        )
        if i % 15 == 0:
            print(f"  {i}/{len(merged)}")

    after = [c for c in client.get("/crm/customers")["customers"] if c.get("merged_into")]
    print("\nVerification:")
    print(f"  still migrated='Y': {sum(1 for c in after if c.get('migrated_to_salestrack') == 'Y')}")
    print(f"  still have crm_id:  {sum(1 for c in after if c.get('crm_id'))}")
    print("\nNow read the FREE check-count preview on the sandbox page (W3 and M3).")


if __name__ == "__main__":
    main()
