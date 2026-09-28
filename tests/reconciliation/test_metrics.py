import pytest

from reconciliation.evaluation.metrics import CLASSES, macro_f1, per_class_f1


def test_perfect_prediction_on_all_classes_scores_one():
    y = list(CLASSES)  # one instance of each class
    assert macro_f1(y, y) == 1.0


def test_one_misclassification_reduces_score():
    y_true = list(CLASSES)
    y_pred = list(CLASSES)
    y_pred[0] = CLASSES[1]  # true CLEAN wrongly predicted as QTY_MISMATCH
    score = macro_f1(y_true, y_pred)
    assert 0.0 < score < 1.0


def test_absent_class_scores_zero_not_excluded():
    y_true = ["CLEAN", "CLEAN"]
    y_pred = ["CLEAN", "CLEAN"]
    scores = per_class_f1(y_true, y_pred)
    assert scores["CLEAN"]["f1"] == 1.0
    assert scores["GST_ERROR"]["support"] == 0
    assert scores["GST_ERROR"]["f1"] == 0.0


@pytest.mark.parametrize("metric", [per_class_f1, macro_f1])
@pytest.mark.parametrize("y_true,y_pred", [
    (["CLEAN", "CLEAN"], ["CLEAN"]),
    (["CLEAN"], ["CLEAN", "CLEAN"]),
])
def test_unequal_label_counts_raise_instead_of_truncating(metric, y_true, y_pred):
    with pytest.raises(ValueError, match="equal label counts"):
        metric(y_true, y_pred)
