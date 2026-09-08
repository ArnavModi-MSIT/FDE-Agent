# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Applied the UOM methodology to Knowledge — no error found, one hypothesis ruled out

Fetched the actual policy PDF text live from `GET /vault/documents` and
diffed all 12 Knowledge answers against it word for word, instead of
trusting our own earlier transcription.

## Content: verified clean

- K-09's `"10% of invoice value"` is a direct quote from WRP-2020.
- K-05's document list matches VOS-7's procedure table exactly.
- K-06's `"Rs 2,00,000"` matches the trial-PO line exactly.
- All PP-2023 figures (discount bands, credit terms, freight, notice
  days) match sections 2–5 exactly; neither tested order value sits near
  a band boundary.

No content error survived this pass.

## governing_source: settled by the actual rules text, not a guess

Fetched the live rules page directly. **R-08's exact wording**: *"0.5
for citing the governing source document. Where the 2019 and 2023
policies conflict, the governing source is the one that actually
applies on the transaction date."* The organizers' own example is
choosing between **two whole documents**, not a section/addendum within
one. That's real evidence document-level citation (already what's
implemented) is correct — and it **specifically rules out** the one
candidate hypothesis under consideration (K-04 as `"WRP-2020 Addendum
A"` instead of `"WRP-2020"`). Good that this wasn't submitted as a
guess — the rules text argues against it.

## Recorded in CLAUDE.md

Full writeup added to the Knowledge section, right after the existing
experiment log.

## Still open

- Reconciliation: **1.0000, solved.**
- Workflow: **0.9444** — W3 (5/6) unexplained after three investigations
- Knowledge: **0.7500** — content and source-citation format both
  re-verified against literal organizer text with no error found; no
  surviving hypothesis. Holding the remaining attempt(s) rather than
  guessing.
- Migration: 1.0000, already solved
- Repo: local commits through this round; not yet pushed — push only on
  explicit request
