import pytest

from workflow.w3_customer_dedup import find_merge_plan, normalize_name


def _c(legacy_id, name):
    return {"legacy_id": legacy_id, "customer_name": name}


def test_unique_name_no_duplicate_left_alone():
    customers = [_c("C-1", "Only One")]
    assert find_merge_plan(customers) == []


def test_real_pattern_suffix_duplicate_merges_into_original():
    # Real pair from the sandbox: C-5001 / C-5041
    customers = [_c("C-5001", "Tirupati Pump House"), _c("C-5041", "Tirupati Pump House (South)")]
    plan = find_merge_plan(customers)
    assert plan == [{"legacy_id": "C-5041", "merge_into_legacy_id": "C-5001"}]


def test_real_pattern_three_way_group_both_duplicates_merge_into_original():
    # Real triple from the sandbox: C-5024 (original), C-5064 (suffix
    # dup), C-5081 (ALL-CAPS dup) -- both duplicates merge into the one
    # canonical original, never into each other.
    customers = [
        _c("C-5024", "Dhanlaxmi Distributors"),
        _c("C-5064", "Dhanlaxmi Distributors (North)"),
        _c("C-5081", "DHANLAXMI DISTRIBUTORS"),
    ]
    plan = find_merge_plan(customers)
    targets = {item["legacy_id"]: item["merge_into_legacy_id"] for item in plan}
    assert targets == {"C-5064": "C-5024", "C-5081": "C-5024"}


def test_various_suffix_tags_all_normalize_the_same():
    assert normalize_name("Foo Bar") == normalize_name("Foo Bar (South)")
    assert normalize_name("Foo Bar") == normalize_name("Foo Bar (North)")
    assert normalize_name("Foo Bar") == normalize_name("Foo Bar (II)")
    assert normalize_name("Foo Bar") == normalize_name("FOO BAR")


def test_ambiguous_group_raises_instead_of_guessing():
    # No canonical (no-suffix, not-all-caps) candidate exists -- must not
    # silently pick one.
    customers = [_c("C-1", "Weird Co (South)"), _c("C-2", "WEIRD CO")]
    with pytest.raises(ValueError):
        find_merge_plan(customers)


def test_unrelated_names_never_grouped_together():
    customers = [_c("C-1", "Alpha Traders"), _c("C-2", "Beta Traders")]
    assert find_merge_plan(customers) == []
