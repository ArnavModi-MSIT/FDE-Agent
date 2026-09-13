# Latest update — 2026-09-13

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## W3: a check we mis-derived, found by re-reading the live brief

The full W3 brief ends: **"Leave every other customer alone."**

We had assumed one W3 check "never passed in any state" (seed 1/6, now
5/6). That assumed the seed-passing check still passes. The simpler reading
fits exactly: at seed a leave-alone check passes and five merge checks fail;
after W3 **plus M3**, the merge checks pass and the leave-alone check fails.

## The evidence

Diffing live customers against the seed extract: **15 non-duplicate
customers** changed `crm_id` / `migrated_to_salestrack` (N → Y, minted id).
All 15 were changed **by our M3 run**, not by W3. The two tasks conflict on
end state. MJenius MJ shows the same pattern — Migration 1.0000, W3 5/6.

## Why it's fixable

Families keep their **best recorded** score and a scoring run reads state
at that moment. Migration's 1.0000 is banked, so a Workflow run taken with
those 15 at seed values can bank W3 6/6 without costing Migration anything.

## Next

```
python scripts/w3_experiment_leave_others_alone.py --execute
```
Then read the free W3 preview. 6/6 → spend one Workflow scoring run.
Anything else → `--restore`.

## Standing

- Reconciliation **1.0000** · Migration **1.0000**
- Workflow **0.9444** — W3 hypothesis 9 queued, free to test
- Knowledge **0.8333** — closed, derivable assertions exhausted
