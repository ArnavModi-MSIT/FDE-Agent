import os
from collections import Counter
from typing import Dict

from common.io import read_csv_rows

from .classify.classifier import classify_invoice
from .duplicates.detector import flag_duplicates
from .evaluation.evaluator import sanity_check
from .matching.exact import build_po_index
from .matching.fuzzy import build_normalized_po_index
from .normalization.invoice import normalize_invoice
from .normalization.po import normalize_po
from .submission.writer import write_submission


def run(data_dir: str, output_path: str) -> Dict:
    invoice_rows = read_csv_rows(os.path.join(data_dir, "vendor_invoices.csv"))
    po_rows = read_csv_rows(os.path.join(data_dir, "purchase_orders.csv"))

    invoices = [normalize_invoice(r) for r in invoice_rows]
    purchase_orders = [normalize_po(r) for r in po_rows]

    po_index = build_po_index(purchase_orders)
    normalized_po_index = build_normalized_po_index(purchase_orders)

    classified = []
    for invoice in invoices:
        detail = classify_invoice(invoice, po_index, normalized_po_index)
        classified.append({"invoice": invoice, "status": detail.status, "detail": detail})

    classified = flag_duplicates(classified)

    predictions = {row["invoice"].invoice_number: row["status"] for row in classified}

    problems = sanity_check(predictions)
    if problems:
        raise RuntimeError(f"Reconciliation sanity check failed: {problems}")

    write_submission(predictions, output_path)

    return {
        "counts": Counter(predictions.values()),
        "total": len(predictions),
        "output_path": output_path,
        "classified": classified,
    }
