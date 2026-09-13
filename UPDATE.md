# Latest update — 2026-09-13

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## W3 solved: 6/6, Workflow 1.0000

Keeping only the **5 ALL-CAPS merges** and unmerging the 40 regional-tag
records scored **W3 6/6**. The Workflow scoring run returned **1.0000**
(best recorded 1.0000). M3 stayed 5/5, since only `merged_into` changed.

## The rule

Duplicates are the SalesTrack re-keys of an existing account: the same name
in ALL CAPS. A `(North)`/`(South)`/`(II)` tag marks a separate account,
covered by the brief's "leave every other customer alone".

Organizer text said it all along: FIX-3415 "a handful", EM-106 "names in
caps". Every earlier W3 test held the 45-merge map fixed and varied things
around it. The map itself was the bug.

## Engine fixed, not just the sandbox

- `src/workflow/w3_customer_dedup.py` keeps the regional tag when grouping,
  and `run_w3` clears stale merges so a re-run converges to 6/6.
- Tests rewritten to the proven rule, including exact reproduction of the
  5-merge map from the seed extract. **109/109 pass.**
- Dry run against the live sandbox: 5 merges, 0 stale, 0 problems.

## Hazard

Do **not** run any old `w3_experiment_*.py --restore`. They restore the
45-merge snapshot and would drop W3 back to 5/6. The winning state is saved
as `crm_customers_w3_6of6_caps_only.json`.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | 0.8333 |

Composite about **96.67**. Knowledge is the only remaining gap.
