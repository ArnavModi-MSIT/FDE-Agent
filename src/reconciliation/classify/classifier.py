from dataclasses import dataclass
from typing import Dict, List, Optional

from ..checks import gst as gst_check
from ..checks import po as po_check
from ..checks import quantity as qty_check
from ..checks import rate as rate_check
from ..checks import uom as uom_check
from ..checks import vendor as vendor_check
from ..matching.resolver import MatchResult, resolve
from ..models.check_result import CheckResult
from ..models.invoice import Invoice
from ..models.purchase_order import PurchaseOrder
from .precedence import PRECEDENCE


@dataclass(frozen=True)
class ClassificationDetail:
    status: str
    check_results: List[CheckResult]  # every check that ran, not just the winner -- full evidence for W2/debugging
    match_result: MatchResult


def classify_invoice(
    invoice: Invoice,
    po_index: Dict[str, PurchaseOrder],
    normalized_po_index: Dict[str, PurchaseOrder],
    vendor_gstin_index: Optional[Dict[str, str]] = None,
) -> ClassificationDetail:
    match_result = resolve(invoice, po_index, normalized_po_index)
    po_result = po_check.check_po_exists(match_result)

    if not po_result.passed:
        return ClassificationDetail("MISSING_PO", [po_result], match_result)

    po = match_result.purchase_order
    results: List[CheckResult] = [po_result, vendor_check.check_vendor(invoice, po, vendor_gstin_index)]

    uom_outcome = uom_check.check_uom(invoice, po)
    results.append(uom_outcome.result)

    if uom_outcome.result.passed:
        # Quantity/rate only make sense once units reconcile -- comparing
        # raw numbers across incompatible units would just add noise on
        # top of the UOM_MISMATCH that already explains the row.
        results.append(qty_check.check_quantity(uom_outcome))
        results.append(rate_check.check_rate(uom_outcome))

    results.append(gst_check.check_gst(invoice))

    failed_checks = {r.check for r in results if not r.passed}
    for status, check_name in PRECEDENCE[1:]:  # po_exists already handled above
        if check_name in failed_checks:
            return ClassificationDetail(status, results, match_result)

    return ClassificationDetail("CLEAN", results, match_result)
