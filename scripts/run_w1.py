#!/usr/bin/env python3
"""W1 -- Onboard the casting vendor. Defaults to --dry-run: shows the
payload/approvals that would be sent without writing. Pass --execute to
actually create the vendor, set trial_po_cap, and record approvals,
followed by a real re-fetch to verify."""
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
from workflow.w1_vendor_onboarding import onboard_vendor, verify_onboarding  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Actually onboard the vendor (default: dry run)")
    args = parser.parse_args()

    load_env_file(os.path.join(REPO_ROOT, ".env"))
    client = DriClient(os.environ["DRI_BASE"], os.environ["DRI_KEY"])

    result = onboard_vendor(client, dry_run=not args.execute)
    print(result)

    if result["action"] == "created":
        print("\nVerifying...")
        problems = verify_onboarding(client, result["vendor_id"])
        if problems:
            print(f"VERIFICATION FAILED ({len(problems)} problems):")
            for p in problems:
                print(f"  {p}")
            sys.exit(1)
        print("Verified: all vendor fields confirmed on re-fetch.")
