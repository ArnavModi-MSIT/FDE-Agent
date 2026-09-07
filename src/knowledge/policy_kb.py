"""Structured policy knowledge base -- every value here is transcribed
directly from the real PDFs in dataset/Document store/, read in full
before this file was written (see CLAUDE.md for the source quotes). This
is a fixed, tiny set of 4 documents; parsing them at runtime would add
complexity for no benefit, so they're baked in here instead, with an
explicit citation comment at every value.

Document codes match each PDF's own header exactly ("Document code: X"),
since that's the only self-identifying string each document provides."""

from datetime import date

PP_2019 = "PP-2019"
PP_2023 = "PP-2023"
VOS_7 = "VOS-7"
WRP_2020 = "WRP-2020"

# PP-2023 "Supersedes: PP-2019 ... in full with effect from 1 October 2023."
PP_2023_EFFECTIVE_FROM = date(2023, 10, 1)


# --- Pricing & Distributor Policy: discount bands -----------------------
# PP-2019 s2.1: <1L nil / 1L-5L 6% / >5L 12% flat
# PP-2023 s2.1: <5L nil / 5L-15L 10% / >15L 14%
def discount_pct(order_value_rupees: float, transaction_date: date) -> float:
    if transaction_date >= PP_2023_EFFECTIVE_FROM:
        if order_value_rupees < 500_000:
            return 0.0
        if order_value_rupees <= 1_500_000:
            return 10.0
        return 14.0
    else:
        if order_value_rupees < 100_000:
            return 0.0
        if order_value_rupees <= 500_000:
            return 6.0
        return 12.0


# --- Credit terms ---------------------------------------------------------
# PP-2019 s3.1: 45 days flat, all tiers, irrespective of tier
# PP-2023 s3.1: 30 days standard, Platinum-tier 60 days
def credit_terms_days(tier: str, transaction_date: date) -> int:
    if transaction_date >= PP_2023_EFFECTIVE_FROM:
        return 60 if tier.strip().lower() == "platinum" else 30
    return 45


# --- Freight ----------------------------------------------------------------
# PP-2019 s4.1: >2L DRI bears freight (FOR destination); <=2L buyer pays (freight-to-pay)
# PP-2023 s4.1: always ex-works -- buyer always bears freight, any order value
def freight_borne_by(order_value_rupees: float, transaction_date: date) -> str:
    if transaction_date >= PP_2023_EFFECTIVE_FROM:
        return "buyer"
    return "DRI" if order_value_rupees > 200_000 else "buyer"


# --- Price revision notice --------------------------------------------------
# PP-2019 s5.1: minimum 30 days written notice
# PP-2023 s5.1: minimum 15 days written notice
def price_revision_notice_days(transaction_date: date) -> int:
    return 15 if transaction_date >= PP_2023_EFFECTIVE_FROM else 30


# --- Warranty & Returns (WRP-2020) ------------------------------------------
WARRANTY_MONTHS_FROM_DESPATCH = 18
WARRANTY_MONTHS_FROM_COMMISSIONING = 12
FLOWTECH_ADDENDUM_MONTHS_FROM_DESPATCH = 24
RESTOCKING_CHARGE_PCT = 10.0
RETURN_WINDOW_DAYS = 30

# WRP-2020 Addendum A: FlowTech pre-acquisition stock gets 24 months from
# despatch instead of the standard 18/12 rule -- but the addendum is an
# unsigned, undated scan flagged by Compliance for regularization. Real
# ambiguity, not a clean lookup -- see CLAUDE.md.
FLOWTECH_ADDENDUM_PROVENANCE_NOTE = (
    "per WRP-2020 Addendum A -- an unsigned, undated scan on file, "
    "flagged by Compliance for regularization"
)


# --- Vendor Onboarding SOP (VOS-7) ------------------------------------------
TRIAL_PO_CAP_RUPEES = 200_000
ONBOARDING_DOCUMENTS = [
    "GST registration certificate",
    "cancelled cheque",
    "MSME declaration (where applicable)",
]

# VOS-7 s3 approval matrix -- compounding, not either/or: a vendor can need
# more than one approval simultaneously.
APPROVAL_SPEND_THRESHOLD_RUPEES = 1_000_000
APPROVAL_SPEND_THRESHOLD_APPROVER = "CFO"
APPROVAL_DIRECT_MATERIAL_APPROVERS = ["Plant Head", "QA"]
APPROVAL_DEFAULT_APPROVER = "GM Procurement"


def required_approvals(projected_annual_spend_rupees: float, is_direct_material: bool = False) -> list:
    approvals = []
    if projected_annual_spend_rupees > APPROVAL_SPEND_THRESHOLD_RUPEES:
        approvals.append(APPROVAL_SPEND_THRESHOLD_APPROVER)
    if is_direct_material:
        approvals.extend(APPROVAL_DIRECT_MATERIAL_APPROVERS)
    if not approvals:
        approvals.append(APPROVAL_DEFAULT_APPROVER)
    return approvals
