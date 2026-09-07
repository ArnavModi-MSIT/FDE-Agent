from configs.reconciliation_config import RATE_TOLERANCE_RUPEES

from ..models.check_result import CheckResult
from .uom import UomCheckOutcome


def check_rate(uom_outcome: UomCheckOutcome) -> CheckResult:
    """Compares CANONICAL (per-base-unit) rates -- a Box(10) invoice's raw
    rate is 10x its PO's per-unit rate by construction, so comparing raw
    rates here would falsely fire on every packaged-uom invoice."""
    a = uom_outcome.invoice_canon.canonical_rate
    b = uom_outcome.po_canon.canonical_rate
    passed = abs(a - b) <= RATE_TOLERANCE_RUPEES
    return CheckResult(
        check="rate",
        passed=passed,
        observed=a,
        expected=b,
        reason="canonical invoice rate differs from PO rate" if not passed else "rates match",
    )
