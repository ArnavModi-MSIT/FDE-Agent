from configs.reconciliation_config import QTY_TOLERANCE

from ..models.check_result import CheckResult
from .uom import UomCheckOutcome


def check_quantity(uom_outcome: UomCheckOutcome) -> CheckResult:
    """Compares CANONICAL quantities, not raw invoice.qty vs po.qty --
    caller must have already confirmed uom_outcome.result.passed."""
    a = uom_outcome.invoice_canon.canonical_qty
    b = uom_outcome.po_canon.canonical_qty
    passed = abs(a - b) <= QTY_TOLERANCE
    return CheckResult(
        check="quantity",
        passed=passed,
        observed=a,
        expected=b,
        reason="canonical invoice quantity differs from PO quantity" if not passed else "quantities match",
    )
