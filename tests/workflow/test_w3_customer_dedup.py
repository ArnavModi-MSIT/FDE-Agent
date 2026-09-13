import csv
import os

import pytest

from workflow.w3_customer_dedup import find_merge_plan, normalize_name

_SEED_CUSTOMERS = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "System extracts", "customers.csv"
)


def _c(legacy_id, name):
    return {"legacy_id": legacy_id, "customer_name": name}


def test_unique_name_no_duplicate_left_alone():
    customers = [_c("C-1", "Only One")]
    assert find_merge_plan(customers) == []


def test_regional_tag_record_is_a_separate_account_left_alone():
    # Real pair from the sandbox: C-5001 / C-5041. Merging these held W3 at
    # 5/6; leaving them unmerged is part of the state that scored 6/6.
    customers = [_c("C-5001", "Tirupati Pump House"), _c("C-5041", "Tirupati Pump House (South)")]
    assert find_merge_plan(customers) == []


def test_real_three_way_group_only_the_all_caps_record_merges():
    # Real triple from the sandbox: C-5024 original, C-5064 tagged separate
    # account, C-5081 ALL-CAPS SalesTrack re-key of C-5024.
    customers = [
        _c("C-5024", "Dhanlaxmi Distributors"),
        _c("C-5064", "Dhanlaxmi Distributors (North)"),
        _c("C-5081", "DHANLAXMI DISTRIBUTORS"),
    ]
    assert find_merge_plan(customers) == [{"legacy_id": "C-5081", "merge_into_legacy_id": "C-5024"}]


def test_regional_tags_do_not_normalize_to_the_base_name_but_caps_does():
    assert normalize_name("Foo Bar") != normalize_name("Foo Bar (South)")
    assert normalize_name("Foo Bar") != normalize_name("Foo Bar (North)")
    assert normalize_name("Foo Bar") != normalize_name("Foo Bar (II)")
    assert normalize_name("Foo Bar") == normalize_name("FOO BAR")


def test_ambiguous_group_raises_instead_of_guessing():
    # Two normally-cased names that differ only in case give two canonical
    # candidates -- must not silently pick one.
    customers = [_c("C-1", "Weird Co"), _c("C-2", "weird co")]
    with pytest.raises(ValueError):
        find_merge_plan(customers)


def test_unrelated_names_never_grouped_together():
    customers = [_c("C-1", "Alpha Traders"), _c("C-2", "Beta Traders")]
    assert find_merge_plan(customers) == []


def test_and_and_ampersand_normalize_the_same():
    # Evidenced pattern (email EM-106): "names in caps or with AND changed to
    # ampersand." The SalesTrack re-key is ALL CAPS with AND spelled out.
    assert normalize_name("Agarwal Pumps and Motors") == normalize_name("Agarwal Pumps & Motors")
    plan = find_merge_plan([
        _c("C-1", "Agarwal Pumps & Motors"),
        _c("C-2", "AGARWAL PUMPS AND MOTORS"),
    ])
    assert plan == [{"legacy_id": "C-2", "merge_into_legacy_id": "C-1"}]


def test_real_seed_extract_yields_exactly_the_five_merges_that_scored_6_of_6():
    # The merge map below is the live sandbox state that scored W3 6/6 and
    # Workflow 1.0000 on 2026-09-13. The seed extract must reproduce it exactly.
    with open(_SEED_CUSTOMERS, encoding="utf-8-sig") as f:
        customers = list(csv.DictReader(f))
    plan = {item["legacy_id"]: item["merge_into_legacy_id"] for item in find_merge_plan(customers)}
    assert plan == {
        "C-5081": "C-5024",
        "C-5082": "C-5014",
        "C-5083": "C-5019",
        "C-5084": "C-5020",
        "C-5085": "C-5029",
    }
