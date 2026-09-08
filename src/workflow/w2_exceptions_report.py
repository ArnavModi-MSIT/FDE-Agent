"""W2 -- The MD's exceptions report. Deliberately reuses reconciliation/
directly (classify_invoice, flag_duplicates, matching) rather than a
second classifier -- see CLAUDE.md sec 9: this is the whole reason
reconciliation/pipeline.py was built to expose per-invoice detail, not
just the final CSV. The CSV Reconciliation family and this Workflow task
must never be able to disagree about what's wrong with a given invoice.

Confirmed against real sandbox calls (not assumed): GET /erp/invoices ->
{"invoices": [...]}, 250 rows, same field names as the local CSV but
numeric fields as native JSON numbers, not strings -- see the safe_float
fix in reconciliation/normalization/common.py this required."""
from typing import Dict, List

from api.client import DriClient
from reconciliation.classify.classifier import classify_invoice
from reconciliation.duplicates.detector import flag_duplicates
from reconciliation.evaluation.metrics import CLASSES
from reconciliation.matching.exact import build_po_index
from reconciliation.matching.fuzzy import build_normalized_po_index
from reconciliation.normalization.invoice import normalize_invoice
from reconciliation.normalization.po import normalize_po

_EXCEPTION_TYPES = [c for c in CLASSES if c != "CLEAN"]


def aggregate_exceptions(classified: List[Dict]) -> Dict:
    """Pure function: classified rows -> the report payload. No API calls,
    so this is directly unit-testable against synthetic data.

    Explicitly includes all 7 exception types in `counts`, even at 0 --
    live sandbox check-count preview showed 6/8 with only nonzero types
    included (UOM_MISMATCH, at 0, was omitted entirely); this is the
    cheap, well-reasoned first fix to try before spending a real scored
    attempt. Confirmed via the free live preview, not the real leaderboard.

    "Value at risk": the total invoice_total of every non-CLEAN invoice,
    not just the mismatch delta. Chosen because it's the only definition
    that applies uniformly across all 7 exception types --
    MISSING_PO/VENDOR_MISMATCH/DUPLICATE_INVOICE/UOM_MISMATCH have no
    natural "delta" to sum (there's no trusted PO comparison for a
    missing PO, and a duplicate's risk is its full amount, not a
    difference). Not independently confirmed against a spec -- same
    open-assumption discipline as Knowledge's governing_source format."""
    counts: Dict[str, int] = {exc_type: 0 for exc_type in _EXCEPTION_TYPES}
    value_at_risk = 0.0
    for row in classified:
        if row["status"] == "CLEAN":
            continue
        counts[row["status"]] += 1
        value_at_risk += row["invoice"].invoice_total

    return {"counts": counts, "value_at_risk": round(value_at_risk, 2)}


def compute_exceptions_report(client: DriClient) -> Dict:
    invoice_rows = client.get("/erp/invoices")["invoices"]
    po_rows = client.get("/erp/purchase_orders")["purchase_orders"]

    invoices = [normalize_invoice(r) for r in invoice_rows]
    purchase_orders = [normalize_po(r) for r in po_rows]

    po_index = build_po_index(purchase_orders)
    normalized_po_index = build_normalized_po_index(purchase_orders)

    classified = []
    for invoice in invoices:
        detail = classify_invoice(invoice, po_index, normalized_po_index)
        classified.append({"invoice": invoice, "status": detail.status})

    classified = flag_duplicates(classified)
    return aggregate_exceptions(classified)


def post_exceptions_report(client: DriClient, report: Dict) -> Dict:
    return client.post("/erp/reports/exceptions", report)
