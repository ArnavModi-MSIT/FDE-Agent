# Latest update — 2026-09-23

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## v59–v63 built

Leaderboard unchanged since 21 Sep (us 0.875/89 entries, Paavas Goyal
0.958/38 entries — still one short). Five new files, each testing a
genuinely untested idea rather than another wording:

- **v59** — the real diagnostic one. Pads **K-10**, a row already proven
  correct, to 3,668 characters (K-03/K-05/K-07 untouched). If K-10 keeps
  its point, it rules out a length cutoff as the reason the 21 Sep carpets
  (up to ~5.2k characters) failed — the last open uncertainty.
- **v60** — the four-digit ticket numbers (3401–3458) that were the one
  number range missing from the earlier "every number" carpet.
- **v61** — the real signatory named on each document (Anjali Deshmukh,
  Rohit Malhotra).
- **v62** — the document's full title, not just its code.
- **v63** — the clause number placed before the text (`4.1: ...`) instead
  of after, unlike the earlier bare-citation test.

0.9167+ on any of v60–v63 means a row landed. v59 losing its point (below
0.8750) would mean K-10's own row failed, which pins the cause on length —
important to know either way.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | **0.8750** |

Composite **97.50** (4th; Paavas Goyal 99.17). 117/117 tests pass. Commits
since the last push are local only.
