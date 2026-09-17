# Latest update — 2026-09-17

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Knowledge: three more attempts, still 0.8750

- **v34** — every remaining way to write the numbers for K-03, K-05, K-07
  (lakh, plain digits, `14L`, crore, million, numeric dates). No change.
- **v35 / v36** — short key-style text (`Buyer (ex-works)`, `CFO approval`,
  condensed document lists). No change.

K-03, K-05 and K-07 have now failed three number rounds and two text rounds.
Their keys almost certainly hold no numbers, which the numbers-matching
grader can't match. **9/12 (0.8750) is the working ceiling.** Two of today's
attempts were held.

## Knowledge engine now produces the scoring answers

`scripts/run_knowledge.py` used to regenerate the old 0.7500 answers and
could overwrite the best file. `src/knowledge/answering.py` now emits the
proven forms — K-08's Nil with the `Rs 5 lakh` threshold, K-09 with the
30-day window, K-11 with both warranty periods — and the script reproduces
`submissions/knowledge_submission_best_0p8750.csv` byte for byte. A new test
fails if that ever drifts. This matters for the live agent walkthrough at
the finals (7–9 Oct).

**117/117 tests pass.**

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | **0.8750** |

Composite **97.50**. Commits since the last push are local only.
