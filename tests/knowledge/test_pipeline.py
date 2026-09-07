import csv
import os

from knowledge.pipeline import run

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(REPO_ROOT, "dataset", "System extracts")


def test_pipeline_is_byte_identical_across_runs(tmp_path):
    out_a = tmp_path / "a.csv"
    out_b = tmp_path / "b.csv"
    run(DATA_DIR, str(out_a))
    run(DATA_DIR, str(out_b))
    assert out_a.read_bytes() == out_b.read_bytes()


def test_submission_has_required_header_and_every_qid_answered(tmp_path):
    out_path = tmp_path / "submission.csv"
    run(DATA_DIR, str(out_path))

    with open(out_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        f.seek(0)
        header = next(csv.reader(f))

    assert header == ["qid", "answer", "governing_source"]

    with open(os.path.join(DATA_DIR, "knowledge_questions.csv"), newline="", encoding="utf-8") as f:
        source_qids = {r["qid"] for r in csv.DictReader(f)}

    output_qids = {r["qid"] for r in rows}
    assert output_qids == source_qids
    for row in rows:
        assert row["answer"] != "UNPARSEABLE", f"{row['qid']} was not answered"
        assert row["governing_source"], f"{row['qid']} has no governing_source"
