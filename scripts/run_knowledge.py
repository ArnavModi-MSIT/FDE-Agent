#!/usr/bin/env python3
"""Runs the Knowledge Q&A pipeline against the local practice questions
and writes submissions/knowledge_submission.csv."""
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(REPO_ROOT, "src")
for path in (REPO_ROOT, SRC_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

from knowledge.pipeline import run  # noqa: E402

DATA_DIR = os.path.join(REPO_ROOT, "dataset", "System extracts")
OUTPUT_PATH = os.path.join(REPO_ROOT, "submissions", "knowledge_submission.csv")

if __name__ == "__main__":
    result = run(DATA_DIR, OUTPUT_PATH)
    print(f"Answered {result['total']} questions -> {result['output_path']}\n")
    for qid, row in result["answers"].items():
        print(f"{qid}: {row['answer']}  [{row['governing_source']}]")
        print(f"    reasoning: {row['reasoning']}")
