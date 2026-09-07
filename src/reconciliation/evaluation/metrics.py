from typing import Dict, List

CLASSES = [
    "CLEAN",
    "QTY_MISMATCH",
    "RATE_MISMATCH",
    "DUPLICATE_INVOICE",
    "MISSING_PO",
    "VENDOR_MISMATCH",
    "GST_ERROR",
    "UOM_MISMATCH",
]


def per_class_f1(y_true: List[str], y_pred: List[str]) -> Dict[str, Dict[str, float]]:
    result = {}
    for cls in CLASSES:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p == cls)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != cls and p == cls)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p != cls)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        result[cls] = {"precision": precision, "recall": recall, "f1": f1, "support": tp + fn}
    return result


def macro_f1(y_true: List[str], y_pred: List[str]) -> float:
    """Averages F1 over ALL 8 classes, not just the ones present in y_true --
    matches the standard (sklearn) macro-F1 convention the rules page cites.
    A class with zero true support and zero predictions scores F1=0 by this
    definition, same as sklearn's default behavior."""
    scores = per_class_f1(y_true, y_pred)
    return sum(v["f1"] for v in scores.values()) / len(scores)
