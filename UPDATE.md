# Latest update — 2026-09-19

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Knowledge: five more candidates built (v44–v48)

On request, five more files for today's attempts. Each changes only K-03,
K-05 and K-07, the three that have never scored, so none can lose a point.
All 15 strings are new against every past answer in git history, even
ignoring case, punctuation and small words:

| File | K-03 | K-05 | K-07 |
|---|---|---|---|
| v44 | `Buyer (EXW)` | `GST certificate, cancelled cheque, MSME declaration (where applicable)` | `CFO (Chief Financial Officer)` |
| v45 | `The buyer bears the freight.` | `GST registration, cancelled cheque, MSME declaration` | `Approval from the CFO` |
| v46 | `Freight is borne by the buyer.` | `GST certificate, cancelled cheque, MSME declaration (if applicable)` | `CFO only` |
| v47 | `Distributor (buyer)` | `GSTIN certificate, cancelled cheque, MSME declaration` | `CFO's approval` |
| v48 | `Buyer bears freight (ex-works)` | `GST cert, cancelled cheque, MSME declaration (where applicable)` | `GM Procurement` |

Odds are low: 93 answers have already failed, and the best explanation is
still that these three hidden answers can't be matched. A score of 0.9167
would mean one landed.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | **0.8750** |

Composite **97.50**. 117/117 tests pass. Commits since the last push are
local only.
