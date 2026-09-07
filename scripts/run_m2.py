#!/usr/bin/env python3
"""M2 -- Map FlowTech SKUs. Defaults to --dry-run: computes and prints
the resolved/unresolved mapping plan without writing. Pass --execute to
actually PATCH mapped_dri_sku for every UNIQUE_MATCH, followed by a real
re-fetch to verify."""
import argparse
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(REPO_ROOT, "src")
for path in (REPO_ROOT, SRC_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

from api.client import DriClient  # noqa: E402
from common.env import load_env_file  # noqa: E402
from migration.m2_flowtech_mapping import run_m2, verify_m2  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Actually PATCH the sandbox (default: dry run)")
    args = parser.parse_args()

    load_env_file(os.path.join(REPO_ROOT, ".env"))
    client = DriClient(os.environ["DRI_BASE"], os.environ["DRI_KEY"])

    plan = run_m2(client, dry_run=not args.execute)
    print(f"Resolved (will write): {len(plan['resolved'])}")
    for item in plan["resolved"]:
        print(f"  {item['sku']} -> {item['mapped_dri_sku']}")
    print(f"\nUnresolved (will NOT write, never guessed): {len(plan['unresolved'])}")
    for item in plan["unresolved"]:
        print(f"  {item['sku']}: {item['status']} {item.get('candidates', [])} {item.get('reason', '')}")

    if args.execute:
        print("\nVerifying...")
        problems = verify_m2(client, plan["resolved"])
        if problems:
            print(f"VERIFICATION FAILED ({len(problems)} problems):")
            for p in problems:
                print(f"  {p}")
            sys.exit(1)
        print(f"Verified: all {len(plan['resolved'])} mappings confirmed on re-fetch.")
    else:
        print("\n(dry run -- pass --execute to actually write these)")
