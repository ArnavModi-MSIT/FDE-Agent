#!/usr/bin/env python3
"""W3 EXPERIMENT -- only the ALL-CAPS records are duplicates.

Every W3 test so far merged all 45 records. The organizer text says otherwise:
  FIX-3415: "At least a HANDFUL of distributors exist twice -- once as legacy
             C- records and once in SalesTrack with slightly different names."
  EM-106:   "several distributors exist as legacy C- codes and again in
             SalesTrack, NAMES IN CAPS or with AND changed to ampersand."

Seed data fits that reading exactly, and does not fit the 45-merge one:
  - the 5 ALL-CAPS records were ALL in SalesTrack at seed, and each one's
    tier, region and credit terms EXACTLY match its clean original;
  - the 40 "(North)/(South)/(II)" records mostly carry a different tier,
    region or credit terms, and their label matches their own region field
    in only 7 of 40 -- they look like separate accounts, i.e. "every other
    customer", which the brief says to leave alone.

Hypothesis 6 tested the opposite (unmerge the CAPS, keep the suffix merges)
and collapsed to 0/6. This mirror has never been run.

Modes:
  (default)          dry run
  --execute          clear merged_into on the suffix records, keep the 5 CAPS merged
  --keep LEGACY_IDS  comma-separated suffix records to keep merged as well
  --restore          rewrite merged_into for all 85 from the snapshot
"""
import argparse, json, os, re, sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (REPO_ROOT, os.path.join(REPO_ROOT, "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from api.client import DriClient          # noqa: E402
from common.env import load_env_file      # noqa: E402

SNAPSHOT = os.path.join(REPO_ROOT, "submissions", "state_snapshots",
                        "crm_customers_before_w3_experiment.json")
_SUFFIX = re.compile(r"\([^)]*\)\s*$")


def build_plan(customers, keep):
    return [c for c in customers
            if c.get("merged_into") and _SUFFIX.search(c["customer_name"] or "")
            and c["legacy_id"] not in keep]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--restore", action="store_true")
    ap.add_argument("--keep", default="")
    args = ap.parse_args()
    keep = {k.strip() for k in args.keep.split(",") if k.strip()}

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
    plan = build_plan(customers, keep)
    caps = [c["legacy_id"] for c in customers
            if c.get("merged_into") and (c["customer_name"] or "").isupper()]
    print(f"{len(plan)} suffix records would be UNMERGED; ALL-CAPS kept merged: {caps}"
          + (f"; also kept: {sorted(keep)}" if keep else ""))
    for c in plan[:5]:
        print(f"  {c['legacy_id']} {c['customer_name'][:36]:<36} merged_into {c['merged_into']} -> None")
    if len(plan) > 5:
        print(f"  ... and {len(plan) - 5} more")

    if not args.execute:
        print("\n(dry run -- pass --execute to apply, --restore to undo)")
        return

    for c in plan:
        client.patch(f"/crm/customers/{c['legacy_id']}", {"merged_into": None})
    after = client.get("/crm/customers")["customers"]
    merged = sorted(c["legacy_id"] for c in after if c.get("merged_into"))
    print(f"\nVerification: {len(merged)} customers still merged: {merged}")
    print("Now read the FREE check-count preview (W3).")


if __name__ == "__main__":
    main()
