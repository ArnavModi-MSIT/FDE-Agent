# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## What happened: a new code review, four hypotheses, all closed for free

A follow-up external code review (working from the pipeline/models/
matching/UOM files, without the classifier/check modules) raised several
"investigate before submitting" hypotheses. Checked every one of them
directly against real practice data rather than guessing — all came back
negative, so **nothing was submitted**.

## The four checks

1. **Malformed/blank numeric fields** (`safe_float()`'s `None`/`""`/bad
   value → `0.0` default) — checked every numeric field on all 250
   invoices + 260 POs: **zero malformed/blank/NaN/inf cells found**.
   Rejected by the review's own stated bar.
2. **Float strict-equality risk** — already settled by existing code the
   reviewer didn't have: `quantity.py`/`rate.py`/`gst.py` all use
   `abs(diff) <= tolerance`, never bare `==`; UOM's only `==` compares
   unit-label strings, not computed floats.
3. **SKU present on both Invoice/PO but never compared — what should a
   real mismatch resolve to?** A genuinely new, sharp question. Checked
   every matched invoice/PO pair: **zero SKU mismatches** across all 250.
   Currently moot — nothing to design a rule against.
4. **Vendor master loaded but unused (GSTIN/MSME/name)** — already
   tested the GSTIN angle earlier today (real regression, reverted, see
   below). The review's own top-priority ask (build the 8-status
   semantic matrix before touching code) was already done the day
   before (`submissions/reconciliation_status_matrix.md`).

## Verified, not narrated

Added two new permanent checks to `scripts/audit_practice_data.py`
(`audit_no_malformed_numeric_fields`, `audit_no_invoice_po_sku_mismatch`)
— both re-run and pass. All 9 audit checks now green.

## No attempt spent

Every checkable claim in this review came back negative by the review's
own explicit "don't submit without evidence" standard. Holding the last
daily Reconciliation attempt.

## Also still fresh from earlier today: vendor-GSTIN experiment, reverted

Tried resolving duplicate vendor codes via GSTIN equivalence (ticket
FIX-3402 + a real GSTIN-duplicate pattern in `vendors.csv`) — scored
**0.8579, down from 0.8700**, a real regression. Reverted immediately
(`git revert`), confirmed 94/94 tests pass and output is back to the
exact baseline (168/21/16/16/12/12/5/0). Settles that duplicate-vendor
-code invoices are meant to be flagged as genuine `VENDOR_MISMATCH`, not
resolved away.

## Recorded in CLAUDE.md

Full writeup of both the vendor-GSTIN regression and this review's
closed-out findings, in place after §5's experiment log.

## Still open

- Reconciliation: holding at 0.8700, **1/5 attempts remain today**, no
  new hypothesis — every checkable lever from two independent external
  reviews is now closed (neutral, disproven, or already confirmed)
- Knowledge (0.75): attempt count from before today's reset — check
  current count before spending
- W3 (5/6), W2 (0.75 of weight): no new investigation this round
- Repo: local commits through this round's documentation; not yet
  pushed — push only on explicit request
