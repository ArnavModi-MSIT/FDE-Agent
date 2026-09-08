# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Two real, zero-risk Knowledge hardening fixes; two proposals declined

A fourth review (delivered via a git worktree) proposed hardening the
Knowledge parser against rotated-question formats and strengthening
submission-invariant checks. Tested every claim directly instead of
building speculatively.

## Fixed: currency-marker recognition

The amount regex only recognized `Rs`/`Rs.`. Tested `INR 720000` and
`₹7,20,000` directly — both failed to extract an amount. Widened to
recognize `Rs`/`Rs.`/`INR`/`₹` — all unambiguous rupee markers, zero
guessing risk. Confirmed `Rs.` (with period) and `"1 March 2024"`-style
dates already worked, no fix needed there. 4 new tests.

## Fixed: submission-invariant checks

`sanity_check()` only caught `UNPARSEABLE`/blank source. Extended to
also check exact qid-set match against the input, duplicate input qids,
and blank (non-UNPARSEABLE) answers — the same class of check
Reconciliation's `test_submission_invariants.py` already does. 7 new
tests.

## Declined: wording synonyms and numeric dates

Both real gaps when tested directly (`"payment terms"` → `topic=None`,
`"01/03/2024"` → no date extracted) — but neither has organizer evidence
behind it. Wording synonyms would mean guessing which specific phrases
might appear, and R-04's "same public extract" language argues against
wholesale wording rotation. Numeric dates carry a genuine DD/MM vs MM/DD
ambiguity with nothing resolving it. Not implemented, matching this
project's "never guess" discipline.

## Verified

101 → 108 tests pass. Both real fixes confirmed byte-identical on the
real 12-question submission (neither condition occurs there) — no
submission spent, since there's nothing for a resubmission to confirm.

## Recorded in CLAUDE.md

Full writeup appended to the Knowledge section.

## Still open

- Reconciliation: **1.0000, solved.**
- Workflow: **0.9444** — W3 (5/6) unexplained after three investigations
- Knowledge: **0.7500** — content, citation format, parser/handler
  execution, and now format-robustness/invariants all audited and
  hardened where evidence supported it. No surviving hypothesis for the
  score gap itself. Holding.
- Migration: 1.0000, already solved
- Repo: local commits through this round; not yet pushed — push only on
  explicit request. Note: a separate git worktree exists at
  `.worktrees/knowledge-score-improvement-strategies` (branch
  `agents/knowledge-score-improvement-strategies`) — not touched, all
  work this round happened in the main worktree.
