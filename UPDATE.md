# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## W2 confirmed fixed: 8/8, Workflow composite now 0.9444

Re-posting W2's exceptions report with the corrected (post-UOM-fix)
classifier worked exactly as predicted: **W1 8/8, W2 8/8, W3 5/6** →
Workflow composite **0.9444**. W2's prior 6/8 gap was never a
W2-specific bug — it was the same UOM misclassification propagating
through the shared `classify_invoice` call. Fixing Reconciliation fixed
W2 as a side effect, no separate work needed.

## What's left

**W3's 5/6 is now the only remaining Workflow gap.** It's already been
investigated extensively in an earlier session — all 45 merges verified
row-by-row against the real 85-customer sandbox data, a fuzzy-similarity
scan for missed duplicates came back empty, and a plausible CRM-id
-consolidation theory was ruled out as too costly to test (would need a
full sandbox reset). No concrete new hypothesis identified yet, though
today's lesson (an "Open" ticket + "look past the surface" reasoning has
now been wrong twice, in both Reconciliation and the vendor-GSTIN
experiment) is worth applying to whatever W3-related tickets exist.

## Recorded in CLAUDE.md

Real confirmation added directly after the W2 repost writeup.

## Still open

- Reconciliation: **1.0000, solved.**
- Workflow: **0.9444** (W1 8/8, W2 8/8, W3 5/6) — only W3 left, no fresh
  hypothesis yet
- Knowledge (0.75): attempt count from before today's reset — check
  current count before spending
- Migration: 1.0000, already solved
- Repo: local commits through this round; not yet pushed — push only on
  explicit request
