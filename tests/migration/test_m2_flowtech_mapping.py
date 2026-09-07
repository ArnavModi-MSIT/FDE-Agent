from migration.m2_flowtech_mapping import compute_mapping_plan, find_match, strip_flowtech_suffix


def _p(sku, description, price_2023, mapped=None, price_2019=None):
    return {
        "sku": sku, "description": description, "list_price_2023": price_2023,
        "list_price_2019": price_2019, "mapped_dri_sku": mapped,
    }


def test_strip_single_suffix():
    assert strip_flowtech_suffix("3 HP Pump (FlowTech)") == "3 HP Pump"


def test_strip_doubled_suffix():
    # Real bug found in the sandbox: FT-1470's description has the
    # suffix twice. Must strip both via a real trailing-suffix loop.
    assert strip_flowtech_suffix("15 HP Pump (FlowTech) (FlowTech)") == "15 HP Pump"


def test_no_suffix_left_alone():
    assert strip_flowtech_suffix("Just A Pump") == "Just A Pump"


def test_unique_match():
    ft = _p("FT-1", "3 HP Pump (FlowTech)", 1000)
    dri = [_p("CP-1", "3 HP Pump", 1000)]
    result = find_match(ft, dri)
    assert result == {"status": "UNIQUE_MATCH", "matched_sku": "CP-1", "candidates": ["CP-1"]}


def test_no_match_when_description_differs():
    ft = _p("FT-1", "3 HP Pump (FlowTech)", 1000)
    dri = [_p("CP-1", "5 HP Pump", 1000)]
    assert find_match(ft, dri)["status"] == "NO_MATCH"


def test_no_match_when_price_differs():
    ft = _p("FT-1", "3 HP Pump (FlowTech)", 1000)
    dri = [_p("CP-1", "3 HP Pump", 2000)]
    assert find_match(ft, dri)["status"] == "NO_MATCH"


def test_multiple_matches_never_silently_picks_one():
    ft = _p("FT-1", "3 HP Pump (FlowTech)", 1000)
    dri = [_p("CP-1", "3 HP Pump", 1000), _p("CP-2", "3 HP Pump", 1000)]
    result = find_match(ft, dri)
    assert result["status"] == "MULTIPLE_MATCHES"
    assert result["matched_sku"] is None
    assert set(result["candidates"]) == {"CP-1", "CP-2"}


def test_none_2023_price_never_matches_even_against_another_none():
    # Neither side has ANY usable price (2023 or 2019) -- must never
    # treat None==None as a match, on either field.
    ft = _p("FT-1", "3 HP Pump (FlowTech)", None)
    dri = [_p("CP-1", "3 HP Pump", None), _p("CP-2", "3 HP Pump", None)]
    result = find_match(ft, dri)
    assert result["status"] == "NO_MATCH"
    assert result["matched_sku"] is None


def test_falls_back_to_2019_price_when_2023_is_none():
    # Real pattern from the sandbox: FT-1442 (list_price_2023=None,
    # list_price_2019=54590) uniquely matches SM-136 (same 2019 price),
    # even though SM-130 also has list_price_2023=None -- SM-130's own
    # 2019 price (93560) doesn't match, so the fallback still resolves
    # uniquely rather than becoming ambiguous.
    ft = _p("FT-1442", "3 HP Openwell Submersible Pump (FlowTech)", None, price_2019=54590)
    dri = [
        _p("SM-104", "3 HP Openwell Submersible Pump", 84800, price_2019=77310),
        _p("SM-130", "3 HP Openwell Submersible Pump", None, price_2019=93560),
        _p("SM-136", "3 HP Openwell Submersible Pump", None, price_2019=54590),
    ]
    result = find_match(ft, dri)
    assert result == {"status": "UNIQUE_MATCH", "matched_sku": "SM-136", "candidates": ["SM-136"]}


def test_2019_fallback_never_guesses_when_still_ambiguous():
    ft = _p("FT-1", "3 HP Pump (FlowTech)", None, price_2019=500)
    dri = [_p("CP-1", "3 HP Pump", None, price_2019=500), _p("CP-2", "3 HP Pump", None, price_2019=500)]
    result = find_match(ft, dri)
    assert result["status"] == "MULTIPLE_MATCHES"
    assert result["matched_sku"] is None


def test_no_2019_fallback_when_ft_has_neither_price():
    ft = _p("FT-1", "3 HP Pump (FlowTech)", None, price_2019=None)
    dri = [_p("CP-1", "3 HP Pump", None, price_2019=None)]
    result = find_match(ft, dri)
    assert result["status"] == "NO_MATCH"


def test_compute_mapping_plan_skips_already_mapped_products():
    products = [
        _p("FT-1", "3 HP Pump (FlowTech)", 1000, mapped="CP-1"),  # already mapped -- skip
        _p("CP-1", "3 HP Pump", 1000),
    ]
    plan = compute_mapping_plan(products)
    assert plan == {"resolved": [], "unresolved": []}


def test_compute_mapping_plan_separates_resolved_and_unresolved():
    products = [
        _p("FT-1", "3 HP Pump (FlowTech)", 1000),
        _p("CP-1", "3 HP Pump", 1000),
        _p("FT-2", "9 HP Pump (FlowTech)", 500),  # no match
    ]
    plan = compute_mapping_plan(products)
    assert plan["resolved"] == [{"sku": "FT-1", "mapped_dri_sku": "CP-1"}]
    assert len(plan["unresolved"]) == 1
    assert plan["unresolved"][0]["sku"] == "FT-2"
