import random
import re

from migration.m3_salestrack_migration import compute_migration_plan

_CRM_ID_PATTERN = re.compile(r"^ST-\d{5}$")


def _c(legacy_id, migrated, crm_id=None):
    return {"legacy_id": legacy_id, "migrated_to_salestrack": migrated, "crm_id": crm_id}


def test_only_unmigrated_customers_get_a_plan_entry():
    random.seed(1)
    customers = [
        _c("C-1", "N"),
        _c("C-2", "Y", "ST-11111"),
        _c("C-3", "N"),
    ]
    plan = compute_migration_plan(customers)
    assert {p["legacy_id"] for p in plan} == {"C-1", "C-3"}


def test_already_migrated_customer_never_appears_in_plan():
    random.seed(1)
    customers = [_c("C-1", "Y", "ST-11111"), _c("C-2", "Y", "ST-22222")]
    assert compute_migration_plan(customers) == []


def test_generated_ids_are_unique_and_correctly_formatted():
    random.seed(1)
    customers = [_c(f"C-{i}", "N") for i in range(20)]
    plan = compute_migration_plan(customers)
    ids = [p["crm_id"] for p in plan]
    assert len(ids) == len(set(ids))  # no collisions among themselves
    assert all(_CRM_ID_PATTERN.match(i) for i in ids)


def test_generated_ids_never_collide_with_existing_ones():
    random.seed(1)
    customers = [_c("C-1", "Y", "ST-50000"), _c("C-2", "N")]
    plan = compute_migration_plan(customers)
    assert plan[0]["crm_id"] != "ST-50000"
