#!/usr/bin/env python3
"""W3 EXPERIMENT -- reverse WHO survives the merge, for the SalesTrack groups.

Every W3 experiment so far has permuted the three writable FIELDS while
holding one thing fixed that was never questioned: which record survives.
`w3_customer_dedup.py` always keeps the clean mixed-case name and merges
the suffixed / ALL-CAPS records into it.

The "any deviation collapses to 0/6" conclusion in CLAUDE.md is drawn from
two deviations that were both structurally catastrophic -- merge chains
(which break the decoded "targets must not themselves be merged" check) and
leaving 5 duplicates unmerged (which breaks "all duplicates merged"). A
merge map that is still internally VALID but picks a different survivor has
never been tested at all. That is a real gap, not a settled question.

The concrete version, and the only one with organizer evidence behind it:
EM-106 says several distributors "exist as legacy C- codes AND AGAIN IN
SALESTRACK". Reconstructing the pre-M3 state (M3 minted its ids under
random.seed(42), so they are exactly derivable) shows 10 groups where the
clean-named original had NO SalesTrack id while one of its duplicates
carried a genuine pre-existing one. Under the reading that the SalesTrack
record is the surviving master and the legacy C- record is the stale
duplicate, the merge direction for exactly those 10 groups is backwards.

This flips `merged_into` for those groups only: the real-SalesTrack record
becomes the survivor and the clean-named original merges into it. Every
group keeps exactly one unmerged survivor, and no target is itself merged,
so the map stays internally valid -- which is what makes this a genuine
test rather than a repeat of the two catastrophic deviations.

Honest counter-evidence: W3's brief says "Merge each duplicate into its
original", which reads for the clean name surviving. The preview is free,
so this is settled by measurement rather than by argument.

Usage:
  python scripts/w3_experiment_reverse_survivor.py            # dry run
  python scripts/w3_experiment_reverse_survivor.py --execute
  python scripts/w3_experiment_reverse_survivor.py --restore
"""
import argparse, json, os, random, re, sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (REPO_ROOT, os.path.join(REPO_ROOT, "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from api.client import DriClient          # noqa: E402
from common.env import load_env_file      # noqa: E402

SNAPSHOT = os.path.join(REPO_ROOT, "submissions", "state_snapshots",
                        "crm_customers_before_w3_experiment.json")
_SUFFIX = re.compile(r"\s*\([^)]*\)\s*$")


def _norm(name):
    return _SUFFIX.sub("", name or "").strip().lower()


def build_plan(customers):
    """Groups where the original's id was minted by our own M3 run (so it had
    no real SalesTrack identity) while a duplicate carries a pre-existing one."""
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
            continue                      # original already had a real identity
        dups = sorted((c for c in g if c.get("merged_into")
                       and c.get("crm_id") not in minted),
                      key=lambda c: c["legacy_id"])
        if not dups:
            continue
        survivor = dups[0]
        others = [c for c in g if c["legacy_id"] not in (orig["legacy_id"],
                                                         survivor["legacy_id"])]
        plan.append({"new_survivor": survivor["legacy_id"],
                     "old_survivor": orig["legacy_id"],
                     "salestrack_id": survivor["crm_id"],
                     "also_repoint": [c["legacy_id"] for c in others]})
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
        print(f"Restoring merged_into for all {len(snap)} customers...")
        for c in snap:
            client.patch(f"/crm/customers/{c['legacy_id']}",
                         {"merged_into": c["merged_into"]})
        live = {c["legacy_id"]: c for c in client.get("/crm/customers")["customers"]}
        bad = [c["legacy_id"] for c in snap
               if live[c["legacy_id"]]["merged_into"] != c["merged_into"]]
        print(f"Restore verified: {'CLEAN' if not bad else 'MISMATCHES ' + str(bad)}")
        return

    customers = client.get("/crm/customers")["customers"]
    plan = build_plan(customers)
    print(f"{len(plan)} groups would flip their surviving record\n")
    for p in plan:
        extra = f" (+ repoint {p['also_repoint']})" if p["also_repoint"] else ""
        print(f"  survivor {p['old_survivor']} -> {p['new_survivor']} "
              f"[holds {p['salestrack_id']}]{extra}")

    if not args.execute:
        print("\n(dry run -- pass --execute to apply, --restore to undo)")
        return

    print("\nApplying...")
    for p in plan:
        client.patch(f"/crm/customers/{p['new_survivor']}", {"merged_into": None})
        client.patch(f"/crm/customers/{p['old_survivor']}",
                     {"merged_into": p["new_survivor"]})
        for other in p["also_repoint"]:
            client.patch(f"/crm/customers/{other}", {"merged_into": p["new_survivor"]})

    after = client.get("/crm/customers")["customers"]
    by_id = {c["legacy_id"]: c for c in after}
    merged = [c for c in after if c.get("merged_into")]
    chained = [c["legacy_id"] for c in merged
               if by_id.get(c["merged_into"], {}).get("merged_into")]
    print(f"\nVerification: {len(merged)} merged, {85-len(merged)} survivors")
    print(f"  chained targets (must be 0): {len(chained)} {chained}")
    print("\nNow read the FREE check-count preview (W3).")


if __name__ == "__main__":
    main()
