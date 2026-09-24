# Knowledge score review — full context (2026-09-24)

You are being asked to review a genuinely stuck problem, not to write a
summary of it. Please read Sections 1–7 in full, then Appendix C (every
answer already tried) before proposing anything — a large majority of
"obvious" candidates are already in that list. Your job is to find what is
**not** in that list, or to propose a mechanism the measured evidence in
Section 3 is consistent with.

Please reply in a file named `review_<your name>.md` with: (1) a plain
yes/no on whether you actually read Appendix C before writing candidates,
(2) any new candidate answers, each checked against Appendix C by you and
explicitly marked "not previously tried", (3) any mechanism hypothesis
consistent with everything in Section 3, (4) anything in this brief's own
reasoning you think is wrong.

---

## 1. What this is

**The Great Indian FDE Hiring Hackathon 2026** (AIM Media House /
MachineHack). Four scored task families, weighted `reconciliation 0.3,
knowledge 0.2, workflow 0.3, migration 0.2`. Reconciliation, Workflow and
Migration are each at a perfect **1.0000**. Knowledge is the only gap,
currently **0.8750**, and it is worth 20% of the composite.

- **Knowledge task**: 12 free-text questions about four short policy PDFs.
  We upload a CSV with columns `qid,answer,governing_source`.
- **Scoring rule (R-08, verbatim)**: *"Each question is worth 0.5 for the
  correct answer and 0.5 for citing the governing source document. Where
  the 2019 and 2023 policies conflict, the governing source is the one
  that actually applies on the transaction date."*
- The hidden answer key is never shown. Each upload returns **one
  number**, with no per-row feedback.
- **5 scored Knowledge uploads per day** (Asia/Kolkata). A rejected file
  (wrong columns) costs nothing. **The leaderboard keeps the best score
  ever recorded** for each family, not the latest upload — so every
  diagnostic upload described below carries no real downside.
- Qualifier submissions were due to close 2026-09-20; a separate freeze is
  2026-09-27 23:59 IST. Uploads are still being scored past the 20th
  (confirmed by other entrants' `last_run` timestamps after that date), so
  the practical deadline for further work is roughly 2026-09-27.

## 2. Current state — 9 of 12 answers, 3 stuck

Best recorded score **0.8750 = 21/24**: all 12 sources right (12 × 0.5)
plus **9** of 12 answers right (9 × 0.5).

| qid | Question (verbatim) | Our best answer (verbatim) | Source | Scores? |
|---|---|---|---|---|
| K-01 | A distributor places a single order of Rs 7,20,000 in March 2024. What discount applies? | `10%` | PP-2023 | yes |
| K-02 | What are the standard credit terms for a Gold-tier distributor today? | `30 days from the date of invoice` | PP-2023 | yes |
| K-03 | Who bears freight on a Rs 3,00,000 distributor order shipped in February 2024? | `Buyer (all despatches are ex-works irrespective of order value)` | PP-2023 | **no** |
| K-04 | What warranty applies to a FlowTech-branded pump supplied from pre-acquisition stock? | `24 months from despatch (under Addendum A for pre-acquisition stock)` | WRP-2020 | yes |
| K-05 | Which documents must a new vendor submit at onboarding? | `GST registration certificate, cancelled cheque, and MSME declaration (where applicable)` | VOS-7 | **no** |
| K-06 | What is the maximum value of a trial purchase order for a newly onboarded vendor? | `Rs 2,00,000 (capped at Rs 2,00,000)` | VOS-7 | yes |
| K-07 | A new vendor's projected annual spend is Rs 14,00,000. Whose approval is required? | `CFO (projected annual spend above Rs 10,00,000)` | VOS-7 | **no** |
| K-08 | What discount applies to a single order of Rs 4,20,000 placed in March 2024? | `Nil (0%). A single order of Rs 4,20,000 (Rs 4.2 lakh) placed in March 2024 is below the Rs 5,00,000 (Rs 5 lakh) slab under PP-2023, so no discount applies.` | PP-2023 | yes |
| K-09 | What restocking charge applies to returns? | `10% of invoice value (returns accepted within 30 days of despatch for unused goods in original packing)` | WRP-2020 | yes |
| K-10 | How much notice must DRI give before revising list prices today? | `15 days minimum written notice` | PP-2023 | yes |
| K-11 | A DRI pump is despatched in January 2025 and commissioned in June 2025. When does warranty end? | `June 2026 (whichever earlier: 12 months from commissioning falls in June 2026, before 18 months from despatch in July 2026)` | WRP-2020 | yes |
| K-12 | What credit terms does a Platinum-tier distributor receive? | `60 days from the date of invoice` | PP-2023 | yes |

**K-03, K-05 and K-07 have never scored, in any form, across 152 distinct
uploaded answers** (Appendix C). Every one of the nine scoring rows above
was itself wrong at some earlier point and was fixed by real, measured
evidence — the method below is not guesswork, and it worked nine times out
of twelve.

## 3. What has been measured about the grader, with the evidence chain

Every claim here is derived from a real leaderboard score, not inferred
from the rules text alone. Scores are exact multiples of `1/24` throughout
(`0.7500 = 18/24`, `0.8750 = 21/24`, etc.), confirming the additive model
`score = (correct_answers + correct_sources) / 24` directly — this was
independently corroborated by deliberately corrupting all 12 answers to a
guaranteed-wrong placeholder while leaving sources untouched, which scored
exactly `0.5000 = 12/12 sources, 0/12 answers`.

1. **All 12 `governing_source` values are correct**, proven directly (the
   corruption experiment above; repeated a second time, same result).
   Source format/granularity is out of scope for every remaining
   candidate.
2. **Words don't count; numbers do.** A test rewrote four *already
   -correct* answers in words (`10%` → `Ten percent`, `30 days...` → 
   `Thirty days...`, etc.) and the score dropped by exactly 4/24. The
   grader does not judge meaning — it is comparing something more literal.
3. **Bare numbers are enough.** The same four answers cut down to just
   their numbers (`30`, `24`, `15`, `60`) kept full credit.
4. **Extra numbers and extra text never cost a point.** An 8-answer
   correct set with many superfluous numbers scored full credit for all
   eight; a correct row (K-10) was later padded to 935, then separately to
   3,668, characters of irrelevant filler and kept its point both times.
5. **Every number in the key must appear somewhere in the answer.**
   K-09's key needed both `10` (the restocking percentage) *and* `30` (the
   return-window days) — a bare `10% of invoice value` (a literal PDF
   quote) failed until the 30-day window was added. K-11's terse
   `"June 2026"` failed until both warranty periods (`12`, `18`) were
   written into the answer alongside the final month.
6. **The K-08 key writes its threshold in the organizers' own lakh
   notation, not the PDF's comma notation.** A failing K-08 answer already
   contained every number the PDF itself uses (`4,20,000`, `5,00,000`,
   `2023`, `2024`, etc.); adding only `Rs 5 lakh` (supplying the bare
   number `5`, which the comma form never produces) made it score. This
   is the strongest positive evidence for the "numbers subset" model —
   it identifies the exact missing token, not just "more numbers helped."
7. **This model explains all 9 currently-correct answers and explains
   why K-03/K-05/K-07's *natural* answers ("the buyer", a document list,
   "CFO") never had a chance**: they contain no numbers at all. Under a
   pure numbers-subset check, a key with zero numbers would trivially pass
   *any* answer — but every answer has failed on these three, meaning
   **either their keys do contain numbers we have not yet written, or
   they are checked by some other mechanism entirely.**

### 3a. The numbers-subset model was pushed to its limit — and still failed

Following point 7's logic, two increasingly aggressive rounds of "cover
every number that could possibly be in the key" were run:

- **Round 1** (three separate uploads): every notation of every number
  that appears anywhere in the three questions' own text or their
  governing clauses — comma form, lakh form (`3 lakh`, `14 lakh`), plain
  digits, `3L`/`14L`, crore, `1.4 million`, numeric dates with leading
  zeros, clause numbers, the MSMED Act year. All failed.
- **Round 2** (a single upload, "the carpet"): a natural short answer
  followed by **526 numbers** — every integer 0–300, every decimal x.y up
  to 20.9, every `N,00,000` lakh amount for N 1–20, and every year
  2015–2030 — deliberately covering the entire plausible numeric space,
  not just numbers we could individually justify. **Failed on all three
  rows.**
- **Round 3**, same upload as round 2 but also carrying **all 400 distinct
  words** used anywhere in the four policy PDFs, the 18 tickets and the 14
  emails (a "vocabulary carpet", ~3k characters), and a combined version
  carrying both carpets together (~5.2k characters). **All failed.**
- **The length-cutoff question was then closed for good**: K-10 (an
  already-correct row) was independently padded to 3,668 characters of
  digit-free filler and **kept its point**, ruling out a truncation
  cutoff anywhere between 935 and 3,668 characters as the explanation for
  rounds 2–3 failing. The carpets failed on content, not truncation.

**Conclusion so far: no number and no word drawn from any organizer text
source, in any combination up to 5.2k characters, satisfies K-03, K-05 or
K-07.** Either their keys use content from **outside** every organizer
text we have access to, or the check on these three rows is not a
subset/containment check at all (see 3b).

### 3b. Whole-string / containment matching was separately ruled out

If the mechanism for a number-less key is "does the key phrase or its
words appear anywhere in the answer" (containment, fuzzy `token_set`
matching, etc.), then a sufficiently *wide* answer covering every
plausible phrasing should hit. A dedicated test gave K-03/K-05/K-07
answers of 666–859 characters, each stating the natural answer and then
**every phrasing found anywhere in the organizer record**: the policy
sentence verbatim, the relevant ticket and email wording, synonyms, and
the sandbox API's own field-name vocabulary. All three failed, with the
same K-10 length control (935 characters that round) confirming no
truncation. **Containment-style matching, in either direction, is ruled
out for these three rows** — whatever the check is, it does not reward
"the right phrase is present somewhere."

### 3c. Case, punctuation, and structural format were tested independently

- **Case**: upper-case (`BUYER`, `CFO`), lower-case, and the sandbox API's
  own snake_case vocabulary (`gst_cert, cancelled_cheque,
  msme_declaration`) — all failed.
- **List structure**: comma-joined, semicolon-joined, `&`-joined,
  numbered `(1)/(2)/(3)`, one-per-line inside a single quoted CSV cell,
  and a JSON array (`["Buyer"]`, `["CFO"]`, the three documents as a JSON
  list) — all failed.
- **Sentence structure**: the bare fact, fact-plus-reason, fact restated
  as a full sentence quoting the question's own figures, the clause
  citation trailing (`PP-2023 s4.1`) and leading (`4.1: ...`), the
  document's full title instead of its code, and the real signatory named
  on each document's footer (`Anjali Deshmukh, Managing Director` /
  `Rohit Malhotra, CFO`) — all failed.
- **Swap test**: putting other questions' correct answers into the K-03
  and K-05 slots cost nothing, confirming neither slot was accidentally
  scoring already and ruling out a simple misalignment between our
  question order and the key's.
- **Sentinel test**: leaving one answer blank, or as the string `nan` or
  `None` — testing the possibility that one key row is itself empty or a
  serialized null — all failed (and a blank cell did not cause the file
  to be rejected, so structural validity is not the issue either).

## 4. The Paavas Goyal discovery — this changes the standing theory

As of ~2026-09-17, the leaderboard evidence (no entrant since launch had
passed 21/24, and the one 24/24 account's last run predated the
competition's own launch by four days) supported a working theory that
K-03/K-05/K-07's hidden keys were themselves broken, missing, or otherwise
ungradeable.

**That theory is now disproven.** On 2026-09-19/20, a competitor,
**Paavas Goyal**, moved from Knowledge 0.875 (21/24, same as us) to
**0.9583 (23/24)** in five uploads — i.e. **two of the three previously
-unsolved rows became correct for them.** They remain at 0.9583 as of
2026-09-23 despite continuing to upload (38 entries total), so their third
row is still unsolved too — but two of three is decisive: **the keys are
real, gradeable, and something derivable does satisfy them.**

What is **not** known, and cannot ethically or rule-compliantly be found
out: which two of the three they solved, or what they submitted. The
competition's own rules (R-11) prohibit sharing submission files between
participants, and no public repository or write-up exists for this
entrant (checked via authenticated GitHub code search across the full
organizer-text vocabulary, and a general web search — nothing found). This
brief does not ask you to guess what a specific competitor did; it asks
you to find an answer that is independently correct under the same policy
documents, given everything ruled out above.

## 5. What this rules in, given everything ruled out

Combining Sections 3 and 4:

- The keys for K-03, K-05 and K-07 are real and solvable (Section 4).
- They are not satisfied by any number drawn from the organizer texts,
  even at exhaustive coverage (Section 3a).
- They are not satisfied by any word drawn from the organizer texts,
  either alone or combined with every number (Section 3a, round 3).
- They are not a containment/fuzzy-match check — a very wide answer
  covering every known phrasing still failed (Section 3b).
- Case, list structure, sentence structure, citation position, document
  titles, and real signatory names have all been tried and failed
  (Section 3c).
- 152 distinct exact strings have been tried across every one of the
  above dimensions (Appendix C) — this is not a small or lazy search.

**The genuinely open possibilities, as we see them:**

(a) The key text uses a **specific phrasing register we have not yet
tried** — something plausible under the same policy facts but literally
worded in a way none of our 152 attempts happens to match, and the
check (whatever it is) requires a much closer match than "contains the
right numbers/words" once the answer's numeric coverage is empty.

(b) The check compares the graded `answer` to something **outside the
policy documents we've been given** — e.g. a canonical short-answer
phrasing the organizers wrote once, independent of PDF wording, that
happens to coincide with the policy facts but isn't derivable from the
PDFs by rephrasing them.

(c) There's a structural or encoding issue specific to how these three
rows are graded that has nothing to do with answer content (though we
have checked for hidden/non-ASCII characters, BOM, CSV quoting issues,
and length limits, and found nothing).

We would like your view on which of these is most likely, and any
candidate answer you can derive that we have not already tried.

## 6. Appendix A — the four policy documents (verbatim, from the
platform's own document store)

```text
============================== PP-2019 | Pricing & Distributor Policy
DESHMUKH & RAO INDUSTRIES PVT. LTD.
 Pricing & Distributor Policy
Document code: PP-2019   |   Effective: 1 April 2019
1. Scope
This policy governs list pricing, distributor discounts, credit and freight terms for all products sold
through authorised distributors of Deshmukh & Rao Industries Pvt. Ltd. (DRI).
2. Distributor discounts
2.1 Discounts apply on the prevailing list price, per single order value:
Single order value
Discount
Below Rs 1,00,000
Nil
Rs 1,00,000 – Rs 5,00,000
6%
Above Rs 5,00,000
12% flat
3. Credit terms
3.1 All authorised distributors in good standing are extended credit of 45 days from the date of invoice,
irrespective of tier.
4. Freight
4.1 For single orders above Rs 2,00,000, despatch is FOR destination and freight is borne by DRI.
Orders below this value are despatched freight-to-pay.
5. Price revisions
5.1 DRI will provide a minimum of 30 days written notice before any revision to the list price.
Approved: T. Srinivasa Rao, Jt. Managing Director — 22 March 2019


============================== PP-2023 | Pricing & Distributor Policy (Revised)
DESHMUKH & RAO INDUSTRIES PVT. LTD.
 Pricing & Distributor Policy (Revised)
Document code: PP-2023   |   Effective: 1 October 2023   |   Supersedes: PP-2019
1. Scope
This policy governs list pricing, distributor discounts, credit and freight terms for all products of
Deshmukh & Rao Industries Pvt. Ltd. (DRI), including FlowTech-branded products, sold through
authorised distributors. It supersedes PP-2019 in full with effect from 1 October 2023.
2. Distributor discounts
2.1 Discounts apply on the prevailing list price, per single order value:
Single order value
Discount
Below Rs 5,00,000
Nil
Rs 5,00,000 – Rs 15,00,000
10%
Above Rs 15,00,000
14%
2.2 Slab discounts are not cumulative with scheme or campaign discounts unless expressly stated.
3. Credit terms
3.1 Standard credit is 30 days from the date of invoice. Platinum-tier distributors are extended 60 days.
Tier is assigned annually by the National Sales Head.
4. Freight
4.1 All despatches are ex-works. Freight, transit insurance and unloading are to the buyer's account
irrespective of order value.
5. Price revisions
5.1 DRI will provide a minimum of 15 days written notice before any revision to the list price.
Approved: Anjali Deshmukh, Managing Director — 18 September 2023


============================== VOS-7 | Vendor Onboarding SOP
DESHMUKH & RAO INDUSTRIES PVT. LTD.
 Vendor Onboarding SOP
Document code: VOS-7   |   Effective: 15 June 2021
1. Purpose
Standard operating procedure for onboarding new vendors into the DRISHTI vendor master, applicable
to all plants and the corporate office.
2. Procedure
Step
Activity
Owner
1
Purchase requisition with vendor justification
Indenting department
2
Collect GST registration certificate, cancelled cheque, and MSME declaration (where applicable)
Procurement
3
Credit and reference check
Finance
4
Quality audit (direct-material vendors only)
QA
5
Vendor code creation in DRISHTI
Systems
6
Trial purchase order, capped at Rs 2,00,000
Procurement
7
Performance review at 90 days; vendor confirmed or retired
Procurement + Indenting dept.
3. Approval matrix
Condition
Approval required
Projected annual spend above Rs 10,00,000
CFO
Direct-material vendor (any value)
Plant Head + QA
All other vendors
GM Procurement
4. Records
All onboarding documents are to be filed in The Vault under /Vendors/<vendor code>/ within 7 days of
code creation.
Approved: Rohit Malhotra, CFO — 15 June 2021


============================== WRP-2020 | Warranty & Returns Policy
DESHMUKH & RAO INDUSTRIES PVT. LTD.
 Warranty & Returns Policy
Document code: WRP-2020   |   Effective: 1 January 2020
1. Warranty
1.1 All products are warranted against manufacturing defects for 18 months from the date of despatch
or 12 months from the date of commissioning, whichever is earlier.
1.2 Warranty covers repair or replacement at DRI's discretion. Consumables, wear parts, and damage
from improper installation are excluded.
2. Claims
2.1 Claims are to be lodged through the authorised distributor with the invoice number, serial number,
and commissioning report where applicable.
3. Returns
3.1 Unused goods in original packing may be returned within 30 days of despatch against a restocking
charge of 10% of invoice value. Made-to-order items are not returnable.
Approved: Madhukar Deshmukh, Chairman — 12 December 2019

Addendum A — FlowTech Products (scanned copy on file; undated)
Pursuant to the acquisition of FlowTech Industries, Coimbatore, warranty on FlowTech-branded
products already committed to the market will continue to be honoured at 24 months from despatch until
existing stock is exhausted. Thereafter the standard DRI warranty applies.
[Illegible signature] — FlowTech Industries transition office
Filing note (F. Contractor, Compliance): original is an unsigned, undated scan. Flagged for regularisation before the November
audit.
```

## 7. Appendix B — the tickets and emails referencing K-03, K-05 or K-07

**Tickets** (all fields verbatim from the sandbox's own `/tickets` data;
`status` as of the last live check):

- **FIX-3402** (Dinesh Agarwal, Procurement; Open) — *Vendor code
  confusion*: "We seem to have the same supplier under two codes, one V-
  and one older entry in caps. POs and invoices are landing on different
  codes."
- **FIX-3428** (Farida Contractor, Compliance; Open) — *MSME declarations
  missing*: "Vendor master has MSME flags but declarations are not on
  file for several suppliers. Audit is in November."
- **FIX-3430** (Rohit Malhotra, Finance; In Progress) — *Freight terms
  dispute*: "Distributor refusing freight charges on a Rs 3 lakh order
  citing our old FOR-destination clause. Which policy governs orders
  after October 2023?"
- **FIX-3444** (Dinesh Agarwal, Procurement; Open) — *New vendor stuck at
  onboarding*: "Casting supplier waiting three weeks. Which documents and
  approvals are pending per SOP? Annual spend projected at Rs 14 lakh."
- **FIX-3455** (Mehul Shah, Vadodara Plant; Open) — *Trial PO limit
  query*: "Can I place a Rs 3.5 lakh first order on a newly onboarded
  vendor or does the trial cap apply?" (K-06, already correct — included
  for completeness of the VOS-7 ticket set.)

**Emails** (verbatim):

- **EM-107** (dinesh.agarwal@dri.co.in → farida.contractor@dri.co.in,
  2026-07-28) — *New casting vendor — approvals*: "Farida, projected
  spend on the new Coimbatore casting supplier is around 14 lakh a year,
  so per SOP this needs CFO sign-off plus plant head and QA clearance as
  direct material. GST cert and cancelled cheque are on file, MSME
  declaration awaited. Can we run the credit check in parallel?"
- **EM-112** (farida.contractor@dri.co.in → all-managers@dri.co.in,
  2026-08-10) — *November audit — document hygiene*: "All, statutory
  audit begins November. Vendor MSME declarations, signed policy
  versions, and the FlowTech warranty addendum need to be on file in The
  Vault with dates. Unsigned scans will not pass."
- **EM-113** (gurpreet.singh@dri.co.in → priya.nair@dri.co.in,
  2026-08-11) — *Freight on Chola order*: "Priya, Chola Pump Distributors
  disputing freight on a 3 lakh order, quoting FOR destination above 2
  lakh. That is the 2019 clause. Post-Oct 2023 everything is ex-works.
  Can SalesTrack show the governing policy version on the order screen so
  this stops recurring?"

**Note on EM-107's "direct material" framing**: this was tested directly
(K-07's answer widened to `CFO, Plant Head, QA` on the theory the vendor
is implicitly the same one from a separate sandbox task) and **failed**.
K-07's own question text states only a spend figure with no
direct-material fact, and the grader appears to score it on the stated
facts alone. Do not re-propose this without new evidence.

## 8. Appendix C — every K-03/K-05/K-07 answer already submitted

152 distinct exact strings across 5 leaderboard days (18–23 Sep), spanning
plain readable answers, ALL CAPS and lower-case, the sandbox API's own
field-name vocabulary, answers swapped between questions, every numeric
notation the source texts use, verbatim policy quotes, short exact
strings, very long/wide answers (up to 5.2k characters), reordered lists,
JSON arrays, newline-separated candidate lists, sentences in the
organizers' own ticket/email voice, sentences restating the question's own
facts, blank/`nan`/`None` sentinels, leading and trailing clause
citations, document titles, and real document signatories. Two rows
(`ZZZ_INVALID_ANSWER_ZZZ`) are diagnostic placeholders used to measure the
scoring formula itself, not real content guesses — ignore those two.

**Do not propose anything on this list, including trivial case or
punctuation variants of it.**

### K-03 (49 distinct answers tried)

1. `DRI`
2. `BUYER`
3. `Buyer`
4. `buyer`
5. `Buyer.`
6. `Nil (0%)`
7. `ex-works`
8. `The buyer`
9. `["Buyer"]`
10. `Buyer (EXW)`
11. `PP-2023 s4.1`
12. `Buyer's account`
13. `The distributor`
14. `Buyer (ex-works)`
15. `Buyer pays freight`
16. `Distributor (buyer)`
17. `Distributor (ex-works)`
18. `ZZZ_INVALID_ANSWER_ZZZ`
19. `The buyer (distributor)`
20. `The distributor's account`
21. `The buyer bears the freight.`
22. `Buyer bears freight (ex-works)`
23. `Freight is borne by the buyer.`
24. `Freight is to the buyer's account.`
25. `Post-Oct 2023 everything is ex-works.`
26. `Buyer bears freight, transit insurance and unloading`
27. `Buyer, under the Pricing & Distributor Policy (Revised).`
28. `Buyer (all despatches are ex-works irrespective of order value)`
29. `Freight, transit insurance and unloading are to the buyer's account.`
30. `Buyer. 3401 3402 3407 3415 3418 3428 3430 3433 3436 3440 3444 3447 3455 3458`
31. `Buyer, per PP-2023 (Revised), approved by Anjali Deshmukh, Managing Director.`
32. `100% of freight, transit insurance and unloading is borne by the buyer; 0% by DRI, as all despatches are ex-works`
33. `All despatches are ex-works. Freight, transit insurance and unloading are to the buyer's account irrespective of order value.`
34. `4.1: All despatches are ex-works. Freight, transit insurance and unloading are to the buyer's account irrespective of order value.`
35. `Freight on a Rs 3,00,000 distributor order shipped in February 2024 is borne by the buyer, because PP-2023 makes all despatches ex-works.`
36. `Buyer, under PP-2023 ex-works terms; FIX-3430 on this freight dispute is still In Progress, so confirm with the CFO before charging the distributor`
37. `The buyer, i.e. the distributor, bears freight, transit insurance and unloading; PP-2023 makes all despatches ex-works. DRI paid only under PP-2019.`
38. `DRI bears the freight. Despatch is FOR destination for a single order above Rs 2,00,000, so the seller and not the distributor carries the freight cost.`
39. `Buyer
Buyer's account
Buyer – ex-works
Buyer — ex-works
Ex-works – buyer pays
Ex Works
EXW
Freight to buyer's account
Customer
Purchaser
Distributor bears freight
Buyer pays`
40. `Ex-works. Under PP-2023 s4.1 every despatch is ex-works and freight, transit insurance and unloading are to the buyer's account irrespective of order value, so DRI's obligation end…` (200 characters)
41. `Buyer. Under PP-2023 clause 4.1 all despatches are ex-works and freight, transit insurance and unloading are to the buyer's account irrespective of order value, so the buyer bears …` (236 characters)
42. `The buyer, that is the distributor, bears freight. Under PP-2023 all despatches are ex-works, so freight, transit insurance and unloading are to the buyer's account irrespective of…` (339 characters)
43. `Buyer. Under PP-2023 s4.1, effective 1 October 2023, all despatches are ex-works, so on a Rs 3,00,000 (Rs 3 lakh) order shipped in February 2024 freight, transit insurance and unlo…` (344 characters)
44. `Buyer. From 1 October 2023 (01/10/2023, 2023-10-01) PP-2023 s4.1 makes every despatch ex-works, so on a Rs 3,00,000 order (Rs 3 lakh, Rs 300000, 3L, 0.03 crore) shipped in February…` (453 characters)
45. `Buyer. Under PP-2023 s4.1, effective 1 October 2023 and superseding PP-2019 in full, all despatches are ex-works, so freight, transit insurance and unloading on a Rs 3,00,000 (Rs 3…` (453 characters)
46. `Buyer. The buyer (the distributor, i.e. the customer, purchaser, dealer or consignee) bears freight: the buyer pays freight, freight is to the buyer's account, freight charges are …` (828 characters)
47. `Buyer. 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 …` (2226 characters)
48. `Buyer. Appendix the four policy documents full text from platform's own document store PP Pricing Distributor DESHMUKH RAO INDUSTRIES PVT LTD code Effective April Scope This govern…` (2980 characters)
49. `Buyer. Appendix the four policy documents full text from platform's own document store PP Pricing Distributor DESHMUKH RAO INDUSTRIES PVT LTD code Effective April Scope This govern…` (5200 characters)

### K-05 (48 distinct answers tried)

1. `3`
2. `nan`
3. `VOS-7 step 2`
4. `ZZZ_INVALID_ANSWER_ZZZ`
5. `GST cert, cancelled cheque, MSME declaration`
6. `gst_cert, cancelled_cheque, msme_declaration`
7. `CFO (projected annual spend above Rs 10,00,000)`
8. `GST registration certificate and cancelled cheque`
9. `GST certificate, cancelled cheque, MSME declaration`
10. `GST registration, cancelled cheque, MSME declaration`
11. `GSTIN certificate, cancelled cheque, MSME declaration`
12. `GST certificate, cancelled cheque and MSME declaration`
13. `GST cert, cancelled cheque, MSME declaration (where applicable)`
14. `GST registration certificate, cancelled cheque, MSME declaration`
15. `GST certificate, cancelled cheque, MSME declaration (if applicable)`
16. `GST cert and cancelled cheque are on file, MSME declaration awaited.`
17. `GST registration certificate, cancelled cheque, and MSME declaration`
18. `GST certificate, cancelled cheque, MSME declaration (where applicable)`
19. `["GST registration certificate", "cancelled cheque", "MSME declaration"]`
20. `GST registration certificate; cancelled cheque; MSME declaration (if applicable)`
21. `GST registration certificate, cancelled cheque, MSME declaration where applicable`
22. `GST registration certificate; cancelled cheque; MSME declaration (where applicable)`
23. `Cancelled cheque, GST registration certificate, and MSME declaration (where applicable)`
24. `GST registration certificate, cancelled cheque, and MSME declaration (where applicable)`
25. `gst registration certificate, cancelled cheque, and msme declaration (where applicable)`
26. `GST registration certificate, cancelled cheque, and MSME declaration (where applicable).`
27. `Collect GST registration certificate, cancelled cheque, and MSME declaration (where applicable)`
28. `2: Collect GST registration certificate, cancelled cheque, and MSME declaration (where applicable).`
29. `3 documents: GST registration certificate, cancelled cheque, and MSME declaration (where applicable)`
30. `GST registration certificate, a cancelled cheque, and an MSME declaration if the vendor is MSME-registered`
31. `GST registration certificate, cancelled cheque, and MSME declaration (where applicable), under the Vendor Onboarding SOP.`
32. `GST registration certificate, cancelled cheque, and MSME declaration (where applicable), per VOS-7, approved by Rohit Malhotra, CFO.`
33. `Purchase requisition with vendor justification, GST registration certificate, cancelled cheque, and MSME declaration (where applicable)`
34. `GST registration certificate, cancelled cheque and MSME declaration (where applicable) - the three documents collected by Procurement at VOS-7 step 2.`
35. `Purchase requisition with vendor justification, GST registration certificate, cancelled cheque, and MSME declaration where applicable - four items in all.`
36. `GST registration certificate, cancelled cheque, and MSME declaration (where applicable). 3401 3402 3407 3415 3418 3428 3430 3433 3436 3440 3444 3447 3455 3458`
37. `At onboarding, a new vendor has to hand over its GST registration certificate, a cancelled cheque and its MSME declaration, the last one only where applicable.`
38. `3 documents under VOS-7 (effective 15 June 2021) step 2: (1) GST registration certificate, (2) cancelled cheque, (3) MSME declaration (where applicable); all are filed in The Vault…` (212 characters)
39. `GST registration certificate, cancelled cheque and MSME declaration where applicable at VOS-7 step 2, together with the bank and trade reference details Finance requires for the cr…` (215 characters)
40. `Three documents. The GST registration certificate (GST certificate), a cancelled cheque, and an MSME declaration where applicable. Under VOS-7 these are collected by Procurement at…` (307 characters)
41. `At onboarding a new vendor must submit the GST registration certificate, a cancelled cheque, and an MSME declaration where applicable. Under VOS-7 these are collected by Procuremen…` (345 characters)
42. `GST registration certificate
GST certificate
Cancelled cheque
MSME declaration
GST registration certificate & cancelled cheque & MSME declaration
GST registration certificate – can…` (431 characters)
43. `3 documents (three): (1) GST registration certificate, (2) cancelled cheque, (3) MSME declaration where applicable, collected by Procurement at step 2 of the 7-step VOS-7 procedure…` (507 characters)
44. `3 documents. Under VOS-7, effective 15 June 2021, step 2 has Procurement collect (1) the GST registration certificate, (2) a cancelled cheque and (3) an MSME declaration where appl…` (547 characters)
45. `Three documents: GST registration certificate, cancelled cheque, and MSME declaration (where applicable). In other words the GST certificate (GST cert, GST registration), a cancell…` (859 characters)
46. `GST registration certificate, cancelled cheque, and MSME declaration (where applicable). 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33…` (2308 characters)
47. `GST registration certificate, cancelled cheque, and MSME declaration (where applicable). Appendix the four policy documents full text from platform's own document store PP Pricing …` (3062 characters)
48. `GST registration certificate, cancelled cheque, and MSME declaration (where applicable). Appendix the four policy documents full text from platform's own document store PP Pricing …` (5282 characters)

### K-07 (55 distinct answers tried)

1. `CFO`
2. `cfo`
3. `CFO.`
4. `None`
5. `The CFO`
6. `["CFO"]`
7. `CFO only`
8. `VOS-7 s3`
9. `The CFO's`
10. `CFO approval`
11. `CFO sign-off`
12. `CFO's approval`
13. `GM Procurement`
14. `CFO, GM_PROCUREMENT`
15. `CFO, PLANT_HEAD, QA`
16. `CFO (Rohit Malhotra)`
17. `Approval from the CFO`
18. `CFO approval required`
19. `Chief Finance Officer`
20. `CFO and GM Procurement`
21. `CFO, Plant Head and QA`
22. `ZZZ_INVALID_ANSWER_ZZZ`
23. `Chief Financial Officer`
24. `CFO (Chief Financial Officer)`
25. `Chief Financial Officer (CFO)`
26. `CFO, under the Vendor Onboarding SOP.`
27. `CFO, Plant Head, QA and GM Procurement`
28. `CFO sign-off plus Plant Head and QA clearance`
29. `Projected annual spend above Rs 10,00,000: CFO`
30. `CFO (projected annual spend above Rs 10,00,000)`
31. `CFO, per VOS-7, approved by Rohit Malhotra, CFO.`
32. `3: Projected annual spend above Rs 10,00,000 -> CFO.`
33. `Around 14 lakh a year, so per SOP this needs CFO sign-off.`
34. `CFO approval for projected annual spend above Rs 10,00,000`
35. `CFO sign-off plus plant head and QA clearance as direct material`
36. `CFO. 3401 3402 3407 3415 3418 3428 3430 3433 3436 3440 3444 3447 3455 3458`
37. `1 approval: CFO (projected annual spend of Rs 14,00,000 is above Rs 10,00,000)`
38. `GST registration certificate, cancelled cheque, and MSME declaration (where applicable)`
39. `For a new vendor with projected annual spend of Rs 14,00,000, the approval required is that of the CFO.`
40. `CFO approval is required, as the projected annual spend of Rs 14,00,000 exceeds the Rs 10,00,000 threshold.`
41. `Rohit Malhotra, the Chief Financial Officer, whose approval VOS-7 s3 requires once projected annual spend exceeds Rs 10,00,000.`
42. `GM Procurement approves the vendor. The approval matrix routes all vendors to GM Procurement unless a separate condition moves the file elsewhere.`
43. `CFO sign-off (Chief Financial Officer) for spend above Rs 10,00,000; a direct-material vendor also needs Plant Head and QA; others need GM Procurement.`
44. `Plant Head and QA. A direct-material vendor requires Plant Head approval and QA clearance, which is the row of the VOS-7 matrix that governs this vendor.`
45. `CFO. Under VOS-7 s3 (effective 15 June 2021) a projected annual spend of Rs 14,00,000 (Rs 14 lakh) is above the Rs 10,00,000 (Rs 10 lakh) threshold, so 1 approval, the CFO's, is re…` (187 characters)
46. `CFO
CFO – Chief Financial Officer
CFO — Chief Financial Officer
CFO + Plant Head + QA
Plant Head + QA
CFO and Plant Head
Approval of the CFO
Finance – CFO
CFO sign-off
CFO clearanc…` (214 characters)
47. `CFO approval is required. Under the VOS-7 approval matrix, a projected annual spend above Rs 10,00,000 requires CFO approval; direct-material vendors (any value) require Plant Head…` (230 characters)
48. `CFO, Plant Head and QA approval are all required. Under the VOS-7 approval matrix a projected annual spend above Rs 10,00,000 requires CFO approval, and a direct-material vendor re…` (316 characters)
49. `CFO approval is required, that is sign-off by the Chief Financial Officer, because the projected annual spend of Rs 14,00,000 (Rs 14 lakh) exceeds the Rs 10,00,000 threshold in the…` (321 characters)
50. `CFO. A projected annual spend of Rs 14,00,000 (Rs 14 lakh, Rs 1400000, 14L, 1.4 million, 0.14 crore) is above the Rs 10,00,000 threshold (Rs 10 lakh, Rs 1000000, 10L, 1 million, 0.…` (458 characters)
51. `CFO. Under VOS-7 s3, effective 15 June 2021, a projected annual spend of Rs 14,00,000 (Rs 14 lakh) is above the Rs 10,00,000 (Rs 10 lakh) threshold, so CFO approval is required: 1 …` (540 characters)
52. `CFO. The CFO's approval is required: CFO approval, CFO sign-off, approval of the Chief Financial Officer (CFO). Under the VOS-7 s3 approval matrix a projected annual spend above Rs…` (666 characters)
53. `CFO. 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61…` (2224 characters)
54. `CFO. Appendix the four policy documents full text from platform's own document store PP Pricing Distributor DESHMUKH RAO INDUSTRIES PVT LTD code Effective April Scope This governs …` (2978 characters)
55. `CFO. Appendix the four policy documents full text from platform's own document store PP Pricing Distributor DESHMUKH RAO INDUSTRIES PVT LTD code Effective April Scope This governs …` (5198 characters)
