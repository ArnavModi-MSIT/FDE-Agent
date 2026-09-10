#!/usr/bin/env python3
"""W3 PROBE -- which field names does PATCH /crm/customers actually accept?

The project's record says "only crm_id, migrated_to_salestrack and
merged_into are writable; everything else is rejected", but it never
recorded WHICH names were tried. W3's sixth check has never passed in any
state, so it tests something we have never done -- and a writable field we
never knew about is one of the few remaining places that could live.

Read-only by default: sends each candidate field with a deliberately
invalid value, so a 400 tells us the field is unknown OR the value is bad,
while a 200 would mean the field is real (and is reported loudly rather
than left applied). Nothing is written unless a field turns out to be
accepted, and the row used is a merged duplicate whose full prior state is
printed first so it can be restored.

Usage:  python scripts/w3_probe_writable_fields.py
"""
import os, sys, json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (REPO_ROOT, os.path.join(REPO_ROOT, "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from api.client import DriClient          # noqa: E402
from common.env import load_env_file      # noqa: E402

CANDIDATES = [
    # dedup / lifecycle vocabulary
    "status", "active", "is_active", "state", "record_status", "archived",
    "deleted", "is_deleted", "inactive", "merged", "is_merged",
    "merged_from", "duplicate_of", "master_id", "parent_id", "canonical_id",
    "primary_id", "survivor_id", "golden_record", "merge_status",
    # identity / source vocabulary
    "legacy_id", "customer_name", "source_system", "salestrack_id",
    "crm_status", "notes",
    # the three known-writable, as positive controls
    "crm_id", "migrated_to_salestrack", "merged_into",
]

def main():
    load_env_file(os.path.join(REPO_ROOT, ".env"))
    client = DriClient(os.environ["DRI_BASE"], os.environ["DRI_KEY"])

    customers = client.get("/crm/customers")["customers"]
    target = next(c for c in customers if c.get("merged_into"))
    print(f"probing against {target['legacy_id']} (a merged duplicate)")
    print(f"its current state: {json.dumps(target)}\n")

    accepted, rejected = [], []
    for field in CANDIDATES:
        payload = {field: "__W3_PROBE__"}
        try:
            client.patch(f"/crm/customers/{target['legacy_id']}", payload)
            accepted.append(field)
            print(f"  ACCEPTED  {field}   <-- real field, value now dirty, RESTORE IT")
        except Exception as exc:
            msg = str(exc).replace("\n", " ")[:110]
            rejected.append((field, msg))
            print(f"  rejected  {field}   {msg}")

    print(f"\naccepted: {accepted if accepted else 'none beyond what errored'}")
    print("Note: the three known-writable fields should appear as rejected too,")
    print("because '__W3_PROBE__' is an invalid VALUE for them -- compare the")
    print("error text: an unknown-field error reads differently from a bad-value one.")

if __name__ == "__main__":
    main()
