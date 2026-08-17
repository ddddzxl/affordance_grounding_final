# Reasoning records — all 445 val instructions

One directory per question. This is the corpus the reported results were produced from.

## What is in each directory

| File | Contents |
|---|---|
| `candidates.txt` | **The sole input to the reasoning stage.** Purely symbolic: the parse, the image coordinate convention, one row per detection (id, bbox, centre, area%, score), and the containment table. No image, no ground truth. |
| `task.md` | The instruction, the parse, and the frame-selection diagnostics (which relaxation level was needed, which alternative frames were ranked). |
| `meta.json` | Machine-readable: frame id, full candidate geometry, frame-selection diagnostics, and the hard-coded geometric solution kept as a control arm. |
| `answer.json` | The result: selected ids, confidence tier, criterion type, and exclusion or defect flags where they apply. |
| `cot.md` | The reasoning transcript. **Present for 58 curated questions** — see below. |

`_index.json` lists every question with its concept, host, answer, confidence, criterion type,
scoring outcome, and whether a transcript is present.

## Why only 58 transcripts

The reasoning was executed interactively, one instruction at a time, in 14 batches, and the
transcripts were written as working notes rather than as a deliverable. The 58 published here
were selected to cover:

- **every excluded question and every flagged question defect**, since those carry the written
  reasons the exclusions rest on
- **all four cases where manual review overturned the automatic score**, so the override and
  its justification can be audited
- **29 distinct criterion types**, including the instructive failure modes: a merged host, a
  broken host chain, giant false detections, twin handles, indistinguishable candidates, and
  cases where the answer was never in the candidate pool
- **21 concepts**, and both correct and incorrect outcomes (23 correct, 29 wrong — deliberately
  weighted towards the failures, which are the more informative half)

The structured fields (`final`, `confidence`, `kind`) are published for **all 445** and are what
every reported number is computed from; the transcripts are supporting evidence for how the
method behaves on individual questions, not an input to any statistic.

## Reading a transcript

Several transcripts contain a "where the previous version went wrong" section. Those are
genuine revisions made during the work and are kept deliberately — they are the clearest record
of how the rule set in [`../../../docs/reasoning_rules.md`](../../../docs/reasoning_rules.md)
was arrived at. The most consequential one appears in q009: ordering constraints must apply to
the **host**, never directly to the target, and every target inside the chosen host's filled
mask must be emitted. That rule then resolves narrow-drawer and wide-drawer cabinets uniformly,
with no need to decide in advance which layer splits left from right.

## Provenance

The reasoning was performed by a frontier LLM working from the written rule specification, with
access to `candidates.txt` only. It never saw an image and never saw ground truth: scoring is a
separate step ([`../../../code/task2/eval/score_cot.py`](../../../code/task2/eval/score_cot.py))
run after the answers were fixed, and the generation stage does not import the annotation
loader at all.

Questions marked `auto (no CoT)` in the original working set had exactly one candidate, where
the ordering constraint can only resolve to `#0` and reasoning has zero information gain; they
are marked as such in their transcripts.
