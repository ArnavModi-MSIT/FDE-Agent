# Latest update — 2026-09-08

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## What changed: a genuinely different Reconciliation lever

With the daily quota reset and 7/15 leaderboard participants at a perfect
Reconciliation score, went looking for a real, different class of
hypothesis instead of another neutral precedence/key tweak (those had
already twice proven they never move local output at all — no new
information to be had there).

## The finding

Cross-applied a discovery from a different family: W1's research
(2026-09-07) unpromptedly found 6 near-duplicate vendor codes sharing a
GSTIN with an existing vendor, in the live sandbox. Checked whether the
same pattern exists in `vendors.csv` (the file Reconciliation's own
vendor check reads) — **it does, independently**: 4 GSTINs each shared by
two different `vendor_id`s. Cross-referenced against ticket **FIX-3402**
("Vendor code confusion" — *"the same supplier under two codes... POs and
invoices are landing on different codes"*) and directly against the 12
real `VENDOR_MISMATCH` invoices: **2 of them** (`ATP/2026/251`,
`INV-JCP-0155`) are exactly this pattern, and both are otherwise fully
clean once vendor resolves (qty/rate/uom/gst all match).

## What changed in code

- `src/reconciliation/checks/vendor.py`: `check_vendor` now accepts an
  optional `vendor_gstin_index`; passes on exact `vendor_id` match **or**
  a shared `gstin` — narrow and evidence-bounded, never a general fuzzy
  vendor match.
- New `src/reconciliation/matching/vendor_gstin.py`: builds the
  `vendor_id -> gstin` index.
- `src/reconciliation/pipeline.py` and `src/workflow/w2_exceptions_report.py`
  (which reuses `classify_invoice` directly) both now load `vendors.csv`
  and wire the index through, so CSV Reconciliation and Workflow's W2
  can't disagree about these invoices.
- `models/vendor.py`/`normalization/vendor.py` — previously built but
  unused — are now actually consumed.

## Verified, not assumed

- 4 new tests in `tests/reconciliation/test_classifier.py` (GSTIN
  -equivalent pass, genuinely-different-vendor still fails even with an
  index present, backward-compat with no index). **37/37 reconciliation
  tests pass, 97/97 overall.**
- New re-runnable proof in `scripts/audit_practice_data.py`
  (`audit_gstin_duplicate_vendor_codes`) — confirms the 4 GSTIN groups
  and the exact 2 resolved invoices, not just narrated.
- **Real pipeline run**: this is the first Reconciliation change since
  the original UOM canonicalization to actually move local output —
  `CLEAN 168 → 170`, `VENDOR_MISMATCH 12 → 10`, everything else
  unchanged. Every prior post-baseline experiment (duplicate key,
  precedence swap, and their reversions) was byte-identical; this one
  isn't, which is itself informative regardless of the leaderboard
  result.

## Genuinely uncertain, not a safe bet

FIX-3402's ticket status is "Open" — the organizers describe this as an
unresolved real-world problem, not a settled rule for how the classifier
should treat it. It's plausible the true ground truth wants a
duplicate-code invoice flagged as `VENDOR_MISMATCH` precisely because
it's a data-hygiene defect worth surfacing. Weighed against that: the
check's stated purpose (brief: "the vendor code on the invoice vs the
PO") reads as catching a wrong-supplier error, which a GSTIN-verified
same-real-vendor case isn't — plus the direct parallel to UOM's own
already-confirmed "look past superficial coding" principle. Real enough
to be worth a submission; not certain enough to call settled without one.

## Not yet submitted

The corrected `submission.csv` is regenerated and ready
(`submissions/submission.csv`), but hasn't been uploaded to the
leaderboard as of this entry — that's the next step, at your call.

## Recorded in CLAUDE.md

Full reasoning, the exact affected invoices, and the new experiment-log
row (#5, pending) documented in place (§4's vendor-check writeup and a
new dated subsection after §5's experiment log).

## Still open

- Reconciliation: fresh 5/5 daily quota as of today; this vendor-GSTIN
  fix is the one queued, real hypothesis to spend it on
- Knowledge (0.75): 1 attempt left (from before quota reset — check
  current count), no new hypothesis
- W3 (5/6), W2 (0.75 of weight): no new investigation this round
- Repo: local commits through `bd8c130`; this round's changes
  (vendor-GSTIN fix) not yet committed or pushed — push only on
  explicit request
