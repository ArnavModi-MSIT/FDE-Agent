#!/usr/bin/env python3
"""Runs the reconciliation pipeline against the local practice dataset and
writes submissions/submission.csv. Adds the repo root and src/ to sys.path
so the package imports resolve without installing anything."""
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(REPO_ROOT, "src")
for path in (REPO_ROOT, SRC_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

from reconciliation.pipeline import run  # noqa: E402

DATA_DIR = os.path.join(REPO_ROOT, "dataset", "System extracts")
OUTPUT_PATH = os.path.join(REPO_ROOT, "submissions", "submission.csv")

if __name__ == "__main__":
    result = run(DATA_DIR, OUTPUT_PATH)
    print(f"Classified {result['total']} invoices -> {result['output_path']}")
    for status, count in sorted(result["counts"].items(), key=lambda kv: -kv[1]):
        print(f"  {status:<20} {count}")
