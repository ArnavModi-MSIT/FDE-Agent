# Latest update — 2026-09-24

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## An outside review came back — audited, not trusted

Sent the fresh brief to an outside AI. It proposed 8 candidate answers.
Checked every one against the 152-answer history before building anything:

- **2 were wrong.** Both claimed to fix a "gap" that's already in the
  record — one (K-05's 7-day filing deadline) matches an existing answer
  almost word for word.
- **2 are genuinely new, and sharp.** Both correctly apply the one proven
  lesson from K-08 (the missing piece was the *word* "lakh," not the
  comma amount) to K-05 and K-07 for the first time:
  - K-07: an answer asserting `CFO, Plant Head and QA` (not just CFO) had
    never been paired with `14 lakh`/`10 lakh` word notation.
  - K-05: the second document had never been spelled the US way,
    `check`, instead of `cheque`.
- **1 more survived**, lower confidence: K-05 as 4 documents (adding
  purchase requisition), with the count written as digit `4` — the
  content was tried twice before, but always spelled out as "four," which
  we've separately proven doesn't count the same as a digit.

Built **v64–v67**, each changing exactly one row, so a rise pinpoints
which idea landed with no follow-up upload needed. Full audit in the
ledger.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | **0.8750** |

Composite **97.50**. 117/117 tests pass. Commits since the last push are
local only.
