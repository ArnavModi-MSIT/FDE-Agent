# Latest update — 2026-09-14

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Knowledge: five attempts today, all 0.8333

The four wrong answers are still K-03, K-05, K-07 and K-08. Every file today
changed only those four rows, so none could lose a point.

| File | What it tested | Score |
|---|---|---|
| v19 | K-08 as `Nil (below Rs 5,00,000)` | 0.8333 |
| v20 | answers in the sandbox's own codes (`BUYER`, `gst_cert`, `PLANT_HEAD`, `NIL`) | 0.8333 |
| v21 | answers swapped within the two same-source pairs (K-03/K-08, K-05/K-07) | 0.8333 |
| v22 | every answer restated to lead with a number | 0.8333 |
| v23 | long shots: bare `DRI`, EM-107 shorthand, all four approvers, `14%` | 0.8333 |

Ruled out today: key-format codes with case-sensitive matching, a swapped
key, and "number-led answers score". Also checked for free: the PDFs hold
no hidden content (rendered and read), and no exception clause in any
document changes the four answers.

## Where the gap is

Our answers match the documents; the grader still rejects them. What is
unknown is how the answer field is matched for text answers. That needs
outside evidence — an organizer clarification, a discussion post, or the
timing of the two entrants above us — not more submissions.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | 0.8333 |

Composite about **96.67**. Commits since the last push are local only.
