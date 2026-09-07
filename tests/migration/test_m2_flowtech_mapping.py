from migration.m2_flowtech_mapping import compute_mapping_plan, find_match, strip_flowtech_suffix


def _p(sku, description, price_2023, mapped=None):
    return {"sku": sku, "description": description, "list_price_2023": price_2023, "mapped_dri_sku": mapped}


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


def test_none_price_never_matches_even_against_another_none():
    # Real bug found in the sandbox: FT-1442 has list_price_2023=None,
    # and two real DRI products also happen to have None -- must never
    # treat that as a price match.
    ft = _p("FT-1", "3 HP Pump (FlowTech)", None)
    dri = [_p("CP-1", "3 HP Pump", None), _p("CP-2", "3 HP Pump", None)]
    result = find_match(ft, dri)
    assert result["status"] == "NO_MATCH"
    assert result["matched_sku"] is None


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
