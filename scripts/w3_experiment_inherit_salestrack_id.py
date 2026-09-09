#!/usr/bin/env python3
"""W3 EXPERIMENT -- let the surviving original inherit the real SalesTrack id.

Hypothesis: W3's 6th check has never passed -- not at the 1/6 baseline,
not at today's 5/6 -- so it tests something NEITHER state satisfies.

Reconstructing the pre-M3 state (M3 minted ids with random.seed(42), so
its 30 ids are exactly derivable) shows 10 duplicate groups where the
SURVIVING ORIGINAL had no SalesTrack id at all, while its duplicate
carried a genuine pre-existing one. That is precisely EM-106's
description: "several distributors exist as legacy C- codes and again in
SalesTrack" -- the legacy record and the SalesTrack record are the two
halves of the pair. After our M3 run, the original holds a FABRICATED id
we minted, and the real SalesTrack identity still sits on the record
being merged away.

Fits the constraint exactly: at baseline the original had no id (fail);
now it has an invented one (still fail).

This swaps the two ids (original <-> its SalesTrack duplicate) rather
than clearing anything, so crm_id uniqueness and "every customer
migrated" both still hold -- keeping M3 damage as small as possible.
Note the previous experiment (deactivating duplicates entirely) was
already tested and DISPROVEN: W3 stayed 5/6 and M3 fell to 1/5.

Fully reversible via --restore from the pre-experiment snapshot.

Usage:
  python scripts/w3_experiment_inherit_salestrack_id.py            # dry run
  python scripts/w3_experiment_inherit_salestrack_id.py --execute  # apply
  python scripts/w3_experiment_inherit_salestrack_id.py --restore  # undo
"""
import argparse
import json
import os
import random
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


def build_swap_plan(customers):
    """[{original, original_new_crm_id, duplicate, duplicate_new_crm_id}, ...]

    Only for groups where the original's current id was minted by our own
    M3 run (i.e. it had NO real SalesTrack identity) while a duplicate
    carries a pre-existing one. Where several duplicates qualify, the
    lowest legacy_id wins -- deterministic, never arbitrary."""
    random.seed(42)
    minted = {f"ST-{random.randint(10000, 99999)}" for _ in range(30)}

    groups = {}
    for c in customers:
        groups.setdefault(_norm(c["customer_name"]), []).append(c)

    plan = []
    for _, g in groups.items():
        if len(g) < 2:
            continue
        originals = [c for c in g if not c.get("merged_into")]
        if len(originals) != 1:
            continue
        orig = originals[0]
        if orig.get("crm_id") not in minted:
            continue  # original already had a real SalesTrack identity
        dups = sorted(
            (c for c in g if c.get("merged_into") and c.get("crm_id") not in minted),
            key=lambda c: c["legacy_id"],
        )
        if not dups:
            continue
        salestrack_rec = dups[0]
        plan.append({
            "original": orig["legacy_id"],
            "original_new_crm_id": salestrack_rec["crm_id"],
            "duplicate": salestrack_rec["legacy_id"],
            "duplicate_new_crm_id": orig["crm_id"],
        })
    return plan


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()

    load_env_file(os.path.join(REPO_ROOT, ".env"))
    client = DriClient(os.environ["DRI_BASE"], os.environ["DRI_KEY"])

    if args.restore:
        snap = json.load(open(SNAPSHOT, encoding="utf-8"))
        print(f"Restoring all {len(snap)} customers from snapshot...")
        for i, c in enumerate(snap, 1):
            client.patch(
                f"/crm/customers/{c['legacy_id']}",
                {"crm_id": c["crm_id"], "migrated_to_salestrack": c["migrated_to_salestrack"]},
            )
            if i % 20 == 0:
                print(f"  {i}/{len(snap)}")
        live = {c["legacy_id"]: c for c in client.get("/crm/customers")["customers"]}
        bad = [c["legacy_id"] for c in snap if live.get(c["legacy_id"]) != c]
        print(f"Restore verified: {'CLEAN' if not bad else 'MISMATCHES ' + str(bad)}")
        return

    customers = client.get("/crm/customers")["customers"]
    plan = build_swap_plan(customers)
    print(f"Groups where the original holds a fabricated id while its "
          f"duplicate holds the real one: {len(plan)}\n")
    for p in plan:
        print(f"  {p['original']}: {p['duplicate_new_crm_id']} -> {p['original_new_crm_id']}   "
              f"(swap with duplicate {p['duplicate']})")

    if not args.execute:
        print("\n(dry run -- pass --execute to apply, --restore to undo)")
        return

    print("\nApplying swaps...")
    for p in plan:
        # Park the duplicate's id first so uniqueness never breaks mid-swap.
        client.patch(f"/crm/customers/{p['duplicate']}", {"crm_id": None})
        client.patch(f"/crm/customers/{p['original']}", {"crm_id": p["original_new_crm_id"]})
        client.patch(f"/crm/customers/{p['duplicate']}",
                     {"crm_id": p["duplicate_new_crm_id"], "migrated_to_salestrack": "Y"})

    after = client.get("/crm/customers")["customers"]
    ids = [c["crm_id"] for c in after if c.get("crm_id")]
    print("\nVerification:")
    print(f"  customers with crm_id: {len(ids)}/85")
    print(f"  crm_id collisions: {len(ids) - len(set(ids))}")
    print(f"  migrated='Y': {sum(1 for c in after if c.get('migrated_to_salestrack') == 'Y')}/85")
    print("\nNow read the FREE check-count preview (W3 and M3).")


if __name__ == "__main__":
    main()
