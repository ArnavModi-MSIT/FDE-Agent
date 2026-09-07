#!/usr/bin/env python3
"""W2 -- The MD's exceptions report. Defaults to --dry-run: computes and
prints the report without posting. Pass --execute to actually POST it."""
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
from workflow.w2_exceptions_report import compute_exceptions_report, post_exceptions_report  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Actually POST the report (default: dry run)")
    args = parser.parse_args()

    load_env_file(os.path.join(REPO_ROOT, ".env"))
    client = DriClient(os.environ["DRI_BASE"], os.environ["DRI_KEY"])

    report = compute_exceptions_report(client)
    print("Counts:")
    for status, count in sorted(report["counts"].items(), key=lambda kv: -kv[1]):
        print(f"  {status:<20} {count}")
    print(f"Value at risk: {report['value_at_risk']}")

    if args.execute:
        print("\nPosting...")
        result = post_exceptions_report(client, report)
        print(f"Response: {result}")
    else:
        print("\n(dry run -- pass --execute to actually POST this)")
