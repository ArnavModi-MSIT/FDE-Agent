"""M3 -- Finish the SalesTrack migration. For every customer still
migrated_to_salestrack == "N", flip to "Y" and assign a unique crm_id of
the form ST-#####. The 55 already-migrated accounts keep their existing
crm_id untouched -- confirmed from /crm/customers: 85 total, 55 with
migrated_to_salestrack == "Y" already,
30 still "N"."""
import random
from typing import Dict, List


def _generate_unique_crm_id(existing_ids: set) -> str:
    while True:
        candidate = f"ST-{random.randint(10000, 99999)}"
        if candidate not in existing_ids:
            existing_ids.add(candidate)
            return candidate


def compute_migration_plan(customers: List[Dict]) -> List[Dict]:
    """[{legacy_id, crm_id}, ...] for every customer still needing
    migration. Never touches an already-migrated customer -- "the 55
    accounts already migrated keep the crm_id they have," per the task
    brief. Caller should seed random beforehand for reproducibility."""
    existing_ids = {c["crm_id"] for c in customers if c.get("crm_id")}
    plan = []
    for c in customers:
        if c.get("migrated_to_salestrack") == "N":
            new_id = _generate_unique_crm_id(existing_ids)
            plan.append({"legacy_id": c["legacy_id"], "crm_id": new_id})
    return plan


def run_m3(client, dry_run: bool = True, seed: int = 42) -> Dict:
    random.seed(seed)
    data = client.get("/crm/customers")
    customers = data["customers"]
    plan = compute_migration_plan(customers)

    if not dry_run:
        for item in plan:
            client.patch(
                f"/crm/customers/{item['legacy_id']}",
                {"crm_id": item["crm_id"], "migrated_to_salestrack": "Y"},
            )

    return {"total_customers": len(customers), "migrations_needed": len(plan), "plan": plan}


def verify_m3(client, plan: List[Dict]) -> List[str]:
    data = client.get("/crm/customers")
    by_id = {c["legacy_id"]: c for c in data["customers"]}
    problems = []

    seen_crm_ids = set()
    for c in data["customers"]:
        cid = c.get("crm_id")
        if cid:
            if cid in seen_crm_ids:
                problems.append(f"duplicate crm_id detected: {cid}")
            seen_crm_ids.add(cid)

    for item in plan:
        actual = by_id.get(item["legacy_id"], {})
        if actual.get("crm_id") != item["crm_id"]:
            problems.append(f"{item['legacy_id']}: expected crm_id={item['crm_id']!r}, got {actual.get('crm_id')!r}")
        if actual.get("migrated_to_salestrack") != "Y":
            problems.append(
                f"{item['legacy_id']}: expected migrated_to_salestrack='Y', "
                f"got {actual.get('migrated_to_salestrack')!r}"
            )
    return problems
