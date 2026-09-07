from migration.m1_price_list import compute_price_updates


def test_product_with_2019_price_stuck_gets_updated():
    # Real pattern from the sandbox: BV-106
    products = [{"sku": "BV-106", "list_price_2019": 19630, "list_price_2023": 22130, "drishti_price": 19630}]
    assert compute_price_updates(products) == [("BV-106", 22130)]


def test_product_without_2019_price_already_correct_is_skipped():
    # Real pattern from the sandbox: BV-103
    products = [{"sku": "BV-103", "list_price_2019": None, "list_price_2023": 24450, "drishti_price": 24450}]
    assert compute_price_updates(products) == []


def test_product_without_any_2023_price_is_left_untouched():
    products = [{"sku": "X-1", "list_price_2019": 1000, "list_price_2023": None, "drishti_price": 1000}]
    assert compute_price_updates(products) == []


def test_idempotent_second_pass_produces_no_updates():
    # Simulates re-running after the first pass already applied its fix.
    products = [{"sku": "BV-106", "list_price_2019": 19630, "list_price_2023": 22130, "drishti_price": 22130}]
    assert compute_price_updates(products) == []
