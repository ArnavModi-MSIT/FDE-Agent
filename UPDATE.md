# Latest update — 2026-09-13

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## W3: M3 interference ruled out; a new, evidenced hypothesis

**Hypotheses 9 and 10 disproven.** With every customer's `crm_id` and
migration flag back at seed — so `merged_into` was the only change anywhere,
exactly W3's own end state — W3 still read **5/6**. M3 is not the cause, and
"leave every other customer alone" on those fields is not the failing check.
The failing check is a property of the merge map itself.

## Hypothesis 11 — only the ALL-CAPS records are duplicates

We have always merged **45**. The organizer text never says 45:

- FIX-3415: "at least **a handful** of distributors exist twice"
- EM-106: "**names in caps** or with AND changed to ampersand"

Seed data fits that:

| Records | Count | In SalesTrack at seed | Tier + region + terms match original |
|---|---|---|---|
| ALL-CAPS | 5 | **5 of 5** | **5 of 5** |
| (North)/(South)/(II) | 40 | 25 of 40 | 4 of 40 |

The suffix label matches its own region field in only 7 of 40. Those look
like separate accounts the brief says to leave alone.

Hypothesis 6 (unmerge CAPS, keep suffix) collapsed to 0/6. **The mirror has
never been run.**

## Next

```
python scripts/w3_experiment_caps_only.py --execute
```
Read the free W3 preview, then `--restore`. If it moves but misses 6/6, the
variant keeping the 4 suffix records that are exact copies is
`--keep C-5057,C-5075,C-5077,C-5078`.

## Standing

- Reconciliation **1.0000** · Migration **1.0000** (banked)
- Workflow **0.9444** — W3 at 5/6, hypothesis 11 queued, free to test
- Knowledge **0.8333** — closed
