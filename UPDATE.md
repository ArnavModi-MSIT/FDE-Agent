# Latest update — 2026-09-15

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Overview page re-read live

- **Evaluation section**: re-runs against a hidden task suite, correctness
  first, cost and latency as tiebreakers, model calls through a metered
  proxy, any stack allowed. Nothing on how Knowledge answers are matched.
  The CSV uploads don't go through the proxy — "How to compete" says to
  submit the output CSV and "how you built it is your business".
- **Timeline not previously recorded**: finalists announced 2 Oct; finals
  7–9 Oct at Cypher 2026, where finalists walk through their agent live.
- **Correction**: an external tip's "SYS-02" and "Task 01" wording was
  dismissed yesterday as not from this competition. It is — the Overview
  lists systems SYS-01 to SYS-05 and challenges 01 to 04. The tip's
  substance is still contradicted by our results.

## Why the finals date matters

The Knowledge engine (`scripts/run_knowledge.py`) still produces the 0.7500
answers; the banked 0.8333 set is hand-written. A live walkthrough would
show the engine, so it should be updated to reproduce the banked answers.

## Knowledge yesterday

Five attempts (v19–v23), all 0.8333. Still wrong: K-03, K-05, K-07, K-08.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | 0.8333 |

Composite about **96.67**. Commits since the last push are local only.
