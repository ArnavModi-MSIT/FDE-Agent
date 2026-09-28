import pytest

from common.io import read_csv_rows


@pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig"])
def test_csv_headers_and_quoted_cells_with_or_without_bom(tmp_path, encoding):
    path = tmp_path / "questions.csv"
    path.write_text('qid,question\nK-01,"Order value, Rs 7,20,000"\n', encoding=encoding)

    assert read_csv_rows(str(path)) == [
        {"qid": "K-01", "question": "Order value, Rs 7,20,000"}
    ]
