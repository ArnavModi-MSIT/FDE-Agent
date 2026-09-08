#!/usr/bin/env python3
"""Permanent, re-runnable record of the empirical checks CLAUDE.md's design
decisions are based on. Every 'confirmed real in the data' claim in that
file should trace back to a check that runs here -- narration alone isn't
verification. Run: .venv/Scripts/python.exe scripts/audit_practice_data.py
"""
import csv
import os
from collections import Counter

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "dataset", "System extracts")


def _rows(filename):
    with open(os.path.join(DATA_DIR, filename), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def audit_uom_and_rate_conversion():
    """Basis for uom/registry.py + uom/converter.py: every Box(10) invoice
    must reconcile exactly against its PO once qty x10 / rate /10."""
    po_index = {r["po_number"]: r for r in _rows("purchase_orders.csv")}
    mismatches = []
    box_count = 0
    for r in _rows("vendor_invoices.csv"):
        if r["uom"] != "Box(10)":
            continue
        box_count += 1
        po = po_index.get(r["po_number"])
        if po is None:
            mismatches.append((r["invoice_number"], "no matching PO"))
            continue
        inv_qty, po_qty = float(r["qty"]), float(po["qty"])
        inv_rate, po_rate = float(r["rate"]), float(po["rate"])
        if inv_qty * 10 != po_qty:
            mismatches.append((r["invoice_number"], f"qty*10={inv_qty*10} != po_qty={po_qty}"))
        if abs(inv_rate / 10 - po_rate) > 1e-9:
            mismatches.append((r["invoice_number"], f"rate/10={inv_rate/10} != po_rate={po_rate}"))
    print(f"[uom] Box(10) invoices found: {box_count}")
    print(f"[uom] mismatches after x10 / div-by-10 conversion: {len(mismatches)}")
    for m in mismatches:
        print(f"    {m}")
    return box_count == 13 and not mismatches


def audit_gst_rate_distribution():
    """Basis for checks/gst.py treating 18% as a fixed business rule."""
    counts = Counter(r["gst_rate_pct"] for r in _rows("vendor_invoices.csv"))
    print(f"[gst] gst_rate_pct distribution: {dict(counts)}")
    return set(counts) == {"18"}


def audit_vendor_namespace_overlap():
    """Basis for checks/vendor.py staying a plain vendor_id equality check
    -- confirms the V-/FTV- split never produces an orphan against the
    vendor master."""
    vendor_ids = {r["vendor_id"] for r in _rows("vendors.csv")}
    orphans = {r["vendor_id"] for r in _rows("vendor_invoices.csv") if r["vendor_id"] not in vendor_ids}
    print(f"[vendor] invoice vendor_ids missing from vendors.csv: {len(orphans)}")
    return not orphans


def audit_po_match_recoverability():
    """Basis for matching/fuzzy.py staying deliberately conservative
    (whitespace/case only, no similarity matching)."""
    po_rows = _rows("purchase_orders.csv")
    po_exact = {r["po_number"] for r in po_rows}
    po_normalized = {r["po_number"].strip().upper() for r in po_rows}

    exact_miss = [r for r in _rows("vendor_invoices.csv") if r["po_number"] not in po_exact]
    recovered = [r for r in exact_miss if r["po_number"].strip().upper() in po_normalized]
    print(f"[matching] exact PO misses: {len(exact_miss)}, recovered by normalization: {len(recovered)}")
    return len(exact_miss) == 12 and len(recovered) == 0


def audit_duplicate_po_billing():
    """Basis for duplicates/detector.py -- confirms the real duplicate
    group count and size the earliest-stays-CLEAN rule is designed for."""
    counter = Counter(r["po_number"] for r in _rows("vendor_invoices.csv"))
    dupes = {k: v for k, v in counter.items() if v > 1}
    print(f"[duplicates] po_numbers billed by >1 invoice: {dupes}")
    return dupes == {
        "PO/2026/1451": 2,
        "PO/2026/1516": 2,
        "PO/2026/1404": 2,
        "PO/2026/1533": 2,
        "PO/2026/1538": 2,
    }


if __name__ == "__main__":
    checks = [
        ("UOM + rate conversion", audit_uom_and_rate_conversion),
        ("GST rate distribution", audit_gst_rate_distribution),
        ("Vendor namespace overlap", audit_vendor_namespace_overlap),
        ("PO match recoverability", audit_po_match_recoverability),
        ("Duplicate PO billing", audit_duplicate_po_billing),
    ]
    all_ok = True
    for name, fn in checks:
        ok = fn()
        print(f"  -> {'OK' if ok else 'CHANGED FROM DOCUMENTED BASELINE'}\n")
        all_ok = all_ok and ok

    if not all_ok:
        raise SystemExit("One or more practice-data assumptions no longer hold -- re-check CLAUDE.md's design rationale.")
    print("All practice-data assumptions confirmed.")
