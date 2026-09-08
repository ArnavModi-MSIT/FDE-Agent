# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Fresh W3 investigation — one real finding, hardened, no lever for today

Went back into W3 (5/6, Workflow's only remaining gap) applying the
day's big lesson: does an "Open" ticket here actually want the literal
defect flagged rather than resolved, the way FIX-3402 and FIX-3418 both
did? **Doesn't apply** — W3's own task brief is unambiguous that merging
IS the job; the open question is only which rows are duplicates.

## What was found

Re-reading every ticket/email for a W3 angle turned up **email EM-106**
(never previously connected to W3): *"several distributors exist as
legacy C- codes and again in SalesTrack, names in caps or with AND
changed to ampersand."* Our `normalize_name()` never handled `AND` ↔
`&`. Checked directly against the live sandbox before touching anything:
**0 of the current 85 `/crm/customers` rows contain a standalone "AND"**
— so this isn't today's missing check. Hardened anyway since it's real,
specific evidence, not a guess.

## Verified neutral, not assumed

Real dry run against the live sandbox: merge plan is byte-identical (45
merges, same pairs) before and after the change. 1 new test, 8/8 W3
tests pass, 96/96 overall. No Workflow attempt spent.

## Also re-verified everything else fresh

All 45 live merges re-checked correct, 0 ambiguous groups, every
duplicate-name suffix is region-coded (no semantically-distinct branch
suffix suggesting a real non-duplicate entity), the live `FIX-3415`
ticket carries nothing beyond the local CSV. Still no concrete
hypothesis for the missing 6th check.

## Recorded in CLAUDE.md

Full writeup appended directly after the existing W3 investigation
section.

## Still open

- Reconciliation: **1.0000, solved.**
- Workflow: **0.9444** (W1 8/8, W2 8/8, W3 5/6) — W3 remains genuinely
  unexplained after two separate deep investigations
- Knowledge (0.75): attempt count from before today's reset — check
  current count before spending; likely the better place to spend
  remaining effort today given W3 has no surviving lead
- Migration: 1.0000, already solved
- Repo: local commits through this round; not yet pushed — push only on
  explicit request
