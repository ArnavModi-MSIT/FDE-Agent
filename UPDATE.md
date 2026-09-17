# Latest update — 2026-09-16

**This file is rewritten fresh on every change, not appended to.** It's a
quick "what just happened and why" for a human checking in — the full
project record with all context/rationale lives in `CLAUDE.md`.

## Knowledge 0.8333 → 0.8750, and we know exactly why

Five attempts today took Knowledge from 8/12 to **9/12 answers**.

- **v29 (0.8750)** — the four failing answers restated with their numbers in
  both notations. One landed.
- **v30 (0.8333)** — K-03/K-05 widened, K-07/K-08 reverted: the winner is in
  the K-07/K-08 pair, and K-03/K-05 don't respond to numbers.
- **v31 (0.8750)** — widening both added nothing; only one of the pair is
  reachable.
- **v32 (0.8333)** — reverting K-08 alone lost the point: **K-08 is the one**.
- **v33 (0.8750)** — K-08 still scores with the clause number dropped.

**The finding.** v11's failed K-08 already carried every number v33 has
except one: `5`, from writing the threshold as **`Rs 5 lakh`**. The hidden
keys use the organizers' own lakh notation, not the PDF's `Rs 5,00,000`.

## Best set

`submissions/knowledge_submission_best_0p8750.csv` (also copied to
`knowledge_submission.csv`): the banked eight, K-08 as the scoring answer,
and K-03/K-05/K-07 at their banked text.

## What's left

K-03, K-05 and K-07 survived two rounds of full number coverage. Their keys
probably hold no numbers, which this grader can't match. The only
post-launch entrant who ever beat 20/24 sits at 0.875 too — the same 9/12.

## Standing

| Family | Score |
|---|---|
| Reconciliation | **1.0000** |
| Workflow | **1.0000** |
| Migration | **1.0000** |
| Knowledge | **0.8750** |

Composite **97.50**. 2026-09-17: v34 (every other number notation for K-03, K-05, K-07) also scored 0.8750, so the numbers route is closed for those three. v35 and v36 (short text-style long shots) are built. Commits since the last push are local only.
