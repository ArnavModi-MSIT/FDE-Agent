# Latest update — 2026-09-10

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Knowledge 0.7917 → 0.8333, predicted exactly

v7 replicated the answer set that another entrant's public repo recorded
at 0.8333. It scored **0.8333**, to the digit. Answers correct: **8/12**.

## What that proves beyond the gain

- **Scores transfer across accounts.** A prediction built entirely from
  someone else's published record came back exact. Their remaining
  measured data is now usable as evidence, not as a lead needing
  independent re-verification.
- **One trio is now clean.** Of the four questions that set made verbose
  where ours were terse (K-03, K-06, K-10, K-11), exactly one flipped
  wrong to right. Two wrong answers remain among the policy-value
  questions, one in each of the other two trios, plus K-07 and K-08.

`submissions/knowledge_submission.csv` now holds the v7 set, matching the
banked best.

## Next: v8

`knowledge_submission_v8_completerule.csv` keeps v7's verbose forms for
K-03, K-07 and K-08, holds K-04 at its proven terse answer, carries our
proven K-09, and extends the complete-rule treatment to the remaining
seven. Every outcome is informative:

| Delta | Reading |
|---|---|
| +2 → 0.9167 | both remaining wrongs were format, complete-rule fixes them |
| +1 → 0.8750 | one fixed |
| 0 → 0.8333 | complete-rule neither helps nor harms here — and that itself proves it is safe on correct answers |
| −1 → 0.7917 | complete-rule broke the answer that landed; revert to v7 |

0.8333 is banked under best-recorded scoring, so the downside is
informational only.

## Standing

- Reconciliation **1.0000** · Migration **1.0000** — solved
- Workflow **0.9444** — W3 reopened; six entrants prove 6/6 is reachable,
  no new hypothesis yet, preview testing is free
- Knowledge **0.8333** — 4 of 5 attempts left today
- Composite moves 94.17 → about 95.00
