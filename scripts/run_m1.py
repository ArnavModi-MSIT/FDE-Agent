#!/usr/bin/env python3
"""M1 -- Load the 2023 price list. Defaults to --dry-run: computes and
prints what would change without writing. Pass --execute to actually
PATCH the sandbox, followed by a real re-fetch to verify."""
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
from migration.m1_price_list import run_m1, verify_m1  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Actually PATCH the sandbox (default: dry run)")
    args = parser.parse_args()

    load_env_file(os.path.join(REPO_ROOT, ".env"))
    client = DriClient(os.environ["DRI_BASE"], os.environ["DRI_KEY"])

    result = run_m1(client, dry_run=not args.execute)
    print(f"Total products: {result['total_products']}")
    print(f"Updates needed: {result['updates_needed']}")
    for sku, price in result["updates"]:
        print(f"  {sku}: -> {price}")

    if args.execute:
        print("\nVerifying...")
        problems = verify_m1(client, result["updates"])
        if problems:
            print(f"VERIFICATION FAILED ({len(problems)} problems):")
            for p in problems:
                print(f"  {p}")
            sys.exit(1)
        print(f"Verified: all {result['updates_needed']} updates confirmed on re-fetch.")
    else:
        print("\n(dry run -- pass --execute to actually write these)")
