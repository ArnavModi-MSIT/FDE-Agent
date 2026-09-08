from typing import Dict, Optional

from ..models.check_result import CheckResult
from ..models.invoice import Invoice
from ..models.purchase_order import PurchaseOrder


def check_vendor(
    invoice: Invoice,
    po: PurchaseOrder,
    vendor_gstin_index: Optional[Dict[str, str]] = None,
) -> CheckResult:
    """vendor_id equality, with a real, evidenced fallback: if the codes
    differ but both resolve to the SAME gstin in vendors.csv, treat it as
    the same real vendor under a duplicate code, not a genuine mismatch.

    This isn't speculative -- confirmed against real data. vendors.csv (60
    rows) has 4 GSTINs each shared by two vendor_ids (e.g. V-1011 and
    V-1055 both file gstin 29XBJJU05331ZB), and ticket FIX-3402 ("Vendor
    code confusion") describes exactly this: "the same supplier under two
    codes... POs and invoices are landing on different codes." Checked
    directly against the 250-invoice practice set: 2 of the 12 raw
    vendor_id mismatches are exactly this pattern (ATP/2026/251 and
    INV-JCP-0155), and both are otherwise fully clean (qty/rate/uom/gst all
    match) once vendor is resolved via GSTIN -- real evidence this is a
    data-hygiene artifact, not a genuine wrong-supplier defect, matching
    the same "look past superficial coding to the real transaction"
    principle already applied to UOM (FIX-3418's "value tallies")."""
    if invoice.vendor_id.strip() == po.vendor_id.strip():
        return CheckResult(
            check="vendor", passed=True, observed=invoice.vendor_id,
            expected=po.vendor_id, reason="vendor_id matches",
        )

    if vendor_gstin_index:
        invoice_gstin = vendor_gstin_index.get(invoice.vendor_id.strip())
        po_gstin = vendor_gstin_index.get(po.vendor_id.strip())
        if invoice_gstin and invoice_gstin == po_gstin:
            return CheckResult(
                check="vendor", passed=True, observed=invoice.vendor_id,
                expected=po.vendor_id,
                reason="vendor_id differs but both resolve to the same gstin (duplicate vendor code)",
            )

    return CheckResult(
        check="vendor", passed=False, observed=invoice.vendor_id,
        expected=po.vendor_id, reason="invoice vendor_id does not match the PO's vendor_id",
    )
