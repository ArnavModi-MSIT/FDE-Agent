# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## The big one: reverted UOM canonicalization, using the last daily attempt

A third external review made the case that the starter kit's own
literal code treats `Box(10)` vs `Nos` as `UOM_MISMATCH` (not `CLEAN`),
that `UOM_MISMATCH` never fires locally under our canonicalization logic
(a macro-F1 class scoring near-zero costs up to `1/8 = 0.125` — almost
exactly the observed 0.13 gap), and that 6+ leaderboard participants hit
a perfect score without inventing packaging-aware conversion. This
question has been open since the project's very first leaderboard
result but was never directly tested.

## What actually tipped it: today's own vendor-GSTIN result

This project's justification for canonicalization rested on ticket
FIX-3418 ("value tallies, count does not"). Re-reading it: it's an
**"Open"** ticket whose first sentence is *"Stores GRN shows quantity
mismatch."* Same ticket-status pattern as FIX-3402 — which the
vendor-GSTIN experiment (earlier today, real regression, 0.8700→0.8579)
just proved means "flag the defect," not "resolve it away." That's a
real, symmetric counter-example from this project's own evidence, not
just an external opinion.

## What changed

`src/reconciliation/checks/uom.py` reverted to the starter's literal raw
string comparison. When uom strings match, `quantity`/`rate` now compare
RAW values (no conversion) — matching the starter's actual behavior.
`uom/registry.py`/`uom/converter.py` kept, unused, in case this
hypothesis is wrong. 2 tests updated, 1 new test added. **95/95 tests
pass.**

## Verified as strongly as this project verifies anything

Local output: `CLEAN 155, QTY_MISMATCH 21, RATE_MISMATCH 16, GST_ERROR
16, UOM_MISMATCH 13, MISSING_PO 12, VENDOR_MISMATCH 12, DUPLICATE_INVOICE
5` — **byte-for-byte identical to `starter_reconciliation.py`'s own
output on all 250 rows, 0 differing predictions.** Stronger confirmation
than any prior Reconciliation change.

## Not yet submitted

`submissions/submission.csv` is regenerated and ready. This is the last
of today's 5 daily Reconciliation attempts — recommending it actually be
spent this time, unlike prior "hold" recommendations, because this is
the first hypothesis with genuine structural support (matches the
macro-F1 math, matches the one organizer reference implementation
byte-for-byte, and has a real internal counter-example backing the
reasoning).

## Recorded in CLAUDE.md

Full writeup in §4 (UOM section, marked REVERTED with both the original
and new reasoning) and a new dated subsection after §5's experiment log,
plus experiment-log row #6 (pending).

## Still open

- Reconciliation: **last daily attempt queued** for this UOM revert —
  once scored, revert-if-regressed or keep-if-improved per the standard
  decision rule
- Knowledge (0.75): attempt count from before today's reset — check
  current count before spending
- W3 (5/6), W2 (0.75 of weight): no new investigation this round
- Repo: local commits through this round; not yet pushed — push only on
  explicit request
