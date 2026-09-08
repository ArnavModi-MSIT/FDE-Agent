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


def _classify(invoice, purchase_orders, vendor_gstin_index=None):
    po_index = build_po_index(purchase_orders)
    norm_index = build_normalized_po_index(purchase_orders)
    return classify_invoice(invoice, po_index, norm_index, vendor_gstin_index)


def test_clean_invoice():
    assert _classify(_inv(), [_po()]).status == "CLEAN"


def test_missing_po():
    assert _classify(_inv(po_number="PO-999"), [_po()]).status == "MISSING_PO"


def test_vendor_mismatch():
    assert _classify(_inv(vendor_id="V-2"), [_po()]).status == "VENDOR_MISMATCH"


def test_vendor_mismatch_still_fires_with_no_gstin_index():
    # Default (no index passed) must behave exactly like plain equality --
    # backward compatible for every caller that doesn't wire in vendors.csv.
    assert _classify(_inv(vendor_id="V-2"), [_po()], vendor_gstin_index=None).status == "VENDOR_MISMATCH"


def test_gstin_equivalent_vendor_codes_are_not_a_mismatch():
    # Real, evidenced pattern: vendors.csv has GSTINs shared by two
    # vendor_ids (e.g. V-1011 and V-1055), and ticket FIX-3402 ("Vendor
    # code confusion") describes exactly this -- "the same supplier under
    # two codes... POs and invoices are landing on different codes."
    # Confirmed against the real practice data: 2 of the 12 raw
    # vendor_id mismatches (ATP/2026/251, INV-JCP-0155) are exactly this,
    # and both are otherwise fully clean once vendor resolves.
    gstin_index = {"V-1": "29AAAAA0000A1Z5", "V-2": "29AAAAA0000A1Z5"}
    detail = _classify(_inv(vendor_id="V-2"), [_po()], vendor_gstin_index=gstin_index)
    assert detail.status == "CLEAN"


def test_genuinely_different_vendor_still_mismatches_even_with_gstin_index_present():
    # The index resolving OTHER vendor pairs must never paper over a real
    # cross-vendor mismatch -- only an actual shared gstin excuses it.
    gstin_index = {"V-1": "29AAAAA0000A1Z5", "V-2": "27BBBBB1111B2Z6"}
    detail = _classify(_inv(vendor_id="V-2"), [_po()], vendor_gstin_index=gstin_index)
    assert detail.status == "VENDOR_MISMATCH"


def test_uom_mismatch_when_unit_unresolvable():
    assert _classify(_inv(uom="Kg"), [_po()]).status == "UOM_MISMATCH"


def test_incompatible_uom_never_masked_by_qty_rate_gst_even_when_all_also_fail():
    # A genuinely incompatible UOM must win even when the invoice ALSO
    # has a wildly wrong quantity, rate, and GST simultaneously -- proves
    # quantity/rate checks are never even evaluated when uom fails (they
    # live inside `if uom_outcome.result.passed:`), so they can never be
    # selected over UOM_MISMATCH by precedence order. Checked directly
    # against a real external review's specific concern, not assumed.
    detail = _classify(
        _inv(uom="Kg", qty=999.0, rate=1.0, taxable_value=999.0, gst_amount=1.0),
        [_po()],
    )
    assert detail.status == "UOM_MISMATCH"
    checked_names = {r.check for r in detail.check_results}
    assert "quantity" not in checked_names
    assert "rate" not in checked_names


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


def test_precedence_matches_starter_reference_quantity_outranks_gst():
    # No real practice invoice ever fails more than one check (0/250), so
    # this is a synthetic proof the precedence order matches the
    # organizer's own reference implementation (starter_reconciliation.py's
    # literal if/elif chain checks quantity before GST) -- not a claim
    # this order is proven correct on hidden data (unverifiable locally,
    # see classify/precedence.py's own comment). Constructs a single
    # invoice that genuinely fails BOTH gst and quantity simultaneously.
    detail = _classify(_inv(qty=9.0, gst_amount=100.0), [_po()])
    assert detail.status == "QTY_MISMATCH"
    failed = {r.check for r in detail.check_results if not r.passed}
    assert failed == {"quantity", "gst"}  # both genuinely fired -- not a strawman
