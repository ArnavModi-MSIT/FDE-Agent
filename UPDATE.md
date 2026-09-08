# Latest update — 2026-09-07

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Real confirmation: the corrected submission scored 0.8700, unchanged

The reverted/corrected `submission.csv` (both deviations below removed)
was submitted for real — result matches the local byte-identical
prediction exactly: **0.8700**, no movement. **5/5 Reconciliation
attempts are now used for today (2026-09-07, IST)** — none remain until
the daily quota resets. The codebase is left in its most
organizer-aligned state so far: matches `starter_reconciliation.py`'s
literal logic on every dimension except the one evidenced `UOM_MISMATCH`
canonicalization deviation.

## What changed

Followed the explicit instruction to build a status-definition matrix
(7 columns: organizer definition / example-ticket / required conditions
/ excluding conditions / coexistence / our implementation / unverified)
for all 8 Reconciliation classes, sourced from every organizer artifact —
the copy-ready brief, all 18 tickets, all 14 emails, and, decisively,
`starter_reconciliation.py`'s actual code (not just its comments) as
real specification. Written up in full in
`submissions/reconciliation_status_matrix.md`.

## The result: no new hidden-set hypothesis, but two real corrections

The matrix surfaced two places our implementation deviates from the
starter's literal reference code with **zero organizer evidence
supporting the deviation** — both already tested via real past
submissions and confirmed byte-identical/score-unchanged either
direction:

1. **Precedence order**: `GST_ERROR` had been promoted above
   `QTY_MISMATCH`/`RATE_MISMATCH`. Reverted to the starter's literal
   `if/elif` order (quantity and rate checked before GST).
2. **Duplicate-detection key**: grouped by `(po_number, sku)` instead of
   the starter's literal `po_number` alone. Reverted — and confirmed
   structurally moot on any data we can see: `po_number` is globally
   unique in both the practice set and the live sandbox (260/260 both
   places), so there's no multi-line PO anywhere for the extra key to
   protect against.

Every other class (`MISSING_PO`, `VENDOR_MISMATCH`, `QTY_MISMATCH`,
`RATE_MISMATCH`, `CLEAN`) already matched the starter exactly.
`UOM_MISMATCH` — the one deliberate, kept deviation — stays as-is: it's
backed by two independent organizer sources (the brief's own `Box(10)`
example and ticket FIX-3418), unlike the two reverted changes.

## Verified, not assumed

- `src/reconciliation/duplicates/detector.py` and
  `src/reconciliation/classify/precedence.py` both reverted, with
  updated in-code comments explaining why.
- `tests/reconciliation/test_classifier.py` and
  `tests/reconciliation/test_duplicates.py` updated to assert the
  *reverted* (starter-matching) behavior instead of the deviation.
- **94/94 tests pass.**
- `scripts/run_reconciliation.py` re-run: output byte-identical —
  168 CLEAN / 21 QTY_MISMATCH / 16 GST_ERROR / 16 RATE_MISMATCH /
  12 MISSING_PO / 12 VENDOR_MISMATCH / 5 DUPLICATE_INVOICE /
  0 UOM_MISMATCH — exactly as predicted (both reversions are the
  symmetric opposite of already-tested, already-neutral changes).

## Recorded in CLAUDE.md

Full matrix findings, reasoning, and both corrections documented in
place (Reconciliation section — duplicate pass, precedence, and a new
"Status-definition matrix audit" writeup with an updated experiment log).

## Still open

- Reconciliation: holding at 0.87, **0/5 attempts remain today** — quota
  resets tomorrow (IST); no further Reconciliation experimentation
  possible today regardless of any new hypothesis
- Knowledge (0.75): 1 attempt left, no new hypothesis
- W3 (5/6): genuinely unexplained, no further action without new evidence
- Repo: local commit `90c8ee9` has the matrix + both reversions on top of
  `e8e029c` (last pushed); not yet re-pushed — push only on explicit
  request
