import csv
import os

import pytest

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


def test_engine_reproduces_the_scoring_submission_byte_for_byte(tmp_path):
    # The protected reference scored 0.9167. The engine must regenerate it
    # exactly so scripts/run_knowledge.py cannot overwrite the best output
    # with a weaker answer bundle.
    out_path = tmp_path / "submission.csv"
    run(DATA_DIR, str(out_path))
    best = os.path.join(REPO_ROOT, "submissions", "knowledge_submission_best_0p9167.csv")
    with open(best, "rb") as f:
        assert out_path.read_bytes() == f.read()


@pytest.mark.parametrize("content", [
    "qid,question\n",
    "id,question\nK-01,What discount applies?\n",
    "qid,question\nK-01,\n",
    "qid,question\n,What discount applies?\n",
    "qid,question\nK-01,What discount applies?,unexpected extra cell\n",
])
def test_bad_input_does_not_overwrite_existing_output(tmp_path, content):
    (tmp_path / "knowledge_questions.csv").write_text(content, encoding="utf-8")
    output = tmp_path / "output.csv"
    output.write_text("existing submission", encoding="utf-8")
    with pytest.raises(ValueError, match="Knowledge input"):
        run(str(tmp_path), str(output))
    assert output.read_text(encoding="utf-8") == "existing submission"


def test_pipeline_accepts_excel_utf8_bom(tmp_path):
    (tmp_path / "knowledge_questions.csv").write_text(
        "qid,question\nK-01,What discount applies to an order of Rs 720000 in March 2024?\n",
        encoding="utf-8-sig",
    )
    result = run(str(tmp_path), str(tmp_path / "output.csv"))
    assert result["answers"]["K-01"]["answer"] == "10%"
