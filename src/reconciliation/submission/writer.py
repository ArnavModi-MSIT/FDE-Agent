import csv
from typing import Dict


def write_submission(predictions: Dict[str, str], path: str) -> None:
    """Format confirmed on the rules page: a single CSV with required
    headers 'invoice_number,status'. A missing/rejected file doesn't
    consume an attempt, but a malformed one would -- so this is the one
    place format correctness matters most."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["invoice_number", "status"])
        for invoice_number, status in predictions.items():
            writer.writerow([invoice_number, status])
