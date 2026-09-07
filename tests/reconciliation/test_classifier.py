from reconciliation.classify.classifier import classify_invoice
from reconciliation.matching.exact import build_po_index
from reconciliation.matching.fuzzy import build_normalized_po_index
from reconciliation.models.invoice import Invoice
from reconciliation.models.purchase_order import PurchaseOrder


def _po(**overrides):
    base = dict(
        po_number="PO-1", po_date="2026-01-01", vendor_id="V-1",
        sku="SKU-1", description="Widget", uom="Nos", qty=10.0,
        rate=100.0, po_value=1000.0, plant="Pune",
    )
    base.update(overrides)
    return PurchaseOrder(**base)


def _inv(**overrides):
    base = dict(
        invoice_number="INV-1", invoice_date="2026-01-05", vendor_id="V-1",
        vendor_name_on_invoice="Vendor One", po_number="PO-1", sku="SKU-1",
        uom="Nos", qty=10.0, rate=100.0, taxable_value=1000.0,
        gst_rate_pct=18.0, gst_amount=180.0, invoice_total=1180.0,
    )
    base.update(overrides)
    return Invoice(**base)


def _classify(invoice, purchase_orders):
    po_index = build_po_index(purchase_orders)
    norm_index = build_normalized_po_index(purchase_orders)
    return classify_invoice(invoice, po_index, norm_index)


def test_clean_invoice():
    assert _classify(_inv(), [_po()]).status == "CLEAN"


def test_missing_po():
    assert _classify(_inv(po_number="PO-999"), [_po()]).status == "MISSING_PO"


def test_vendor_mismatch():
    assert _classify(_inv(vendor_id="V-2"), [_po()]).status == "VENDOR_MISMATCH"


def test_uom_mismatch_when_unit_unresolvable():
    assert _classify(_inv(uom="Kg"), [_po()]).status == "UOM_MISMATCH"


def test_box_packaging_reconciles_not_uom_mismatch():
    # The real trap: a naive string/raw-number comparison would call this
    # BOTH UOM_MISMATCH and RATE_MISMATCH. Once canonicalized it's CLEAN.
    po = _po(qty=200.0, rate=5781.65)
    inv = _inv(
        uom="Box(10)", qty=20.0, rate=57816.5,
        taxable_value=20 * 57816.5,
        gst_amount=round(20 * 57816.5 * 0.18, 2),
    )
    assert _classify(inv, [po]).status == "CLEAN"


def test_box_packaging_on_po_side_also_reconciles():
    # Every real practice-data Box(10) case has the PACKAGING on the
    # invoice side, PO always plain Nos. canonicalize() is called
    # identically on both sides (checks/uom.py), so this should already
    # work symmetrically -- proving it rather than assuming it, since an
    # external review specifically flagged this direction as untested.
    po = _po(uom="Box(10)", qty=20.0, rate=57816.5)
    inv = _inv(
        uom="Nos", qty=200.0, rate=5781.65,
        taxable_value=200 * 5781.65,
        gst_amount=round(200 * 5781.65 * 0.18, 2),
    )
    assert _classify(inv, [po]).status == "CLEAN"


def test_qty_mismatch():
    assert _classify(_inv(qty=9.0), [_po()]).status == "QTY_MISMATCH"


def test_rate_mismatch():
    assert _classify(_inv(rate=105.0), [_po()]).status == "RATE_MISMATCH"


def test_gst_error_wrong_amount():
    assert _classify(_inv(gst_amount=100.0), [_po()]).status == "GST_ERROR"


def test_gst_error_wrong_declared_rate():
    assert _classify(_inv(gst_rate_pct=12.0), [_po()]).status == "GST_ERROR"


def test_precedence_gst_error_outranks_quantity_mismatch():
    # No real practice invoice ever fails more than one check (0/250), so
    # this is a synthetic proof the precedence.py reorder actually took
    # effect -- not a claim it's the CORRECT order (unverifiable locally,
    # see classify/precedence.py's own comment). Constructs a single
    # invoice that genuinely fails BOTH gst and quantity simultaneously.
    detail = _classify(_inv(qty=9.0, gst_amount=100.0), [_po()])
    assert detail.status == "GST_ERROR"
    failed = {r.check for r in detail.check_results if not r.passed}
    assert failed == {"quantity", "gst"}  # both genuinely fired -- not a strawman
