from configs.reconciliation_config import GST_RATE_PCT, GST_TOLERANCE_RUPEES

from ..models.check_result import CheckResult
from ..models.invoice import Invoice


def check_gst(invoice: Invoice) -> CheckResult:
    """Confirmed against real data: gst_rate_pct is 18.0 on all 250
    practice invoices, so a declared rate other than 18% is itself treated
    as an error, not a legitimate variant rate."""
    rate_ok = abs(invoice.gst_rate_pct - GST_RATE_PCT) <= 1e-6
    expected_amount = round(invoice.taxable_value * (GST_RATE_PCT / 100.0), 2)
    amount_ok = abs(invoice.gst_amount - expected_amount) <= GST_TOLERANCE_RUPEES
    passed = rate_ok and amount_ok

    if not rate_ok:
        reason = f"declared gst_rate_pct is not {GST_RATE_PCT}%"
    elif not amount_ok:
        reason = "gst_amount does not match taxable_value at the expected rate"
    else:
        reason = "gst amount matches expected"

    return CheckResult(
        check="gst",
        passed=passed,
        observed=invoice.gst_amount,
        expected=expected_amount,
        reason=reason,
    )
