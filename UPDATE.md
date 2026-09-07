# Latest update — 2026-09-07

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## What changed

Built the entire Knowledge family from scratch: a real policy-reasoning
engine (not a hardcoded lookup of the 12 practice answers), full test
suite, and a generated submission ready to upload.

## Why a reasoning engine, not a lookup table

The rules page says scored sets "rotate weekly." Combined with the R-05
submission spec ("one row per qid in `knowledge_questions.csv`" — your
own downloaded file), the most likely shape is: same question
*templates*, different numbers/dates/tiers each week. A hardcoded
qid->answer table would break on refresh; a real parser + policy engine
survives it.

## Architecture (mirrors reconciliation's proven shape)

`parsing.py` (question text -> topic + extracted amount/date/tier, regex
-based) -> `answering.py` (topic-routed handler) -> `policy_kb.py`
(every rule transcribed from the real PDFs, cited inline) + `temporal.py`
(date -> PP-2019/PP-2023 resolution) -> `submission.py`
(`qid,answer,governing_source`). Zero LLM calls, fully deterministic.

## Two real bugs found and fixed

**1. Tier extraction bug, caught by reading the reasoning trace, not a
failing test.** K-02 asks about a "standard credit terms for a **Gold**
-tier distributor" — the tier regex grabbed "standard" (an adjective
appearing earlier in the sentence) instead of "Gold" (the real tier,
appearing later). The final answer was accidentally still correct
(neither maps to Platinum, so both give 30 days) — exactly the kind of
bug that hides silently. Fixed by requiring a `-tier` suffix as the real
tier designation before falling back to a bare word match.

**2. Test collision bug**: gave `tests/knowledge/` an `__init__.py`
(unlike `tests/reconciliation/`, which deliberately has none) — this made
pytest treat `tests/knowledge` itself as the `knowledge` package,
shadowing `src/knowledge` entirely. Every test failed importing
`policy_kb`. Fixed by removing the `__init__.py`.

## Verified

- **54/54 tests pass** (25 new for knowledge: policy_kb boundary cases
  including the exact 2023-10-01 cutover, topic classification against
  all 12 real questions, the tier-extraction regression, pipeline
  determinism, submission structural invariants)
- **All 12 real practice questions answered and manually cross-checked**
  by independent domain reasoning: K-01 10%, K-02 30 days, K-03 buyer
  bears freight, K-04 24 months + Addendum A caveat, K-05 the 3 VOS-7
  documents, K-06 ₹2,00,000, K-07 CFO, K-08 Nil, K-09 10% restocking,
  K-10 15 days, K-11 June 2026, K-12 60 days — every one matches
  independent hand-reasoning, not just "the code produced something"

## Two open, unverified assumptions (same shape as reconciliation's)

- `governing_source`'s exact expected string format (used each
  document's own "Document code," e.g. `PP-2023`, `VOS-7`) — not
  confirmed against any spec text, since none states the expected
  granularity
- `answer` text's exact expected precision/format — chose natural,
  information-dense short strings; scoring method (exact/substring/
  semantic) is unknown

## Ready to submit

`submissions/knowledge_submission.csv` is generated and ready. This is
the first Knowledge attempt — unlike Reconciliation, we have zero prior
signal here, so whatever score comes back is entirely new information.

## Still open (unrelated to Knowledge)

- Reconciliation: 2 of 5 daily attempts remain, no new hypothesis to
  spend them on (see previous investigation — all local levers exhausted)
- Workflow/Migration: still blocked on the sandbox API key
