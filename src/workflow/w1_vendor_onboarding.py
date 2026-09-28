"""W1 -- Onboard the casting vendor. Task: Sri Ranga Castings, Coimbatore
(TN), GSTIN 33AAACS1234R1ZK, MSME-registered, direct-material supplier,
projected annual spend Rs 14,00,000, per VOS-7.

Reuses knowledge/policy_kb.py's VOS-7 constants directly (trial PO cap,
approval matrix) -- the same policy engine already built and verified for
the Knowledge family, not a second copy of VOS-7's rules. Approval matrix
is compounding for this exact vendor: spend Rs 14L > Rs 10L threshold
(CFO) AND direct-material (Plant Head + QA) -- all three required."""
from typing import Dict, List, Optional

from api.client import DriClient
from knowledge.policy_kb import TRIAL_PO_CAP_RUPEES, required_approvals

VENDOR_NAME = "Sri Ranga Castings"
GSTIN = "33AAACS1234R1ZK"
CITY = "Coimbatore"
STATE = "TN"
PROJECTED_ANNUAL_SPEND = 1_400_000
IS_DIRECT_MATERIAL = True
IS_MSME_REGISTERED = "Y"


def find_existing_vendor_in_list(vendors: List[Dict]) -> Optional[Dict]:
    """Pure matching logic, directly testable. Confirmed real risk from
    the sandbox's own vendor list: 6 near-duplicate
    vendors already exist under a different code/ALL-CAPS name for the
    same real company. Matches on GSTIN (should be invariant across name
    -format drift) or an exact case-insensitive name match -- NOT fuzzy
    name similarity, since we have no real example locally of how close
    is "close enough" and would rather under-match (create a vendor that
    might already exist under a wildly different name) than over-match
    (skip onboarding a genuinely new vendor)."""
    for v in vendors:
        if v.get("gstin") == GSTIN:
            return v
        if (v.get("vendor_name") or "").strip().lower() == VENDOR_NAME.lower():
            return v
    return None


def find_existing_vendor(client: DriClient) -> Optional[Dict]:
    data = client.get("/erp/vendors")
    return find_existing_vendor_in_list(data["vendors"])


def onboard_vendor(client: DriClient, dry_run: bool = True) -> Dict:
    existing = find_existing_vendor(client)
    if existing is not None:
        return {"action": "skipped_existing", "vendor": existing}

    payload = {
        "vendor_name": VENDOR_NAME,
        "gstin": GSTIN,
        "city": CITY,
        "state": STATE,
        "msme_registered": IS_MSME_REGISTERED,
        "direct_material": IS_DIRECT_MATERIAL,
        "gst_cert": True,
        "cancelled_cheque": True,
        "msme_declaration": True,
    }
    approvals = required_approvals(PROJECTED_ANNUAL_SPEND, IS_DIRECT_MATERIAL)

    if dry_run:
        return {
            "action": "would_create",
            "vendor_payload": payload,
            "trial_po_cap": TRIAL_PO_CAP_RUPEES,
            "approvals_needed": approvals,
        }

    created = client.post("/erp/vendors", payload)
    vendor = created.get("vendor", created)
    vendor_id = vendor["vendor_id"]

    client.patch(f"/erp/vendors/{vendor_id}", {"trial_po_cap": TRIAL_PO_CAP_RUPEES})

    approval_results = []
    for role in approvals:
        role_code = role.upper().replace(" ", "_")  # "Plant Head" -> "PLANT_HEAD"
        result = client.post("/erp/approvals", {"vendor_name": VENDOR_NAME, "role": role_code})
        approval_results.append(result)

    return {
        "action": "created",
        "vendor_id": vendor_id,
        "trial_po_cap": TRIAL_PO_CAP_RUPEES,
        "approvals": approvals,
        "approval_results": approval_results,
    }


def verify_onboarding(client: DriClient, vendor_id: str) -> List[str]:
    data = client.get("/erp/vendors")
    vendor = next((v for v in data["vendors"] if v["vendor_id"] == vendor_id), None)
    if vendor is None:
        return [f"vendor {vendor_id} not found after creation"]

    expected = {
        "vendor_name": VENDOR_NAME,
        "gstin": GSTIN,
        "city": CITY,
        "state": STATE,
        "msme_registered": IS_MSME_REGISTERED,
        "direct_material": IS_DIRECT_MATERIAL,
        "gst_cert": True,
        "cancelled_cheque": True,
        "msme_declaration": True,
        "trial_po_cap": TRIAL_PO_CAP_RUPEES,
    }
    problems = []
    for field, expected_value in expected.items():
        actual = vendor.get(field)
        if actual != expected_value:
            problems.append(f"{field}: expected {expected_value!r}, got {actual!r}")
    return problems
