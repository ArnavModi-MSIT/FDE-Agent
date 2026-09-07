from datetime import date

from knowledge import policy_kb


def test_discount_2019_bands():
    d = date(2023, 6, 1)  # before the 2023-10-01 cutover
    assert policy_kb.discount_pct(50_000, d) == 0.0
    assert policy_kb.discount_pct(100_000, d) == 6.0
    assert policy_kb.discount_pct(500_000, d) == 6.0
    assert policy_kb.discount_pct(500_001, d) == 12.0


def test_discount_2023_bands():
    d = date(2024, 3, 1)
    assert policy_kb.discount_pct(499_999, d) == 0.0
    assert policy_kb.discount_pct(500_000, d) == 10.0
    assert policy_kb.discount_pct(1_500_000, d) == 10.0
    assert policy_kb.discount_pct(1_500_001, d) == 14.0


def test_discount_cutover_boundary_is_2023_not_2019():
    # PP-2023 "effective 1 October 2023" -- exactly on the cutover date,
    # the NEW policy already applies (not the day before).
    on_cutover = date(2023, 10, 1)
    day_before = date(2023, 9, 30)
    assert policy_kb.discount_pct(600_000, on_cutover) == 10.0  # 2023 band
    assert policy_kb.discount_pct(600_000, day_before) == 12.0  # 2019 band


def test_credit_terms():
    old = date(2020, 1, 1)
    new = date(2024, 1, 1)
    assert policy_kb.credit_terms_days("Gold", old) == 45
    assert policy_kb.credit_terms_days("Platinum", old) == 45  # 2019: flat, irrespective of tier
    assert policy_kb.credit_terms_days("Gold", new) == 30
    assert policy_kb.credit_terms_days("Platinum", new) == 60
    assert policy_kb.credit_terms_days("Standard", new) == 30


def test_freight():
    old = date(2020, 1, 1)
    new = date(2024, 1, 1)
    assert policy_kb.freight_borne_by(300_000, old) == "DRI"     # >2L under 2019: DRI pays
    assert policy_kb.freight_borne_by(100_000, old) == "buyer"   # <=2L under 2019: buyer pays
    assert policy_kb.freight_borne_by(300_000, new) == "buyer"   # 2023: always buyer, any value
    assert policy_kb.freight_borne_by(100_000, new) == "buyer"


def test_price_revision_notice():
    assert policy_kb.price_revision_notice_days(date(2020, 1, 1)) == 30
    assert policy_kb.price_revision_notice_days(date(2024, 1, 1)) == 15


def test_approval_matrix_compounding():
    # A vendor can trigger more than one approval simultaneously -- the W1
    # task's own vendor (Rs 14L, direct-material) needs CFO AND Plant Head
    # AND QA, not just one.
    assert policy_kb.required_approvals(1_400_000, is_direct_material=True) == ["CFO", "Plant Head", "QA"]
    assert policy_kb.required_approvals(1_400_000, is_direct_material=False) == ["CFO"]
    assert policy_kb.required_approvals(50_000, is_direct_material=True) == ["Plant Head", "QA"]
    assert policy_kb.required_approvals(50_000, is_direct_material=False) == ["GM Procurement"]
    assert policy_kb.required_approvals(1_000_000, is_direct_material=False) == ["GM Procurement"]  # exactly at threshold: not ">" so no CFO
