from dataclasses import dataclass

from ..models.check_result import CheckResult
from ..models.invoice import Invoice
from ..models.purchase_order import PurchaseOrder
from ..uom.converter import CanonicalQuantity, canonicalize


@dataclass(frozen=True)
class UomCheckOutcome:
    """Carries the canonicalized quantities/rates that quantity.py and
    rate.py need, plus the reportable CheckResult for this check itself."""

    invoice_canon: CanonicalQuantity
    po_canon: CanonicalQuantity
    result: CheckResult


def check_uom(invoice: Invoice, po: PurchaseOrder) -> UomCheckOutcome:
    invoice_canon = canonicalize(invoice.qty, invoice.rate, invoice.uom)
    po_canon = canonicalize(po.qty, po.rate, po.uom)
    ok = invoice_canon.ok and po_canon.ok and invoice_canon.base_unit == po_canon.base_unit

    result = CheckResult(
        check="uom",
        passed=ok,
        observed=invoice.uom,
        expected=po.uom,
        reason="unit could not be reconciled to a common base"
        if not ok
        else "units reconcile to a common base",
    )
    return UomCheckOutcome(invoice_canon=invoice_canon, po_canon=po_canon, result=result)
