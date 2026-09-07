import csv
from typing import Dict


def write_submission(answers: Dict[str, Dict[str, str]], path: str) -> None:
    """Format confirmed directly from the rules page: qid,answer,governing_source."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["qid", "answer", "governing_source"])
        for qid, row in answers.items():
            writer.writerow([qid, row["answer"], row["governing_source"]])
