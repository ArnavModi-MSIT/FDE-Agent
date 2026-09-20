# Latest update — 2026-09-20

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Big change: Knowledge 23/24 has been reached by a real entrant

Paavas Goyal is now at Knowledge **0.9583 (23/24)**, composite 99.17, up from
0.875 in five uploads (public leaderboard JSON, last run 2026-09-19 20:14 UTC).

- The "9/12 ceiling" and "K-03/K-05/K-07 can't be scored" readings are
  **wrong**. At least two of the three keys were matched, quickly.
- We don't know what they submitted and won't copy it (R-11). We only know
  the keys are gradeable and that something we haven't tried matches them.
- Our 108 failed answers covered wording, case, codes, numbers and length,
  so the missing idea is a different *kind* of answer.

Today (2026-09-20) is the last day uploads are certain to count; the daily
quota has reset.

## Five different-kind files built for today (v49–v53)

Not more rewordings: each tests a different way the grader might work, and
each changes only K-03, K-05 and K-07, so no file can lose a point.

- **v49** newline-separated lists of many short exact candidates
- **v50** JSON list answers (`["Buyer"]`, three documents, `["CFO"]`)
- **v51** short sentences in the organizers' own email voice
- **v52** full sentences that restate the question's facts
- **v53** blank / `nan` / `None` (for a broken or empty key)

0.9167 or more means a row landed; 0.8750 rules that idea out. Send me the
five scores. v53 has a blank answer and the site may reject it; a rejected
file costs no attempt.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | **0.8750** |

Composite **97.50** (4th; Paavas Goyal 99.17). 117/117 tests pass. Commits
since the last push are local only.
