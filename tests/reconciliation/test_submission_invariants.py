import csv
import os

from reconciliation.evaluation.metrics import CLASSES
from reconciliation.pipeline import run

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(REPO_ROOT, "dataset", "System extracts")


def _read_submission_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_submission_has_required_header(tmp_path):
    out_path = tmp_path / "submission.csv"
    run(DATA_DIR, str(out_path))
    with open(out_path, newline="", encoding="utf-8") as f:
        header = next(csv.reader(f))
    assert header == ["invoice_number", "status"]


def test_every_invoice_appears_exactly_once(tmp_path):
    out_path = tmp_path / "submission.csv"
    result = run(DATA_DIR, str(out_path))
    rows = _read_submission_rows(out_path)

    invoice_numbers = [r["invoice_number"] for r in rows]
    assert len(invoice_numbers) == len(set(invoice_numbers)), "duplicate output row for an invoice"
    assert len(rows) == result["total"]


def test_every_status_is_a_legal_class(tmp_path):
    out_path = tmp_path / "submission.csv"
    run(DATA_DIR, str(out_path))
    rows = _read_submission_rows(out_path)
    for row in rows:
        assert row["status"] in CLASSES, f"{row['invoice_number']}: illegal status {row['status']!r}"


def test_no_missing_or_extra_invoices_vs_source(tmp_path):
    out_path = tmp_path / "submission.csv"
    run(DATA_DIR, str(out_path))
    rows = _read_submission_rows(out_path)

    with open(os.path.join(DATA_DIR, "vendor_invoices.csv"), newline="", encoding="utf-8") as f:
        source_ids = {r["invoice_number"] for r in csv.DictReader(f)}

    output_ids = {r["invoice_number"] for r in rows}
    assert output_ids == source_ids
