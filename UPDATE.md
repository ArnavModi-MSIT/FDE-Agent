# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## A real, concrete parsing finding — the same shape as the K-02 bug, fixed

A follow-up review asked a genuinely different question: not "is the
policy content wrong" but "does the code correctly parse every
question's parameters before applying the policy." Ran the full audit
directly — `parse_question()`/`answer_question()` against all 12 real
questions, printing topic/amount/dates/tier alongside the final answer.

## What was found

**K-11** ("A DRI pump is despatched in January 2025 and commissioned in
June 2025") has two dates. The parser assigned despatch/commissioning
purely by **mention order** (first date = despatch), never by checking
which keyword each date actually sits next to. On this specific
question the orderings coincide, so the answer was already correct —
but that's coincidence, exactly the same shape as the earlier K-02
tier-extraction bug (a correct answer that didn't prove correct
reasoning). A rotated question phrased with commissioning first would
have silently swapped the dates.

## Fixed

`parsing.py` now assigns each date to whichever role-keyword
(`despatch`/`dispatch` vs `commission`) it's closest to in the text,
falling back to positional order only when ambiguous. Proven with a
real reversed-order test and an end-to-end proof both phrasings produce
the same final answer. **98/98 tests pass (2 new).**

## Verified neutral on the real question set

Re-ran the pipeline — `knowledge_submission.csv` is byte-identical to
before the fix (K-11 still "June 2026"). **Not submitted** — a
byte-identical resubmission teaches nothing new, matching this
project's own established discipline. Kept as permanent, evidenced
hardening against a real hidden-set risk class, invisible to today's
score but correct regardless.

## Recorded in CLAUDE.md

Full writeup appended to the Knowledge section, following the review's
own requested format (question / parser assignment / risk).

## Still open

- Reconciliation: **1.0000, solved.**
- Workflow: **0.9444** — W3 (5/6) unexplained after three investigations
- Knowledge: **0.7500** — content, governing_source format, mechanics,
  and now full parser/handler execution all audited against real
  evidence, one real defensive fix made (locally neutral). No
  surviving hypothesis for the score gap itself. Holding.
- Migration: 1.0000, already solved
- Repo: local commits through this round; not yet pushed — push only on
  explicit request
