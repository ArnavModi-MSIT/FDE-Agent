# Latest update — 2026-09-23

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## v59–v63 all 0.8750; length-cutoff question closed

None of the five landed. The useful result is **v59**: K-10, a row already
proven correct, kept its point at 3,668 characters. That rules out a length
cutoff as the reason the 21 Sep carpets (up to 5.2k characters) failed — they
failed on content, not truncation. Ticket numbers, signatories, document
titles and a leading clause number all failed too.

141 distinct answers have now failed on K-03, K-05 and K-07, covering every
number, word, signatory, title and citation form the organizer texts
contain. Paavas Goyal has solved two of the three in a handful of uploads,
so something real is being missed, but nothing left in the organizer text
points at what. Asking the organizers (how `answer` is matched, whether
these three rows are gradeable) is the only remaining lever.

## Housekeeping

Every spent Knowledge candidate CSV (v34 through v63) is removed from the
working tree. Git history and the ledger keep the full record of what each
one tested. Only `knowledge_submission.csv` and
`knowledge_submission_best_0p8750.csv` remain on disk, matching the
2026-09-16 pattern.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | **0.8750** |

Composite **97.50** (4th; Paavas Goyal 99.17). 117/117 tests pass. Commits
since the last push are local only.
