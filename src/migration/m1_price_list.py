"""M1 -- Load the 2023 price list. Confirmed against sandbox data:
a product WITH a list_price_2019 is currently
stuck at that stale figure in drishti_price; a product with NO
list_price_2019 already shows list_price_2023 as its drishti_price.
Task brief: 'Set drishti_price to list_price_2023 for every product that
has a 2023 price. Products without one keep the price they already hold.'"""
from typing import Dict, List, Tuple

from api.client import DriClient


def compute_price_updates(products: List[Dict]) -> List[Tuple[str, float]]:
    """Returns [(sku, desired_price), ...] only for products that
    genuinely need a write. Idempotent: a product already at the target
    price produces no entry, so running this twice is always safe."""
    updates = []
    for p in products:
        list_2023 = p.get("list_price_2023")
        if list_2023 is None:
            continue  # no 2023 price -- leave untouched, per the task brief
        if p.get("drishti_price") == list_2023:
            continue  # already correct -- don't write a no-op
        updates.append((p["sku"], list_2023))
    return updates


def run_m1(client: DriClient, dry_run: bool = True) -> Dict:
    data = client.get("/erp/products")
    products = data["products"]
    updates = compute_price_updates(products)

    if not dry_run:
        for sku, price in updates:
            # Minimal mutation: only the one writable field this task
            # touches, per VOS-7-adjacent discipline of never sending
            # more than the API says is writable (only drishti_price/
            # mapped_dri_sku are PATCH-able on /erp/products).
            client.patch(f"/erp/products/{sku}", {"drishti_price": price})

    return {
        "total_products": len(products),
        "updates_needed": len(updates),
        "updates": updates,
        "dry_run": dry_run,
    }


def verify_m1(client: DriClient, expected_updates: List[Tuple[str, float]]) -> List[str]:
    """Post-mutation verification: re-fetch and confirm every updated SKU
    genuinely landed at its target price. Returns a list of problems,
    empty if everything verified clean."""
    data = client.get("/erp/products")
    by_sku = {p["sku"]: p for p in data["products"]}

    problems = []
    for sku, expected_price in expected_updates:
        actual = by_sku.get(sku, {}).get("drishti_price")
        if actual != expected_price:
            problems.append(f"{sku}: expected drishti_price={expected_price}, got {actual}")
    return problems
