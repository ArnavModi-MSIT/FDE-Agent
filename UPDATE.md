# Latest update — 2026-09-07

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## What changed

Checked the real Migration score after the `FT-1442` fix: **1.0000 —
perfect.** M1 6/6, M2 12/12, M3 5/5. Migration family fully solved.

## Full picture across all four families now

| Family | Score | Weight |
|---|---|---|
| Reconciliation | 0.8700 | 30% |
| Knowledge | 0.7500 | 20% |
| Workflow | 0.8611 | 30% |
| **Migration** | **1.0000** | 20% |

Composite: `0.3×0.87 + 0.2×0.75 + 0.3×0.8611 + 0.2×1.00 ≈ 0.8693` —
86.93%, up from 86.38% before the M2 fix.

## Recorded in CLAUDE.md

Migration's experiment log now shows the full arc: 0.4667 (baseline,
before M2/M3 built) → 0.9722 (after M2/M3 first built, FT-1442
unresolved by design) → **1.0000** (after the real list_price_2019
fallback fix). 2 of 5 daily Migration attempts used, not needed further
unless something regresses.

## Still open

- Reconciliation (0.87): still no untested hypothesis, 2/5 attempts remain
- Knowledge (0.75): 1 attempt left, no new hypothesis
- W3 (5/6): genuinely unexplained, no further action without new evidence
- Repo: pushed as of commit `c804907`; today's later changes (M2 fix,
  the two reverted/tested Knowledge experiments) not yet re-pushed
