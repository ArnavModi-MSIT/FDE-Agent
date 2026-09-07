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

**Reconciliation and Knowledge are both built.** Workflow/Migration are
still empty top-level siblings-to-be (`api/`, etc. per §3) — no sandbox
key yet.

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

**The one decision that actually matters: UOM-aware canonicalization,
not string comparison.** The organizers' own starter script does
`str(invoice.uom) != str(po.uom)` — a bare string mismatch. Checked the
real practice data before trusting either approach: `purchase_orders.csv`
is uom=`Nos` on all 260 rows; `vendor_invoices.csv` has 237 `Nos` and
**13 rows billed as `Box(10)`**. For every one of those 13, `invoice_qty ×
10 == po_qty` exactly, **and** `invoice_rate / 10 == po_rate` exactly
(confirmed by direct computation, not assumed) — meaning a box of 10 is
billed at 10x the per-unit rate, exactly as real packaging pricing would
work. The naive starter script therefore misclassifies all 13 as
`UOM_MISMATCH` (and would additionally hit `RATE_MISMATCH` on raw
comparison if it got that far, which it doesn't since `UOM_MISMATCH` fires
first in its elif chain) when they are genuinely `CLEAN`.

Fixed with `uom/registry.py` (regex-parses any `Label(N)` packaging
notation into a base-unit multiplier — not hardcoded to `Box`, so
`Carton(20)`/`Pack(5)` would parse identically if they appear in the
hidden set) and `uom/converter.py` (canonicalizes both qty and rate to the
base unit before any comparison). `checks/quantity.py` and
`checks/rate.py` both consume the canonicalized values, never raw
`invoice.qty`/`invoice.rate`. `checks/uom.py` itself only fires
`UOM_MISMATCH` when the unit **can't be resolved at all** (e.g. `Kg`
against a `Nos` PO) — an unrecognized unit is treated as a genuine error,
never guessed at.

**Verified empirically, not just unit-tested**: ran the full engine
against all 250 practice invoices and diffed against the starter script's
own output. Identical on every class except: **CLEAN 155 -> 168,
UOM_MISMATCH 13 -> 0** — precisely the 13 Box(10) rows, nothing else
moved. `QTY_MISMATCH` (21), `RATE_MISMATCH` (16), `GST_ERROR` (16),
`MISSING_PO` (12), `VENDOR_MISMATCH` (12), `DUPLICATE_INVOICE` (5) are
byte-identical between the two. Re-run both (`scripts/run_reconciliation.py`
and `starter_reconciliation.py`) after any future change to confirm this
still holds unless the change is deliberately meant to move one of those
numbers.

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
**`(po_number, sku)`** — not `po_number` alone — the earliest-dated
invoice stays `CLEAN`; the rest become `DUPLICATE_INVOICE`, with
`invoice_number` as a deterministic tiebreak on same-date ties. A row
that already carries a genuine defect (e.g. `RATE_MISMATCH`) is never
touched by this pass — that defect is real regardless of billing
duplication. Verified against real data: exactly 5 `po_number`s are each
billed by 2 invoices in the practice set, all 5 resolve as expected, and
all 5 also happen to share the same `sku` (see §5's leaderboard-driven
hardening for why the key includes `sku` anyway).

**Important honesty check, raised by a second external review and
correct**: `(po_number, sku)` is *my own reasonable extension*, not a
confirmed official rule. The only authoritative text on this class is the
starter kit's own comment: "multiple invoices against one PO" — it never
mentions SKU at all. The extension is defensible (a genuine duplicate
should mean the same billed line item, not merely the same PO number),
and it's provably safe (zero change to local behavior), but it is not
verified against an official spec, because no such spec text exists
beyond that one sentence. Don't treat this as settled — if the hidden
duplicate rule turns out to be pure `po_number`-only, this key is still
correct, but if it's something else entirely (e.g. matching amount too),
this hasn't ruled that out.

**Precedence (`classify/precedence.py`)**: kept as its own module,
separate from the classifier's mechanics, specifically because it's a
genuine tunable — the starter kit's own comment says reordering it moves
macro-F1, and its own confirmed prose explicitly declines to state a rule
for invoices with multiple defects. Represented as `(status, check_name)`
pairs so the classifier never hardcodes the status-to-check mapping twice.

**Current order is an active, labeled experiment, not the starter kit's
default anymore**: `MISSING_PO > VENDOR_MISMATCH > UOM_MISMATCH >
GST_ERROR > QTY_MISMATCH > RATE_MISMATCH` — `GST_ERROR` promoted above
`QTY_MISMATCH`/`RATE_MISMATCH` (one isolated swap from the starter kit's
original order). Reasoning: `gst` is the only check computed entirely
from the invoice's own fields (`taxable_value` vs `gst_amount`) — quantity
and rate both depend on comparing against an external reference (the PO),
which could plausibly tolerate legitimate real-world variance in ways an
internal arithmetic inconsistency shouldn't. **This cannot be verified
locally**: 0 of 250 practice invoices ever fail more than one check, so
no reorder — this one or any other — changes the local pipeline output at
all (confirmed: still byte-identical 168/21/16/16/12/12/5/0 after this
change). A synthetic test (`test_precedence_gst_error_outranks_quantity_mismatch`)
proves the mechanism actually took effect in code, not that the order is
correct — that can only come from a submission. See §5's experiment log.

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

---

## 9. Sandbox API (Workflow + Migration) — from user-provided screenshots, not yet independently verified

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
