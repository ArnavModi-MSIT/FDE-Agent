from knowledge.parsing import parse_question

# The 12 real practice questions, topic-labeled by hand -- proves the
# classifier routes every one of them correctly, not just a synthetic case.
_REAL_QUESTIONS = [
    ("K-01", "A distributor places a single order of Rs 7,20,000 in March 2024. What discount applies?", "discount"),
    ("K-02", "What are the standard credit terms for a Gold-tier distributor today?", "credit_terms"),
    ("K-03", "Who bears freight on a Rs 3,00,000 distributor order shipped in February 2024?", "freight"),
    ("K-04", "What warranty applies to a FlowTech-branded pump supplied from pre-acquisition stock?", "warranty_flowtech"),
    ("K-05", "Which documents must a new vendor submit at onboarding?", "vendor_documents"),
    ("K-06", "What is the maximum value of a trial purchase order for a newly onboarded vendor?", "trial_po_cap"),
    ("K-07", "A new vendor's projected annual spend is Rs 14,00,000. Whose approval is required?", "approval_matrix"),
    ("K-08", "What discount applies to a single order of Rs 4,20,000 placed in March 2024?", "discount"),
    ("K-09", "What restocking charge applies to returns?", "restocking_charge"),
    ("K-10", "How much notice must DRI give before revising list prices today?", "price_revision_notice"),
    ("K-11", "A DRI pump is despatched in January 2025 and commissioned in June 2025. When does warranty end?", "warranty_calc"),
    ("K-12", "What credit terms does a Platinum-tier distributor receive?", "credit_terms"),
]


def test_all_real_practice_questions_classify_correctly():
    for qid, text, expected_topic in _REAL_QUESTIONS:
        parsed = parse_question(text)
        assert parsed.topic == expected_topic, f"{qid}: got {parsed.topic}, expected {expected_topic}"


def test_tier_extraction_prefers_suffixed_designation_over_bare_adjective():
    # Real bug found by reading the pipeline's own reasoning trace: "the
    # standard credit terms for a Gold-tier distributor" used to extract
    # tier="standard" (the first bare word match) instead of "Gold" (the
    # real tier, appearing later with a "-tier" suffix). The wrong answer
    # happened to coincide with the right one for THIS question (neither
    # is Platinum), which is exactly how a bug like this hides.
    parsed = parse_question("What are the standard credit terms for a Gold-tier distributor today?")
    assert parsed.tier == "Gold"


def test_tier_extraction_falls_back_to_bare_word_when_no_suffix_exists():
    parsed = parse_question("What credit terms does Platinum receive?")
    assert parsed.tier == "Platinum"


def test_unrecognized_question_returns_no_topic_not_a_guess():
    parsed = parse_question("What is the capital of France?")
    assert parsed.topic is None


def test_amount_extraction_handles_indian_grouping():
    parsed = parse_question("A distributor places a single order of Rs 7,20,000 in March 2024. What discount applies?")
    assert parsed.amount_rupees == 720_000


def test_warranty_calc_extracts_both_dates_in_order():
    parsed = parse_question("A DRI pump is despatched in January 2025 and commissioned in June 2025. When does warranty end?")
    assert (parsed.month, parsed.year) == (1, 2025)
    assert (parsed.second_month, parsed.second_year) == (6, 2025)
