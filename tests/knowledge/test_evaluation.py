from knowledge.evaluation import sanity_check


def _answers(**overrides):
    base = {"K-1": {"answer": "10%", "governing_source": "PP-2023", "reasoning": "x"}}
    base.update(overrides)
    return base


def test_clean_answers_no_input_rows_passes():
    assert sanity_check(_answers()) == []


def test_unparseable_answer_flagged():
    answers = _answers(**{"K-2": {"answer": "UNPARSEABLE", "governing_source": "", "reasoning": "no topic"}})
    problems = sanity_check(answers)
    assert any("K-2" in p for p in problems)


def test_blank_answer_flagged_even_with_a_source():
    answers = _answers(**{"K-2": {"answer": "  ", "governing_source": "PP-2023", "reasoning": "x"}})
    problems = sanity_check(answers)
    assert any("K-2" in p and "blank" in p for p in problems)


def test_duplicate_input_qid_flagged():
    input_rows = [{"qid": "K-1", "question": "a"}, {"qid": "K-1", "question": "b"}]
    problems = sanity_check(_answers(), input_rows)
    assert any("duplicate qids" in p for p in problems)


def test_missing_qid_from_answers_flagged():
    input_rows = [{"qid": "K-1", "question": "a"}, {"qid": "K-2", "question": "b"}]
    problems = sanity_check(_answers(), input_rows)  # answers only has K-1
    assert any("missing from answers" in p and "K-2" in p for p in problems)


def test_extra_qid_in_answers_flagged():
    input_rows = [{"qid": "K-1", "question": "a"}]
    answers = _answers(**{"K-99": {"answer": "x", "governing_source": "PP-2023", "reasoning": "y"}})
    problems = sanity_check(answers, input_rows)
    assert any("not in input" in p and "K-99" in p for p in problems)


def test_exact_matching_qids_with_input_rows_passes():
    input_rows = [{"qid": "K-1", "question": "a"}]
    assert sanity_check(_answers(), input_rows) == []


def test_whitespace_only_source_is_rejected():
    answers = _answers(**{"K-2": {"answer": "10%", "governing_source": "  ", "reasoning": "x"}})
    assert any("K-2" in problem for problem in sanity_check(answers))


def test_blank_input_qid_is_rejected_even_when_present_in_answers():
    answers = {" ": {"answer": "10%", "governing_source": "PP-2023"}}
    assert "blank qid in input" in sanity_check(answers, [{"qid": " ", "question": "x"}])
