#!/usr/bin/env python3
"""W3 EXPERIMENT -- unbundle the two halves of hypothesis 1.

Hypothesis 1 changed TWO things at once on all 45 merged duplicates:
crm_id -> null AND migrated_to_salestrack -> "N". W3 stayed 5/6 and M3
collapsed 5/5 -> 1/5, so the pair was abandoned together. But a bundled
null result does not rule out either half on its own, and W3's sixth check
has never passed in any state -- so it tests a property false at the seed
baseline AND false today.

Exactly one such property survives everything measured so far:

    "a merged duplicate must not hold its own SalesTrack identity"

At seed the duplicates carried their own crm_ids (false), and today they
still do (false). That matches the organizer symptom precisely --
FIX-3415 "Renewal mailers going out twice", EM-106 "two of them got the
scheme letter twice" -- a duplicate that still has a live SalesTrack id is
still mailable.

  --mode clear-id-keep-migrated   crm_id -> null, migrated_to_salestrack
                                  left at "Y". Never tested. Keeps M3's
                                  "every customer migrated" satisfied,
                                  which is the half that plausibly caused
                                  hypothesis 1's M3 collapse.
  --mode unmigrate-keep-id        the mirror: migrated -> "N", crm_id
                                  untouched. Also never tested alone.

Only the 45 merged duplicates are touched, and only the one field the mode
names. Read the FREE check-count preview afterwards; it costs no scoring
run. Restore with --restore, which rewrites both fields for all 85
customers from the pre-experiment snapshot.

Usage:
  python scripts/w3_experiment_unbundle_duplicate_identity.py --mode clear-id-keep-migrated
  python scripts/w3_experiment_unbundle_duplicate_identity.py --mode clear-id-keep-migrated --execute
  python scripts/w3_experiment_unbundle_duplicate_identity.py --restore
"""
import argparse, json, os, sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (REPO_ROOT, os.path.join(REPO_ROOT, "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from api.client import DriClient          # noqa: E402
from common.env import load_env_file      # noqa: E402

SNAPSHOT = os.path.join(REPO_ROOT, "submissions", "state_snapshots",
                        "crm_customers_before_w3_experiment.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["clear-id-keep-migrated", "unmigrate-keep-id"],
                    default="clear-id-keep-migrated")
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--restore", action="store_true")
    args = ap.parse_args()

    load_env_file(os.path.join(REPO_ROOT, ".env"))
    client = DriClient(os.environ["DRI_BASE"], os.environ["DRI_KEY"])

    if args.restore:
        snap = json.load(open(SNAPSHOT, encoding="utf-8"))
        print(f"Restoring crm_id + migrated_to_salestrack for all {len(snap)} customers...")
        for i, c in enumerate(snap, 1):
            client.patch(f"/crm/customers/{c['legacy_id']}",
                         {"crm_id": c["crm_id"],
                          "migrated_to_salestrack": c["migrated_to_salestrack"]})
            if i % 20 == 0:
                print(f"  {i}/{len(snap)}")
        live = {c["legacy_id"]: c for c in client.get("/crm/customers")["customers"]}
        bad = [c["legacy_id"] for c in snap if live.get(c["legacy_id"]) != c]
        print(f"Restore verified: {'CLEAN' if not bad else 'MISMATCHES ' + str(bad)}")
        return

    customers = client.get("/crm/customers")["customers"]
    dups = [c for c in customers if c.get("merged_into")]
    field, value = (("crm_id", None) if args.mode == "clear-id-keep-migrated"
                    else ("migrated_to_salestrack", "N"))

    print(f"mode={args.mode}: {len(dups)} merged duplicates would get {field} = {value!r}")
    print(f"the other field is left exactly as it is\n")
    for c in dups[:5]:
        print(f"  {c['legacy_id']}  crm_id={c['crm_id']}  migrated={c['migrated_to_salestrack']}"
              f"  -> {field}={value!r}")
    print(f"  ... and {len(dups)-5} more")

    if not args.execute:
        print("\n(dry run -- pass --execute to apply, --restore to undo)")
        return

    print("\nApplying...")
    for c in dups:
        client.patch(f"/crm/customers/{c['legacy_id']}", {field: value})

    after = {c["legacy_id"]: c for c in client.get("/crm/customers")["customers"]}
    changed = sum(1 for c in dups if after[c["legacy_id"]][field] == value)
    migrated_y = sum(1 for c in after.values() if c.get("migrated_to_salestrack") == "Y")
    with_id = sum(1 for c in after.values() if c.get("crm_id"))
    print(f"\nVerification: {changed}/{len(dups)} duplicates now have {field}={value!r}")
    print(f"  customers migrated='Y': {migrated_y}/85")
    print(f"  customers holding a crm_id: {with_id}/85")
    print("\nNow read the FREE check-count preview (W3, and note M3).")


if __name__ == "__main__":
    main()
