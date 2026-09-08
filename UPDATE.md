# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Tried a genuinely new Reconciliation lever — real, confirmed regression, reverted

With the daily quota reset and 7/15 leaderboard participants at a
perfect Reconciliation score, tried something genuinely different
instead of another neutral tweak: `vendors.csv` has 4 GSTINs each shared
by two different `vendor_id`s (a real duplicate-vendor-code pattern,
matching ticket FIX-3402's "Vendor code confusion" — *"the same supplier
under two codes... POs and invoices landing on different codes"*). 2 of
the 12 local `VENDOR_MISMATCH` invoices are exactly this pattern and are
otherwise fully clean. Implemented a GSTIN-equivalence fallback in
`checks/vendor.py` so these resolve to CLEAN instead — the first change
since the original UOM canonicalization to actually move local output
(`CLEAN 168→170`, `VENDOR_MISMATCH 12→10`).

## Real result: regressed, not improved

**Scored 0.8579, down from 0.8700** — a real, confirmed drop of about
0.0121. Since this was the only variable changed, the loss pins
precisely on this fallback: **the hidden ground truth wants duplicate
-vendor-code invoices flagged as a genuine `VENDOR_MISMATCH`**, not
silently resolved via GSTIN. This is the opposite conclusion from UOM's
"look past superficial coding to the real transaction" logic — a useful,
concrete lesson: that principle doesn't generalize automatically across
different checks in this dataset.

## Reverted immediately

`git revert` of the whole experiment commit (`checks/vendor.py`,
`matching/vendor_gstin.py`, `classifier.py`, `pipeline.py`,
`w2_exceptions_report.py`, the 4 new tests) — cleanly undone. Verified
via a real re-run: **94/94 tests pass**, pipeline output back to the
exact prior baseline (168/21/16/16/12/12/5/0).

## This is real information, not a wasted attempt

The vendor-code-confusion hypothesis is now a *settled* question,
removed from the list of candidate explanations for the ~0.13
Reconciliation gap. 4 of 5 daily attempts used today, 1 remains — no new
hypothesis to test it with as of this entry.

## Recorded in CLAUDE.md

Full writeup (hypothesis, real score, revert, and the generalization
lesson) in place after §5's experiment log, plus the log's new row #5.

## Still open

- Reconciliation: holding at 0.8700 (current code state), 1/5 attempts
  remain today, no new hypothesis
- Knowledge (0.75): attempt count as of before today's reset — check
  current count before spending
- W3 (5/6), W2 (0.75 of weight): no new investigation this round
- Repo: local commit history now includes the experiment
  (`954f293`) and its clean revert (`627709c`) plus this documentation
  round, on top of `bd8c130`; not yet pushed — push only on explicit
  request
