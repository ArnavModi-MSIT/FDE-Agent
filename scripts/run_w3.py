#!/usr/bin/env python3
"""W3 -- Dedupe the distributor master. Defaults to --dry-run: computes
and prints the merge plan without writing. Pass --execute to actually
PATCH merged_into for every duplicate, followed by a real re-fetch to
verify."""
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
from workflow.w3_customer_dedup import run_w3, verify_w3  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Actually PATCH the sandbox (default: dry run)")
    args = parser.parse_args()

    load_env_file(os.path.join(REPO_ROOT, ".env"))
    client = DriClient(os.environ["DRI_BASE"], os.environ["DRI_KEY"])

    result = run_w3(client, dry_run=not args.execute)
    print(f"Total customers: {result['total_customers']}")
    print(f"Merges needed: {result['merges_needed']}")
    for item in result["plan"]:
        print(f"  {item['legacy_id']} -> merged_into {item['merge_into_legacy_id']}")

    if args.execute:
        print("\nVerifying...")
        problems = verify_w3(client, result["plan"])
        if problems:
            print(f"VERIFICATION FAILED ({len(problems)} problems):")
            for p in problems:
                print(f"  {p}")
            sys.exit(1)
        print(f"Verified: all {result['merges_needed']} merges confirmed on re-fetch.")
    else:
        print("\n(dry run -- pass --execute to actually write these)")
