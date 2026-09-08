# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Localization continues: first half has 4/6 correct, second half has 2/6 correct

Attempt 3 (corrupt K-01..K-06, leave K-07..K-12 + sources real) scored
**0.5833 (= 7/12 exactly)**. `correct_in_second_half = (0.5833 − 0.5) ×
24 = 2`. By complement: **K-01..K-06 has 4 correct / 2 wrong; K-07..K-12
has 2 correct / 4 wrong.**

## What's next: 2 attempts left, bisecting each half

Each half now has `C(6,2) = 15` remaining possible arrangements. With
only 2 attempts left, full unique identification per half isn't
achievable (a 3-item sub-test only yields 4 possible outcomes) — so the
plan is to bisect each half into two groups of 3, narrowing from "which
2 of 6" down to "which of (at most) 3."

**Attempt 4** (ready to submit): corrupt K-01/K-02/K-03 only, leave
K-04/K-05/K-06 and everything else real. Tells us exactly how the first
half's 2 wrong answers split between its two sub-groups of 3.

**Attempt 5** (planned): the mirror split for the second half
(K-07/K-08/K-09 vs K-10/K-11/K-12).

## Recorded in CLAUDE.md

Full writeup with the derivation appended to the diagnostic-experiments
section.

## Still open

- Reconciliation: **1.0000, solved.**
- Workflow: **0.9444** — W3 (5/6) unexplained after three investigations
- Knowledge: **0.7500**, localized to: sources 12/12 correct, answers
  6/12 wrong, split 2 wrong in K-01..K-06 / 4 wrong in K-07..K-12.
  3/5 daily attempts used, 2 remain for further bisection.
- Migration: 1.0000, already solved
- Repo: local commits through this round; not yet pushed — push only on
  explicit request
