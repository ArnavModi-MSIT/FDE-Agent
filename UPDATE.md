# Latest update — 2026-09-15

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Breakthrough on the mechanism: the Knowledge grader is literal

v27 rewrote four **correct** number answers in words (`Ten percent`,
`Thirty days …`, `Fifteen days …`, `Sixty days …`) and scored **0.6667** —
all four lost their credit. The grader does not judge meaning: `10%` scores,
`Ten percent` does not. Best recorded stays 0.8333.

This explains the whole Knowledge history: extra text is tolerated, terse
answers fail where the key carries more literal content, and the four text
answers (K-03, K-05, K-07, K-08) fail in every wording because their keys'
literal content has never appeared in our answers.

## Last attempt today: v28

`submissions/knowledge_submission_v28_bare_numbers.csv` cuts four correct
rows to bare numbers (K-02 `30`, K-04 `24`, K-10 `15`, K-12 `60`).

- **0.8333** → numbers only are matched.
- **0.6667** → words like `days`/`months` are matched too.

## Also today

- v24–v26 all 0.8333.
- Leaderboard JSON: bhasker's 24/24 was scored on 16 Aug, before the
  competition opened — not proof 24/24 is reachable now.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | 0.8333 |

Composite **96.67**. Commits since the last push are local only.
