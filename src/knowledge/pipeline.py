import os
from typing import Dict

from common.io import read_csv_rows

from .answering import answer_question
from .evaluation import sanity_check
from .submission import write_submission


def run(data_dir: str, output_path: str) -> Dict:
    rows = read_csv_rows(os.path.join(data_dir, "knowledge_questions.csv"))
    if not rows:
        raise ValueError("Knowledge input contains no questions")
    for index, row in enumerate(rows, start=2):
        if None in row or any(not row.get(field) or not row[field].strip() for field in ("qid", "question")):
            raise ValueError(f"Knowledge input row {index}: expected nonblank qid and question columns")

    answers: Dict[str, Dict[str, str]] = {}
    for row in rows:
        result = answer_question(row["qid"], row["question"])
        answers[row["qid"]] = {
            "answer": result.answer,
            "governing_source": result.governing_source,
            "reasoning": result.reasoning,
        }

    problems = sanity_check(answers, rows)
    if problems:
        raise RuntimeError(f"Knowledge sanity check failed: {problems}")

    write_submission(answers, output_path)

    return {"total": len(answers), "output_path": output_path, "answers": answers}
