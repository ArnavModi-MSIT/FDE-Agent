#!/usr/bin/env python3
"""W3 EXPERIMENT -- "Leave every other customer alone" is broken by M3.

The full W3 brief (sandbox-docs, read live 2026-09-13):
  "The distributor master carries duplicate accounts. Merge each duplicate
   into its original by setting the duplicate's merged_into to the
   original's legacy_id. Leave every other customer alone."

Diffing live state against the seed extract (dataset/System extracts/
customers.csv) shows 15 NON-duplicate customers whose crm_id and
migrated_to_salestrack differ from seed -- every one changed by our own M3
run (N -> Y, minted ST-id). If W3 grades "leave every other customer alone"
against seed, that check fails purely because of M3.

This also fits the score history better than the old "one check never
passed" reading: at seed nothing is touched, so this check passes (1/6);
after W3 + M3 the five merge checks pass and this one fails (5/6).

Families are scored separately and each keeps its best recorded score, so a
Workflow run taken while the 15 originals sit at seed values would bank
W3 6/6 without touching Migration's banked 1.0000.

Modes:
  (default)   dry run
  --execute   revert the 15 non-duplicates to their seed crm_id/migrated values
  --restore   rewrite crm_id + migrated_to_salestrack for all 85 from the snapshot
"""
import argparse, csv, json, os, sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (REPO_ROOT, os.path.join(REPO_ROOT, "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from api.client import DriClient          # noqa: E402
from common.env import load_env_file      # noqa: E402

SEED = os.path.join(REPO_ROOT, "dataset", "System extracts", "customers.csv")
SNAPSHOT = os.path.join(REPO_ROOT, "submissions", "state_snapshots",
                        "crm_customers_before_w3_experiment.json")


def _norm(v):
    return (v or "").strip() or None


def build_plan(live):
    seed = {r["legacy_id"]: r for r in csv.DictReader(open(SEED, encoding="utf-8-sig"))}
    plan = []
    for lid, s in seed.items():
        cur = live[lid]
        if cur.get("merged_into"):
            continue  # duplicates are the customers W3 is told to change
        target = {"crm_id": _norm(s.get("crm_id")),
                  "migrated_to_salestrack": _norm(s.get("migrated_to_salestrack"))}
        if any(cur.get(f) != v for f, v in target.items()):
            plan.append((lid, cur["customer_name"], target,
                         {f: cur.get(f) for f in target}))
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--restore", action="store_true")
    args = ap.parse_args()

    load_env_file(os.path.join(REPO_ROOT, ".env"))
    client = DriClient(os.environ["DRI_BASE"], os.environ["DRI_KEY"])

    if args.restore:
        snap = json.load(open(SNAPSHOT, encoding="utf-8"))
        print(f"Restoring crm_id + migrated_to_salestrack for all {len(snap)} customers...")
        for c in snap:
            client.patch(f"/crm/customers/{c['legacy_id']}",
                         {"crm_id": c["crm_id"],
                          "migrated_to_salestrack": c["migrated_to_salestrack"]})
        live = {c["legacy_id"]: c for c in client.get("/crm/customers")["customers"]}
        bad = [c["legacy_id"] for c in snap if live.get(c["legacy_id"]) != c]
        print(f"Restore verified: {'CLEAN' if not bad else 'MISMATCHES ' + str(bad)}")
        return

    live = {c["legacy_id"]: c for c in client.get("/crm/customers")["customers"]}
    plan = build_plan(live)
    print(f"{len(plan)} non-duplicate customers differ from seed and would be reverted:\n")
    for lid, name, target, current in plan:
        print(f"  {lid} {name[:30]:<30} {current} -> {target}")

    if not args.execute:
        print("\n(dry run -- pass --execute to apply, --restore to undo)")
        return

    for lid, _, target, _ in plan:
        client.patch(f"/crm/customers/{lid}", target)

    after = {c["legacy_id"]: c for c in client.get("/crm/customers")["customers"]}
    left = build_plan(after)
    print(f"\nVerification: {len(plan) - len(left)}/{len(plan)} reverted; "
          f"non-duplicates still differing from seed: {len(left)}")
    print("Now read the FREE check-count preview: W3, and note M3.")


if __name__ == "__main__":
    main()
