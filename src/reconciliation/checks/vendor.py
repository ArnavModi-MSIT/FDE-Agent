from ..models.check_result import CheckResult
from ..models.invoice import Invoice
from ..models.purchase_order import PurchaseOrder


def check_vendor(invoice: Invoice, po: PurchaseOrder) -> CheckResult:
    """Plain vendor_id equality. Confirmed sufficient against real data:
    both the 'V-' (native DRI) and 'FTV-' (legacy FlowTech) code namespaces
    appear in both invoices and POs with zero orphans against vendors.csv --
    no cross-namespace resolution needed here. That kind of entity
    -resolution problem belongs to W3 (CRM dedup), not this check."""
    passed = invoice.vendor_id.strip() == po.vendor_id.strip()
    return CheckResult(
        check="vendor",
        passed=passed,
        observed=invoice.vendor_id,
        expected=po.vendor_id,
        reason="invoice vendor_id does not match the PO's vendor_id" if not passed else "vendor_id matches",
    )
