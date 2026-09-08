# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Reconciliation is solved: 1.0000

The UOM revert scored **1.0000 — a perfect score**, confirmed for real
on the leaderboard. Reconciliation now matches Migration as a fully
solved family. This closes the entire ~0.13 gap that had persisted since
the very first submission on 2026-09-07.

## What it turned out to be

`checks/uom.py`'s packaging-aware canonicalization (`Box(10)` → treated
as `Nos × 10`, reconciling as `CLEAN`) was wrong. The organizer's own
literal starter code — raw string comparison, `Box(10) != Nos` →
`UOM_MISMATCH` — was the correct rule all along. This project's original
justification rested on ticket FIX-3418 ("value tallies, count does
not"), which is itself an "Open" ticket opening with "Stores GRN shows
quantity mismatch" — the same status pattern as FIX-3402, which the
vendor-GSTIN experiment (same day, real regression) had just proven
means "flag the defect," not "resolve it away." That internal
counter-example is what actually tipped the decision to test this,
alongside the external review's structural argument (a near-zero-F1
class costs up to 1/8 = 0.125 of macro-F1 — almost exactly the observed
gap) and the fact that 6+ leaderboard participants hit 1.000 without
apparent packaging-aware logic.

## The generalizable lesson

"Look past the surface label to the real transaction" isn't a
free-standing principle in this dataset — it was wrong for UOM and wrong
for vendor codes, both times because it was applied by analogy from
somewhere it wasn't actually evidenced, rather than checked against real
outcomes. Every check's exact tolerance needs its own evidence.

## Verified

Local output before submitting was byte-for-byte identical to
`starter_reconciliation.py`'s own output on all 250 practice rows — the
strongest local confirmation this project has ever had for a change,
and it held on the hidden set too.

## Recorded in CLAUDE.md

Full writeup in §4 (UOM section) and the dated experiment subsection
after §5's log, including the generalizable lesson, plus the log's
row #6 updated with the real 1.0000 result.

## Still open

- Reconciliation: **1.0000, solved.** 3/5 daily attempts used today, no
  further work needed barring a future regression.
- Knowledge (0.75): attempt count from before today's reset — check
  current count before spending
- W3 (5/6), W2 (0.75 of weight): no new investigation this round
- Migration: 1.0000, already solved
- Repo: local commits through this round; not yet pushed — push only on
  explicit request
