# Reconciliation report

Accompanies `submissions/submission.csv`. Full architecture and
verification detail lives in `CLAUDE.md`; this is the specific report
the brief asks for: predicted class distribution and the cases we were
least sure about.

## Approach, briefly

Deterministic pipeline, zero LLM calls: normalize -> canonicalize units
-> match invoice to PO on `po_number` (exact, then a conservative
whitespace/case-normalized fallback) -> run 6 independent checks (PO
exists, vendor code, UOM, quantity, rate, GST) -> resolve to a single
status via a precedence order when more than one check fails -> a
second pass flags duplicate billing among otherwise-CLEAN invoices.
Every check returns structured evidence (`observed`/`expected`/`reason`),
not just pass/fail — see `src/reconciliation/models/check_result.py`.

## Class distribution predicted (250 invoices)

| Status | Count | % |
|---|---|---|
| CLEAN | 168 | 67.2% |
| QTY_MISMATCH | 21 | 8.4% |
| GST_ERROR | 16 | 6.4% |
| RATE_MISMATCH | 16 | 6.4% |
| MISSING_PO | 12 | 4.8% |
| VENDOR_MISMATCH | 12 | 4.8% |
| DUPLICATE_INVOICE | 5 | 2.0% |
| UOM_MISMATCH | 0 | 0.0% |

Real leaderboard result on this submission's methodology: **0.8700
macro-F1** (first attempt, 2026-09-07). Since macro-F1 weights all 8
classes equally regardless of support, a single class scoring near-zero
F1 while the rest score ~1.0 would alone produce `7/8 = 0.875` —
suspiciously close to the observed score. That points squarely at the
two classes below as the most likely source of the gap, not a general
weakness across the board.

## Cases we were least sure about

**1. `UOM_MISMATCH` = 0 predicted, and we have zero real evidence this
branch is correct.** Every genuine unit difference found in the data (13
invoices billed as `Box(10)` against a plain-`Nos` PO) turned out to be a
resolvable packaging notation — quantity ×10 and rate ÷10 both reconcile
exactly against the PO, so all 13 are correctly `CLEAN`, not
`UOM_MISMATCH`. The mismatch-detection code path (an unrecognized unit
like `Kg`) is unit-tested but has **never fired on real data**. If the
scored set contains a genuinely incompatible unit we haven't seen the
shape of, this is where we'd be wrong.

**2. 11 invoices are a deliberate near-boundary case within
`QTY_MISMATCH`, and we want to flag them specifically rather than bury
them in the count**: `INV-PIS-0298, AT00125, INV-SH-0060, INV-SVS-0269,
INV-RFP-0189, INV-RST-0070, INV-EF-0151, JEW00161, JC/2026/144,
INV-REW-0250, PCP/2026/157`. Each has an *exact* rate match, *exact* uom
match, and the invoice quantity is consistently 1-2 units HIGHER than the
PO — a clear, deliberate small-overbilling pattern (confirmed by direct
inspection, not assumed), distinct from 10 other invoices off by 3+
units. We're confident these are genuine `QTY_MISMATCH` (loosening the
tolerance to treat them as `CLEAN` would be wrong, and we deliberately
did not do that), but naming them here because they're the entire reason
our quantity-comparison tolerance is a hard `1e-6`, not a looser business
"close enough" threshold.

**3. Precedence order when an invoice fails more than one check
simultaneously is completely untested against real data.** 0 of 250
practice invoices ever fail two checks at once, so our precedence order
(`MISSING_PO > VENDOR_MISMATCH > UOM_MISMATCH > GST_ERROR > QTY_MISMATCH
> RATE_MISMATCH`) has never actually been exercised. We can't name
specific invoice IDs for this (none exist locally) — it's a structural
blind spot, not a case-level one.

**4. Vendor-name format variance.** The brief itself flags this as a
scenario needing "model calls or fuzzy matching," and we checked directly
for it: all 250 invoices have `vendor_name_on_invoice` byte-identical to
the vendor master (`vendors.csv`), so there's zero real example to build
or validate a name-matching rule against. Vendor mismatch is currently
decided purely on `vendor_id` (the vendor *code*, confirmed correct per
the brief's own wording), never the free-text name. If the scored set
has genuine name-format drift, this is the other place we'd be exposed.

**5. The `DUPLICATE_INVOICE` grouping key is our own extension beyond the
literal brief wording.** The brief says duplicate billing is "against one
PO" — we key on `(po_number, sku)` instead of `po_number` alone, since
every PO in the practice data happens to be single-line (260 rows, 260
unique `po_number`s) and a multi-line PO on a larger scored set could
otherwise let two legitimately different invoices get falsely paired.
Verified this changes zero rows locally, and a same-day tiebreak
(`invoice_number` ascending) was added defensively since no local example
of a same-date duplicate exists either.

## What we did NOT do

No LLM/model calls or fuzzy matching are used anywhere in this
submission, despite the brief inviting them for messy cases ("vendor
names in different formats... use model calls or fuzzy matching"). We
checked specifically for that scenario (#4 above) and found zero local
evidence to build against — adding speculative fuzzy-matching logic with
nothing to tune or test it on would be a guess dressed up as
engineering, which this project's own working discipline treats as worse
than leaving it explicitly flagged as open.
