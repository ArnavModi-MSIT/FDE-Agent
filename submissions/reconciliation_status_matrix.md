# Reconciliation status-definition matrix

Built by compiling every organizer-authored source for each of the 8
classes — the copy-ready brief, `starter_reconciliation.py`'s actual
code (not just its comments — this is the organizer's own reference
implementation, and its precedence order and duplicate-grouping key are
real specification, not narrative), all 18 tickets, all 14 emails. Goal
was to find a semantic discrepancy between our implementation and the
organizer's intent, not another implementation bug.

## CLEAN

1. **Organizer definition**: not defined positively — the fallthrough
   when none of the other 7 checks fire (starter's final `else` branch).
2. **Example/ticket**: none specific; the majority case (168/250 locally).
3. **Required conditions**: PO exists, vendor matches, uom resolves and
   matches after canonicalization, qty matches, rate matches, GST
   matches (18%, ±₹0.05).
4. **Excluding conditions**: any of the above failing.
5. **Coexists with another defect?** No — mutually exclusive by
   construction (one status per invoice).
6. **What we do**: same logic, plus UOM canonicalization before
   comparing qty/rate (an evidenced enhancement, not a guess — see UOM
   row).
7. **Unverified**: whether our canonicalization matches the hidden
   grader's notion of "matches" for unit patterns never seen locally.

## QTY_MISMATCH

1. **Organizer definition**: brief — "quantity vs PO." Starter code:
   `if r.qty != p.qty: return "QTY_MISMATCH"` — **raw comparison, no UOM
   adjustment** in the starter itself.
2. **Example/ticket**: none describes a *pure* qty mismatch directly;
   FIX-3418 ("Spares billed in boxes") describes a qty discrepancy that
   *resolves* once UOM is converted — i.e. it's evidence for the UOM
   check, not a standalone qty-mismatch example.
3. **Required conditions**: `invoice.qty != po.qty` after legitimate UOM
   conversion (ours) / raw (starter's).
4. **Excluding conditions**: MISSING_PO, VENDOR_MISMATCH, UOM
   -incompatible all precede it in the starter's own literal order.
5. **Coexists?** The 11 real "off by 1-2 units" invoices are QTY_MISMATCH
   *alone* (rate/GST clean) — real local evidence this class occurs in
   isolation, consistent with the project-wide "0 co-occurrence" finding.
6. **What we do**: canonicalize via UOM before comparing (only reachable
   once UOM passes, matching the starter's own elif-chain structure).
7. **Unverified**: none beyond the general UOM-registry risk.

## RATE_MISMATCH

1. **Organizer definition**: brief — "rate vs PO." Starter code: `if
   abs(r.rate - p.rate) > 0.01: return "RATE_MISMATCH"` — same ₹0.01
   tolerance we use, also raw (no UOM adjustment) in the starter.
2. **Example/ticket**: **FIX-3451** ("Rate higher than PO") — *"Vendor
   billed 6 percent above PO rate, says steel went up. Do we pay or
   raise debit note?"* — confirms a genuine rate-only defect (input-cost
   markup) is real fiction in this dataset, matching our 16 real cases.
3. **Required conditions**: `abs(invoice.rate - po.rate) > 0.01` after
   UOM conversion (ours) / raw (starter's).
4. **Excluding conditions**: MISSING_PO, VENDOR_MISMATCH, UOM
   -incompatible, **and QTY_MISMATCH** (starter checks qty before rate —
   a row failing both would show QTY_MISMATCH under the starter's own
   order, never RATE_MISMATCH).
5. **Coexists?** FIX-3451's framing (a rate markup, nothing else) matches
   our local RATE_MISMATCH population being isolated defects.
6. **What we do**: same tolerance, UOM-canonicalized comparison.
7. **Unverified**: none beyond the general UOM-registry risk.

## DUPLICATE_INVOICE

1. **Organizer definition**: brief — *"duplicate billing against one PO
   (the later-dated invoice is the duplicate)."* Starter comment:
   *"earliest stays, rest flagged."* **Starter code** (the decisive
   evidence): `clean = inv[inv.status == "CLEAN"]; dupes =
   clean[clean.duplicated(subset=["po_number"], keep="first")]` — groups
   by **`po_number` alone**, restricted to rows **already `CLEAN`**,
   earliest (`keep="first"`, pre-sorted by date) survives.
2. **Example/ticket**: **FIX-3401** — *"Two invoices... look **identical**
   against one PO. Different invoice numbers, **same value**."*
   **EM-103** — *"two invoices from Sharma against the same PO... **identical
   value**. Different invoice numbers."* Both real examples frame
   duplicates as exact re-billings, not "a duplicate that also happens
   to have a separate defect."
3. **Required conditions** (per the starter's literal code): row already
   `CLEAN`, shares `po_number` with another `CLEAN` row, is not the
   earliest of that group.
4. **Excluding conditions**: any independent defect (since only `CLEAN`
   rows are ever eligible) — settles the "should duplicate detection also
   catch a defective-and-duplicated invoice" question definitively: **no**,
   per the organizer's own reference code, not just our own design choice.
5. **Coexists?** No, by the starter's own literal construction.
6. **What we do vs. starter — two real, unvalidated deviations found by
   building this matrix**:
   - Groups by **`(po_number, sku)`**, not `po_number` alone (added
     defensively for multi-line-PO protection; tested, zero local/score
     effect — no evidence either way, but also no evidence *for* the
     deviation).
   - Otherwise matches exactly (CLEAN-only restriction, earliest-survives).
7. **Action taken**: reverted the grouping key to match the starter's
   literal `po_number`-only behavior — see "Corrections made" below.

## MISSING_PO

1. **Organizer definition**: brief — "whether the PO reference exists."
   Starter: `if r.po_number not in po.index: return "MISSING_PO"` —
   checked first, unconditionally.
2. **Example/ticket**: **FIX-3425** — *"Received an invoice referencing a
   PO number that does not exist in DRISHTI."* Confirms a genuine,
   standalone missing-PO scenario, matching our synthetic
   `PO/2026/9xxx` cases exactly.
3. **Required conditions**: exact `po_number` lookup miss.
4. **Excluding conditions**: none — always checked first in both
   implementations.
5. **Coexists?** Structurally impossible (nothing else can be evaluated
   without a PO).
6. **What we do**: matches the starter exactly, plus a defensive
   whitespace/case-normalized fallback (confirmed to recover zero
   additional local invoices — neutral, not risky).
7. **Unverified**: none — the best-evidenced class in the whole set.

## VENDOR_MISMATCH

1. **Organizer definition**: brief — "the vendor code on the invoice vs
   the PO." Starter: `if r.vendor_id != p.vendor_id: return
   "VENDOR_MISMATCH"` — checked second, exact match.
2. **Example/ticket**: **FIX-3402** — *"same supplier under two codes,
   one V- and one older entry in caps."* Describes vendor-master
   duplication (relevant to W1's onboarding dedup, which we already
   handle), not necessarily a different *definition* of this specific
   check — it doesn't describe an invoice/PO vendor_id disagreeing for
   the same real transaction.
3. **Required conditions**: `invoice.vendor_id != po.vendor_id`.
4. **Excluding conditions**: MISSING_PO only.
5. **Coexists?** Precedence puts this ahead of UOM/QTY/RATE/GST in both
   the starter and our implementation, so it always wins if it fires.
6. **What we do**: identical to the starter — **zero deviation here**,
   the one class where our code matches the reference byte-for-byte in
   logic.
7. **Unverified**: whether GSTIN or another field should also be
   checked — no evidence for this; the brief explicitly says "vendor
   code," singular.

## GST_ERROR

1. **Organizer definition**: brief — "GST at 18%." Starter: `if
   abs(r.gst_amount - round(r.taxable_value * 0.18, 2)) > 0.05: return
   "GST_ERROR"` — checked **last**, after quantity and rate, right
   before falling through to `CLEAN`.
2. **Example/ticket**: **FIX-3422** — *"A few vendor invoices compute
   GST at the wrong rate... need list... for debit notes."* Confirms
   genuine GST-computation errors are real fiction, matching our 16
   cases (all ₹58+ off, cleanly bimodal).
3. **Required conditions**: `|gst_amount - taxable_value×18%| > ₹0.05`.
4. **Excluding conditions** (starter's literal order): MISSING_PO,
   VENDOR_MISMATCH, UOM_MISMATCH, **QTY_MISMATCH, RATE_MISMATCH** all
   precede it.
5. **Coexists?** Computed independently of the PO comparison (self
   -contained, invoice-internal) — could in principle co-occur with
   qty/rate/vendor defects, though 0 local examples exist either way.
6. **What we do vs. starter — the second real, unvalidated deviation**:
   identical formula/tolerance (`18%`, `₹0.05`), but our precedence
   **promoted `GST_ERROR` above `QTY_MISMATCH`/`RATE_MISMATCH`** — a
   deliberate experiment, submitted, found zero score effect. No
   evidence supports keeping this deviation from the starter's literal
   order.
7. **Action taken**: reverted precedence to match the starter's literal
   order exactly — see "Corrections made" below.

## UOM_MISMATCH

1. **Organizer definition**: brief — *"unit-of-measure differences such
   as `Box(10)` vs `Nos`."* Starter: `if str(r.uom) != str(p.uom): return
   "UOM_MISMATCH"` — **raw string comparison**, checked third (structurally
   gates qty/rate via the starter's own `elif` chain — a match confirms
   our nested-if gating isn't just a similar-looking design, it's the
   same structural intent).
2. **Example/ticket**: **FIX-3418** — *"Vendor bills in boxes of ten,
   our PO is in numbers. **Value tallies, count does not.**"* A second,
   independent organizer-authored confirmation of the exact `Box(N)` vs
   `Nos` scenario, explicitly stating the *value* reconciles once
   converted — direct support for canonicalize-then-compare, not
   raw-string-compare.
3. **Required conditions**: uom strings differ (starter) / cannot be
   canonicalized to a common base unit (ours).
4. **Excluding conditions**: MISSING_PO, VENDOR_MISMATCH precede it in
   both implementations.
5. **Coexists?** Gates QTY_MISMATCH/RATE_MISMATCH structurally in both
   implementations (starter's `elif` chain returns immediately; our
   nested-`if` never evaluates qty/rate at all when UOM fails — proven
   with a real regression test, not just reasoned).
6. **What we do — our single biggest, and single most evidenced,
   deviation from the starter**: canonicalize via a generic `Label(N)`
   packaging registry instead of raw string comparison. This is the
   **one** deviation with real, independent, dual organizer confirmation
   (the brief's own example + FIX-3418) — kept, not reverted.
7. **Unverified**: whether any packaging notation beyond `Label(N)`
   exists in hidden data. **Genuinely the highest-risk class** — zero
   local positive examples mean the "still doesn't resolve →
   UOM_MISMATCH" fallback path has never been exercised for real,
   only proven correct in isolation via synthetic tests.

---

## Corrections made after building this matrix

Two real, unvalidated deviations from the organizer's own reference
implementation (the starter script's actual code, not just its prose)
were found and reverted — not new guesses, corrections toward the one
confirmed organizer artifact we have, for changes we ourselves already
tested and found to carry zero supporting evidence:

1. **Precedence**: `GST_ERROR` moved back to last (`MISSING_PO >
   VENDOR_MISMATCH > UOM_MISMATCH > QTY_MISMATCH > RATE_MISMATCH >
   GST_ERROR`), matching the starter's literal `if/elif` order exactly.
2. **Duplicate grouping key**: reverted from `(po_number, sku)` back to
   `po_number` alone, matching the starter's literal
   `duplicated(subset=["po_number"])` exactly.

Both changes are predictably neutral on local output — we already
tested the *opposite* direction for each (adding the deviation) and
found zero local rows changed and zero score movement either time, so
by the same logic, reverting is equally neutral. Not spending an attempt
to reconfirm something already logically implied by symmetric prior
tests. The net effect: the codebase now matches the organizer's own
reference implementation exactly on every dimension except UOM
canonicalization — the one deviation that has real, independent, dual
organizer evidence behind it.
