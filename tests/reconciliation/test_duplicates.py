from reconciliation.duplicates.detector import flag_duplicates
from reconciliation.models.invoice import Invoice


def _row(invoice_number, invoice_date, po_number, sku="SKU-1", status="CLEAN"):
    inv = Invoice(
        invoice_number=invoice_number, invoice_date=invoice_date, vendor_id="V-1",
        vendor_name_on_invoice="Vendor", po_number=po_number, sku=sku,
        uom="Nos", qty=1.0, rate=1.0, taxable_value=1.0, gst_rate_pct=18.0,
        gst_amount=0.18, invoice_total=1.18,
    )
    return {"invoice": inv, "status": status}


def test_earliest_stays_clean_rest_flagged():
    rows = [
        _row("A", "2026-01-15", "PO-1"),
        _row("B", "2026-01-10", "PO-1"),
        _row("C", "2026-01-20", "PO-1"),
    ]
    result = {r["invoice"].invoice_number: r["status"] for r in flag_duplicates(rows)}
    assert result["B"] == "CLEAN"
    assert result["A"] == "DUPLICATE_INVOICE"
    assert result["C"] == "DUPLICATE_INVOICE"


def test_genuine_defect_not_overridden_by_duplicate_pass():
    rows = [
        _row("A", "2026-01-10", "PO-1", status="RATE_MISMATCH"),
        _row("B", "2026-01-15", "PO-1"),
    ]
    result = {r["invoice"].invoice_number: r["status"] for r in flag_duplicates(rows)}
    assert result["A"] == "RATE_MISMATCH"
    assert result["B"] == "CLEAN"  # only one CLEAN row on this PO, nothing to dedupe


def test_grouping_is_by_po_number_alone_matching_starter_reference():
    # SETTLED: matches the organizer's own reference code (`duplicated(
    # subset=["po_number"])`), not (po_number, sku). A prior version of
    # this test asserted the opposite -- that two different SKUs under
    # the same po_number should NOT be treated as duplicates -- as
    # defensive multi-line-PO protection. Reverted once the status-matrix
    # audit confirmed po_number is globally unique in both the practice
    # set and the live sandbox (260/260 both places), so no multi-line PO
    # exists anywhere for that protection to matter, and the starter's
    # own code groups by po_number alone. So the correct assertion is now
    # the reverse: sharing a po_number is sufficient to flag a duplicate,
    # regardless of sku.
    rows = [
        _row("A", "2026-01-10", "PO-1", sku="SKU-1"),
        _row("B", "2026-01-15", "PO-1", sku="SKU-2"),
    ]
    result = {r["invoice"].invoice_number: r["status"] for r in flag_duplicates(rows)}
    assert result["A"] == "CLEAN"
    assert result["B"] == "DUPLICATE_INVOICE"


def test_same_date_ties_break_on_invoice_number_deterministically():
    rows = [
        _row("Z-999", "2026-01-10", "PO-1"),
        _row("A-001", "2026-01-10", "PO-1"),
    ]
    result = {r["invoice"].invoice_number: r["status"] for r in flag_duplicates(rows)}
    assert result["A-001"] == "CLEAN"
    assert result["Z-999"] == "DUPLICATE_INVOICE"
