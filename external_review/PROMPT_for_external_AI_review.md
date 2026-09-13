# Request for an independent review — FDE Hackathon 2026, Knowledge family

You are being asked for an independent second opinion on a competition
entry. Read this whole brief and the attached files, then **produce one
Markdown file** in the format specified at the end.

Be sceptical of everything here, including our conclusions. Several of our
"proven" conclusions have turned out to be wrong before, and the two
breakthroughs we did have came from questioning something we had held fixed.
If you think a claim below is wrong, say so and show why.

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
  keeps each family's **best** recorded score.
- One number per submission. No per-row feedback, ever.
- **R-11:** *"No probing of the scoring endpoints, no attempts to obtain the
  hidden key, no sharing of submission files between participants, no
  multiple accounts to farm attempts. Organisers may disqualify a
  participant."* The FAQ also bans "sharing solutions across teams".
- Submissions freeze 2026-09-27 23:59 IST. Qualifier close is 2026-09-20.

---

## 2. Where we stand

| Family | Our best | Status |
|---|---|---|
| Reconciliation | 1.0000 | solved |
| Workflow | 1.0000 | solved |
| Migration | 1.0000 | solved |
| **Knowledge** | **0.8333 (20/24)** | **4 answers wrong — the only open gap** |

Composite about 96.67, tied with three others for third. Two entrants beat
us on Knowledge: **bhasker 1.000 (24/24)**, whose last run was 28 days ago,
and **Sanjay Prasad 0.875 (21/24)**, last run 3 days ago.

---

## 3. What we believe is established about Knowledge

Please check each of these against the evidence, not just accept it.

**3.1 All 12 `governing_source` values are correct.** Measured twice, on
2026-09-08 and 2026-09-12, by submitting a file with every answer replaced by
a meaningless placeholder and the sources left intact. Both returned 0.5000,
which is 12 of 12 sources. So 20/24 means 8 correct answers.

**3.2 The scoring is additive per question.** Answers-only and sources-only
placeholder files scored 0.2500 and 0.5000, summing to the 0.7500 baseline of
that day.

**3.3 The 8 correct answers are K-01, K-02, K-04, K-06, K-09, K-10, K-11,
K-12. The 4 wrong ones are K-03, K-05, K-07, K-08.** Several placeholder
diagnostics narrowed this to three possible sets. The final identification
rests on something stronger: seven later submissions rewrote K-03, K-05, K-07
and K-08 with very different content and the score never moved off 0.8333.
Had any of the four been correct, rewriting it would have cost a point.

**3.4 The question file is current.** A fresh download on 2026-09-13 is
byte-identical to the copy used throughout.

**3.5 The grader tolerates extra text.** A correct answer kept its credit
with an irrelevant filler sentence appended (110 characters total), and
again when padded with filler to 297 characters.

**3.6 Naming an alternative inside an answer does not earn credit.** Answers
that stated our reading and also mentioned the competing reading, all under
160 characters, scored nothing extra. We read this as: the grader judges what
an answer *asserts*, not which words it *contains*.

**3.7 How K-09 was solved.** `10%` failed. `10% of invoice value`, which is a
literal quote of the governing sentence, also failed. This scored:
*"A restocking charge of 10% of invoice value applies to unused goods in
original packing returned within 30 days of despatch; made-to-order items
are not returnable."* It restates the whole clause: value, condition and
exclusion.

---

## 4. The four wrong questions, and everything already rejected

Do **not** propose anything below again unless you explain what makes your
version materially different. "Probably wrong" marks a variant submitted
alongside other changes, so its own status is slightly less certain.

### K-03 — *"Who bears freight on a Rs 3,00,000 distributor order shipped in February 2024?"*
Source `PP-2023` is correct. Rejected:
- `The buyer (distributor)`
- `Buyer`
- `Buyer (all despatches are ex-works irrespective of order value)` ← current
- `Buyer (ex-works)` — another entrant's attempt, scored as wrong
- `The distributor`
- `Buyer bears freight, transit insurance and unloading`
- A full-clause sentence citing PP-2023 s4.1, ex-works, and all three cost categories (probably wrong)
- A 339-character paragraph covering buyer, distributor, ex-works, the three cost categories, and "DRI does not bear freight"
- `The buyer, i.e. the distributor, bears freight, transit insurance and unloading; PP-2023 makes all despatches ex-works. DRI paid only under PP-2019.`
- `DRI bears the freight. Despatch is FOR destination for a single order above Rs 2,00,000, so the seller and not the distributor carries the freight cost.`

**Both parties have been asserted and rejected.**

### K-05 — *"Which documents must a new vendor submit at onboarding?"*
Source `VOS-7` is correct. Rejected:
- `GST registration certificate, cancelled cheque, and MSME declaration (where applicable)` ← current
- `GST registration certificate, cancelled cheque, MSME declaration` — another entrant's attempt
- `GST registration certificate, cancelled cheque, and MSME declaration`
- `GST registration certificate and cancelled cheque`
- `GST registration certificate, cancelled cheque and MSME declaration (where applicable) - the three documents collected by Procurement at VOS-7 step 2.`
- A full paragraph adding "collected by Procurement at step 2" and "filed in The Vault within 7 days of vendor code creation" (asserted twice, once probably wrong)
- `Purchase requisition with vendor justification, GST registration certificate, cancelled cheque, and MSME declaration where applicable - four items in all.`

### K-07 — *"A new vendor's projected annual spend is Rs 14,00,000. Whose approval is required?"*
Source `VOS-7` is correct. Rejected:
- `CFO`
- `Chief Financial Officer`
- `CFO sign-off`
- `CFO (projected annual spend above Rs 10,00,000)` ← current
- `CFO approval is required, as the projected annual spend of Rs 14,00,000 exceeds the Rs 10,00,000 threshold.`
- The full approval matrix stated, asserting CFO only
- `CFO, Plant Head, QA`
- `CFO, Plant Head and QA`
- The full matrix stated, asserting CFO + Plant Head + QA (backed by email EM-107)
- `CFO sign-off (Chief Financial Officer) for spend above Rs 10,00,000; a direct-material vendor also needs Plant Head and QA; others need GM Procurement.`
- `GM Procurement approves the vendor. …`
- `Plant Head and QA. …`
- `CFO and GM Procurement`

**Every approval set the matrix can produce has been asserted and rejected.**

### K-08 — *"What discount applies to a single order of Rs 4,20,000 placed in March 2024?"*
Source `PP-2023` is correct. Rejected:
- `Nil`
- `0%`
- `Nil (0%)` ← current
- `No discount`
- `Nil discount`
- `Nil - no discount applies, as the order value of Rs 4,20,000 is below the Rs 5,00,000 threshold.`
- The full PP-2023 band table plus the non-cumulative clause
- A supersession-led sentence (PP-2023 replaced PP-2019)
- A 261-character paragraph covering Nil, no discount, 0%, zero, both notations of the amount, and the slab
- `Nil, no discount: Rs 4,20,000 is below the Rs 5,00,000 slab under PP-2023. Had it reached that slab the rate would be 10%, and above Rs 15,00,000, 14%.`
- `6% discount applies …` (the PP-2019 band)
- `10% discount. …`

**The paradox we cannot explain.** K-01 is the same question template in the
same month — *"A distributor places a single order of Rs 7,20,000 in March
2024. What discount applies?"* — and is **correct with the bare string
`10%`**. Yet every expression of zero fails for K-08. The source PP-2023 is
proven correct, and PP-2023 puts Rs 4,20,000 in the "Below Rs 5,00,000:
Nil" band.

---

## 5. The eight correct answers (current file)

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

All eight lead with a quantity. All four wrong answers lead with a party, a
list, a role, or a nil.

---

## 6. Organizer text we have used as corroboration

These tickets and emails appear to confirm our reading of the four wrong
questions. Check whether they say what we think they say.

- **FIX-3407, EM-101, EM-102** — the Rs 7,20,000 order: "10 percent stands".
- **FIX-3430, EM-113** — a distributor disputing freight on a Rs 3 lakh
  order: "Post-Oct 2023 everything is ex-works."
- **FIX-3444, EM-107** — a casting supplier at Rs 14 lakh: "per SOP this needs
  CFO sign-off plus plant head and QA clearance as direct material. GST cert
  and cancelled cheque are on file, MSME declaration awaited."
- **FIX-3455** — a Rs 3.5 lakh first order on a new vendor, asking whether the
  trial cap applies.
- **FIX-3440** — Gold tier: "Old timers say 45. Policy PDF says otherwise."

---

## 7. Lessons from the families we solved

These may transfer.

- **Reconciliation.** We spent days on a clever unit-of-measure conversion
  treating `Box(10)` as equal to 10 `Nos`. The organizers' own starter script
  simply flags the string difference as `UOM_MISMATCH`. Switching to the
  literal reading went straight to 1.0000. An "Open" ticket describing the
  issue meant "flag it", not "resolve it away".
- **Workflow W3, deduplicating distributors.** For days we merged 45 records
  and sat at 5/6 through a dozen experiments. The ticket said "at least **a
  handful** of distributors exist twice" and an email said "names in caps".
  Merging only the 5 ALL-CAPS records scored 6/6. Every earlier test had held
  the 45-record assumption fixed.

In both cases the literal organizer wording beat the structurally elegant
reading, and the bug was an assumption no experiment had varied.

---

## 8. Constraints on your suggestions

1. **Stay inside R-11.** Do not propose deliberately wrong or placeholder
   submissions designed to reveal the hidden key, probing of any scoring
   endpoint, or copying another participant's submission file. Submitting
   your own genuine best answer for a question, one change at a time, is
   ordinary iteration and is fine.
2. **No repeats** of anything in section 4 without saying what is materially
   new.
3. **Cite the source text** behind every candidate: document and section,
   ticket id, or email id. Mark anything that is a guess as a guess.
4. **Five attempts a day.** Plan for that.

We would also value your view on a compliance question. Our current 0.8333
answer set replicates an answer file another entrant posted publicly in a
GitHub repo. Several earlier submissions were deliberate placeholder
diagnostics. Is either a meaningful R-11 risk, and what would you do about it?

---

## 9. Your output

Produce **one Markdown file** named `review_<your-model-name>.md` with exactly
these sections:

1. **Verdict** — two or three sentences on whether our conclusions hold and
   where you think the real problem is.
2. **Claims you dispute** — each claim from sections 3–7 you think is wrong or
   unsupported, and why.
3. **Candidate answers** — for each of K-03, K-05, K-07 and K-08, up to three
   ranked candidates. For each give the exact answer string to submit, the
   reasoning, the supporting source text, why it is not a repeat of section 4,
   and a confidence of high, medium or low.
4. **A different explanation** — if you think the paradox in section 4 has a
   cause other than wrong wording or wrong content, describe it and say how to
   test it legitimately.
5. **Compliance view** — your answer to the R-11 question in section 8.
6. **Submission plan** — which files to submit over the next two days, in
   order, and how to read each result.
7. **Checked and rejected** — ideas you considered and discarded, so we do not
   re-derive them.
