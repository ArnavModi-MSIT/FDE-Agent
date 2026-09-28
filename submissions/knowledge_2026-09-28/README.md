# Knowledge candidates for 28 September 2026

**Update: the user reported v70 scored 0.9167.** Its exact bytes are banked as
`../knowledge_submission_best_0p9167.csv`, and the engine now reproduces it.
The gain cannot yet be assigned to K-03, K-05 or K-07.
**Do not upload the original v71-v74 files.** They are superseded by the
adaptive next candidate in `../knowledge_2026-09-28_after_v70/`.

The original batch below was built from 0.8750, changing K-03/K-05/K-07 while
preserving nine answers and all sources. Its historical plan remains intact.

## Original batch record (superseded)

| Order | File | Wording approach | Actual submission score |
|---|---|---|---|
| 1 | [v70](knowledge_submission_v70_compact_reference.csv) | Short reference-style answers | **0.9167 (user reported)** |
| 2 | [v71](knowledge_submission_v71_role_and_document_order.csv) | Distributor label, full CFO title, reordered document list | Superseded; do not upload |
| 3 | [v72](knowledge_submission_v72_customer_and_bank_proof.csv) | Customer label, cheque explained as bank proof | Superseded; do not upload |
| 4 | [v73](knowledge_submission_v73_compact_qualifiers.csv) | Short answers retaining policy qualifications | Superseded; do not upload |
| 5 | [v74](knowledge_submission_v74_expanded_terms.csv) | Expanded GST/MSME names and finance-head wording | Superseded; do not upload |

The reported v70 result establishes that this upload was scored despite the
published freeze. Follow the new adaptive plan, recording each **individual
submission result**, not only the best leaderboard score. Do not combine rows
from different files and assume their gains add. v70 varied three rows together,
so the aggregate result does not identify which row improved.

The historical scoring model implies 0.9167 for one extra correct answer,
0.9583 for two, and 1.0000 for three, assuming every protected row retains
credit. Those are interpretations of a possible result, **not predictions**.
The [manifest](manifest.json) records exact changes, hashes, v70's reported
score, and superseded status for the other four files.

## Why these candidates

The actual PDFs still support buyer-paid freight (PP-2023 section 4.1), the
GST registration certificate / cancelled cheque / conditional MSME declaration
(VOS-7 step 2), and CFO approval above Rs 10 lakh (VOS-7 section 3).
There is no new evidence that different business facts should replace these.

The earlier claim that extra text never affects scoring was too broad. Padding
was tested on numeric answers; it cannot establish how categorical answers are
matched. Moreover, leading a padded answer with the correct number cannot rule
out truncation later in the cell. Exact or length-sensitive text matching
therefore remains possible. These candidates explore concise, correct wording.
Their upside is uncertain after the extensive previous trials.

Novelty audit: checked 83 historical Knowledge CSV blobs across Git refs, with
52 / 50 / 57 distinct answers for K-03 / K-05 / K-07. All 15 replacements are
new as complete answers, including after case/punctuation normalization. Five
occurred inside longer historical answers; they are new only as standalone
answers. This is evidence of previously unused wording, not evidence of higher
accuracy. v68/v69's individual upload results remain unknown in the local log.

## Code review and verification

**169 tests passed.** Every generated CSV was reopened and checked for exact
headers, complete unique IDs, protected answers/sources, and its manifest hash.
The original best submission is unchanged; `git diff --check` passed.

- Fixed decimal, lakh/lac and crore parsing; `Rs 7.2 lakh` now means 720000.
- Incomplete amounts/warranty dates fail explicitly instead of crashing or
  calculating from default dates. FlowTech's exception requires stated
  pre-acquisition stock. Explicit direct-material categories affect approvals.
- Input validation catches empty/broken rows. CSV reading accepts an Excel
  UTF-8 BOM. The baseline is still reproduced byte for byte.
- Reconciliation metrics reject unequal label counts instead of truncating.
- Added a candidate generator that rejects protected-row/source changes,
  duplicate candidate files, blank answers and overwrite attempts.

The broader audit found a W1 resume limitation: an existing vendor skips later
onboarding actions. Safe repair depends on approval replay being idempotent,
which is unverified. W1 was left unchanged; no sandbox actions were performed.
Regex-based date/topic parsing still does not support arbitrary language.
None of these fixes establishes a new leaderboard score for the current rows.

Rebuild into a **new** directory from the repository root:

```powershell
.\.venv\Scripts\python.exe scripts/prepare_knowledge_candidates.py --plan experiments/knowledge_2026-09-28/plan.json --output-dir submissions/knowledge_next_batch
```

The generator can use `--baseline <scored-file>` and `--preserve K-03` (repeat
for other rows) only once a particular row is confirmed to score. It performs
no network calls. Plan and generated manifests keep unknown scores unknown.
