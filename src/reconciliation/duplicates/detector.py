from collections import defaultdict
from typing import Dict, List


def flag_duplicates(classified_rows: List[Dict]) -> List[Dict]:
    """Second pass, after every other check has run. Among rows currently
    classified CLEAN, if more than one invoice shares a po_number, the
    earliest-dated one stays CLEAN and the rest become DUPLICATE_INVOICE.
    Only ever demotes a CLEAN row; a row that already has a genuine
    defect (e.g. RATE_MISMATCH) keeps it, since that defect is real
    regardless of billing duplication.

    SETTLED: keyed on po_number alone, matching the organizer's own
    reference implementation exactly (starter_reconciliation.py's literal
    `clean.duplicated(subset=["po_number"], keep="first")`). A prior
    version keyed on (po_number, sku) as multi-line-PO protection --
    submitted, scored byte-identical to baseline, no local rows changed
    either. Also structurally moot on this data: po_number is confirmed
    globally unique across both the practice set and the live sandbox
    (260/260 both places), so it already uniquely determines sku -- there
    is no multi-line PO anywhere in either dataset for the extra key to
    protect against. Reverted once reconciliation_status_matrix.md's
    audit surfaced the starter's code itself as authoritative reference.

    Ties on invoice_date fall back to invoice_number for a deterministic
    result -- no tie exists in the practice data, but an arbitrary
    file-order tiebreak would be a real nondeterminism risk on a larger
    set, and this refinement was never in question (unlike the key)."""
    by_po = defaultdict(list)
    for row in classified_rows:
        if row["status"] == "CLEAN":
            by_po[row["invoice"].po_number].append(row)

    for group in by_po.values():
        if len(group) <= 1:
            continue
        group.sort(key=lambda r: (r["invoice"].invoice_date, r["invoice"].invoice_number))
        for row in group[1:]:
            row["status"] = "DUPLICATE_INVOICE"

    return classified_rows
