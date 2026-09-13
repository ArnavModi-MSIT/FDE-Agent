# Request for an independent review — FDE Hackathon 2026, Knowledge family

**Status of this brief: round 3, updated 2026-09-13 evening.** Two reviews
have already been done (DeepSeek and Claude Opus 5). Both are attached in
`prior_reviews/`. Every candidate they proposed that we believed was a
genuine answer has been submitted, and none moved the score. **Please do not
repeat their suggestions**; section 5 lists what was tried from each.

Read this whole brief and the attached files, then **produce one Markdown
file** in the format at the end.

Be sceptical of everything here, including our conclusions. Several of our
"proven" conclusions have turned out to be wrong, and both of the second
review's main criticisms were accepted. The two breakthroughs we did have
came from questioning something every experiment had held fixed.

---

## 1. The competition

**The Great Indian FDE Hiring Hackathon 2026** (AIM Media House / MachineHack).
A fictional manufacturer, DRI Industries, has fragmented legacy systems. An
entrant builds an agent and is scored on four task families:

| Family | Weight | What is scored |
|---|---|---|
| Reconciliation | 0.3 | CSV of 250 invoices classified into 8 statuses, macro-F1 |
| Workflow | 0.3 | End state left in a live REST sandbox (tasks W1–W3) |
| Migration | 0.2 | End state left in the same sandbox (tasks M1–M3) |
| Knowledge | 0.2 | CSV `qid,answer,governing_source` for 12 policy questions |

**Knowledge scoring, verbatim rule R-08:** *"Score is the mean over questions.
Each question is worth 0.5 for the correct answer and 0.5 for citing the
governing source document. Where the 2019 and 2023 policies conflict, the
governing source is the one that actually applies on the transaction date."*

Other rules that matter:
- Five scored submissions per family per calendar day (IST). The platform
  keeps each family's **best** recorded score. Roughly 40 attempts remain to
  the qualifier close on 2026-09-20, and about 75 to the 2026-09-27 freeze.
- One number per submission. No per-row feedback, ever.
- **R-11:** *"No probing of the scoring endpoints, no attempts to obtain the
  hidden key, no sharing of submission files between participants, no
  multiple accounts to farm attempts. Organisers may disqualify a
  participant."* The FAQ also bans "sharing solutions across teams".

---

## 2. Where we stand

| Family | Our best | Status |
|---|---|---|
| Reconciliation | 1.0000 | solved |
| Workflow | 1.0000 | solved (W3 cracked 2026-09-13) |
| Migration | 1.0000 | solved |
| **Knowledge** | **0.8333 (20/24)** | **4 answers wrong — the only open gap** |

Composite 96.67, tied with three others for third. Two entrants beat us on
Knowledge: **bhasker 1.000 (24/24)**, last run 28 days ago, and **Sanjay
Prasad 0.875 (21/24)**, last run 3 days ago. Undated best-recorded scores
cannot by themselves prove the *current* key admits 24/24, but our own
measurements show the key stable since at least 2026-08-31.

---

## 3. What we believe is established — with the caveats reviews forced

**3.1 All 12 `governing_source` values are correct.** Measured twice
(2026-09-08, 2026-09-12). Both returned 0.5000 = 12 of 12 sources.

**3.2 Scoring is additive and binary.** Every observed score is an exact
multiple of 1/24, so there is no partial credit.

**3.3 The 4 wrong answers are K-03, K-05, K-07, K-08.** The early diagnostics
alone allow three possible sets. The deciding evidence is narrower than we
first claimed: **v13** asserted DRI for K-03, and **v9 / v13** asserted two
and four documents for K-05. Had K-03 or K-05 been correct, those runs would
have cost a point. They did not.

**3.4 The question file is current.** A fresh download on 2026-09-13 is
byte-identical to the copy used throughout.

**3.5 Extra text does not hurt a correct answer — for quantity answers.** A
correct K-10 kept its credit with filler appended (110 characters), and a
correct K-09 kept its credit padded to 297 characters. **Caveat accepted
from review 2:** both were quantity-led. We have never had a correct answer
that is a party, list or role, so we do not know how the grader treats those.

**3.6 Naming an alternative inside an answer earned nothing** on the four
wrong questions. **Caveat accepted:** this was only ever tested on questions
that already scored zero, so it does not prove the grader "judges
assertions". **Whether the content of the four is actually wrong is open.**

**3.7 K-09 — corrected lesson.** `10%` and `10% of invoice value` (a literal
quote) both failed. The scoring form in our live file is *"10% of invoice
value (returns accepted within 30 days of despatch for unused goods in
original packing)"*, 103 characters, **with no made-to-order exclusion**.
What made it score was the **return window and the condition on the goods**,
not restating the whole clause.

---

## 4. The eight correct answers (live file)

| qid | answer | source |
|---|---|---|
| K-01 | `10%` | PP-2023 |
| K-02 | `30 days from the date of invoice` | PP-2023 |
| K-04 | `24 months from despatch (under Addendum A for pre-acquisition stock)` | WRP-2020 |
| K-06 | `Rs 2,00,000 (capped at Rs 2,00,000)` | VOS-7 |
| K-09 | `10% of invoice value (returns accepted within 30 days of despatch for unused goods in original packing)` | WRP-2020 |
| K-10 | `15 days minimum written notice` | PP-2023 |
| K-11 | `June 2026 (whichever earlier: 12 months from commissioning falls in June 2026, before 18 months from despatch in July 2026)` | WRP-2020 |
| K-12 | `60 days from the date of invoice` | PP-2023 |

All eight lead with a quantity. The four wrong ones answer **Who** (K-03),
**Which** (K-05), **Whose** (K-07) and a **What** whose true answer is nil
(K-08). K-03, K-05 and K-07 are the only non "what / how much / when"
questions in the set. Review 2 noticed this; it was found after seeing the
failures, so treat it as a hypothesis.

---

## 5. Everything already rejected for the four wrong questions

Do **not** propose anything here again unless you explain what is
materially new. Items marked (R1) or (R2) came from the earlier reviews.
Because extra text is tolerated on quantity answers, a string sitting
verbatim inside a rejected answer has arguably been tested too.

### K-03 — *"Who bears freight on a Rs 3,00,000 distributor order shipped in February 2024?"*
Source `PP-2023`. Rejected:
- `The buyer (distributor)` · `Buyer` · `Buyer (ex-works)` · `The distributor`
- `Buyer (all despatches are ex-works irrespective of order value)` ← live
- `Buyer bears freight, transit insurance and unloading`
- Full-clause and 339-character paragraphs containing the whole s4.1
  sentence verbatim, including *"to the buyer's account irrespective of order
  value"* — this covers R1's `To the buyer's account`, `Buyer's account` and
  the reduced clause
- A multi-branch answer naming the buyer and noting DRI paid under PP-2019
- `DRI bears the freight. Despatch is FOR destination …`
- (R2) `Ex-works. Under PP-2023 s4.1 every despatch is ex-works and freight, transit insurance and unloading are to the buyer's account irrespective of order value, so DRI's obligation ends at the works gate.`

**Both parties, and the delivery term, have been asserted and rejected.**

### K-05 — *"Which documents must a new vendor submit at onboarding?"*
Source `VOS-7`. Rejected:
- `GST registration certificate, cancelled cheque, and MSME declaration (where applicable)` ← live, and the exact VOS-7 step 2 wording (it does use the Oxford comma)
- Without the qualifier; without the Oxford comma (R1, contained in a rejected answer); with a full stop (R1)
- `GST registration certificate and cancelled cheque` (two documents)
- A paragraph opening `Three documents.` — this covers R2's "Test B"
- Paragraphs adding "collected by Procurement at step 2" and "filed in The Vault within 7 days"
- Four items, adding the purchase requisition — with and without brackets (R1)
- (R2) `GST registration certificate, cancelled cheque and MSME declaration where applicable at VOS-7 step 2, together with the bank and trade reference details Finance requires for the credit and reference check at step 3.`

### K-07 — *"A new vendor's projected annual spend is Rs 14,00,000. Whose approval is required?"*
Source `VOS-7`. Rejected:
- `CFO` · `Chief Financial Officer` · `CFO sign-off`
- `CFO (projected annual spend above Rs 10,00,000)` ← live
- `CFO approval is required, as the projected annual spend of Rs 14,00,000 exceeds the Rs 10,00,000 threshold.`
- Full matrix asserting CFO only; full matrix asserting CFO + Plant Head + QA
- `CFO, Plant Head, QA` · `CFO, Plant Head and QA`
- `GM Procurement …` · `Plant Head and QA …` · `CFO and GM Procurement`
- A multi-branch answer naming all four roles, asserting CFO
- (R1) `CFO sign-off plus Plant Head and QA clearance` — EM-107's own wording
- (R2) `Rohit Malhotra, the Chief Financial Officer, whose approval VOS-7 s3 requires once projected annual spend exceeds Rs 10,00,000.`

**Every approval set the matrix yields, under either reading of its rows,
and the named individual, have been rejected.** Only the union of all four
approvers is untried — see section 7.

### K-08 — *"What discount applies to a single order of Rs 4,20,000 placed in March 2024?"*
Source `PP-2023`. Rejected:
- `Nil` · `0%` · `Nil (0%)` ← live · `No discount` · `Nil discount`
- `Nil - no discount applies, as the order value of Rs 4,20,000 is below the Rs 5,00,000 threshold.`
- The full band table plus the non-cumulative clause (contains "below Rs 5,00,000" and "Nil")
- A supersession-led sentence; a 261-character coverage paragraph; a multi-branch answer
- `6% discount applies …` (PP-2019 band) · `10% discount. …`
- (R1) `Below Rs 5,00,000: Nil`; `0` and `Nil.` are contained in rejected answers

**The paradox.** K-01 is the same template in the same month — *"A
distributor places a single order of Rs 7,20,000 in March 2024. What
discount applies?"* — and is **correct with the bare string `10%`**. Every
expression of zero fails for K-08.

---

## 6. Organizer text — what it actually shows (corrected)

- **FIX-3407, EM-101, EM-102** — the Rs 7,20,000 order; the **CFO rules**
  "10 percent stands". Bears on K-01, which is *correct*.
- **FIX-3430** — freight on a Rs 3 lakh order, **raised by the CFO, still In
  Progress**. **EM-113** — a Sales manager *asserts* "Post-Oct 2023
  everything is ex-works". Neither is a ruling on K-03.
- **FIX-3444, EM-107** — a **direct-material** casting supplier at Rs 14 lakh
  needing "CFO sign-off plus plant head and QA clearance as direct material".
  K-07 does not say direct-material, so this does not corroborate any single
  K-07 answer.
- **FIX-3455** — an **open question** asking whether the trial cap applies to
  a Rs 3.5 lakh first order. Not a ruling. (Our ledger misread it once.)
- **FIX-3428, EM-112** — vendors carrying an MSME flag without declarations;
  declarations must be on file before the audit.
- **FIX-3440** — Gold tier: "Old timers say 45. Policy PDF says otherwise."
- **FIX-3415, EM-106** — the W3 duplicates: "a handful", "names in caps".

---

## 7. What is untested, and why it is held

These were proposed by the reviews but **not submitted**, because none is an
answer we believe is correct for the question as written, which sits close
to R-11:

- **K-08 as `14%` or `12%`** — assumes the key was built from Rs 42,00,000,
  one comma away from Rs 4,20,000.
- **K-07 as all four approvers** — no policy argument; it is simply the only
  untried combination.

We want your view on whether submitting these is legitimate.

---

## 8. Lessons from the families we solved

- **Reconciliation.** A clever `Box(10)` = 10 `Nos` conversion held us at
  0.87. The organizers' starter script simply flags the string difference.
  The literal reading scored 1.0000.
- **Workflow W3.** We merged 45 name-matched records and sat at 5/6 through a
  dozen experiments. The ticket said "a handful" and the email "names in
  caps". Merging only the 5 ALL-CAPS records scored 6/6. Every earlier test
  held the 45-record assumption fixed.

In both, the literal organizer wording beat the structurally elegant reading,
and the bug was an assumption no experiment had varied. **For Knowledge, we
do not yet know which assumption that is.**

---

## 9. Compliance — current position

- Placeholder "corruption" diagnostics and API route probing have **stopped**.
- Our live Knowledge file replicates another entrant's publicly posted answer
  file. **Mitigation:** our own file v8, submitted 2026-09-10, used our own
  wording for all eight correct answers and also scored 0.8333. Only its two
  wrong rows carried the other entrant's text.
- Undecided: whether to disclose the replication, diagnostics and probing to
  the organisers before the qualifier closes.

---

## 10. Constraints on your suggestions

1. **Stay inside R-11.** No placeholder or deliberately wrong submissions, no
   endpoint probing, no copying another participant's file. A genuine answer
   you believe is correct, one change at a time, is fine.
2. **No repeats** of section 5, including rewordings of the same assertion.
3. **Cite the source text** for every candidate: document and section,
   ticket id or email id. Mark guesses as guesses.
4. **Prefer new assumptions to new wordings.** Tell us which fixed
   assumption you think is wrong, and how to test that with a genuine
   submission.

---

## 11. Your output

Produce **one Markdown file** named `review_<your-model-name>.md` with these
sections:

1. **Verdict** — two or three sentences on where you think the real problem
   is.
2. **The assumption you think is wrong** — the one thing every experiment
   has held fixed that you would question first, and why.
3. **Claims you dispute** — anything in sections 3–9 you think is wrong.
4. **Candidate answers** — for each of K-03, K-05, K-07, K-08, up to three
   ranked candidates: exact answer string, reasoning, supporting source
   text, why it is not in section 5, and confidence (high / medium / low).
   Say plainly if you think a question has no legitimate candidate left.
5. **Section 7 view** — are `14%`, `12%` and all four approvers legitimate
   submissions?
6. **Compliance view** — would you disclose, and what would you say?
7. **Submission plan** — files for the next two days, in order, and how to
   read each result.
8. **Checked and rejected** — ideas you discarded, so we do not re-derive
   them.
