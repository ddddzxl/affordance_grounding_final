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

The structured fields are what every reported number is computed from; a transcript is there
to show how the method behaves on one question. Publishing all 445 would bury that, so 58 were
selected to cover:

- **every excluded question and every flagged question defect**, since those carry the written
  reasons the exclusions rest on
- **the four questions where pose error displaces the projected ground truth away from a
  correct pick**, so the criterion applied there can be audited
- **30 distinct criterion types**, including the instructive failure modes: a merged host, a
  broken host chain, giant false detections, twin handles, indistinguishable candidates, and
  cases where the answer was never in the candidate pool
- **21 concepts**, and both outcomes in equal measure (27 correct, 29 wrong, plus the two
  excluded questions, which carry no score), so the failures — the more informative half —
  are as visible as the successes

The structured fields (`final`, `confidence`, `kind`) are published for **all 445** and are what
every reported number is computed from; the transcripts are supporting evidence for how the
method behaves on individual questions, not an input to any statistic.

## Reading a transcript

Each transcript works from the candidate table alone and in the same order: fix the container,
resolve the host layer, then apply the ordering constraint. The most consequential rule in
[`../../../docs/reasoning_rules.md`](../../../docs/reasoning_rules.md) is the one worked
through in q009: ordering constraints apply to the **host**, never directly to the target, and
every target inside the chosen host's filled mask is emitted. That rule resolves narrow-drawer
and wide-drawer cabinets uniformly, with no need to decide in advance which layer splits left
from right.

## Provenance

The reasoning was performed by a frontier LLM working from the written rule specification, with
access to `candidates.txt` only. It never saw an image and never saw ground truth: scoring is a
separate step ([`../../../code/task2/eval/score_cot.py`](../../../code/task2/eval/score_cot.py))
run after the answers were fixed, and the generation stage does not import the annotation
loader at all.

Questions with exactly one candidate carry no transcript: the ordering constraint can only
resolve to `#0`, so reasoning has zero information gain there.
