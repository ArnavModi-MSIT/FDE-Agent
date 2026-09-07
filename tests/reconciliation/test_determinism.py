import os

from reconciliation.pipeline import run

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(REPO_ROOT, "dataset", "System extracts")


def test_pipeline_is_byte_identical_across_runs(tmp_path):
    """A submission system with a 5-attempts/day budget can't afford a
    nondeterministic classifier. Runs the real pipeline against the real
    practice data twice, into two separate files, and requires an exact
    byte match."""
    out_a = tmp_path / "submission_a.csv"
    out_b = tmp_path / "submission_b.csv"

    run(DATA_DIR, str(out_a))
    run(DATA_DIR, str(out_b))

    assert out_a.read_bytes() == out_b.read_bytes()
