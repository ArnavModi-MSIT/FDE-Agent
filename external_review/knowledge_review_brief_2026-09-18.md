# Knowledge score review — brief for an outside reviewer

*Prepared 2026-09-18. Everything you need is in this one file. Appendix A
holds the full policy documents, Appendix B the relevant tickets and emails,
and Appendix C every answer we have already submitted for the three open
questions.*

---

## 1. The prompt — read this first

You are reviewing one part of a hackathon entry: the **Knowledge** task. We
have spent dozens of scored uploads on it and are stuck at **0.8750
(9 of 12 answers right)**. Three questions — **K-03, K-05 and K-07** — have
failed with 81 different answers. We want a genuinely fresh look, not more
rewordings of what is already listed in Appendix C.

Please do four things, in this order:

1. **Audit our reasoning.** Section 5 lists what we believe we have
   measured about the grader, with the evidence for each claim. Section 7
   lists what we believe we have ruled out. Tell us plainly where an
   inference does not follow from its evidence, or where a simpler
   explanation fits the same scores.
2. **Model the grader.** List every grader design you can think of that is
   consistent with *all* the observations in Sections 5–7 at once. For each,
   say what it predicts for K-03, K-05 and K-07.
3. **Design tests.** For each design that could still let us score on the
   three questions, propose one submission that would confirm or rule it
   out, with the score you expect under each outcome. Remember we only learn
   one number per submission (Section 3).
4. **Propose candidates.** If you believe specific answer strings have a real
   chance, give at most **five per question**, ranked, each with a one-line
   reason. Check each one against Appendix C first — an exact match, or a
   match once you ignore case, spaces and punctuation, counts as already
   tried.

Be concrete and evidence-based. If you think the three questions cannot be
won by any answer, say so and explain why; that is a useful answer too.

### Rules for your proposals

- **Change only K-03, K-05 and K-07.** The other nine rows and all twelve
  `governing_source` values stay exactly as in Section 4. They are banked, and
  keeping them fixed keeps every result readable.
- **Every proposed answer must be a genuine answer to the question as
  written** — something you believe is correct under the governing policy.
  No deliberately wrong placeholders and no answers built only to read the
  hidden key.
- **Nothing that touches the scoring system other than normal uploads.** No
  probing of scoring endpoints, no scraping, no using other participants'
  files, no extra accounts. The competition rules (R-11) forbid these and the
  penalty is disqualification of the whole entry.
- **Don't propose** more ways of writing numbers for these three (Section 7
  shows three rounds already failed), more synonyms of answers already in
  Appendix C, or answering K-07 as if the vendor were direct-material (the
  question does not say so, and that was tested).

### Output format

Write your review as a markdown file named `review_<your-model-name>.md`
with these sections:

1. **Where our reasoning is wrong or weak** — each point with the evidence it
   rests on.
2. **Grader designs consistent with everything** — a table: design, what it
   predicts for the three questions, whether any answer can score under it.
3. **Proposed tests** — for each: the exact CSV rows to change, the expected
   score under each outcome, and what we learn.
4. **Candidate answers** — at most five per question, exact strings, ranked,
   each confirmed absent from Appendix C.
5. **Anything outside submissions** — for example a question worth asking
   the organizers, and its exact wording.
6. **What you would stop doing.**

---

## 2. The competition, only what matters here

- **The Great Indian FDE Hiring Hackathon 2026** (MachineHack / AIM Media
  House). A fictional manufacturer, DRI Industries, with messy legacy
  systems. Four scored task families; Knowledge is worth 20% of the
  composite.
- **Knowledge task:** 12 free-text questions about four short policy
  documents. We upload a CSV with columns `qid,answer,governing_source`.
- **Scoring rule (R-08, verbatim):** *"Each question is worth 0.5 for the
  correct answer and 0.5 for citing the governing source document. Where the
  2019 and 2023 policies conflict, the governing source is the one that
  actually applies on the transaction date."*
- The hidden answer key is never shown. Each upload returns **one number**,
  with no per-row feedback.
- Our other three families are already at 1.0000. Knowledge is the only gap:
  each extra correct answer adds 0.0417 to Knowledge and 0.83 to the
  composite (97.50 now).

## 3. Budget and constraints

- **5 scored Knowledge uploads per day** (Asia/Kolkata). A rejected file
  (wrong columns) costs nothing.
- **The leaderboard keeps the best score ever recorded.** A worse upload
  cannot lower it. Because K-03, K-05 and K-07 are proven wrong, changing
  them can only gain.
- **Qualifier submissions close 2026-09-20.** A later "freeze" date of
  2026-09-27 also appears, but it is unclear whether uploads after the 20th
  count. Plan on about **14 uploads left** (4 on the 18th, 5 each on the 19th
  and 20th).
- One upload tells us how many of the changed rows landed, not which. If
  several rows change and the score rises, we need extra uploads to find the
  winner.

## 4. The 12 questions, our best answers, and which are right

Best recorded score **0.8750 = 21/24**: all 12 sources right (12 × 0.5) plus
9 answers right (9 × 0.5).

| qid | Question (verbatim) | Our best answer (verbatim) | Source | Answer scores? |
|---|---|---|---|---|
| K-01 | A distributor places a single order of Rs 7,20,000 in March 2024. What discount applies? | 10% | PP-2023 | yes |
| K-02 | What are the standard credit terms for a Gold-tier distributor today? | 30 days from the date of invoice | PP-2023 | yes |
| K-03 | Who bears freight on a Rs 3,00,000 distributor order shipped in February 2024? | Buyer (all despatches are ex-works irrespective of order value) | PP-2023 | **no** |
| K-04 | What warranty applies to a FlowTech-branded pump supplied from pre-acquisition stock? | 24 months from despatch (under Addendum A for pre-acquisition stock) | WRP-2020 | yes |
| K-05 | Which documents must a new vendor submit at onboarding? | GST registration certificate, cancelled cheque, and MSME declaration (where applicable) | VOS-7 | **no** |
| K-06 | What is the maximum value of a trial purchase order for a newly onboarded vendor? | Rs 2,00,000 (capped at Rs 2,00,000) | VOS-7 | yes |
| K-07 | A new vendor's projected annual spend is Rs 14,00,000. Whose approval is required? | CFO (projected annual spend above Rs 10,00,000) | VOS-7 | **no** |
| K-08 | What discount applies to a single order of Rs 4,20,000 placed in March 2024? | Nil (0%). A single order of Rs 4,20,000 (Rs 4.2 lakh) placed in March 2024 is below the Rs 5,00,000 (Rs 5 lakh) slab under PP-2023, so no discount applies. | PP-2023 | yes |
| K-09 | What restocking charge applies to returns? | 10% of invoice value (returns accepted within 30 days of despatch for unused goods in original packing) | WRP-2020 | yes |
| K-10 | How much notice must DRI give before revising list prices today? | 15 days minimum written notice | PP-2023 | yes |
| K-11 | A DRI pump is despatched in January 2025 and commissioned in June 2025. When does warranty end? | June 2026 (whichever earlier: 12 months from commissioning falls in June 2026, before 18 months from despatch in July 2026) | WRP-2020 | yes |
| K-12 | What credit terms does a Platinum-tier distributor receive? | 60 days from the date of invoice | PP-2023 | yes |

## 5. What we believe we have measured about the grader

| # | Claim | Evidence |
|---|---|---|
| 1 | Score = (correct answers + correct sources) / 24, all-or-nothing per half | Every score we and the leaderboard have ever seen is a multiple of 1/24. |
| 2 | All 12 sources are right | Replacing all 12 answers with a meaningless placeholder while keeping our sources scored exactly 0.5000, twice (09-08, 09-12). |
| 3 | The wrong answers are exactly K-03, K-05, K-07 (and K-08, later fixed) | Split diagnostics on 09-10/11, plus v21, which put *other questions'* answers into K-03 and K-05 with no loss — impossible if either had been scoring. |
| 4 | **Words don't count; numbers do.** Written-out numbers fail | v27 rewrote four *correct* answers in words (`Ten percent`, `Thirty days …`) and scored 0.6667: all four lost credit. |
| 5 | **Bare numbers are enough** | v28 cut four correct answers to `30`, `24`, `15`, `60` and scored 0.8333: all four kept credit. |
| 6 | **Extra numbers and extra text don't hurt** | v8 (0.8333) carried many extra figures in correct answers; K-10 kept credit with irrelevant filler appended, and again padded to 935 characters (v39). |
| 7 | **Every number in the key must appear in the answer** | K-09: `10%` and `10% of invoice value` failed; every scoring form also contains `30` (the 30-day window). K-11: the terse `June 2026` was the one wrong answer in its group (inferred from the diagnostics, not isolated directly); the scoring form also contains `12` and `18` (the two warranty periods). |
| 8 | **The K-08 key writes its threshold in lakh** | v11's K-08 (failed) already contained 0, 4,20,000, 4.2 lakh, 5,00,000, 2023 and 2024. v33 (scores) adds only `Rs 5 lakh`. The key needs a number that `Rs 5,00,000` does not supply but `Rs 5 lakh` does. |
| 9 | The 12 scored questions are the ones in our file | A fresh download on 09-13 was byte-identical to our copy, and another entrant's copy from 08-31 matches too. |

**Our working model:** the grader pulls the numbers out of the key and
passes an answer if every one of them appears in it. That explains all nine
scoring answers. It cannot explain K-03, K-05 and K-07: their natural
answers ("the buyer", a document list, "CFO") contain no numbers. A key with
no numbers would pass *every* answer under a pure numbers check, yet every
answer fails. So those three keys must go through some **other check on
text**, and nothing we have written satisfies it.

## 6. The three open questions

**K-03** — *"Who bears freight on a Rs 3,00,000 distributor order shipped
in February 2024?"* February 2024 is after the 1 October 2023 switch, so
PP-2023 governs (source proven right). PP-2023 s4.1: *"All despatches are
ex-works. Freight, transit insurance and unloading are to the buyer's
account irrespective of order value."* → **the buyer (the distributor)**.
Organizer text agrees (EM-113, FIX-3430).

**K-05** — *"Which documents must a new vendor submit at onboarding?"*
VOS-7 step 2: *"Collect GST registration certificate, cancelled cheque, and
MSME declaration (where applicable)."* → **those three**. EM-107 uses the
shorthand "GST cert and cancelled cheque … MSME declaration awaited".

**K-07** — *"A new vendor's projected annual spend is Rs 14,00,000. Whose
approval is required?"* VOS-7 s3 matrix: spend above Rs 10,00,000 → **CFO**.
The question gives no direct-material fact, so Plant Head + QA does not
apply; the matrix's third row sends "all other vendors" to GM Procurement.
EM-107 describes a direct-material vendor at the same 14 lakh and says "CFO
sign-off plus plant head and QA clearance".

## 7. What we believe we have ruled out for K-03, K-05, K-07

| Tested | Uploads | Result |
|---|---|---|
| The natural correct answer in many readable wordings, short and long | v7–v18 | all fail |
| All-caps text and the sandbox's own codes (`BUYER`, `PLANT_HEAD`, `gst_cert`) | v20 | fail |
| Answers swapped between same-source questions (key misalignment) | v21 | fail |
| Every answer led by a number (`3 documents: …`, `1 approval: CFO …`) | v22 | fail |
| The policy sentence verbatim | v25 | fail |
| Every relevant number in every notation: comma, lakh, plain digits, `14L`, crore, million, numeric dates, clause numbers, statute years | v29, v30, v31, v34 | fail (this is how K-08 was won) |
| Short exact strings (`The buyer`, `ex-works`, `The CFO`, condensed document lists) | v35–v38 | fail |
| **Very wide answers, 666–859 characters, carrying every phrasing on record** (policy text, ticket and email wording, synonyms, codes), with K-10 padded to 935 characters as a length control | v39 | fail, and K-10 kept credit |
| The opposite party for K-03 (`DRI`) and every approver combination for K-07 | v13, v14, v15, v23 | fail |

**Our conclusion from v39:** for these three keys the grader does not look
for a phrase or set of words anywhere in the answer. It compares the whole
string against something we cannot derive, or these keys cannot be matched
by any answer. We would like this challenged.

## 8. The leaderboard (public, 2026-09-15)

- 18 entrants. **Apart from us, only one entrant has passed 20/24 since
  launch**: 0.875 (21/24), the same as our score now.
- The only 24/24 belongs to an account whose last upload was **16 Aug, four
  days before the competition opened** — most likely an organizer test
  account, possibly on an earlier key.
- The most common score among complete entries is 0.8333 (20/24), and one
  entrant reached it in two uploads. Ordinary answers land on exactly the
  eight questions whose answers contain a number.

## 9. Things we would especially like your view on

1. Is the "number-less key ⇒ separate text check" inference sound? Could a
   single rule explain both the nine scoring answers and the three failures?
2. Do the K-08 facts (Section 5, row 8) tell us anything about how the key
   file was written — for example, that keys are phrases in the organizers'
   ticket style ("5 lakh") rather than the policy's style — that would help
   guess the K-03, K-05 and K-07 keys?
3. If the text check is a whole-string comparison, is there any
   rule-compliant way to learn its normalisation (case, punctuation,
   articles) using only these three rows?
4. Is there a reading of any of the three questions under which our policy
   answer is actually wrong?

---

## Appendix A — the four policy documents (full text, from the platform's own document store)

### PP-2019 — Pricing & Distributor Policy

```text
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
```

### PP-2023 — Pricing & Distributor Policy (Revised)

```text
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
```

### VOS-7 — Vendor Onboarding SOP

```text
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
```

### WRP-2020 — Warranty & Returns Policy

```text
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

## Appendix B — relevant tickets and emails (verbatim)

**Tickets**

- **FIX-3407** (Gurpreet Singh, Sales; status Open, 2026-06-10) — *Which discount slab applies*: "Distributor quoting our 2019 policy for a Rs 7.2 lakh order. My team says the 2023 policy applies. Both PDFs are on The Vault. Need a ruling."
- **FIX-3430** (Rohit Malhotra, Finance; status In Progress, 2026-07-08) — *Freight terms dispute*: "Distributor refusing freight charges on a Rs 3 lakh order citing our old FOR-destination clause. Which policy governs orders after October 2023?"
- **FIX-3440** (Gurpreet Singh, Sales; status In Progress, 2026-07-20) — *Credit days for Gold tier*: "New joiner asking whether Gold distributors get 45 or 30 days. Old timers say 45. Policy PDF says otherwise."
- **FIX-3444** (Dinesh Agarwal, Procurement; status Open, 2026-07-24) — *New vendor stuck at onboarding*: "Casting supplier waiting three weeks. Which documents and approvals are pending per SOP? Annual spend projected at Rs 14 lakh."
- **FIX-3455** (Mehul Shah, Vadodara Plant; status Open, 2026-08-05) — *Trial PO limit query*: "Can I place a Rs 3.5 lakh first order on a newly onboarded vendor or does the trial cap apply?"
- **FIX-3428** (Farida Contractor, Compliance; status Open, 2026-07-04) — *MSME declarations missing*: "Vendor master has MSME flags but declarations are not on file for several suppliers. Audit is in November."

**Emails**

- **EM-101** (gurpreet.singh@dri.co.in → rohit.malhotra@dri.co.in, 2026-07-14) — *Discount for Marudhar Machinery — 7.2L order*: "Rohit, Marudhar has placed Rs 7,20,000 in one order and is asking for 12 percent citing the 2019 circular. My reading of the October 2023 policy is 10 percent for the 5 to 15 lakh slab. Please confirm so I can close this today."
- **EM-102** (rohit.malhotra@dri.co.in → gurpreet.singh@dri.co.in, 2026-07-14) — *RE: Discount for Marudhar Machinery — 7.2L order*: "The 2023 policy superseded 2019 from 1 October 2023. 10 percent stands. Separately, ask Suresh why the old PDF is still the first result on The Vault."
- **EM-107** (dinesh.agarwal@dri.co.in → farida.contractor@dri.co.in, 2026-07-28) — *New casting vendor — approvals*: "Farida, projected spend on the new Coimbatore casting supplier is around 14 lakh a year, so per SOP this needs CFO sign-off plus plant head and QA clearance as direct material. GST cert and cancelled cheque are on file, MSME declaration awaited. Can we run the credit check in parallel?"
- **EM-112** (farida.contractor@dri.co.in → all-managers@dri.co.in, 2026-08-10) — *November audit — document hygiene*: "All, statutory audit begins November. Vendor MSME declarations, signed policy versions, and the FlowTech warranty addendum need to be on file in The Vault with dates. Unsigned scans will not pass."
- **EM-113** (gurpreet.singh@dri.co.in → priya.nair@dri.co.in, 2026-08-11) — *Freight on Chola order*: "Priya, Chola Pump Distributors disputing freight on a 3 lakh order, quoting FOR destination above 2 lakh. That is the 2019 clause. Post-Oct 2023 everything is ex-works. Can SalesTrack show the governing policy version on the order screen so this stops recurring?"

## Appendix C — every answer already submitted for K-03, K-05 and K-07

Listed shortest first. Answers over 200 characters are shortened, with their
full length shown; nothing shorter than that is abbreviated. Treat any
proposal that matches one of these — exactly, or once case, spaces and
punctuation are ignored — as already tried.

### K-03 (freight) — 26 answers

1. `DRI`
2. `BUYER`
3. `Buyer`
4. `Nil (0%)`
5. `ex-works`
6. `The buyer`
7. `Buyer's account`
8. `The distributor`
9. `Buyer (ex-works)`
10. `Distributor (ex-works)`
11. `The buyer (distributor)`
12. `The distributor's account`
13. `Buyer bears freight, transit insurance and unloading`
14. `Buyer (all despatches are ex-works irrespective of order value)`
15. `100% of freight, transit insurance and unloading is borne by the buyer; 0% by DRI, as all despatches are ex-works`
16. `All despatches are ex-works. Freight, transit insurance and unloading are to the buyer's account irrespective of order value.`
17. `Buyer, under PP-2023 ex-works terms; FIX-3430 on this freight dispute is still In Progress, so confirm with the CFO before charging the distributor`
18. `The buyer, i.e. the distributor, bears freight, transit insurance and unloading; PP-2023 makes all despatches ex-works. DRI paid only under PP-2019.`
19. `DRI bears the freight. Despatch is FOR destination for a single order above Rs 2,00,000, so the seller and not the distributor carries the freight cost.`
20. `Ex-works. Under PP-2023 s4.1 every despatch is ex-works and freight, transit insurance and unloading are to the buyer's account irrespective of order value, so DRI's obligation ends at the works gate.`
21. `Buyer. Under PP-2023 clause 4.1 all despatches are ex-works and freight, transit insurance and unloading are to the buyer's account irrespective of order value, so the buyer bears freight on a Rs 3,00… (236 characters)`
22. `The buyer, that is the distributor, bears freight. Under PP-2023 all despatches are ex-works, so freight, transit insurance and unloading are to the buyer's account irrespective of order value. DRI do… (339 characters)`
23. `Buyer. Under PP-2023 s4.1, effective 1 October 2023, all despatches are ex-works, so on a Rs 3,00,000 (Rs 3 lakh) order shipped in February 2024 freight, transit insurance and unloading are to the buy… (344 characters)`
24. `Buyer. From 1 October 2023 (01/10/2023, 2023-10-01) PP-2023 s4.1 makes every despatch ex-works, so on a Rs 3,00,000 order (Rs 3 lakh, Rs 300000, 3L, 0.03 crore) shipped in February 2024 (02/2024, 2024… (453 characters)`
25. `Buyer. Under PP-2023 s4.1, effective 1 October 2023 and superseding PP-2019 in full, all despatches are ex-works, so freight, transit insurance and unloading on a Rs 3,00,000 (Rs 3 lakh) order shipped… (453 characters)`
26. `Buyer. The buyer (the distributor, i.e. the customer, purchaser, dealer or consignee) bears freight: the buyer pays freight, freight is to the buyer's account, freight charges are borne by the buyer a… (828 characters)`

### K-05 (documents) — 24 answers

1. `3`
2. `GST cert, cancelled cheque, MSME declaration`
3. `gst_cert, cancelled_cheque, msme_declaration`
4. `CFO (projected annual spend above Rs 10,00,000)`
5. `GST registration certificate and cancelled cheque`
6. `GST certificate, cancelled cheque, MSME declaration`
7. `GST certificate, cancelled cheque and MSME declaration`
8. `GST registration certificate, cancelled cheque, MSME declaration`
9. `GST registration certificate, cancelled cheque, and MSME declaration`
10. `GST registration certificate; cancelled cheque; MSME declaration (if applicable)`
11. `GST registration certificate, cancelled cheque, and MSME declaration (where applicable)`
12. `Collect GST registration certificate, cancelled cheque, and MSME declaration (where applicable)`
13. `3 documents: GST registration certificate, cancelled cheque, and MSME declaration (where applicable)`
14. `GST registration certificate, a cancelled cheque, and an MSME declaration if the vendor is MSME-registered`
15. `Purchase requisition with vendor justification, GST registration certificate, cancelled cheque, and MSME declaration (where applicable)`
16. `GST registration certificate, cancelled cheque and MSME declaration (where applicable) - the three documents collected by Procurement at VOS-7 step 2.`
17. `Purchase requisition with vendor justification, GST registration certificate, cancelled cheque, and MSME declaration where applicable - four items in all.`
18. `3 documents under VOS-7 (effective 15 June 2021) step 2: (1) GST registration certificate, (2) cancelled cheque, (3) MSME declaration (where applicable); all are filed in The Vault within 7 days of co… (212 characters)`
19. `GST registration certificate, cancelled cheque and MSME declaration where applicable at VOS-7 step 2, together with the bank and trade reference details Finance requires for the credit and reference c… (215 characters)`
20. `Three documents. The GST registration certificate (GST certificate), a cancelled cheque, and an MSME declaration where applicable. Under VOS-7 these are collected by Procurement at step 2 of the onboa… (307 characters)`
21. `At onboarding a new vendor must submit the GST registration certificate, a cancelled cheque, and an MSME declaration where applicable. Under VOS-7 these are collected by Procurement at step 2 of the o… (345 characters)`
22. `3 documents (three): (1) GST registration certificate, (2) cancelled cheque, (3) MSME declaration where applicable, collected by Procurement at step 2 of the 7-step VOS-7 procedure (effective 15 June… (507 characters)`
23. `3 documents. Under VOS-7, effective 15 June 2021, step 2 has Procurement collect (1) the GST registration certificate, (2) a cancelled cheque and (3) an MSME declaration where applicable. Step 1 is th… (547 characters)`
24. `Three documents: GST registration certificate, cancelled cheque, and MSME declaration (where applicable). In other words the GST certificate (GST cert, GST registration), a cancelled cheque, and an MS… (859 characters)`

### K-07 (approval) — 31 answers

1. `CFO`
2. `The CFO`
3. `The CFO's`
4. `CFO approval`
5. `CFO sign-off`
6. `CFO, GM_PROCUREMENT`
7. `CFO, PLANT_HEAD, QA`
8. `CFO approval required`
9. `CFO and GM Procurement`
10. `CFO, Plant Head and QA`
11. `Chief Financial Officer`
12. `Chief Financial Officer (CFO)`
13. `CFO, Plant Head, QA and GM Procurement`
14. `CFO sign-off plus Plant Head and QA clearance`
15. `Projected annual spend above Rs 10,00,000: CFO`
16. `CFO (projected annual spend above Rs 10,00,000)`
17. `CFO sign-off plus plant head and QA clearance as direct material`
18. `1 approval: CFO (projected annual spend of Rs 14,00,000 is above Rs 10,00,000)`
19. `GST registration certificate, cancelled cheque, and MSME declaration (where applicable)`
20. `CFO approval is required, as the projected annual spend of Rs 14,00,000 exceeds the Rs 10,00,000 threshold.`
21. `Rohit Malhotra, the Chief Financial Officer, whose approval VOS-7 s3 requires once projected annual spend exceeds Rs 10,00,000.`
22. `GM Procurement approves the vendor. The approval matrix routes all vendors to GM Procurement unless a separate condition moves the file elsewhere.`
23. `CFO sign-off (Chief Financial Officer) for spend above Rs 10,00,000; a direct-material vendor also needs Plant Head and QA; others need GM Procurement.`
24. `Plant Head and QA. A direct-material vendor requires Plant Head approval and QA clearance, which is the row of the VOS-7 matrix that governs this vendor.`
25. `CFO. Under VOS-7 s3 (effective 15 June 2021) a projected annual spend of Rs 14,00,000 (Rs 14 lakh) is above the Rs 10,00,000 (Rs 10 lakh) threshold, so 1 approval, the CFO's, is required.`
26. `CFO approval is required. Under the VOS-7 approval matrix, a projected annual spend above Rs 10,00,000 requires CFO approval; direct-material vendors (any value) require Plant Head and QA; all other v… (230 characters)`
27. `CFO, Plant Head and QA approval are all required. Under the VOS-7 approval matrix a projected annual spend above Rs 10,00,000 requires CFO approval, and a direct-material vendor requires Plant Head an… (316 characters)`
28. `CFO approval is required, that is sign-off by the Chief Financial Officer, because the projected annual spend of Rs 14,00,000 (Rs 14 lakh) exceeds the Rs 10,00,000 threshold in the VOS-7 approval matr… (321 characters)`
29. `CFO. A projected annual spend of Rs 14,00,000 (Rs 14 lakh, Rs 1400000, 14L, 1.4 million, 0.14 crore) is above the Rs 10,00,000 threshold (Rs 10 lakh, Rs 1000000, 10L, 1 million, 0.1 crore) in the VOS-… (458 characters)`
30. `CFO. Under VOS-7 s3, effective 15 June 2021, a projected annual spend of Rs 14,00,000 (Rs 14 lakh) is above the Rs 10,00,000 (Rs 10 lakh) threshold, so CFO approval is required: 1 approval on the fact… (540 characters)`
31. `CFO. The CFO's approval is required: CFO approval, CFO sign-off, approval of the Chief Financial Officer (CFO). Under the VOS-7 s3 approval matrix a projected annual spend above Rs 10,00,000 requires… (666 characters)`

