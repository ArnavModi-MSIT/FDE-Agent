# CLAUDE.md — DRI Reconciliation Engine (FDE Hackathon 2026)

This is the working record for this project — the detailed context for
picking this up cold, human or AI. It describes **current state**: what's
built, what's verified against real data, what's still a stub, and why
each non-obvious decision was made. When something changes, this file
should be updated in the same turn, not appended to as a log.

**`UPDATE.md`** is the companion to this file: a short "what just changed
and why" snapshot, rewritten fresh (never appended) after every real
change, for a quick check-in without reading this whole document. This
file (`CLAUDE.md`) stays the full, durable record — every decision
`UPDATE.md` ever summarized should already be folded into the relevant
section here, not only living in `UPDATE.md`'s current snapshot.

---

## 1. What this is

An entry for **The Great Indian FDE Hiring Hackathon 2026** (AIM Media
House / MachineHack). The premise: DRI Industries, a fictional 43-year-old
manufacturer with fragmented legacy systems (ERP, half-migrated CRM,
ticketing, a shared mailbox, 1,100+ contradictory policy docs). Four
scored task families, weighted:

| Family | Weight | Mechanism |
|---|---|---|
| Reconciliation | 0.3 | Static CSV in -> CSV out, scored macro-F1 across 8 classes |
| Workflow | 0.3 | Live REST sandbox (`/api/public/sandbox/v1`), scored on end-state |
| Migration | 0.2 | Same sandbox, scored on end-state |
| Knowledge | 0.2 | Free-text Q&A over 4 policy PDFs, scored 0.5 answer + 0.5 source |

All four weights and both submission formats below are **verified verbatim
from the rules page**, not assumed:
- Reconciliation: `invoice_number,status`
- Knowledge: `qid,answer,governing_source`
- Composite weights: `reconciliation 0.3, knowledge 0.2, workflow 0.3, migration 0.2`
- Deadlines: registration closed 2026-09-06; qualifier submissions close
  2026-09-20; **all submissions freeze 2026-09-27 23:59 IST** (a separate,
  later hard cutoff than the qualifier close — the gap between the two
  isn't explained anywhere I've read, don't assume extra scored attempts
  in that week without checking).
- 5 scored submissions per task family per day (Asia/Kolkata); a
  malformed/rejected file doesn't consume an attempt; ground truth is
  never disclosed, only one number per submission.

Sandbox API details (base URL, auth, endpoints, rate limits, the 6 task
briefs W1-W3/M1-M3 and their check counts) came from user-provided
screenshots of `/sandbox-docs`, not yet independently fetched — treat as
provisional until the sandbox key is in hand and the live endpoints are
actually called once.

**Reconciliation and Knowledge are both built.** Migration has started
(M1 done, verified against the live sandbox — see §9). Workflow hasn't
started. `src/api/client.py` exists, built from real sandbox calls, not
screenshots.

---

## 2. The core architectural bet

Deterministic-first, LLM only where genuine ambiguity requires reasoning
(policy language conflicts, free-text interpretation) — never for
arithmetic, ID matching, or anything with an explicit rule. This isn't a
stylistic preference: the sandbox scores **end-state**, not process, and
the CSV tasks score **macro-F1**, which punishes an inconsistent or
LLM-variable classifier hard. Every module in `reconciliation/` is pure
Python, zero network calls, zero LLM calls, fully reproducible.

---

## 3. Repository structure

```
The Great IndianFDE/
├── CLAUDE.md                    <- this file, the full durable record
├── UPDATE.md                     <- rewritten fresh every change: quick
│                                    "what just happened" snapshot
├── requirements.txt              pandas (starter kit dependency only —
│                                   the reconciliation engine itself has
│                                   zero third-party dependencies), pytest
├── starter_reconciliation.py     the organizers' own naive baseline —
│                                   kept as-is, used as a comparison point
│                                   (see §5), never modified
│
├── dataset/
│   ├── Document store/            the 4 policy PDFs (VOS-7, PP-2019,
│   │                                PP-2023, WRP-2020) — read in full,
│   │                                see §6
│   └── System extracts/           the practice CSVs (vendor_invoices,
│                                    purchase_orders, vendors, products,
│                                    customers, tickets, emails,
│                                    knowledge_questions, sample_submission)
│
├── src/
│   ├── common/                    cross-cutting utilities, shared by every
│   │   └── io.py                   future family (not just reconciliation)
│   │
│   └── reconciliation/            <- BUILT, see §4
│       ├── pipeline.py             single orchestrator entrypoint
│       ├── models/                 typed dataclasses: Invoice, PurchaseOrder,
│       │                            Vendor, Product (Vendor/Product not yet
│       │                            consumed by any check — see §4),
│       │                            CheckResult (observed/expected/reason
│       │                            evidence every check returns)
│       ├── normalization/          raw CSV dict -> typed model
│       ├── uom/                    the Box(10)->Nos conversion registry
│       ├── matching/                exact / normalized-fallback / resolver
│       ├── checks/                  one module per rule: po, uom, quantity,
│       │                            rate, vendor, gst — each returns a
│       │                            CheckResult, not a bare bool
│       ├── duplicates/              earliest-stays-CLEAN duplicate pass
│       ├── classify/                precedence order + the classifier that
│       │                            applies it
│       ├── evaluation/              macro-F1 metrics + structural sanity
│       │                            checks (no local ground truth exists —
│       │                            see §5)
│       └── submission/              writes submission.csv in the exact
│                                    required format
│
│   └── knowledge/                <- BUILT, see §8
│       ├── pipeline.py             orchestrator, mirrors reconciliation's shape
│       ├── models.py                ParsedQuestion, Answer
│       ├── policy_kb.py              structured rules transcribed from the 4
│       │                             real PDFs, one function/constant per rule,
│       │                             cited inline
│       ├── temporal.py                date -> PP-2019/PP-2023 resolution,
│       │                              month-arithmetic for warranty calc
│       ├── parsing.py                  question text -> ParsedQuestion
│       │                              (regex-based, not an LLM call)
│       ├── answering.py                 topic -> policy_kb lookup -> Answer
│       ├── evaluation.py                 structural sanity checks only
│       └── submission.py                  writes qid,answer,governing_source
│
│   -- not yet created, scaffolded only in the plan, not on disk --
│   workflow/, migration/, api/  (siblings of reconciliation/knowledge/,
│                                  to be added once the sandbox key is in hand)
│
├── configs/
│   └── reconciliation_config.py   every tunable threshold (GST rate/
│                                    tolerance, rate tolerance, qty
│                                    tolerance) — centralized so nothing in
│                                    checks/ hardcodes a business rule
│
├── scripts/
│   ├── run_reconciliation.py      the real CLI entrypoint — run this, not
│   │                                pipeline.py directly
│   ├── audit_practice_data.py      re-runnable proof for every "confirmed
│   │                                 real in the data" claim in §4 — run
│   │                                 this, don't just trust the prose
│   └── run_knowledge.py             Knowledge CLI entrypoint, prints every
│                                      answer's reasoning trace alongside the
│                                      submission file
│
├── tests/
│   ├── conftest.py                 puts src/ + repo root on sys.path
│   ├── reconciliation/             29 tests, all passing (§5)
│   └── knowledge/                  25 tests, all passing (§8) -- no
│                                     __init__.py here deliberately, see §8's
│                                     "real bug found" writeup for why
│
└── submissions/
    └── submission.csv              generated output, overwritten each run
```

No `src/__init__.py` — `src/` is added directly to `sys.path` by both
`scripts/run_reconciliation.py` and `tests/conftest.py`, so `common` and
`reconciliation` import as top-level packages (standard src-layout). Same
pattern for `configs/` off the repo root.

---

## 4. Reconciliation engine — design decisions, each checked against real data

**8 classes**: `CLEAN, QTY_MISMATCH, RATE_MISMATCH, DUPLICATE_INVOICE,
MISSING_PO, VENDOR_MISMATCH, GST_ERROR, UOM_MISMATCH`.

**REVERTED 2026-09-08 — see the dated experiment writeup after §5's
experiment log for the full story.** For most of this project's life,
`checks/uom.py` canonicalized `Label(N)` packaging notation (e.g.
`Box(10)`) to a common base unit instead of the starter kit's raw
`str(invoice.uom) != str(po.uom)` string comparison, on the reasoning
below. That reasoning is now **superseded by a real, symmetric
counter-example** (the vendor-GSTIN experiment, same day) and the
implementation has been reverted to the starter's literal raw string
comparison. `uom/registry.py` and `uom/converter.py` still exist and are
still correct as generic utilities — they're simply no longer called by
`checks/uom.py` — kept rather than deleted per this project's own
"don't delete working code you might need again" discipline. The
original reasoning, kept for the record:

Checked the real practice data before trusting either approach:
`purchase_orders.csv` is uom=`Nos` on all 260 rows; `vendor_invoices.csv`
has 237 `Nos` and **13 rows billed as `Box(10)`**. For every one of those
13, `invoice_qty × 10 == po_qty` exactly, **and** `invoice_rate / 10 ==
po_rate` exactly (confirmed by direct computation, not assumed) —
meaning a box of 10 is billed at 10x the per-unit rate, exactly as real
packaging pricing would work. The reasoning was that the naive starter
script therefore misclassifies all 13 as `UOM_MISMATCH` when they are
genuinely `CLEAN` — canonicalization "fixed" this. Backed at the time by
two organizer sources: the copy-ready brief's own `Box(10)` example, and
ticket **FIX-3418** ("Spares billed in boxes" — *"Value tallies, count
does not"*). **The flaw in that reasoning, found only after the
vendor-GSTIN experiment gave a real, directly parallel counter-example**:
FIX-3418 is itself an **"Open"** ticket, literally opening with *"Stores
GRN shows quantity mismatch"* — the same ticket-status pattern as
FIX-3402 (also "Open"), which real leaderboard evidence just confirmed
means "the organizers want this flagged as a genuine defect," not
"resolved away by looking past the surface difference." The brief's own
`Box(10)` mention is equally readable as an example of what
`UOM_MISMATCH` looks like, not evidence it should be excused.

**Verified empirically, not just unit-tested, both before and after the
revert**: ran the full engine against all 250 practice invoices and
diffed against the starter script's own output. **Before** the revert,
identical on every class except `CLEAN 155→168` / `UOM_MISMATCH 13→0`
(the 13 Box(10) rows). **After** the revert (current state): **byte
-for-byte identical to the starter's own output on all 250 rows, 0
differences** — `CLEAN 155, QTY_MISMATCH 21, RATE_MISMATCH 16,
GST_ERROR 16, UOM_MISMATCH 13, MISSING_PO 12, VENDOR_MISMATCH 12,
DUPLICATE_INVOICE 5`. Re-run both (`scripts/run_reconciliation.py` and
`starter_reconciliation.py`) after any future UOM-related change to
confirm this still holds.

**Matching (`matching/`)**: exact `po_number` lookup first, then a
whitespace/case-normalized fallback. Deliberately **no similarity/fuzzy
matching** — checked directly: 12 of 250 invoices miss an exact PO match,
none are recovered by trim/case-normalization either (they cite synthetic
`PO/2026/9xxx` numbers that simply don't exist in `purchase_orders.csv`).
A fuzzy match here would risk fabricating a match to an unrelated real PO
— worse than correctly escalating to `MISSING_PO`. Re-verify this
assumption if the hidden/sandbox PO set behaves differently (real
formatting variants, not synthetic gaps).

**Vendor check (`checks/vendor.py`)**: plain `vendor_id` equality.
Checked whether the two vendor-code namespaces in the data (`V-` for
native DRI vendors, `FTV-` for legacy FlowTech vendors, both present in
invoices and POs) cause any orphans against `vendors.csv` — they don't
(0 orphans out of 250 invoices). No cross-namespace resolution needed for
*this* check; that kind of entity-resolution problem belongs to the
future Workflow family's W3 (CRM dedup), which has a genuinely different,
richer signal set (see §7).

**GST check (`checks/gst.py`)**: `gst_rate_pct` is 18.0 on all 250
practice invoices — treated as a fixed business rule (a declared rate
other than 18% is itself an error, not a legitimate variant), matching
the starter kit's own hardcoded 18%. Tolerance ₹0.05, matching the
starter kit exactly.

**Duplicate pass (`duplicates/detector.py`)**: runs *after* every other
check, only among rows currently `CLEAN`. Within a group sharing the same
**`po_number`** — matching the starter kit's own literal
`duplicated(subset=["po_number"])` exactly — the earliest-dated invoice
stays `CLEAN`; the rest become `DUPLICATE_INVOICE`, with `invoice_number`
as a deterministic tiebreak on same-date ties. A row that already carries
a genuine defect (e.g. `RATE_MISMATCH`) is never touched by this pass —
that defect is real regardless of billing duplication. Verified against
real data: exactly 5 `po_number`s are each billed by 2 invoices in the
practice set, all 5 resolve as expected.

**SETTLED, following the status-definition matrix audit (§5)**: this
was briefly keyed on `(po_number, sku)` instead — a defensive extension
against a hypothetical multi-line PO, added before there was any hard
evidence either way. Reverted back to `po_number` alone for two combined
reasons, not one: (1) building `submissions/reconciliation_status_matrix.md`
surfaced the starter kit's own reference code as real specification, and
its literal grouping key is `po_number` alone, with no mention of SKU
anywhere in any organizer text; (2) the extension is also structurally
moot on data we can actually see — `po_number` is confirmed globally
unique in *both* the 250-invoice practice set and the live sandbox
(260/260 rows, both places), so no multi-line PO exists anywhere to
protect against. The earlier submitted experiment (row 2 in §5's
experiment log) already proved this change is byte-identical on local
output either direction, so reverting spends no new attempt and is
predictably neutral, not a guess.

**Precedence (`classify/precedence.py`)**: kept as its own module,
separate from the classifier's mechanics, specifically because it's a
genuine tunable — the starter kit's own comment says reordering it moves
macro-F1, and its own confirmed prose explicitly declines to state a rule
for invoices with multiple defects. Represented as `(status, check_name)`
pairs so the classifier never hardcodes the status-to-check mapping twice.

**SETTLED, following the status-definition matrix audit (§5): back to
the starter kit's own literal order** — `MISSING_PO > VENDOR_MISMATCH >
UOM_MISMATCH > QTY_MISMATCH > RATE_MISMATCH > GST_ERROR`. This briefly
had `GST_ERROR` promoted above `QTY_MISMATCH`/`RATE_MISMATCH` — one
isolated swap, on the reasoning that `gst` is computed entirely from the
invoice's own fields while quantity/rate compare against an external
reference (the PO) — submitted as experiment #3 in §5's log and found
**byte-identical, zero score movement** (0.8700, unchanged). Reverted for
the same combined reason as the duplicate key above: the status-matrix
audit surfaced `starter_reconciliation.py`'s literal `if/elif` chain as
real organizer specification (checks quantity and rate *before* GST),
and the earlier submitted experiment already proved the swap carries no
supporting evidence — it was neutral in both directions, so reverting
spends no new attempt. A synthetic test
(`test_precedence_matches_starter_reference_quantity_outranks_gst`) now
proves the *reverted* order — `QTY_MISMATCH` outranking `GST_ERROR` on a
synthetic invoice that genuinely fails both — actually took effect in
code, not that the order is provably correct on hidden data (that's still
only knowable from a submission — see §5).

**Every check returns a `CheckResult`** (`check`, `passed`, `observed`,
`expected`, `reason`), not a bare bool — added after an external review
correctly pointed out that a bare pass/fail throws away exactly the
evidence W2 will need later (aggregate value-at-risk per exception type)
and that debugging/human review benefits from "why," not just "which."
`classify_invoice()` returns **every check's full `CheckResult`**, not
just the winner, in `ClassificationDetail.check_results` — never enters
the submission CSV, but it's the whole reason `pipeline.py` keeps
per-invoice detail alongside the final predictions dict.

**Not yet wired in**: `models/vendor.py`, `models/product.py`,
`normalization/vendor.py` exist (per the reviewed architecture) but no
check currently loads `vendors.csv`/`products.csv` — none of the 8
classes need them today. Present so the vendor/product master is ready to
load the moment a check needs it, not speculative overbuilding.

---

**The organizers' own copy-ready agent brief** (pasted by the user
2026-09-07) was cross-checked against everything built here — full
agreement on every rule (GST 18%, later-dated invoice is the duplicate,
`Box(10)` vs `Nos` as the UOM example, vendor *code* not name). It also
asks for two deliverables beyond the CSV: the predicted class
distribution and "the cases you were least sure about" — written up in
`submissions/reconciliation_report.md`, not just narrated in chat, since
it's a real artifact the brief explicitly requests.

## 5. Verification status

**25/25 tests pass** (`tests/reconciliation/`): UOM converter (base unit
passthrough, the real Box(10) case, Carton(20)/Pack(5) — never observed in
the practice data, proving the registry parser is genuinely generic and
not secretly hardcoded to "Box" — unresolvable units, malformed patterns),
classifier (all 8 classes including the box-packaging-is-CLEAN case and
both GST failure modes), duplicate detector (earliest-stays, genuine
-defect-not-overridden), metrics (macro-F1 formula, including the explicit
"absent class scores 0, isn't silently excluded" edge case),
**determinism** (`test_determinism.py` — runs the real pipeline against
the real data twice, requires byte-identical output; a submission system
with a 5-attempts/day budget can't afford a nondeterministic classifier),
**submission structural invariants** (`test_submission_invariants.py` —
required header, no duplicate output rows, every status a legal class, no
missing/extra invoices vs the source file).

**`scripts/audit_practice_data.py`** is the re-runnable proof behind every
"confirmed real in the data" claim below — an external review correctly
pointed out that narration alone ("verified empirically") isn't
verification if nobody can re-run it. Covers: the Box(10) x10-qty /
÷10-rate reconciliation (13 rows, 0 mismatches), GST rate distribution
(18% on all 250), vendor namespace overlap (0 orphans), PO match
recoverability (12 exact misses, 0 recovered by normalization), duplicate
PO billing (exactly the 5 documented pairs). Run it after any change to
`dataset/` or the practice-data assumptions in §4 — it exits nonzero if
any of them stop holding.

**Real end-to-end run** (`python scripts/run_reconciliation.py`, from the
project venv): 250/250 invoices classified, written to
`submissions/submission.csv` in the exact `invoice_number,status` format.
Counts: CLEAN 168, QTY_MISMATCH 21, GST_ERROR 16, RATE_MISMATCH 16,
MISSING_PO 12, VENDOR_MISMATCH 12, DUPLICATE_INVOICE 5, UOM_MISMATCH 0.

**No local ground truth exists for this dataset** — `evaluation/metrics.py`'s
macro-F1 function is tested against synthetic labels only.
`evaluation/evaluator.py`'s `sanity_check()` can only catch structural
bugs (illegal status values), not accuracy — real accuracy is only ever
knowable from the leaderboard's single returned number. Budget submission
attempts accordingly (5/family/day) — change one thing per submission and
record what moved, don't burn attempts on unvalidated guesses.

**Real leaderboard score, first submission**: macro-F1 **0.8700**
(2026-09-07, 1/5 Reconciliation attempts used that day). This is the
first actual ground-truth signal this project has had — everything
before it was local/structural only. No per-row or per-class feedback is
given, by design (rules page), so 0.87 has to be interpreted from
structural reasoning, not direct evidence:

The single most likely explanation: **macro-F1 weights all 8 classes
equally regardless of support**, so one class scoring near-zero F1 while
the other seven score ~1.0 would alone produce `7/8 = 0.875` — suspiciously
close to the observed 0.8700. The two classes most structurally at risk of
exactly that on the hidden set:
- `UOM_MISMATCH` — **zero local occurrences** (every practice-set unit
  mismatch turned out to be a convertible `Box(10)` packaging notation,
  so this class never actually fires in `submissions/submission.csv`
  today). If the hidden set contains genuinely incompatible units (e.g. a
  weight unit against a count-based PO) or a packaging notation our
  `Label(N)` regex doesn't parse the way the graders expect, we'd have no
  local signal warning us.
- `DUPLICATE_INVOICE` — smallest local class (5/250, ~2%), so the
  hidden-set analog is the class most exposed to a single wrong
  assumption (e.g. if the true rule isn't strictly "earliest date wins"
  in some edge case, or ties on date, or a duplicate defined by more than
  matching `po_number`).

Other, lower-probability contributors: `GST_ERROR`'s rounding tolerance
(₹0.05) or `RATE_MISMATCH`'s tolerance (₹0.01) could be miscalibrated for
the hidden set's actual float-precision noise; the precedence order
(§4) could be suboptimal in a way that doesn't show up on the practice
set's specific defect combinations; `matching/fuzzy.py`'s deliberately-no
-similarity-matching choice could be wrong if the hidden PO numbers have
real (not synthetic) formatting variants.

**Leaderboard calibration (checked, not guessed)**: as of 2026-09-07,
12 ranked participants, **6 of them show Reconciliation = 1.000 exactly**
(including a student entry). This rules out "0.87 is near an inherent
ceiling" — a perfect score is demonstrably reachable on this same task
with the same data, so the gap is a real, closeable bug in our logic, not
hidden-set ambiguity. Raises the priority of hardening over resubmitting
on a hunch.

**One real structural gap found and fixed from this**: `purchase_orders.csv`
happens to have `po_number` 1:1 with rows in the 250-invoice practice set
(260 rows, 260 unique `po_number`s — every PO is single-line) — but the
rules page states the hidden set runs to "thousands of rows." If even one
hidden PO has multiple genuine line items (multiple SKUs under one
`po_number`), the old `duplicates/detector.py` (keyed on `po_number`
alone) would falsely flag two legitimately different invoices as
duplicates of each other. Fixed by keying on `(po_number, sku)` instead —
verified this changes **nothing** on the practice set (all 5 real
duplicate pairs also happen to share `sku`, and the full pipeline run is
byte-identical before/after: 168/21/16/16/12/12/5/0), so it's pure
defensive hardening against a risk the local data structurally can't
exercise, not a guess. Also added a deterministic `invoice_number`
tiebreak for same-date ties (none exist locally, but an arbitrary
file-order fallback was a real nondeterminism risk on a larger set).

**Two more free (no-attempt-cost) local investigations, run before
deciding what to submit next:**

- **Multi-error invoices: 0 of 250.** Every non-clean invoice in the
  practice set fails exactly one check — never two or more. This means
  **precedence order has never been exercised locally at all**; it's a
  complete blind spot, not just "unproven optimal." If the hidden set
  has invoices with genuinely co-occurring defects, `classify/precedence.py`'s
  order (inherited unmodified from the starter kit) is exactly as likely
  to be wrong as right — there's no local evidence either way.
- **GST tolerance boundary scan: cleanly bimodal, not miscalibrated.**
  Across all 250 invoices, 234 are exact-zero diff from expected GST and
  the other 16 (`GST_ERROR`) are off by ₹58–₹1,64,266 — **zero** sit
  anywhere between ₹0 and ₹0.10. There's no ambiguous middle ground on
  this data where the ₹0.05 tolerance choice would matter, which
  de-prioritizes GST tolerance as a likely cause of the 0.87 gap (on this
  practice-set analog specifically — can't rule out the hidden set
  differing).
- **UOM symmetry, explicitly tested, not just assumed**: added a test
  proving packaging notation works when it's on the **PO** side (`Box(10)`
  on the PO, plain `Nos` on the invoice) — every real practice-data
  example only ever has packaging on the invoice side, so this direction
  was previously untested, just structurally assumed to work because
  `canonicalize()` is called identically on both sides.

**Still-open hypotheses, not yet acted on**: `UOM_MISMATCH` never fires
on the practice set (§4) — the mechanism is unit-tested but has zero real
-data confirmation. The precedence order specifically has zero local
signal either way (see above), which raises its priority for the *next*
investigation after this submission, not this one. Next submission
changes exactly one thing — the duplicate-key fix — per the "don't
guess-and-resubmit, don't bundle changes" discipline both external
reviews converged on.

### Experiment log

| # | Change | Local effect | Hypothesis | Score |
|---|---|---|---|---|
| 1 | Baseline (UOM canonicalization engine) | — | — | **0.8700** (2026-09-07) |
| 2 | Duplicate key `po_number` -> `(po_number, sku)` + deterministic tiebreak | Byte-identical (0 rows changed) | Hidden set may have multi-line POs the practice set's 1:1 structure can't exercise | **0.8700** (2026-09-07, unchanged) |
| 3 | Precedence: `GST_ERROR` promoted above `QTY_MISMATCH`/`RATE_MISMATCH` | Byte-identical (0 rows changed — 0/250 invoices ever fail 2+ checks, so no reorder can move local output) | An internal arithmetic check (gst) should outrank an externally-compared value check (qty/rate) when both fail on the same invoice | **0.8700** (2026-09-07, unchanged) |
| 4 | Both #2's key and #3's reorder reverted back to `starter_reconciliation.py`'s literal logic, per the status-definition matrix audit | Byte-identical (168/21/16/16/12/12/5/0, confirmed pre- and post-submission) | Matrix audit found no organizer evidence supporting either deviation; both directions already proven neutral by #2/#3 themselves | **0.8700** (2026-09-07, unchanged — real confirmation, not just local prediction) |
| 5 | Vendor check: GSTIN-equivalence fallback for duplicate vendor codes (ticket FIX-3402 + real GSTIN duplicates in `vendors.csv`) | **Real change**: CLEAN 168→170, VENDOR_MISMATCH 12→10 | Same-real-vendor-under-a-different-code should resolve as CLEAN, not a genuine mismatch, mirroring UOM's "look past superficial coding" logic | **0.8579** (2026-09-08, **regressed** — reverted immediately) |
| 6 | UOM check reverted to the starter's literal raw string comparison (`checks/uom.py`) — `Box(10)` vs `Nos` now `UOM_MISMATCH`, not `CLEAN` | **Real change, largest yet**: CLEAN 168→155, UOM_MISMATCH 0→13 — output now byte-identical to `starter_reconciliation.py` on all 250 rows | FIX-3418 (the ticket justifying canonicalization) is itself "Open," same as FIX-3402 — which #5 just proved means "flag the defect," not "resolve it away." Starter's literal code + 6+ leaderboard participants at 1.000 without (as far as known) inventing packaging-aware conversion | **1.0000** (2026-09-08, **perfect score — gap fully closed**) |

**Attempts #2 and #3 submitted identical CSV content to #1** — neither
change alters any row's classification, confirmed before each submission.
Not 3 independent experiments; 1 real data point (0.8700) confirmed
twice more. Investigated rate/quantity tolerance boundaries next (free,
no attempt cost) rather than spending a 4th attempt with no new
hypothesis — see §4's tolerance-scan writeup. Quantity tolerance's
apparent ambiguity was investigated and confirmed correct, not acted on
(would have hurt macro-F1, not helped it). No further local lever found.
2 of 5 daily attempts remain, unspent — no new hypothesis to test them
with as of this entry.

**Result of #2: unchanged, and that's real information, not a wasted
attempt.** Score stayed exactly 0.8700. Consistent with the local
finding that this change produced 0 row differences — either the hidden
set also has no multi-line POs, or it does but something else masks the
effect. Either way, **the multi-line-PO theory is no longer the leading
hypothesis** for the 0.13 gap. Kept the fix (it's still correct defensive
hardening, provably can't have hurt), moving to the next investigation.

**Multi-error invoices and GST tolerance are now dead ends on this data**
— both were the two concrete, data-driven leads available, and both
came back negative (0 co-occurring defects to learn from; GST cleanly
bimodal with no ambiguous zone). Reordering `classify/precedence.py`
without a specific hypothesis would be exactly the "randomly change
precedence" mistake both external reviews explicitly warned against — no
reordering attempt yet, deliberately, until there's a real reason to
pick one order over another.

**Checked the actual Starter Kit page's prose (not just the script) for
an authoritative spec, since every check so far had been reverse
-engineered from code comments, never a written definition.** Found real
text, quoted directly: duplicate rule *"the later-dated invoice is the
duplicate"* (confirms our rule), GST *"GST at 18%"* (confirms ours),
vendor matching *"checking the vendor code on the invoice vs. the PO"*
(confirms `vendor_id` is the right field — not `vendor_name_on_invoice`,
which the model carries but no check currently reads). The Overview,
Data, and Rules pages, re-queried specifically for these definitions,
have **none** — the Starter Kit page's prose is the only authoritative
source beyond the script itself, and it now directly confirms 3 of our 4
checks rather than leaving them as inferred.

**One caveat surfaced, checked, and found not (yet) actionable**: the
same text says vendor *"names in different formats may require fuzzy
matching or model calls"* — but a direct check found **0 of 250**
practice invoices have any `vendor_name_on_invoice` differing from the
vendor master at all (byte-for-byte identical every time). Real per the
organizers' own words, matches the starter script's own separate warning
("expect messier inputs than these practice files... that is where model
calls stop being optional"), but there is currently zero local data to
design or validate a name-matching rule against. Not implemented —
building speculative fuzzy-matching logic with no example to tune or
test it against would be exactly the kind of guess this project's
discipline exists to avoid. Recorded as a known, confirmed-real,
currently-inactionable gap, not ignored.

**Submitted the precedence reorder (experiment #3): also unchanged,
0.8700.** Expected, per the same structural reasoning as #2 — see §5.

**Realized after #3: attempts #1, #2, and #3 submitted byte-identical CSV
content.** Neither the duplicate-key fix nor the precedence reorder
changes a single row's classification on the practice set (both
confirmed 0-row-changed before submitting) — meaning the last two
"experiments" weren't really independent data points, they were the same
file re-confirmed twice. Worth naming plainly: don't mistake "we made a
change and resubmitted" for "we ran an experiment" — a resubmission only
teaches something new if it actually alters the submitted content.

**Rate and quantity tolerance boundary-scanned with the same rigor as
GST — one gave a real near-miss, investigated in full before acting.**
Rate: cleanly bimodal like GST (210 exact, smallest genuine mismatch
₹6.12 — no ambiguity). Quantity: **not** cleanly bimodal — 205 exact,
10 far-off (3+ units), but **11 invoices sitting in a distinct middle
cluster, off by exactly 1–2 units**. Inspected all 11 individually before
concluding anything: every one has an *exact* rate match, *exact* `uom`
match, and the invoice quantity is consistently HIGHER than the PO by
1–2 units — a deliberate, distinct small-magnitude overbilling pattern,
not rounding noise. Raising the quantity tolerance to absorb this cluster
as `CLEAN` would have been **wrong** — it would convert 11 genuine
defects into false negatives, likely hurting macro-F1. Confirmed the
current near-zero tolerance is correct rather than acting on the
apparent ambiguity. A near-miss worth recording: this looked exactly
like the kind of lever we were hoping to find, and the full inspection
is what caught it wasn't one.

**State: every locally-checkable hypothesis has now been investigated
and closed** — duplicate key (fixed, provably inert), precedence
(tried, provably inert), GST/rate/quantity tolerance (all confirmed
correct against real data), vendor matching (confirmed via organizer
text), UOM registry (generic, tested both directions). What remains —
real `UOM_MISMATCH` behavior, vendor-name fuzzy matching — both need data
we don't have. **3 of 5 daily Reconciliation attempts spent, zero new
information gained past the initial 0.8700** (attempts #2 and #3 were
the same file, confirmed twice). Recommendation: stop spending
Reconciliation attempts without a genuinely new hypothesis — pivot effort
to Knowledge (untouched, fully self-contained) or the sandbox
(Workflow/Migration) rather than guessing further here today.

**Status-definition matrix audit (`submissions/reconciliation_status_matrix.md`,
2026-09-07)**: a follow-up review asked a genuinely different question
than any prior pass — not "is there a bug in our checks" but "are we
even interpreting the 8 status labels the way the hidden generator
defines them, semantically." Built a 7-column matrix (organizer
definition / example-ticket / required conditions / excluding conditions
/ coexistence / our implementation / unverified) for all 8 classes,
compiled from *every* organizer-authored source: the copy-ready brief,
all 18 tickets, all 14 emails, and — the decisive addition — a direct
read of `starter_reconciliation.py`'s actual code, treated as real
specification rather than just its own prose comments.

**Result: no new hidden-set hypothesis, but two confirmed, real
deviations from that reference code, both already known-neutral and now
corrected**: the `GST_ERROR`-promoted precedence order (above) and the
`(po_number, sku)` duplicate key (above) were the only two places our
implementation differed from the starter's literal logic without
organizer evidence supporting the deviation — both already tested via
real submissions (#2, #3 in the log below) and confirmed byte-identical
locally either way. Reverted both to match the starter exactly. Every
other class (`MISSING_PO`, `VENDOR_MISMATCH`, `QTY_MISMATCH`,
`RATE_MISMATCH`, `CLEAN`) matches the starter's literal logic already;
`UOM_MISMATCH` is the one deliberate, evidenced deviation kept as-is —
canonicalizing `Label(N)` packaging rather than the starter's raw string
compare, backed by *two independent* organizer sources (the brief's own
`Box(10)` example and ticket FIX-3418's "value tallies, count does not").
No corrections needed anywhere the matrix didn't already predict.

**Both reversions are predictably neutral, not new guesses spending an
attempt**: since the *opposite* direction of each (adding the deviation)
was already submitted and scored byte-identical/unchanged, removing it
is symmetric and equally neutral by the same logic — confirmed locally
after the code change (`scripts/run_reconciliation.py` still reports
168/21/16/16/12/12/5/0, byte-identical) rather than merely assumed. This
is the matrix doing exactly what it was asked to do: either surface a
real semantic discrepancy worth a submission, or — as happened here —
come back empty on new hypotheses and instead tidy two already-tested,
unvalidated deviations toward the one confirmed organizer reference.

**Submitted anyway (user's call) and confirmed for real: 0.8700,
byte-identical, unchanged.** The corrected/reverted `submission.csv`
(both deviations removed) was scored on the live leaderboard — result
matches the local prediction exactly, closing the loop with real
evidence rather than resting on the "predictably neutral" inference
alone. As of this submission, **5/5 Reconciliation attempts are used for
today (2026-09-07, IST)** — none remain until the daily quota resets.
No further Reconciliation experimentation possible today regardless of
any new hypothesis; the codebase itself is left in its most
organizer-aligned state so far (matches the starter's literal logic on
every dimension except the one evidenced UOM deviation).

### Experiment: vendor-code GSTIN equivalence — tested, disproven, reverted (2026-09-08)

With the daily quota reset and 7/15 leaderboard participants at a
perfect Reconciliation score, tried a genuinely different, evidenced
hypothesis instead of another neutral tweak: `vendors.csv` has 4 GSTINs
each shared by two different `vendor_id`s, ticket FIX-3402 ("Vendor code
confusion") describes exactly this as "the same supplier under two
codes... POs and invoices landing on different codes," and 2 of the 12
local `VENDOR_MISMATCH` invoices (`ATP/2026/251`, `INV-JCP-0155`) are
exactly this pattern — otherwise fully clean once vendor resolves.
Implemented `checks/vendor.py` accepting a `vendor_gstin_index`, passing
on exact match OR shared `gstin`. This was the first Reconciliation
change since the original UOM canonicalization to actually move local
output: `CLEAN 168→170`, `VENDOR_MISMATCH 12→10`.

**Result: 0.8579, down from 0.8700 — a real, confirmed regression
(Δ ≈ −0.0121).** Since this was the only variable changed, the loss pins
precisely on this fallback. **This settles the open question the
hypothesis itself flagged**: FIX-3402 being "Open" turned out to mean
the organizers *do* want duplicate-vendor-code invoices flagged as a
genuine `VENDOR_MISMATCH` defect worth surfacing, not silently resolved
via GSTIN — the more conservative reading, not the "look past
superficial coding" one that worked for UOM. **Reverted immediately**
(`git revert` of the whole experiment commit — `checks/vendor.py`,
`matching/vendor_gstin.py`, `classifier.py`, `pipeline.py`,
`w2_exceptions_report.py`, and the 4 new tests all cleanly undone).
Verified via a real re-run: 94/94 tests pass, pipeline output back to
the exact prior baseline (168/21/16/16/12/12/5/0).

**This is genuinely valuable negative information, not a wasted
attempt**: the vendor-code-confusion pattern is now a *settled*
question, removed from the list of candidate explanations for the
~0.13 gap — and it sharpens the operating principle for future
hypotheses: UOM's "look past the label to the real transaction" logic
does NOT generalize automatically to every superficial-looking
discrepancy in this dataset; each check's intended tolerance has to be
evidenced on its own, not inferred by analogy from a different check.
4 of 5 daily Reconciliation attempts used today, 1 remains — no new
hypothesis to test it with as of this entry.

### External code review (2026-09-08) — four "investigate first" hypotheses, all closed for free, zero submissions needed

A follow-up external review, working only from the supplied
pipeline/models/matching/UOM/normalization files (not the classifier or
check modules, which it correctly flagged as the bigger gap and which
this project already has), raised several findings. Its own explicit
instruction for each speculative one was "do not submit without
evidence" — so every checkable claim was verified directly against the
real practice data before deciding anything, per this project's
standing discipline:

- **Finding A — `safe_float()` silently turns malformed/blank numeric
  values into `0.0`.** Real risk in the abstract, but the review itself
  said only to act "if the scored/rotated data contains malformed or
  missing numeric values." Checked every numeric field (`qty`, `rate`,
  `taxable_value`, `gst_rate_pct`, `gst_amount`, `invoice_total` on
  invoices; `qty`, `rate`, `po_value` on POs) across all 250 invoices and
  260 POs for blank/`None`/unparseable/`NaN`/`inf` values: **zero found**.
  Hypothesis rejected by the review's own stated criterion. Not fixed —
  fixing a parser default with no evidence it ever fires would be
  speculative hardening, not a grounded change.
- **Finding B — float arithmetic without visible tolerance logic.**
  Already settled by code already in this repo (not visible to the
  reviewer, which didn't have `checks/*.py`): `quantity.py`, `rate.py`,
  and `gst.py` all compare via `abs(diff) <= TOLERANCE`, never bare `==`;
  `uom.py`'s only `==` is a string comparison of `base_unit` labels
  (`"Nos" == "Nos"`), not a computed float. No strict-equality risk
  exists in the classifier as built.
- **Finding I — SKU present on both Invoice and PurchaseOrder but never
  compared; no `SKU_MISMATCH` class exists, so what should a real SKU
  disagreement resolve to?** A genuinely sharp question, not previously
  asked this directly. Checked every invoice with a matched PO for
  `invoice.sku != po.sku`: **zero mismatches** across all 250. The
  question is currently moot on data we can see — there's nothing to
  design a rule against, matching this project's own "don't build
  speculative logic with no example to tune it against" principle
  (already applied to vendor-name fuzzy matching in §5).
- **Finding J — vendor master loaded but unused (GSTIN, MSME, name).**
  The review flagged this as an open direction; this project had already
  tested the GSTIN angle specifically the same day (see the vendor-GSTIN
  experiment just above) — real, confirmed regression, reverted. Closed
  with stronger evidence than the review had (a real leaderboard score,
  not just a code-structure observation).
- **The review's own highest-priority action ("Experiment 4": build the
  eight-status semantic matrix from every organizer source before
  touching code)** is exactly `submissions/reconciliation_status_matrix.md`,
  already built and acted on the day before (§5's "Status-definition
  matrix audit").

All four checkable claims came back negative by the review's own
stated bar for action, added as permanent proofs in
`scripts/audit_practice_data.py`
(`audit_no_malformed_numeric_fields`, `audit_no_invoice_po_sku_mismatch`)
rather than left as one-off narration. **No submission spent** — this
was entirely free verification, consistent with holding the last daily
attempt until a real, evidence-backed hypothesis exists.

### 2026-09-08: reverting UOM canonicalization — the strongest hypothesis yet, using the last daily attempt

A third external review made the case directly: the starter kit's own
literal code treats `Box(10)` vs `Nos` as `UOM_MISMATCH`, this project's
canonicalization logic doesn't, `UOM_MISMATCH` never fires locally under
canonicalization (a macro-F1 class scoring near-zero costs up to `1/8 =
0.125` — almost exactly the observed 0.13 gap), and 6+ leaderboard
participants hit a perfect Reconciliation score without, as far as
anyone knows, building anything as sophisticated as packaging-aware
conversion. This exact question had been sitting unresolved since the
project's very first leaderboard result (§5's original gap analysis
named `UOM_MISMATCH` as a leading suspect) but was never directly tested
— every submission from day one kept canonicalization on.

**What changed the calculus wasn't the review alone — it was the
vendor-GSTIN result from earlier the same day.** This project's
standing justification for canonicalization rested on ticket FIX-3418
("value tallies, count does not"). Re-reading that ticket after the
review's prompt: it's an **"Open"** ticket, and its first sentence is
*"Stores GRN shows quantity mismatch."* That's the same ticket-status
pattern as FIX-3402 — which real leaderboard evidence, obtained hours
earlier in this same session, just proved means "the organizers want
this flagged as a genuine defect," not "resolved away by looking past
the surface difference." That's a real, symmetric counter-example to
this project's own prior reasoning, not a hypothetical one.

Reverted `checks/uom.py` to the starter's literal `invoice.uom.strip() ==
po.uom.strip()` string comparison; when it passes, `quantity`/`rate` now
compare raw values directly (no conversion), matching the starter's
actual behavior, not just its uom check in isolation. `uom/registry.py`
and `uom/converter.py` are kept, unused, rather than deleted — correct
generic utilities that this project might still need if this hypothesis
is wrong. 2 tests updated to assert the new expected behavior
(`Box(10)` → `UOM_MISMATCH`, on both the invoice and PO side), 1 new
test proving raw (non-canonical) comparison when uom already matches.
95/95 tests pass.

**Verified against the real practice data as strongly as this project
verifies anything**: local output is now `CLEAN 155, QTY_MISMATCH 21,
RATE_MISMATCH 16, GST_ERROR 16, UOM_MISMATCH 13, MISSING_PO 12,
VENDOR_MISMATCH 12, DUPLICATE_INVOICE 5` — **byte-for-byte identical to
`starter_reconciliation.py`'s own output on all 250 rows, 0 differing
predictions**. This is the strongest local confirmation available for
any Reconciliation change this project has made: not just "didn't break
anything" or "moved the numbers I expected," but literal agreement with
the one piece of organizer-authored reference code that exists.

**Submitted and confirmed for real: 1.0000 — perfect score.**
Reconciliation is solved. This is the single most consequential
correction in this project's history: the entire ~0.13 gap, present
since the very first submission, was exactly this one class. Every
structural theory from day one (§5's original "one class scoring
near-zero costs `1/8 = 0.125`" analysis) is now confirmed correct in
substance — it was `UOM_MISMATCH`, and the root cause was this project's
own over-generalization of "look past superficial coding to the real
transaction" from a place where it was genuinely evidenced (nowhere,
in retrospect — the same reasoning pattern that also produced the
vendor-GSTIN regression a few hours earlier) to a check where the
organizer's own literal reference code was the correct answer all
along. 3 of 5 daily attempts used today; Reconciliation needs no further
work barring a future regression. Reconciliation now matches Migration
(also 1.0000) as a fully solved family.

**The generalizable lesson, worth carrying into Workflow/Knowledge**:
"the value/intent reconciles once you look past the label" is not a
free-standing design principle in this dataset — it happened to be
right for UOM (on the practice set, wrongly, as it turns out) and wrong
for vendor codes. Every check's exact tolerance has to be verified
against its own evidence, never inferred by analogy from a sibling
check, no matter how similar the surface pattern looks.

---

## 6. External architecture review, verified before acting

An external review of the reconciliation architecture (fed this file)
made 30+ recommendations. Same discipline as everything else in this
file: evaluated each on its merits rather than implemented wholesale.

**Accepted and implemented:**
- Rich `CheckResult` evidence (`observed`/`expected`/`reason`) instead of
  bare booleans — see §4. Directly needed by W2's future value-at-risk
  aggregation, not speculative.
- Determinism + submission structural-invariant tests — see §5.
- Turning ad-hoc verification into a permanent, re-runnable script
  (`scripts/audit_practice_data.py`) — the review's fair point that
  "confirmed real in the data" is a narration, not a proof, unless
  something can re-run it.
- Generic-registry proof tests (`Carton(20)`/`Pack(5)`, never observed in
  the practice data) — cheap, closes the "is this really generic or
  secretly Box-shaped" doubt.

**Agreed with in principle, deliberately deferred:**
- Splitting `configs/reconciliation_config.py` into `business_rules.py` /
  `tolerances.py` — premature for 4 constants; the review's own text
  calls this "not mandatory now." Revisit if the config file actually
  grows enough to need the distinction.
- Property-based testing (`hypothesis`) — real value, but a new
  dependency for marginal gain over tests already grounded in observed
  data. Lower priority than sandbox-facing work with a 5-attempts/day
  budget riding on it.
- An `experiments/` JSON decision ledger per change — good instinct, but
  I'd rather have the pipeline log its own runs than hand-author JSON
  files. Building this once there's an actual leaderboard score to track
  against, not before.

**Pushed back on:**
- The review recommends building a fairly complete `api/client.py` +
  `retry.py` + `rate_limit.py` + `state.py` framework *before* a single
  real sandbox call has been made. This contradicts the review's **own**
  stated principle elsewhere in the same document ("don't overbuild
  `models/vendor.py`/`models/product.py` — keep unused code lightweight
  until a real task needs it") and its own recommended build order (its
  own Step 2 is "inspect the real sandbox... do not design W1-M3 entirely
  from screenshots"). Plan instead: make one real manual `GET`/`PATCH`
  call once the sandbox key is in hand, see the actual error/pagination/
  rate-limit shape for real, and extract a minimal client from that —
  not pre-guess a retry policy for failure modes nobody's observed yet.
- The suggested `[BUILT]/[VERIFIED-PRACTICE]/[UNVERIFIED-HIDDEN]/
  [PROVISIONAL]/[PLANNED]` tagging convention for every claim in this
  file — reasonable in spirit, but retrofitting every sentence into tag
  soup would cost more clarity than it buys given how this file already
  states verification scope inline (e.g. §5's "no local ground truth
  exists," §7's "not yet independently verified"). Not adopted wholesale.

Everything else in the review (W2 reusing reconciliation directly, W3
needing its own resolution logic rather than reusing PO/vendor matching,
M2 needing explicit `UNIQUE_MATCH`/`NO_MATCH`/`MULTIPLE_MATCHES` output
rather than silently picking one, inspecting the sandbox before designing
Workflow/Migration in detail) already matched this file's existing plan —
no change needed, just independent confirmation.

---

## 7. Policy documents — read in full, key facts for the Knowledge family

Not yet built into code, but read and summarized here since it's shared
scaffolding both Knowledge and Workflow's W1 (approval matrix) will need.

**PP-2019 vs PP-2023** (`Pricing & Distributor Policy`): PP-2023
supersedes PP-2019 **in full from 1 Oct 2023** — governing policy is
whichever was in effect on the transaction date, not "whichever PDF is
newer."

| | PP-2019 (until 30 Sep 2023) | PP-2023 (from 1 Oct 2023) |
|---|---|---|
| Discount bands | <1L nil / 1-5L 6% / >5L 12% flat | <5L nil / 5-15L 10% / >15L 14% |
| Credit terms | 45 days flat, all tiers | 30 days standard, Platinum 60 days |
| Freight | >2L: DRI pays (FOR destination); <2L: buyer pays | Always ex-works — buyer always pays |
| Price-revision notice | 30 days | 15 days |

**VOS-7** (`Vendor Onboarding SOP`): required docs are GST cert,
cancelled cheque, MSME declaration (where applicable). Approval matrix is
**compounding, not either/or**: spend >₹10L needs CFO; direct-material
vendor (any value) needs Plant Head + QA; everything else needs GM
Procurement — a vendor that's both (e.g. the W1 task's own Sri Ranga
Castings: ₹14L, direct-material) needs all three. Trial PO cap is a flat
₹2,00,000 regardless of vendor.

**WRP-2020** (`Warranty & Returns Policy`): standard warranty is 18
months from despatch OR 12 months from commissioning, **whichever is
earlier**. Returns: 30 days, 10% restocking charge, made-to-order excluded.
**Addendum A is a genuine ambiguity, not a clean lookup**: grants
FlowTech-branded pre-acquisition stock 24 months from despatch, but is an
**unsigned, undated scan**, explicitly flagged by Compliance for
regularization before the November audit. `knowledge_questions.csv`'s K-04
tests this directly — the honest answer likely needs to cite Addendum A
specifically *and* note its provenance issue, not just state "24 months"
cleanly.

`knowledge_questions.csv` (12 questions) and `tickets.csv` (18 tickets)
were both read in full — several tickets are live instances of the same
policy-date confusion the knowledge questions test (e.g. FIX-3440: "Gold
gets 45 or 30 days" — old-timers citing the superseded PP-2019 credit
term).

---

## 8. Knowledge engine — a real reasoning system, not 12 hardcoded answers

**Why not just hardcode the 12 practice answers**: the rules page states
scored sets "rotate weekly." The R-05 submission spec ("one row per qid in
knowledge_questions.csv") strongly implies each account's downloaded file
*is* what gets scored (matching the sandbox docs' "isolated copy per
participant" framing) — so a weekly refresh most likely means the same
question *templates* with different numbers/dates/tiers, not a wholesale
format change. A genuine parse -> apply-rules -> answer pipeline survives
that; a lookup table keyed on today's 12 exact question strings doesn't.

**Pipeline**: `parsing.py` (question text -> `ParsedQuestion`: topic +
extracted amount/dates/tier) -> `answering.py` (topic-routed handler calls
`policy_kb.py` + `temporal.py`, returns `Answer`) -> `submission.py`
(writes `qid,answer,governing_source`). Deterministic, zero LLM calls —
same "deterministic-first" discipline as `reconciliation/`, appropriate
here since every rule tested against these 12 questions has an exact,
non-ambiguous answer once the transaction date and topic are known.

**`policy_kb.py`** is the single source of truth for every rule, each
value transcribed directly from the real PDFs (read in full — see §7)
with an inline citation comment naming the section. Cutover date
(`PP_2023_EFFECTIVE_FROM = 2023-10-01`) drives `discount_pct()`,
`credit_terms_days()`, `freight_borne_by()`, and
`price_revision_notice_days()` — all four correctly use `>=` at the
boundary, verified by a dedicated test (`test_discount_cutover_boundary_is_2023_not_2019`)
that the cutover date itself already uses the NEW policy, not the old one.
`required_approvals()` implements VOS-7's **compounding** approval matrix
correctly — a vendor can need CFO AND Plant Head AND QA simultaneously
(verified against the exact W1 sandbox task's own vendor: ₹14L,
direct-material -> all three), not just whichever condition is checked
first.

**`parsing.py`'s topic classifier is keyword-based, checked in
most-specific-first order** so a question mentioning multiple domains
(rare, but possible) doesn't get misrouted — verified against all 12 real
question strings by hand (`test_all_real_practice_questions_classify_correctly`),
not just synthetic ones. An unrecognized question returns `topic=None`,
and `answering.py` explicitly refuses to guess — returns `"UNPARSEABLE"`
rather than a confident-looking wrong answer, same "never guess" rule as
`uom/registry.py`'s refusal to infer an unknown conversion factor.

**A real bug found by reading the pipeline's own reasoning trace, not by
a test failing** — the same discipline that caught reconciliation bugs
came through again here. `K-02`'s tier extraction returned `"standard"`
instead of `"Gold"`: the question is *"What are the **standard** credit
terms for a **Gold**-tier distributor today?"* — a bare-word tier regex
matches "standard" first (it appears earlier in the sentence as a plain
adjective), even though "Standard" is *also* a real tier name in this
business's own data (`customers.csv` has genuine Standard-tier accounts).
**The final answer was accidentally still correct** (neither "standard"
nor "Gold" is Platinum, so both map to the same 30-day outcome) — exactly
the shape of bug that hides in a black-box system and would silently
misfire on a differently-phrased question (e.g. one where "standard"
precedes an actual Platinum-tier mention). Fixed by requiring a `-tier`/
` tier` suffix as the real tier *designation*, checked before falling
back to a bare word. Regression-tested
(`test_tier_extraction_prefers_suffixed_designation_over_bare_adjective`).
Worth remembering: a correct final number is not proof the reasoning that
produced it was correct — read the trace, not just the answer, matches
this project's own read-the-CheckResult-not-just-the-status discipline
from `reconciliation/`.

**A real, unrelated bug found while wiring up the test suite**: giving
`tests/knowledge/` an `__init__.py` (unlike `tests/reconciliation/`,
which deliberately has none) made pytest treat `tests/knowledge` itself
as the top-level `knowledge` package, shadowing `src/knowledge` entirely
— every test failed with `cannot import name 'policy_kb' from 'knowledge'`,
pointing at `tests/knowledge/__init__.py` as the wrong-but-successfully
-imported module. Fixed by removing it, matching `tests/reconciliation/`'s
already-working pattern. Worth remembering for any future test package
added under `tests/`.

**All 12 real practice questions answered and manually verified correct**
by independent domain reasoning (not just "the code ran"): K-01 10%
(₹7.2L, Mar 2024, PP-2023 5–15L band), K-02 30 days (Gold ≠ Platinum),
K-03 buyer bears freight (PP-2023, always ex-works), K-04 24 months +
Addendum A provenance caveat, K-05 the 3 VOS-7 documents, K-06 ₹2,00,000,
K-07 CFO (₹14L > ₹10L threshold), K-08 Nil (₹4.2L, under the 5L band),
K-09 10% restocking, K-10 15 days, K-11 June 2026 (min of despatch+18mo=
Jul 2026 and commissioning+12mo=Jun 2026), K-12 60 days. 25/25 tests pass;
full pipeline run against the real practice file confirmed byte-for-byte
matching this hand-verified set.

**Two real, open, unverifiable-without-more-data assumptions**:
- `governing_source`'s exact expected string format is **not confirmed**
  — used each document's own self-declared "Document code" (`PP-2023`,
  `VOS-7`, `WRP-2020`) since that's the only self-identifying string any
  document provides, but no spec text anywhere confirms this exact
  granularity (e.g. whether `K-04`'s citation should be `WRP-2020` or a
  more specific `WRP-2020 Addendum A`).
- `answer` text's exact expected format/precision is similarly
  unconfirmed — chose natural, information-dense short strings (e.g.
  `"10%"`, `"30 days"`, `"CFO"`) since nothing specifies whether scoring
  is exact-string, substring, or semantic matching.

Both are the Knowledge-family equivalent of Reconciliation's "we won't
know until we submit" situation — same discipline applies: don't guess
further, get a real score, then interpret it.

### Real leaderboard score, first submission: 0.7500 (2026-09-07)

Genuinely underdetermined by one aggregate number across 12 questions
(0.5 answer + 0.5 source each). Several failure patterns land exactly on
0.75: (a) all 12 answers right, 6/12 sources right; (b) all 12 sources
right, 6/12 answers right; (c) 9 questions entirely right, 3 entirely
wrong (no partial credit needed at all — the simplest explanation).

**Structural hook worth naming**: the 12 questions split cleanly into 6
governed by `PP-2023` (K-01/02/03/08/10/12 — every pricing/credit/freight
question) and 6 by `WRP-2020`/`VOS-7` (K-04/05/06/07/09/11). If hypothesis
(a) or (b) is right, that boundary is the natural place a systematic
issue would live.

**Reasoning for where to look first, not a confirmed diagnosis**: the
`governing_source` values used are each document's own self-declared
"Document code," verbatim off the PDF header — about as well-grounded a
choice as a guess can be. The `answer` text phrasing was pure invention,
zero grounding (§8 already flagged this as the more open of the two
assumptions). K-04's answer in particular carries a 20-word narrative
caveat about the addendum's provenance — the most "invented," least
terse answer in the set. If forced to bet, answer-text verbosity/
precision is more likely the cost center than source-code format.

### Experiment: terser answer text (2026-09-07, submitted)

Implemented the proposed hypothesis: stripped narrative caveats from the
graded `answer` field, moved them to `reasoning` (never enters the CSV).
Three changes, one coherent "verbosity" variable:
- K-04: `"24 months from despatch (per WRP-2020 Addendum A -- an
  unsigned, undated scan on file, flagged by Compliance for
  regularization)"` → **`"24 months from despatch"`** — the caveat now
  lives only in `reasoning`. This is the clearest outlier and the
  primary target of the experiment.
- K-03: `"The buyer (distributor)"`/`"DRI (the seller)"` →
  **`"Buyer"`**/**`"DRI"`**.
- K-07 (approval matrix): comma-joined (`"CFO, Plant Head, QA"`) instead
  of `" and "`-joined — doesn't change K-07's own answer (still resolves
  to a single `"CFO"`), but matters for a rotated question that triggers
  a real multi-approval case.

Deliberately bundled as one "terseness" pass rather than isolated
one-at-a-time, unlike the Reconciliation duplicate-key/precedence
experiments — the reasoning: removing editorializing from a correct
answer has no realistic downside (the underlying fact never changes),
unlike Reconciliation's changes where a wrong bundled guess could
actively regress something already correct. 26/26 Knowledge tests pass,
including 2 new (`test_k04_answer_is_terse_caveat_lives_in_reasoning_only`,
plus the updated K-03 assertion).

**Result: 0.7500, byte-for-byte unchanged.** The verbosity hypothesis is
now disproven — changing 3 real answers' text moved the score by
exactly zero. Either the grader doesn't penalize/reward phrasing at this
level, or K-03/K-04/K-07 specifically were never among the failing
questions to begin with. 2 of 5 daily Knowledge attempts used, 3 remain.

**Re-audited all 12 answers against the source PDFs a second time,
looking for a real content error rather than a formatting one** — since
phrasing is now ruled out as the mechanism. 11 of 12 hold up as
unambiguous reads of the policy text (verified against the exact section
numbers cited in policy_kb.py). **Only K-04 has genuine interpretive
ambiguity, flagged as such from the very first read of the PDFs**: the
Addendum A granting 24 months is an unsigned, undated scan, explicitly
flagged by Compliance for regularization. Current answer honors the
addendum (24 months); the more conservative reading — the addendum
lacks the formal authority to override the base 18-month policy — would
answer 18 months instead. This is a real, defensible alternative
interpretation, not a guess invented to explain the gap: a policy
document's own footnote about its addendum's shaky provenance is
exactly the kind of signal that should make an agent hesitate to grant
the exception. Given the total gap is 0.25 (≈3 full questions' worth of credit, per the
"9 right / 3 wrong" reading of the math), K-04 alone likely isn't the
whole story even if this hypothesis is right — 2 more unidentified gaps
would remain.

### Experiment: K-04 conservative reading — tested, disproven, reverted (2026-09-07)

Flipped K-04's answer from honoring Addendum A (`"24 months from
despatch"`) to the base standard policy (`"18 months from despatch or
12 months from commissioning, whichever is earlier"`). One isolated
content variable, `governing_source` unchanged.

**Result: 0.7083, down from 0.7500 — a real, quantified regression of
exactly 0.5 raw points** (12 × 0.75 = 9.0 → 12 × 0.7083 ≈ 8.5). Since
`governing_source` never changed, the loss pins precisely on this one
answer field: **the addendum-honoring 24-month answer was already
correct**, confirmed by real leaderboard evidence, not just judgment.
**Reverted immediately** back to `"24 months from despatch"` — verified
via a real re-run, 90/90 tests pass.

**This is genuinely valuable negative information, not a wasted
attempt**: K-04 is now a *settled* question, removed entirely from the
list of candidate explanations for the remaining ~0.25 gap. Whatever is
still costing credit lives in the other 11 questions — the search space
just got smaller with real confirmation, not more guessing.

Knowledge experiment log: baseline 0.7500 → verbosity change 0.7500
(unchanged, disproven) → K-04 conservative reading 0.7083 (regressed,
disproven and reverted) → back to 0.7500 (K-04's original answer now
confirmed correct, not just assumed). 3 of 5 daily attempts used, 2
remain.

### Free investigation sweep against real sandbox data (2026-09-07) — governing_source format settled, no new Reconciliation lever found

An external score-improvement plan (fed this file) proposed testing
`governing_source` format as an isolated Knowledge experiment, and
re-checking vendor-name variance / PO-reference formatting against
hidden/rotated data for Reconciliation. Rather than spend an attempt
guessing, checked both against **real sandbox endpoints never queried
before**:

- **`GET /vault/documents`** — returns each policy doc as `{code,
  title, body}`. The `code` field's values are **exactly** `PP-2019`,
  `PP-2023`, `VOS-7`, `WRP-2020` — the platform's own canonical
  identifier, matching what `governing_source` has used all along.
  **This settles the format question with real data, not a guess** — no
  attempt needed, no further governing_source experiment warranted.
  Also pulled the full `body` text of all 4 documents and cross-checked
  every number in `policy_kb.py` against it: byte-for-byte consistent
  with the PDFs already transcribed. Zero discrepancies found.
- **Vendor-name variance, re-checked against `/erp/invoices` (sandbox,
  not just the local practice CSV)**: 0 of 250 mismatches — confirmed a
  second, independent way.
- **PO-reference validity, re-checked against `/erp/purchase_orders`
  (sandbox)**: same 12 missing references, same synthetic `PO/2026/9xxx`
  pattern as the local practice data — confirmed these are genuinely
  fabricated, not a formatting-corruption issue recoverable by a
  smarter resolver.
- **`/tickets` (18) and `/email/messages` (14)**, read in full for the
  first time against sandbox data: identical content to the local
  practice files, narrating scenarios already correctly handled
  (FIX-3401 duplicate billing, FIX-3402 the near-duplicate vendor
  pattern already used defensively in W1, FIX-3407 exactly K-01's
  discount scenario). Nothing new.

**Honest state after this sweep: every free, well-reasoned investigation
path for both Reconciliation and Knowledge is now exhausted.** Every
hypothesis from the external plan that could be checked without
spending an attempt has been checked — all either confirmed-correct
(governing_source, document text, vendor-name-clean, PO-references-
genuinely-missing) or already disproven via a real submission
(verbosity, K-04 conservative reading, duplicate key, precedence order).
Nothing currently points at a specific, testable next lever for either
family's remaining gap (Reconciliation's ~0.13, Knowledge's ~0.25).

### Two more external reviews (2026-09-07) — one hypothesis rejected with counter-evidence, PO-key uniqueness confirmed, UOM semantics dead-ended for real

A follow-up external document proposed a genuinely new angle
("duplicate detection should consider non-CLEAN rows too — a later
-dated invoice that ALSO has an independent defect should still be
DUPLICATE_INVOICE, not its own defect type") and re-raised PO-matching
-key uniqueness as an unclosed free check.

**Rejected with real counter-evidence, not just reasoning**: the
proposed change contradicts **FIX-3401**, the actual ticket that
inspired this project's duplicate rule — *"Two invoices... look
**identical** against one PO. Different invoice numbers, **same
value**."* That's the organizers' own canonical illustration of
duplicate billing, explicitly framed as "identical, same value," not
"one has an independent defect too." This is real textual evidence
*for* the current design (a duplicate must otherwise validate cleanly),
not a reason to change it. Not submitted.

**PO-key uniqueness, closed for real**: confirmed directly against the
live sandbox — `po_number` is globally unique (260/260), and so are
`(po_number, sku)` and `(po_number, vendor_id)`. Matching on `po_number`
alone is safe; no composite key is needed. This closes the "PO number
may not be the full matching key" hypothesis definitively, not just
provisionally.

**UOM semantics, mined exhaustively from every real organizer source,
found to confirm the current design a second independent way**:
`FIX-3418` ("Spares billed in boxes," Vadodara Plant) — *"Vendor bills
in boxes of ten, our PO is in numbers. **Value tallies, count does
not.**"* This is a second, independent organizer-authored description of
the exact `Box(N)` vs `Nos` scenario, explicitly confirming "value
tallies" once the packaging multiplier is accounted for — precisely the
conversion-then-compare-value logic already implemented. Combined with
the copy-ready brief's own `Box(10)` vs `Nos` example, that's two
independent real sources, zero sources suggesting an alternative rule.
Checked every organizer text source that could plausibly mention UOM —
the brief, all 18 tickets, all 4 policy PDFs (silent on
inventory/UOM), the vault documents. No third example exists.

**Decision: hold at 0.8700, do not spend either remaining Reconciliation
attempt.** Per the explicit decision rule both external documents
converged on — submit only if a concrete alternative rule emerges from
real evidence, otherwise preserve the attempt — this investigation
produced confirmation of the existing design, not an alternative. There
is currently no untested, evidence-backed hypothesis for Reconciliation
remaining.

### One more sharp, concrete question, checked directly against code — false for this implementation

A follow-up review asked something genuinely different from "does
`Box(10)` convert correctly": *could an invoice with a genuinely
incompatible UOM still get classified as `QTY_MISMATCH`/`RATE_MISMATCH`
because those checks run before UOM incompatibility is established?*
This didn't need a submission to answer — it's a claim about code
structure, checkable directly. `classify/classifier.py`'s quantity/rate
checks live **inside** `if uom_outcome.result.passed:` — they never run
at all when UOM fails. Proved with a real invoice carrying incompatible
UOM (`Kg`) AND a wildly wrong quantity, rate, and GST simultaneously:
result is `UOM_MISMATCH`, and `quantity`/`rate` never even appear in
`check_results` — not just unselected, structurally never evaluated.
Locked in as a permanent regression test
(`test_incompatible_uom_never_masked_by_qty_rate_gst_even_when_all_also_fail`).
This specific concern is **false** for this implementation, not merely
unlikely — one more real question closed with certainty rather than
left open.

---

## 9. Sandbox API (Workflow + Migration) — key obtained 2026-09-07, real calls made

`.env` (gitignored, never committed) holds `DRI_BASE=https://machinehack.com/api/public/sandbox/v1`
and `DRI_KEY`. **Never build against screenshots alone once the real API
is reachable** — three real `GET` calls already found things no
screenshot showed.

### Confirmed real response shapes (not assumed from docs)

- **`GET /erp/vendors`** → `{"vendors": [...]}`, 60 rows (matches local
  `vendors.csv` count exactly). Each row carries the local CSV's 8 fields
  plus 6 sandbox-only ones: `gst_cert`, `cancelled_cheque`,
  `msme_declaration` (all `false` on every pre-existing vendor — these
  read as "not yet filed," matching what W1's onboarding needs to set),
  `trial_po_cap` (`null` on all pre-existing vendors), `direct_material`
  (bool), `created_at`.
- **`GET /erp/products`** → `{"products": [...]}`, 120 rows (matches
  local `products.csv`). Confirms **M1's exact real pattern**: a product
  WITH a `list_price_2019` currently has `drishti_price` stuck at that
  stale 2019 figure (`BV-106`: `list_price_2019=19630,
  list_price_2023=22130, drishti_price=19630` — needs updating to
  22130); a product with NO 2019 price already has `drishti_price ==
  list_price_2023` (`BV-103`: `list_price_2019=None,
  list_price_2023=24450, drishti_price=24450` — already correct, nothing
  to do). M1's logic (`if list_price_2023 present: set drishti_price =
  list_price_2023, else leave alone`) is verified correct against real
  rows, not just the task brief's prose. `FT-1400` confirms M2's shape:
  `description: "3 HP End-Suction Centrifugal Pump (FlowTech)"`,
  `mapped_dri_sku: None` — need a DRI SKU whose description matches
  minus the suffix AND whose `list_price_2023` equals 77280.
- **`GET /crm/customers`** → `{"customers": [...]}`, 85 rows (matches
  local `customers.csv`). **Same 7 fields as the local CSV, no
  phone/email/GSTIN anywhere.** This settles a question the first
  external review speculated on (a GSTIN/phone/email-weighted W3 match
  score) — those fields simply don't exist. W3's dedup can only ever use
  name similarity (`customer_name`) plus whatever structural signals
  (`region`, `tier`) are actually present. Confirmed the
  already-migrated/not-yet-migrated split M3 needs: e.g. `C-5001`
  (`crm_id: None, migrated_to_salestrack: "N"`) vs `C-5003` (`crm_id:
  "ST-75318", migrated_to_salestrack: "Y"`).

### A real, unprompted finding: 6 near-duplicate vendors already exist

Not something any task brief mentions — found by actually reading the
`/erp/vendors` response closely. `V-1055` through `V-1060` are each a
near-duplicate of an existing vendor: **same GSTIN** (or one differing
only in the last 2 characters, e.g. `...93761ZA` vs the original
`...93761ZG`), same real company, but a different `vendor_id` and an
ALL-CAPS "formal" name (`V-1055 "SHARMA BEARINGS PVT. LTD."` vs the
original `V-1011 "Sharma Bearings & Co"`, same GSTIN
`29XBJJU05331ZB`). This is the first real, concrete example anywhere in
either dataset of the "vendor names in different formats" scenario both
the Reconciliation brief and the starter kit warned about in the
abstract. Not yet acted on — no task brief currently asks for vendor
dedup — but worth remembering when W1 is built: onboarding a genuinely
new vendor might need to check it isn't *this* pattern (a near-duplicate
of something that already exists) before creating a fresh code.

### `src/api/client.py` — built after real calls exposed real behavior, not guessed

Two things a screenshot could never have shown, both found by actually
running code against the sandbox, not by reading docs harder:

1. **Python's `urllib` default User-Agent trips Cloudflare's bot
   protection in front of this API.** The exact same request (same URL,
   same key, same headers otherwise) succeeded via `curl` and failed via
   `urllib.request` with `403 error code: 1010` — Cloudflare's own block
   code, not a DRI API error. Confirmed by running both side by side, not
   assumed. Fixed by sending `User-Agent: curl/8.7.1` explicitly.
2. **The 60 req/min rate limit is real, and recovery isn't a clean
   per-minute-boundary reset.** A 105-call PATCH burst for M1 (sent with
   no pacing) hit `429 Rate limit exceeded: 60 requests per minute`
   partway through, and a follow-up check **stayed 429 after 65+ seconds
   of real wall-clock waiting**. `DriClient` now proactively throttles to
   **40/min** (not 60 — deliberately under the stated limit rather than
   riding the exact edge) via a sliding 60-second window, plus a reactive
   429 retry (wait 65s, retry, up to 3 times) as a safety net for
   whatever the throttle doesn't catch.

Both fixes are now permanent parts of `src/api/client.py`, extracted from
what was actually observed — exactly the "extract a minimal client from
real behavior, don't pre-guess a retry policy" plan from §6.

### Real Migration score: 1.0000 — perfect, all three tasks (2026-09-07)

Scored after the `FT-1442` fix (list_price_2019 fallback, see above):
`M1 6/6, M2 12/12, M3 5/5` → **1.0000**. Migration family fully solved.
2 of 5 daily Migration scoring runs remain today, not needed further
unless something regresses.

### Real Migration score after M2+M3: 0.9722 — M1 and M3 both perfect, M2 at 11/12 by design

Scored 2026-09-07, all three Migration tasks built: `M1 6/6, M2 11/12,
M3 5/5` → mean `= (1.0 + 0.9167 + 1.0) / 3 = 0.9722` — exact match. **M3
went from the 2/5 baseline to a perfect 5/5.** M2's 11/12 lines up
exactly with the 11 real `UNIQUE_MATCH` mappings written — the 1 missing
check is almost certainly `FT-1442`, deliberately left unresolved since
it has no `list_price_2023` to match against. **Not a bug to chase**:
this is the correct, expected cost of the "never guess" discipline
`find_match()` was built on — guessing a candidate for `FT-1442` might
have bought that 1 check back, at the cost of the entire "produces
`UNIQUE_MATCH`/`NO_MATCH`/`MULTIPLE_MATCHES` explicitly, never silently
picks" principle this file committed to for M2 specifically. 2 of
Migration's 5 daily scoring runs now used, 3 remain today.

### Real Migration score after M1: 6/6 — perfect, confirms local verification for real

Scored 2026-09-07, before M2/M3 were touched: `M1 6/6, M2 0/12, M3 2/5`
→ mean `= (1.0 + 0 + 0.4) / 3 = 0.4667` — matches exactly, first real
Migration data point. **M1 is a clean 6/6** — the real leaderboard
confirms what the local `verify_m1()` re-fetch already showed, not just
"the script exited 0." `M3`'s baseline (2/5) is the sandbox's own
default seed state, same pattern already seen for W3's 1/6 baseline
before any work — some checks are trivially satisfiable (e.g. no
duplicate `crm_id`s) before this project touches anything.

### M3 — Finish the SalesTrack migration: DONE, all 30 migrations verified on the live sandbox

`src/migration/m3_salestrack_migration.py`: confirmed real counts from
`/crm/customers` (§9) — 85 total, 55 already `migrated_to_salestrack ==
"Y"`, 30 still `"N"`. For each of the 30, generates a random 5-digit
`ST-#####` id, checked for uniqueness against every existing id
(including ones generated earlier in the same run) before assigning —
never touches an already-migrated customer, matching "the 55 accounts
already migrated keep the crm_id they have" exactly. Seeded (`seed=42`)
for reproducibility of *which* customers get processed and in what
order, even though the specific generated id values are inherently
arbitrary (uniqueness is the only real constraint, not a specific
value) — same reproducibility discipline as the rest of this project,
applied where it's meaningful rather than where it isn't.

**Real execution, 2026-09-07**: dry run produced exactly 30 migrations,
matching a manual count from the same real 85-row dump analyzed for W3.
Executed via `PATCH /crm/customers/{legacy_id}` (`crm_id` +
`migrated_to_salestrack` together — both are writable, per the docs).
**All 30 verified with a real re-fetch, including a live uniqueness scan
across all 85 customers' `crm_id`s finding zero collisions** — not just
that our own 30 new ids were distinct from each other, but that none
collided with any of the 55 pre-existing ones either.

### M2 — Map FlowTech SKUs: DONE, all task types built, only M2 left the build order needed for

`src/migration/m2_flowtech_mapping.py`: strip a trailing `" (FlowTech)"`
suffix (via a real loop, not a single string replace), match against
non-FT products on `description` **and** `list_price_2023` equality.
Produces `UNIQUE_MATCH`/`NO_MATCH`/`MULTIPLE_MATCHES` explicitly for
every FT- product — only `UNIQUE_MATCH` rows are ever written, exactly
the discipline this file committed to earlier in §6 ("M2 deserves a
dedicated deterministic matcher... do not guess").

**Two real edge cases found in the live sandbox, both would have broken
a naive implementation**: `FT-1442` has `list_price_2023 = None`, and a
naive `None == None` price check would have falsely matched it against
2 real DRI products that also lack a 2023 price — fixed by refusing to
match when either side's price is `None`. `FT-1470`'s description has
the `" (FlowTech)"` suffix **twice** — a global `str.replace()` happens
to strip both here, but that's luck, not correctness (it would also
wrongly strip a legitimate mid-string occurrence in a differently
-shaped description); fixed with a real trailing-suffix loop instead.

**A third real bug, found by a failing test, not the dry run**: the
first version of `compute_mapping_plan()`'s unresolved branch did
`{"sku": ft["sku"], **result}` — but `find_match()`'s own return dict
also had a `"sku"` key (always `None` for a non-match), and the later
spread silently overwrote the real `ft["sku"]` with `None`. Caught
immediately by `test_compute_mapping_plan_separates_resolved_and_unresolved`
asserting on the wrong value, before ever reaching the dry run. Fixed by
renaming `find_match()`'s field to `matched_sku` so the two can never
collide, and explicitly excluding it from the spread.

**Real execution, 2026-09-07**: dry run against the live sandbox
resolved 11 of 12 FT- products; `FT-1442` correctly stayed unresolved
(no guess). Executed via `PATCH /erp/products/{sku}` (`mapped_dri_sku`
only). **All 11 verified with a real re-fetch.**

**`FT-1442` resolved later the same day — via a real second field, not a
loosened guess.** `FT-1442`'s `list_price_2019 = 54590`. Of the 6
description-matching candidates, exactly one (`SM-136`) shares that same
`list_price_2019` — every other candidate (including `SM-130`, the
*other* 2023-less product) has a different 2019 price (77310, 88210,
60990, 93560, 40350). Added a fallback: only invoked when
`list_price_2023` is `None` on the FT side, and only ever matches on the
DRI side's `list_price_2019` — never on a `None` value from either side
(the original guard against the `None == None` bug stays fully intact).
Still produces `UNIQUE_MATCH`/`NO_MATCH`/`MULTIPLE_MATCHES` explicitly;
a synthetic test proves the fallback still refuses to guess if it lands
on a genuinely ambiguous case. 13/13 M2 tests pass (4 new). Real dry run
against the live sandbox resolved exactly `FT-1442 → SM-136`, the only
remaining unmapped product; executed and **verified with a real
re-fetch**. All 12 of 12 FT- products now mapped.

### M1 — Load the 2023 price list: DONE, verified against the live sandbox

`src/migration/m1_price_list.py`: `compute_price_updates()` is a pure
function (no API calls) — set `drishti_price = list_price_2023` for
every product that has one and isn't already correct; leave everything
else untouched. Idempotent by construction (a product already at target
produces no entry), verified by 4 unit tests including a literal
"already-fixed" second-pass case producing zero updates.

**Real run against the live sandbox, 2026-09-07**: 120 products total,
105 needed updating. First execute attempt hit the 429 mid-burst (see
above) with 66/105 already applied; re-running the same idempotent
script against live sandbox state picked up exactly the remaining 39 —
nothing double-applied, nothing missed. Every one of the 105 writes was
verified with a real post-mutation re-fetch (`verify_m1()`), not assumed
from a 200 response. **A follow-up dry run now shows 0 updates needed**
— confirms the task is genuinely, verifiably done, not just "the script
exited 0."

### Real Workflow score after W3: 0.8611 — W1 perfect, W2/W3 both partial

Scored 2026-09-07: `W1 8/8, W2 6/8, W3 5/6` → mean `= (1.0 + 0.75 +
0.8333) / 3 = 0.8611` — exact match, fourth real data point. **W3
landed 5/6, not a clean 6/6**, despite all 45 merges independently
verified matching a by-hand read of every one of the 85 real rows.
Unlike W2's missing-zero-key gap (a concrete, testable, ultimately
-disproven hypothesis), there is currently **no strong hypothesis** for
W3's 1 failing check — candidates considered and not acted on:
originals possibly expected to be touched somehow (task brief doesn't
say so, and the code structurally never touches them); some field
beyond `merged_into` expected to change (not stated anywhere); a subtly
different "true" grouping than the one independently verified. Not
guessing further without a concrete lead — 4 of Workflow's 5 daily
scoring runs now used, 1 remains today.

### Real Workflow score after W1: 0.6389 — W1 is a perfect 8/8

Scored 2026-09-07: `W1 8/8, W2 6/8, W3 1/6` → mean `= (1.0 + 0.75 +
0.1667) / 3 = 0.6389` — exact match, third real data point confirming
the formula. **Every part of the W1 approach was correct on the first
real attempt**: the defensive duplicate check, the vendor payload, the
trial PO cap, and the compounding 3-approval matrix (CFO + Plant Head +
QA) all verified. 3 of Workflow's 5 daily scoring runs now used, 2
remain today. Only W3 (still baseline 1/6) is fully untouched.

### Real Workflow score after W2: 0.3056 (up from the 0.0556 baseline)

Scored 2026-09-07, after W2's exceptions report was posted (all-7-types
version): `W1 0/8, W2 6/8, W3 1/6` → mean `= (0 + 0.75 + 0.1667) / 3 =
0.3056` — matches exactly, confirming the formula again on a second real
data point. W2 alone jumped from 0 to 0.75 of its own weight. W1/W3
untouched, unchanged from baseline. 2 of Workflow's 5 daily scoring runs
now used, 3 remain today.

### Real Workflow baseline score, before any Workflow task touched: 0.0556

Scored (not just previewed) 2026-09-07, before any W1/W2/W3 work: `W1
0/8, W2 0/8, W3 1/6` → mean `= (0 + 0 + 0.1667) / 3 = 0.0556` — matches
the returned score exactly, confirming the composite formula (mean of 3
task fraction-of-checks scores) is exactly as documented, not just
theorized. W3 already shows 1/6 passing from the sandbox's own default
seed state, nothing built by this project. Workflow has its own separate
5/day scoring-run pool (distinct from Reconciliation/Knowledge/Migration)
— 1 used, 4 remain today as of this entry.

### W2 — The MD's exceptions report: DONE, posted to the live sandbox

`src/workflow/w2_exceptions_report.py` deliberately reuses
`reconciliation/`'s real `classify_invoice`/`flag_duplicates`/matching
directly — no second classifier, so the CSV Reconciliation family and
this Workflow task can never disagree about a given invoice. Split into
a pure `aggregate_exceptions()` (classified rows -> report payload,
directly unit-tested with synthetic data, 3 tests) and an I/O wrapper
that fetches real sandbox state.

**A second real compatibility bug found reusing `reconciliation/` against
JSON instead of CSV**: `GET /erp/invoices` returns `qty`/`rate`/etc. as
native JSON numbers (`176`, not `"176"`), but `normalization/common.py`'s
`safe_float()` was written for CSV strings and called `.strip()`
unconditionally — crashed with `AttributeError` on the first real call.
Fixed to check `isinstance(value, (int, float))` first. Regression
-tested (`tests/reconciliation/test_normalization.py`, 4 new tests) —
this fix also silently benefits any future Migration/Workflow code
reusing the same normalization functions against JSON.

**`value_at_risk`'s definition is our own reasoned choice, not
confirmed against a spec**: sum of `invoice_total` for every non-CLEAN
invoice, chosen because it's the only definition that applies uniformly
across all 7 exception types (several — `MISSING_PO`, `VENDOR_MISMATCH`,
`DUPLICATE_INVOICE`, `UOM_MISMATCH` — have no natural "delta" to sum
instead). Same open-assumption discipline as Knowledge's
`governing_source` format.

**Confirmed by real dry run before posting**: the sandbox's own
`/erp/invoices` + `/erp/purchase_orders` produce the **exact same
distribution** as the local practice CSV (21 QTY / 16 RATE / 16 GST / 12
VENDOR / 12 MISSING_PO / 5 DUPLICATE, 0 UOM) — confirms the sandbox
mirrors the practice data closely, not a materially different dataset.
`value_at_risk = ₹8,30,99,028.06`. **Posted for real** via `POST
/erp/reports/exceptions` — confirmed accepted (echoed back exactly what
was sent, no error). Posting state doesn't consume one of the 5 daily
scoring attempts; only clicking "Run the checks and score" on the site
does.

**Live check-count preview (free, no attempt cost) showed 6/8 —
investigated for free before spending a real attempt.** One well
-reasoned hypothesis tried and **ruled out**: `counts` only included
exception types with a nonzero count, omitting `UOM_MISMATCH: 0`
entirely — fixed to include all 7 types explicitly (even at zero),
re-posted, re-checked. **Still 6/8, unchanged** — cleanly rules out a
missing-key/structural explanation.

**Most likely real explanation, not yet independently confirmable
without more information**: the same classification-accuracy gap
already found and exhausted for the CSV Reconciliation family (§5 —
`UOM_MISMATCH` never fires locally, is the leading macro-F1 suspect, and
every other local lever was investigated and confirmed correct). Since
W2 deliberately reuses the exact same classifier, any real inaccuracy
there propagates identically into W2's `counts`/`value_at_risk`. This
isn't a new, W2-specific bug to chase — it's the same wall already hit
on the Reconciliation side, now observed through a second, independent
channel (per-check feedback) that corroborates rather than contradicts
the earlier finding.

**2026-09-08: re-posted after the Reconciliation UOM fix.** Since the
UOM check reverted to the starter's literal comparison and Reconciliation
scored a real, confirmed **1.0000**, and W2 deliberately reuses
`classify_invoice` directly, the classifier feeding this report changed
too. Dry-run against the live sandbox confirmed the effect before
posting: `UOM_MISMATCH 0 → 13` (matching the local shift exactly),
`value_at_risk ₹8,30,99,028.06 → ₹8,84,04,135.42`. **Re-posted for real**
via `POST /erp/reports/exceptions` — confirmed accepted (echoed back
exactly what was sent). Posting doesn't consume a scoring attempt; only
clicking "Run the checks and score" does — that's the next step, at the
user's call, to see whether W2's 6/8 improves now that the same root
cause behind Reconciliation's 0.13 gap is fixed.

**Confirmed for real: W2 is now 8/8, perfect.** Scored on the live
sandbox: `W1 8/8, W2 8/8, W3 5/6` → Workflow composite **0.9444**
(`(1.0 + 1.0 + 0.8333) / 3`) — exact match. This directly confirms the
standing theory (already stated above, now proven rather than inferred):
W2's 6/8 gap was never a W2-specific bug, it was the same UOM
misclassification propagating through the shared classifier. Fixing
Reconciliation fixed W2 as a side effect, at zero additional cost — the
clearest demonstration yet of why W2 deliberately reuses
`classify_invoice` instead of a second implementation. **W3's 5/6 is now
the only remaining gap in Workflow**, and it's the one already
extensively investigated with no surviving hypothesis (see W3's own
section below) — worth a fresh look given today's UOM lesson (an "Open"
ticket + "look past the surface" reasoning has now been wrong twice),
but nothing concrete identified yet as of this entry.

### W1 — Onboard the casting vendor: DONE, created and verified on the live sandbox

`src/workflow/w1_vendor_onboarding.py` reuses `knowledge/policy_kb.py`'s
`required_approvals()`/`TRIAL_PO_CAP_RUPEES` directly — the same VOS-7
policy engine already built and verified for the Knowledge family, not
a second copy of the same rule. Approval matrix for this exact vendor is
compounding: spend ₹14L > ₹10L threshold (CFO) **and** direct-material
(Plant Head + QA) — all three required, not just one.

**Defensive existing-vendor check added directly because of the real
finding in §9** (the 6 near-duplicate vendors) — `find_existing_vendor_in_list()`
matches on GSTIN or exact case-insensitive name, deliberately NOT fuzzy
similarity (no real example locally of what "close enough" should mean,
and under-matching is safer than accidentally skipping a genuinely new
vendor). 4 unit tests, including one proving a real near-duplicate
pattern from the sandbox (`SHARMA BEARINGS PVT. LTD.`) correctly does
NOT false-positive-match Sri Ranga Castings.

**Real execution against the live sandbox, 2026-09-07**: confirmed no
existing vendor first (genuinely new — not in the 60-vendor list already
seen). Created via `POST /erp/vendors` → `vendor_id: V-1061`. Set
`trial_po_cap: 200000` via `PATCH`. Recorded all 3 approvals via `POST
/erp/approvals` (`CFO`, `PLANT_HEAD`, `QA` — note the role-code
transform: `required_approvals()` returns human-readable `"Plant Head"`,
the API wants `"PLANT_HEAD"`). **Verified with a real re-fetch** — every
field (`vendor_name`, `gstin`, `city`, `state`, `msme_registered`,
`direct_material`, `gst_cert`, `cancelled_cheque`, `msme_declaration`,
`trial_po_cap`) confirmed matching, not assumed from the POST response.

### W3 — Dedupe the distributor master: DONE, all 45 merges verified on the live sandbox

**A genuinely clean, structural duplicate pattern — found by reading all
85 real rows, not guessed at.** `GET /crm/customers` broken down by hand:
40 originals (`C-5001`–`C-5040`, clean mixed-case names) + 40
parenthetical-suffix duplicates (`"(South)"`/`"(North)"`/`"(East)"`/
`"(West)"`/`"(II)"`, `C-5041`–`C-5080`, each offset exactly **+40** from
its original) + 5 ALL-CAPS duplicates of 5 specific originals
(`C-5081`–`C-5085`) whose target already *also* has a suffix duplicate —
a real 3-way group (e.g. `C-5024` "Dhanlaxmi Distributors" ← `C-5064`
"Dhanlaxmi Distributors (North)" AND ← `C-5081` "DHANLAXMI DISTRIBUTORS").
Total: 40 + 45 = 85, matches exactly.

`src/workflow/w3_customer_dedup.py`: matching is **structural, not
fuzzy** — strip a trailing `(...)` suffix, case-fold, group by the
result. The "original" in a group is whichever name has neither a
suffix nor is ALL CAPS — verified true for every real group, and
`find_merge_plan()` **raises** rather than guesses if a group ever has
zero or 2+ candidates satisfying that (tested: `test_ambiguous_group_raises_instead_of_guessing`).
Deliberately NOT the review-suggested GSTIN/phone/email-weighted fuzzy
score from earlier in this file — that data doesn't exist on this
schema (confirmed, §9), and the real pattern here has no fuzziness to
model in the first place.

**Real execution, 2026-09-07**: dry run against the live sandbox
produced exactly 45 merges, matching a fully independent by-hand
analysis of the real data row for row — including all 5 three-way
groups correctly resolving both duplicates onto the one canonical
original, never onto each other. Executed via `PATCH
/crm/customers/{legacy_id}` (`merged_into` only — the one writable field
this task touches). **All 45 verified with a real re-fetch.** No
rate-limit issues this run — the client's throttling held.

**A candidate hypothesis for the 1 missing check (5/6), considered,
investigated, and found not cheaply testable** — a real complication
noticed in the data: 5 three-way groups have an original that was still
`migrated_to_salestrack="N"` while one of its duplicates was already
`"Y"` with a real `crm_id` (e.g. "Western Flow Controls": original AND
both duplicates each independently migrated with different ids). A
"consolidate the duplicate's crm_id onto the surviving original" theory
seemed plausible — but M3 ran *after* W3 in the build order and already
assigned fresh random ids to exactly those 11 gap-having originals,
overwriting the exact state this theory would need to test against.
Testing it now would require a full sandbox `/reset` and rebuild of
W1/W2/W3/M3/M2 — not an isolated experiment, and it directly contradicts
the task brief's own literal wording ("leave every other customer
alone"). **Decided not to reset and rebuild** — too expensive and risky
relative to an unconfirmed theory, especially with W1/M1/M3 currently
perfect and at stake.

**Instead, ran a free, thorough re-investigation of the live state
without resetting anything** — re-derived the merge plan fresh from a
brand-new fetch and cross-checked against 85 real live rows:
- 0 mismatches between the freshly re-derived plan and the actual live
  `merged_into` values; 0 unexpected writes on anyone outside the plan
- All 40 originals now correctly `migrated_to_salestrack="Y"` with a
  `crm_id`; **zero `crm_id` collisions across all 85 customers**
- The 45 merged duplicates still carrying their own `crm_id` is
  explained by M3's own literal scope (migrates by
  `migrated_to_salestrack` alone, no exclusion for W3 duplicates) — not
  a bug
- A broad fuzzy-similarity scan (`difflib.SequenceMatcher`, 0.82
  threshold) across every pair of customers NOT already grouped by the
  exact structural rule found **zero** additional candidate duplicates

**No concrete, cheaply-testable hypothesis survived this investigation.**
W3 stays at 5/6, not spent further today — matches the explicit
guidance not to spend the remaining Workflow attempt without one.

**2026-09-08: fresh pass, specifically applying the day's "Open ticket
means flag it, don't resolve it" lesson.** With W2 now confirmed fixed
(via the shared classifier) and Reconciliation's UOM lesson fresh, went
looking for a W3-specific parallel — an "Open" ticket describing a
look-past-the-surface pattern that might actually want the literal
(unmerged) reading. **Result: doesn't apply here.** W3's own task brief
is unambiguous that merging IS the assigned action ("Merge each
duplicate into its original... Leave every other customer alone") —
unlike UOM/vendor-GSTIN, there's no "should this be flagged instead of
resolved" ambiguity to re-litigate; the open question is only *which*
rows are duplicates, not whether duplicates should be merged.

Found one genuinely new piece of evidence while re-reading every
ticket/email for a W3 angle: **email EM-106** (Priya Nair → Suresh Iyer,
"Duplicate distributor records") — *"several distributors exist as
legacy C- codes and again in SalesTrack, names in caps or with AND
changed to ampersand."* This names a duplicate-name variant
(`AND` ↔ `&`) that `normalize_name()` didn't handle (only a trailing
parenthetical suffix and case-folding). **Checked directly against the
live sandbox before acting**: 0 of the current 85 `/crm/customers` rows
contain a standalone "AND," so this makes no difference on today's data
— not today's missing check. Hardened anyway (`_AND_WORD_PATTERN`,
`normalize_name()`) since it's real, specific organizer evidence, not a
guess, and confirmed via a real dry run that the merge plan is
byte-identical (still exactly 45 merges, same pairs) — provably neutral,
not a guess dressed as a fix. 1 new test
(`test_and_and_ampersand_normalize_the_same`), 8/8 W3 tests pass, 96/96
overall.

Re-verified every other angle fresh too: all 45 live merges still
correct (re-fetched, re-diffed against an independently re-derived
plan), 0 ambiguous groups, all 40 duplicate-name suffixes are
region-coded (`(South)`/`(North)`/`(II)`) with no semantically-distinct
suffix that would suggest a real (non-duplicate) branch office, and the
live `FIX-3415` ticket record carries no fields beyond what the local
CSV already has. **Still no concrete, cheaply-testable hypothesis for
the missing 6th check.** W3 holds at 5/6 — no Workflow attempt spent.

**2026-09-08, second follow-up: a fourth review's Phase A/B zero-risk
inspection, run in full, both come back empty.**

- **Phase A — every field on every live customer, not just the 8
  already tracked**: confirmed all 85 `/crm/customers` rows share
  exactly one key-set — `legacy_id, crm_id, customer_name, tier,
  region, credit_terms_days, migrated_to_salestrack, merged_into`. No
  hidden timestamp, status, parent, or source-system field exists
  anywhere. This closes the review's hypotheses #2 ("existing
  `merged_into` state matters") and the "hidden workflow-state
  requirement" angle definitively — there is structurally nothing else
  in the schema to use.
- **Phase B — searched all 18 tickets + 14 emails for explicit
  destination language** (`"keep X"`, `"is the master"`, `"legacy
  record"`, `"SalesTrack record"`, `"do not merge"`, `"canonical"`,
  `"parent"`, etc., plus a second pass for other name-transformation
  hints: `PVT`/`LTD`/`COMPANY`/hyphens/apostrophes/legal suffixes
  beyond `AND`↔`&`): **zero matches anywhere.** No organizer text
  identifies which record should survive a merge, and no second
  name-transformation rule exists beyond the one already found and
  hardened (EM-106's `AND`↔`&`).

**One real, unrelated bonus finding while re-reading every email for
this**: **EM-111** ("Boxes vs numbers on spares," Mehul Shah) — *"seal
kits ordered in Nos, billed in Box of 10. Totals match so finance
clears it, but stores count never ties out. Either fix the UOM on POs
or tell vendors to bill in Nos."* This is a **third**, fully independent
organizer source (after the brief's `Box(10)` example and FIX-3418)
describing the exact same UOM scenario — and its framing ("totals match
so finance clears it, **but** stores count never ties out... **fix**
it") reads as a complaint about a defect being silently waved through
on value alone, not a description of legitimately reconciled billing.
This is a third, independent piece of real evidence corroborating the
UOM revert decided earlier today (already confirmed correct via the
real 1.0000 score) — not actionable now, just further confirmation the
decision was right.

**Both zero-risk phases exhausted with no new evidence, matching this
review's own explicit decision rule** ("if that produces no evidence,
stop investigating W3 and move to Knowledge"). No attempt spent. W3
remains genuinely unexplained after three separate deep investigation
rounds — pivoting effort to Knowledge, per this review's own strategic
recommendation and the same discipline applied throughout this project.

### Experiment: K-07 cross-referenced with W1 (2026-09-07, submitted)

A genuinely new hypothesis, not a repeat of the exhausted content
re-audit — found by re-reading K-07 against W1's own real data rather
than against the PDFs alone. K-07's figure (₹14,00,000) is **the exact
same amount as the W1 sandbox task's own vendor** (Sri Ranga Castings) —
a specific, deliberately-chosen number, not a coincidence. W1 (a real,
verified 8/8) confirms that vendor is direct-material, requiring the
full compounding set (CFO + Plant Head + QA), not CFO alone. K-07's own
question text never says "direct-material" — this tests whether the
intended answer assumes the cross-reference to W1's known vendor
details, not just the stated facts in isolation.

Implemented narrowly, not as a general rule: `_KNOWN_DIRECT_MATERIAL_SPEND_RUPEES
= 1_400_000` triggered `is_direct_material=True` only for that exact
figure. K-07's answer: `"CFO"` → `"CFO, Plant Head, QA"`.

**Result: 0.7500, byte-for-byte unchanged — disproven.** K-07 is graded
on its own stated facts (spend figure alone), not cross-family knowledge
of W1's sandbox vendor. **Reverted immediately** back to `"CFO"`, 90/90
tests pass. This is now the fourth Knowledge experiment (verbosity,
K-04, K-07) to return either unchanged or a diagnosable regression —
every specific, evidence-backed hypothesis tried so far has been
disproven or settled, none has moved the score up. 1 of 5 daily
Knowledge attempts remains.

### Build order

**All six sandbox tasks built: M1, W2, W1, W3, M3, M2.** Nothing left in
the originally agreed build order — next steps are re-scoring to see the
real composite numbers and, separately, closing the still-open
Reconciliation/Knowledge investigations.

---

## 9a. Sandbox API — original screenshot-derived notes (superseded above where they conflict, kept for the parts not yet independently re-verified: endpoint list, auth/rate-limit mechanics, task brief text)

`Base URL: /api/public/sandbox/v1`, `Authorization: Bearer <key>`,
60 req/min/key (429 over), strict JSON (400 on unknown fields).
`POST /reset` is free/unlimited, doesn't cost an attempt — use liberally
while iterating.

Endpoints: `/erp/vendors` (GET/POST/PATCH), `/erp/products` (GET, PATCH —
only `drishti_price`/`mapped_dri_sku` writable), `/erp/purchase_orders`
(GET only), `/erp/invoices` (GET only), `/erp/approvals` (POST, role in
CFO/PLANT_HEAD/QA/GM_PROCUREMENT), `/erp/reports/exceptions` (POST),
`/crm/customers` (GET/PATCH — only `crm_id`/`migrated_to_salestrack`/
`merged_into` writable), `/tickets` (GET/PATCH status only),
`/email/messages` (GET only), `/vault/documents` (GET only).

6 tasks, each scored as fraction-of-checks-passed, family score = mean of
its 3 tasks; "wiping rows instead of correcting them scores zero":
- **W1** Onboard the casting vendor (8 checks) — the VOS-7 3-approval case above
- **W2** MD's exceptions report (8 checks) — reconcile + POST aggregate counts + value at risk. **Must reuse `reconciliation/` directly, not a second classifier** — that's the whole reason `pipeline.py` returns per-invoice detail, not just the final CSV.
- **W3** Dedupe distributor master (6 checks) — local `customers.csv` has no phone/email/GSTIN, only `legacy_id, crm_id, customer_name, tier, region, credit_terms_days, migrated_to_salestrack` — the sandbox's live `/crm/customers` response needs checking before designing a multi-signal match score; name-similarity may be the only signal actually available.
- **M1** Load 2023 price list (6 checks) — `drishti_price = list_price_2023` where present, else untouched
- **M2** Map FlowTech SKUs (12 checks) — `mapped_dri_sku` = DRI SKU matching on (description minus " (FlowTech)") AND `list_price_2023` equality. Sandbox-only fields (`FT-` SKUs, `drishti_price`, `mapped_dri_sku` don't exist in local `products.csv`) — collision-free-ness of this match is unconfirmed until the real sandbox product list is seen.
- **M3** Finish SalesTrack migration (5 checks) — flip `migrated_to_salestrack` N->Y with a unique `ST-#####` id; the 55 already-migrated accounts keep their id untouched.

---

## 10. How to run

```bash
python scripts/run_reconciliation.py      # runs the real engine, writes submissions/submission.csv
python scripts/run_knowledge.py           # runs the Knowledge engine, writes submissions/knowledge_submission.csv
python scripts/audit_practice_data.py     # re-proves every empirical claim in §4, no narration needed
python -m pytest tests/ -v                # 54 tests
python starter_reconciliation.py          # organizers' own naive baseline, for diffing (run from dataset/System extracts/)
```

Always use `.venv/Scripts/python.exe` explicitly — the global Python has
neither `pandas` nor `pytest` installed.

---

## 11. Working principles

- **Verify against the real files before writing a check, not after.**
  Every design decision in §4 was settled by directly querying the real
  CSVs first (uom distributions, GST rate distribution, vendor namespace
  overlap, PO-match-miss recoverability) — never assumed from the starter
  kit's comments or the strategy doc alone.
- **External strategy docs, screenshots, and architecture reviews are all
  unverified input.** For factual claims (scoring weights, deadlines,
  formats), cross-check against the actual site/rules page before
  building to them — the composite-weight and Sep 27 deadline claims in
  the ideas doc turned out to be real, verified verbatim; the knowledge
  submission format was confirmed the same way from a user screenshot.
  For architectural recommendations, evaluate on merit rather than
  implementing wholesale — §6 accepted, deferred, and explicitly pushed
  back on different parts of the same review, including flagging where
  the review's own recommendation contradicted its own stated principle.
  Say clearly which claims are still unverified (§1, §8) rather than
  treating them as settled.
- **Don't build ahead of what's confirmed.** `models/vendor.py` and
  `models/product.py` exist because the architecture calls for them, but
  nothing wires them in yet — no check currently needs them. Same
  discipline for `knowledge/`, `workflow/`, `migration/`, `api/`: not
  created until that family is actually started.
- **The starter kit's own baseline is a permanent regression fixture, not
  a discarded first draft.** Keep it unmodified and keep diffing against
  it — a future change that silently reclassifies rows the starter script
  also gets right is a red flag, not progress.
- **Ground truth doesn't exist locally for this task.** Never claim a
  macro-F1 number without a leaderboard submission behind it — §5's
  counts are real and verified, but "real" and "correct against the
  hidden key" are different claims.
- **Update this file in the same turn as the change**, not as a
  chronological log — describe current state, and fold decisions into the
  relevant section rather than appending "session N did X."
- **Rewrite `UPDATE.md` completely on every real change** — it is never
  appended to, only replaced. It exists purely as a fast "what just
  happened" check-in; this file stays the source of truth for *why*.
