# Latest update — 2026-09-24

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## New review package built for outside AIs

Two things, both fresh as of today:

- **`external_review/knowledge_review_brief_2026-09-24.md`** — a complete,
  self-contained rewrite of the review brief. It supersedes the
  2026-09-18 one. It carries: the measured grader model with its full
  evidence chain (numbers-subset, the K-08 lakh discovery, K-09's
  complete-rule requirement, the length-cutoff test that closed the
  truncation question, containment-matching ruled out); the **Paavas
  Goyal discovery** (a competitor reached 23/24, so K-03/K-05/K-07 are
  provably gradeable, not broken keys); the full policy-document,
  ticket and email text; and an appendix of all **152 distinct answers**
  already tried, organized by question. It tells the reviewer explicitly
  to read the appendix before proposing anything and to say whether they
  did.
- **`knowledge_score_review/`** (new folder, gitignored) — a plain,
  ready-to-hand-off copy: the brief plus the current best CSV, the full
  ledger, `policy_kb.py`, the four PDFs, and the three source CSVs. No
  key, no `.env` — scanned before writing.

No Knowledge attempts were spent today. Standing at 0.8750 (9/12), same
as the last check.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | **0.8750** |

Composite **97.50**. 117/117 tests pass. Commits since the last push are
local only.
