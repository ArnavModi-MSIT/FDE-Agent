from typing import Dict, List

from .metrics import CLASSES, macro_f1, per_class_f1


def evaluate(y_true: List[str], y_pred: List[str]) -> Dict:
    return {"macro_f1": macro_f1(y_true, y_pred), "per_class": per_class_f1(y_true, y_pred)}


def sanity_check(predictions: Dict[str, str]) -> List[str]:
    """Structural invariants only -- there is no local ground truth for the
    practice dataset, so this cannot measure accuracy, only catch bugs:
    every invoice classified exactly once, every status a legal class."""
    problems: List[str] = []
    for invoice_number, status in predictions.items():
        if status not in CLASSES:
            problems.append(f"{invoice_number}: illegal status {status!r}")
    return problems
