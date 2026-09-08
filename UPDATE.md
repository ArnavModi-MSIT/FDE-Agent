# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Ran the recommended zero-risk W3 investigation (Phase A + B) — both empty

A follow-up review recommended two specific, zero-risk checks before
touching any code: inspect every field on every live customer, and
search every ticket/email for explicit "which record survives a merge"
language. Ran both for real.

## Phase A: full field inspection

All 85 `/crm/customers` rows share exactly one key-set — `legacy_id,
crm_id, customer_name, tier, region, credit_terms_days,
migrated_to_salestrack, merged_into`. No hidden timestamp, status,
parent, or source-system field exists anywhere. This closes the "hidden
state" and "existing `merged_into` matters" hypotheses definitively —
there's structurally nothing else in the schema to use.

## Phase B: destination-language and name-transformation search

Searched all 18 tickets + 14 emails for explicit survivor language
("keep X", "is the master", "legacy record", "canonical", "do not
merge", etc.) and for other name-transformation hints (PVT/LTD/COMPANY/
punctuation, beyond the already-found `AND`↔`&`). **Zero matches
anywhere.** No organizer text says which record should survive, and no
second transformation rule exists.

## A real bonus find, unrelated to W3

**Email EM-111** ("Boxes vs numbers on spares") describes the exact same
UOM scenario as FIX-3418, independently: *"Totals match so finance
clears it, but stores count never ties out... fix the UOM."* A third
independent source confirming today's UOM revert was the right call
(already proven for real via the 1.0000 score) — not actionable, just
further corroboration.

## Recorded in CLAUDE.md

Full writeup appended to the W3 investigation section.

## Still open

- Reconciliation: **1.0000, solved.**
- Workflow: **0.9444** (W1 8/8, W2 8/8, W3 5/6) — three separate deep
  investigations now, zero surviving hypotheses; both zero-risk phases
  this review specified are exhausted. Per that review's own decision
  rule, pivoting to Knowledge.
- Knowledge (0.75): next up — check current attempt count before
  spending
- Migration: 1.0000, already solved
- Repo: local commits through this round; not yet pushed — push only on
  explicit request
