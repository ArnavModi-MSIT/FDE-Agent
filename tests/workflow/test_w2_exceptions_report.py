from reconciliation.models.invoice import Invoice
from workflow.w2_exceptions_report import aggregate_exceptions

_ALL_ZERO = {
    "QTY_MISMATCH": 0, "RATE_MISMATCH": 0, "DUPLICATE_INVOICE": 0,
    "MISSING_PO": 0, "VENDOR_MISMATCH": 0, "GST_ERROR": 0, "UOM_MISMATCH": 0,
}


def _invoice(invoice_total: float) -> Invoice:
    return Invoice(
        invoice_number="X", invoice_date="2026-01-01", vendor_id="V-1",
        vendor_name_on_invoice="Vendor", po_number="PO-1", sku="S-1",
        uom="Nos", qty=1.0, rate=1.0, taxable_value=1.0, gst_rate_pct=18.0,
        gst_amount=0.18, invoice_total=invoice_total,
    )


def test_clean_invoices_excluded_from_value_at_risk_all_counts_zero():
    classified = [{"invoice": _invoice(1000), "status": "CLEAN"}]
    report = aggregate_exceptions(classified)
    assert report == {"counts": _ALL_ZERO, "value_at_risk": 0.0}


def test_counts_per_exception_type_includes_zero_types_explicitly():
    classified = [
        {"invoice": _invoice(100), "status": "QTY_MISMATCH"},
        {"invoice": _invoice(200), "status": "QTY_MISMATCH"},
        {"invoice": _invoice(300), "status": "RATE_MISMATCH"},
        {"invoice": _invoice(400), "status": "CLEAN"},
    ]
    report = aggregate_exceptions(classified)
    expected_counts = dict(_ALL_ZERO)
    expected_counts["QTY_MISMATCH"] = 2
    expected_counts["RATE_MISMATCH"] = 1
    assert report["counts"] == expected_counts
    assert report["value_at_risk"] == 600.0  # 100+200+300, CLEAN's 400 excluded


def test_value_at_risk_rounded_to_two_decimals():
    classified = [
        {"invoice": _invoice(100.111), "status": "GST_ERROR"},
        {"invoice": _invoice(0.001), "status": "GST_ERROR"},
    ]
    report = aggregate_exceptions(classified)
    assert report["value_at_risk"] == 100.11
