#!/usr/bin/env python3
"""Build up to five CSV candidates locally. Does not upload or spend attempts."""
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from knowledge.experiments import prepare_candidates  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True, help="New directory; existing paths are refused")
    parser.add_argument("--baseline", type=Path, default=REPO_ROOT / "submissions/knowledge_submission_best_0p9167.csv")
    parser.add_argument("--preserve", action="append", default=[], choices=["K-03", "K-07"],
                        help="Keep a newly confirmed scoring answer from the supplied baseline")
    args = parser.parse_args()
    try:
        manifest = prepare_candidates(
            args.baseline, REPO_ROOT / "submissions/knowledge_submission_best_0p9167.csv",
            args.plan, args.output_dir, tuple(args.preserve),
        )
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f"Cannot prepare candidates: {error}\n")
    for candidate in manifest["candidates"]:
        print(f"{args.output_dir / candidate['file']}: changes {', '.join(candidate['changes'])}; unscored")
    print("All sources and the ten confirmed scoring answers were preserved. No uploads made.")


if __name__ == "__main__":
    main()
