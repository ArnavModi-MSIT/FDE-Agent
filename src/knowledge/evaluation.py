from typing import Dict, List


def sanity_check(answers: Dict[str, Dict[str, str]]) -> List[str]:
    """Structural invariants only -- there is no local ground truth for
    Knowledge either. Catches bugs: every qid answered, no unparseable
    rows silently slipping through unnoticed."""
    problems = []
    for qid, row in answers.items():
        if row["answer"] == "UNPARSEABLE" or not row["governing_source"]:
            problems.append(f"{qid}: could not be answered -- {row.get('reasoning', '')}")
    return problems
