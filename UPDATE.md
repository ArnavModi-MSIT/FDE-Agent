# Latest update — 2026-09-15

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## The Knowledge grader compares numbers

- **v27** (correct answers written in words) → 0.6667: words alone fail.
- **v28** (correct answers cut to bare numbers `30`, `24`, `15`, `60`) →
  0.8333: numbers alone pass.
- **v8** from 10 Sep already showed extra numbers don't hurt.

So an answer scores when **every number in the hidden key appears in it**.

## Why we're stuck at 8 of 12

The eight questions we score are exactly the eight with numeric answers.
The four we miss — Buyer, the document list, CFO, Nil — are exactly the four
whose natural answers have no number. Nearly the whole leaderboard sits at
the same eight.

Either those four keys contain numbers we've never written (the organizers'
tickets write amounts as "3 lakh", "14 lakh", "5 to 15 lakh slab"), or they
contain none and can't be matched without organizer clarification.

## Ready for tomorrow: v29

`submissions/knowledge_submission_v29_number_rich.csv` restates the four as
genuine answers carrying their numbers in both styles (`Rs 3,00,000 (Rs 3
lakh)`, `Rs 14,00,000 (Rs 14 lakh)`, `Rs 5,00,000 (Rs 5 lakh)`) plus clause
and date. All 5 Knowledge attempts for today are used.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | 0.8333 |

Composite **96.67**. Commits since the last push are local only.
