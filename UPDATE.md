# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Four more mechanical checks on Knowledge — all clean, still no lever

Followed up on the earlier content/governing_source audit with the
remaining concrete angles suggested: whether the question set could be
stale/rotated, whether the submission CSV itself has a subtle format
issue, and whether any Knowledge-specific guidance exists on the site
beyond what's already known.

## What was checked

- **Live Starter Kit / Data / Overview pages**, fetched directly: no
  Knowledge-specific starter code or format guidance exists anywhere —
  the copy-ready brief is Reconciliation-only.
- **Question-set rotation**: the "rotate weekly" language pairs with
  "thousands of rows" in the FAQ, reading as Reconciliation-scale, not
  Knowledge's 12 questions. R-04 says every participant works from "the
  same public extract" — not per-account personalized. No evidence our
  local file is stale.
- **Raw submission CSV bytes**: no BOM, correct CRLF, exactly 12 rows in
  order, correct header, proper quoting on the two comma-containing
  answers. Nothing structurally wrong.
- **Pipeline genericity**: reads `qid`/`question` dynamically from
  whatever the input file contains — no hardcoded question list, so a
  rotated set would already be handled correctly.

## Result

Every checkable angle from both today's reviews is now closed with a
real answer, not a guess. No surviving hypothesis for Knowledge's gap.

## Recorded in CLAUDE.md

Appended directly after the content/governing_source audit writeup.

## Still open

- Reconciliation: **1.0000, solved.**
- Workflow: **0.9444** — W3 (5/6) unexplained after three investigations
- Knowledge: **0.7500** — exhaustively audited (content, governing_source
  format, question-set staleness, CSV bytes, pipeline genericity), no
  error found anywhere. Holding the remaining attempt(s).
- Migration: 1.0000, already solved
- Repo: local commits through this round; not yet pushed — push only on
  explicit request
