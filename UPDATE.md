# Latest update — 2026-09-07

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## What changed

You shared an external score-improvement plan. Cross-checked its key
claims, then did a free investigation sweep against real sandbox
endpoints never queried before, rather than spend an attempt guessing.

## Plan cross-check

Confirmed real: the "#1 99.44%..." competitive numbers match your own
earlier leaderboard screenshot exactly, and the composite math (≈86.38%)
checks out. Flagged as unverified: "we're currently #7" — that depends
on other participants' live scores, not something the plan could have
actually observed. One internal inconsistency noted: the plan's
"priority order" (Knowledge first) contradicts its own composite-math
scenarios (Workflow/Reconciliation fixes are worth more) — the real
justification is tractability, not value, and the doc doesn't say so.

## Free investigation results — big one first

**`GET /vault/documents`** (never queried before) returns each policy
doc as `{code, title, body}` — and `code`'s values are **exactly**
`PP-2019`/`PP-2023`/`VOS-7`/`WRP-2020`, the platform's own canonical
identifier. This is real confirmation, not a guess: our `governing_source`
format has been correct all along. No experiment needed — settled for
free. Also cross-checked the full document text against `policy_kb.py`:
byte-for-byte consistent, zero discrepancies.

**Vendor-name variance and PO-reference validity**, re-checked against
the *sandbox's* real `/erp/invoices` and `/erp/purchase_orders` (not
just the local practice CSV): both confirmed clean a second, independent
way — 0 name mismatches, same 12 genuinely-synthetic missing PO
references.

**`/tickets` and `/email/messages`**, read in full for the first time:
identical content to local practice data, narrating scenarios already
correctly handled. Nothing new.

## Honest bottom line

Every free, well-reasoned investigation path for both Reconciliation
and Knowledge is now exhausted. Everything checkable without spending
an attempt has been checked — all either confirmed correct or already
disproven via a real submission. No new concrete lever for either
family's remaining gap right now.

## Recorded in CLAUDE.md

Full sweep documented in place, folded into the existing experiment
logs rather than a separate section.

## Still open

- Reconciliation (0.87) and Knowledge (0.75): no untested hypothesis
  remains for either — 2 attempts left on each today
- Workflow W2 (6/8) / W3 (5/6): same shared-wall situation, not
  independently investigated this round
- Repo: not re-pushed since before the whole Workflow/Migration build
