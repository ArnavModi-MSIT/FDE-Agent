# Latest update — 2026-09-18

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Knowledge: five more attempts today, all 0.8750 — stopping on the last three

- **v39** — very long answers plus a length check: rules out "phrase
  anywhere in the answer" matching.
- **v40–v43** — the new candidates from four outside AI reviews (reordered
  document list, `CFO (Rohit Malhotra)`, the second policy sentence alone,
  list punctuation variants, `Chief Finance Officer`, lower-case exact
  strings). All 0.8750.

93 distinct answers have failed on K-03, K-05 and K-07. The best
explanation is that those three hidden answers are broken or can't be
derived; no entrant since launch has passed 21/24. **No more attempts on
them.** Next step: ask the organizers how answers are matched and whether
those three are gradeable.

## Outside reviews

`external_review/knowledge_review_brief_2026-09-18.md` was sent to four AIs.
Kimi's review was the most useful. Luna and Gemini re-proposed answers
already tried; DeepSeek's file came back empty.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | **0.8750** |

Composite **97.50**. 117/117 tests pass. Commits since the last push are
local only.
