from collections import Counter
from typing import Dict, List


def sanity_check(answers: Dict[str, Dict[str, str]], input_rows: List[Dict[str, str]] = None) -> List[str]:
    """Structural invariants only -- there is no local ground truth for
    Knowledge either. Catches bugs: every qid answered, no unparseable
    rows silently slipping through unnoticed, and (when the raw input
    rows are supplied) the submission-invariant checks a code-review
    audit flagged as missing: exact qid-set match against the input, no
    duplicate input qids silently overwriting each other, no blank
    answer/source string sneaking past the UNPARSEABLE check."""
    problems = []
    for qid, row in answers.items():
        if row["answer"] == "UNPARSEABLE" or not row["governing_source"].strip():
            problems.append(f"{qid}: could not be answered -- {row.get('reasoning', '')}")
        elif not row["answer"].strip():
            problems.append(f"{qid}: answer is blank")

    if input_rows is not None:
        input_qids = [r["qid"] for r in input_rows]
        if any(not qid.strip() for qid in input_qids):
            problems.append("blank qid in input")
        dupes = [qid for qid, count in Counter(input_qids).items() if count > 1]
        if dupes:
            problems.append(f"duplicate qids in input: {dupes}")
        missing = set(input_qids) - set(answers)
        if missing:
            problems.append(f"qids in input but missing from answers: {sorted(missing)}")
        extra = set(answers) - set(input_qids)
        if extra:
            problems.append(f"qids in answers but not in input: {sorted(extra)}")

    return problems
