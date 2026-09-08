# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Knowledge fully localized for today: K-07, K-08, K-09 are all wrong

Attempt 5 (corrupt K-07/K-08/K-09 only) scored **0.7500 — exactly the
original baseline.** Re-derived every experiment's implied counts with
exact fractions to be sure of this load-bearing result:
**`correct_in_{K-07,K-08,K-09} = 0` — all three answers are wrong**, and
`correct_in_{K-10,K-11,K-12} = 2` — exactly 1 wrong there.

## The full picture, 5/5 attempts used today

- Sources: 12/12 correct (settled with certainty)
- Answers: 6/12 wrong, fully localized:
  - **K-07, K-08, K-09: all three wrong, no ambiguity left**
  - 1 wrong somewhere in {K-01, K-02, K-03}
  - 1 wrong somewhere in {K-04, K-05, K-06}
  - 1 wrong somewhere in {K-10, K-11, K-12}

## A real hypothesis for tomorrow

K-08 ("Nil") and K-09 ("10% of invoice value") both passed every content
audit — K-09 is a literal PDF quote — yet both are wrong. The pattern:
K-01 answers as a bare `"10%"`, but K-08 and K-09 don't follow that
convention (`"Nil"` instead of `"0%"`; `"10% of invoice value"` instead
of bare `"10%"`). If the grader wants uniform bare-percentage answers,
that would explain both at once. Doesn't explain K-07 (`"CFO"`, not a
percentage) — that one still needs its own explanation. This is genuinely
untested ground, not a repeat of the earlier verbosity experiment (which
never touched K-08/K-09's specific format).

## Recorded in CLAUDE.md

Full derivation and the hypothesis appended to the diagnostic
-experiments section.

## Still open

- Reconciliation: **1.0000, solved.**
- Workflow: **0.9444** — W3 (5/6) unexplained after three investigations
- Knowledge: **0.7500**, fully localized for today (see above). 0/5
  attempts remain — resumes tomorrow with a concrete format hypothesis
  for K-08/K-09, plus 3 still-unresolved single-item ambiguities
  (K-01-03, K-04-06, K-10-12) and K-07 fully unexplained.
- Migration: 1.0000, already solved
- Repo: local commits through this round; not yet pushed — push only on
  explicit request
