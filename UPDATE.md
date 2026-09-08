# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Re-posted W2's exceptions report with the fixed classifier

Now that Reconciliation's UOM fix is confirmed (real leaderboard score:
1.0000), the natural next step was checking whether that same fix
propagates to Workflow's W2 — it deliberately reuses `classify_invoice`
directly, so any classification improvement there should carry straight
into W2's `counts`/`value_at_risk`.

## What was checked before posting

Dry-run (`scripts/run_w2.py`, no `--execute`) against the live sandbox
confirmed the effect for real, not just assumed: `UOM_MISMATCH 0 → 13`
(exactly matching the local shift), `value_at_risk` moved from
₹8,30,99,028.06 to ₹8,84,04,135.42. This is the same, well-understood
fix — no new hypothesis, no new risk.

## Posted

`scripts/run_w2.py --execute` — confirmed accepted by the sandbox
(echoed back exactly what was sent). **Posting doesn't consume a scoring
attempt** — only clicking "Run the checks and score" on the site does.
That's the next step, at your call, to see whether W2's 6/8 improves.

## Recorded in CLAUDE.md

Dated note added directly after the original W2 writeup in §9.

## Still open

- Reconciliation: **1.0000, solved.**
- Workflow: W1 was last known at 8/8 (perfect, untouched by this
  change). W2's corrected report is posted but not yet scored — check
  the sandbox for the real result. W3 (5/6) still genuinely unexplained.
- Knowledge (0.75): attempt count from before today's reset — check
  current count before spending
- Migration: 1.0000, already solved
- Repo: local commits through this round; not yet pushed — push only on
  explicit request
