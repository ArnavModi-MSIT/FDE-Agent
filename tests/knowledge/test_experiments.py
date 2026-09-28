import csv
import json
from pathlib import Path

import pytest

from knowledge.experiments import prepare_candidates, read_submission

REFERENCE = Path(__file__).resolve().parents[2] / "submissions/knowledge_submission_best_0p9167.csv"


def _plan(tmp_path, variants=None):
    path = tmp_path / "plan.json"
    path.write_text(json.dumps({"variants": variants or [
        {"name": "test", "answers": {"K-03": "The customer bears freight"}},
    ]}), encoding="utf-8")
    return path


def _baseline(tmp_path, qid, field, value):
    rows = read_submission(REFERENCE)
    for row in rows:
        if row["qid"] == qid:
            row[field] = value
    path = tmp_path / "baseline.csv"
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["qid", "answer", "governing_source"])
        writer.writeheader()
        writer.writerows(rows)
    return path


def test_candidates_preserve_sources_and_scoring_answers(tmp_path):
    output = tmp_path / "batch"
    reference_bytes = REFERENCE.read_bytes()
    result = prepare_candidates(REFERENCE, REFERENCE, _plan(tmp_path), output)
    before = read_submission(REFERENCE)
    after = read_submission(output / result["candidates"][0]["file"])
    assert len(after) == 12
    assert [row["qid"] for row in after] == [row["qid"] for row in before]
    for old, new in zip(before, after):
        assert old["governing_source"] == new["governing_source"]
        if old["qid"] != "K-03":
            assert new == old
    assert result["candidates"][0]["score"] is None
    assert REFERENCE.read_bytes() == reference_bytes


@pytest.mark.parametrize("qid,field,value", [
    ("K-08", "answer", "Nil"),
    ("K-05", "answer", "GST registration certificate, cancelled cheque, MSME declaration (as applicable)"),
    ("K-03", "governing_source", "PP-2019"),
])
def test_rejects_regressed_baseline_before_creating_files(tmp_path, qid, field, value):
    output = tmp_path / "batch"
    baseline = _baseline(tmp_path, qid, field, value)
    with pytest.raises(ValueError, match="baseline changes"):
        prepare_candidates(baseline, REFERENCE, _plan(tmp_path), output)
    assert not output.exists()


def test_can_keep_newly_confirmed_answer_while_varying_other_rows(tmp_path):
    baseline = _baseline(tmp_path, "K-03", "answer", "Confirmed freight wording")
    plan = _plan(tmp_path, [{"name": "next", "answers": {
        "K-03": "Discarded freight wording", "K-07": "Updated approval wording",
    }}])
    output = tmp_path / "batch"
    result = prepare_candidates(baseline, REFERENCE, plan, output, preserve=("K-03",))
    rows = {row["qid"]: row for row in read_submission(output / result["candidates"][0]["file"])}
    assert rows["K-03"]["answer"] == "Confirmed freight wording"
    assert rows["K-07"]["answer"] == "Updated approval wording"
    assert set(result["candidates"][0]["changes"]) == {"K-07"}


@pytest.mark.parametrize("variants", [
    [{"name": "bad", "answers": {"K-08": "Nil"}}],
    [{"name": "bad_k05", "answers": {"K-05": "Different document wording"}}],
    [{"name": "../escape", "answers": {"K-03": "Freight"}}],
    [{"name": "one", "answers": {"K-03": "Freight"}},
     {"name": "two", "answers": {"K-03": "Freight"}}],
    [{"name": "blank", "answers": {"K-05": "  "}}],
    [{"name": "trial", "answers": {"K-03": "Customer"}},
     {"name": "TRIAL", "answers": {"K-03": "Distributor"}}],
])
def test_invalid_batch_writes_nothing(tmp_path, variants):
    output = tmp_path / "batch"
    with pytest.raises(ValueError):
        prepare_candidates(REFERENCE, REFERENCE, _plan(tmp_path, variants), output)
    assert not output.exists()


def test_refuses_overwriting_existing_batch(tmp_path):
    output = tmp_path / "batch"
    plan = _plan(tmp_path)
    result = prepare_candidates(REFERENCE, REFERENCE, plan, output)
    path = output / result["candidates"][0]["file"]
    original = path.read_bytes()
    with pytest.raises(FileExistsError):
        prepare_candidates(REFERENCE, REFERENCE, plan, output)
    assert path.read_bytes() == original
