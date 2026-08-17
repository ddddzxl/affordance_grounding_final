# Reasoning Rules

This is the written specification the reasoning stage works from — the complete instruction
set given to the model at stage S3, alongside a `candidates.txt` table and nothing else.

It matters for two reasons beyond documentation:

- **It is the ablation's control.** The open-model arm in [`../REPORT.md`](../REPORT.md) §7
  receives this same specification, which is what makes that comparison about the model
  rather than about the prompt. (The frontier arm worked from a longer version of the same
  rules; the two are therefore not a pure model comparison, and are not presented as one.)
- **It is where per-question error analysis was reinvested.** Several sections below —
  in particular "Masks do not always carve the scene the way the instruction does" — exist
  because a specific class of mistake was observed, attributed, and turned into a rule.

The `kind` enumeration at the end is also a measurement instrument, not decoration: it is
what revealed that the 9B model collapses 45 of 99 questions onto a single template and never
once uses the `merged_host` label.

---


## The task

A user gives a natural-language instruction about acting on something in a room, e.g.
*"Open the top left drawer of the cabinet to the left of the TV."*

You are shown **one RGB frame** of that room, described as a table of object detections.
Your job: decide **which detected instance(s) the instruction refers to** — specifically,
the instance(s) of the *target concept*, which is the part a person would actually touch
(a handle, a knob, a switch, a plug).

The answer is a list of instance ids.

## What you are given

**`TASK`** — the original instruction.

**`PARSE`** — the instruction already decomposed for you:

- `target concept` — the class you must output ids from.
- `host` — the countable object the target sits on (a handle sits on a *drawer*).
  May be `None` when the target stands alone (a socket on a wall).
- entity roles — `target`, `host`, `container` (encloses the host, e.g. a cabinet holding
  drawers), `landmark` (used only to locate, never the answer).
- `relation` — spatial constraints between entities, e.g. `left_of(a='cabinet', b='TV')`,
  `above(a='window', b='radiator')`, `contains(a='cabinet', b='drawer')`.
- `select` — an ordering constraint, e.g. `on='drawer' axis=vertical value='top'`,
  or `axis=ordinal index=3`. **It always names which class it applies to via `on=`.**
- `residual` — notes about parts of the instruction that could not be grounded.

**`INSTANCES`** — every detection in this frame:
`id, xmin, xmax, ymin, ymax, cx, cy, area%, score`. Multiple classes are listed together;
ids restart from 0 within each class.

**`CONTAINMENT`** — for tasks that have a host: which target ids fall inside each host's
mask. Rows tagged `[via bbox]` fell back to bounding-box containment because the mask test
found nothing, so they are less reliable than untagged rows.

## Coordinate convention

x increases to the right, y increases **downward**.
So `top` = small y, `bottom` = large y, `left` = small x, `right` = large x.
`A above B` means `A.cy < B.cy`.

## Masks do not always carve the scene the way the instruction does

This is the single most common way to get a task wrong, so read it carefully.

A detector segments by visual similarity; a person speaks in terms of functional units.
The two often disagree. **One detected host may span what the user considers two or three
separate objects** — a single mask covering a stack of drawers, or a row of them. Its
containment row will then list several targets that are *not* siblings on one object, but
one target each from several objects.

Read the target geometry to tell the two cases apart:

- Targets at roughly the **same height, spread horizontally** across the host — usually
  siblings on one wide object (two pulls on one drawer). All of them are the answer.
- Targets at clearly **different heights**, or **evenly spaced** across an unusually wide
  host — usually one target per object. Only one of them is the answer.

A host whose extent is much larger than one physical unit of its kind is itself the tell.

When a `select` is present it resolves the ambiguity: it names *which* object the user
means. So when the host is too coarse to separate them, apply the ordering to the targets
themselves. **Emitting every id in a containment row when the instruction asked for one of
them is the most frequent way to lose precision here.**

## When the target is not physically on its host

Some targets connect to their host functionally rather than spatially — a plug belongs to
a lamp but sits at the socket end, metres away. The containment rows will be empty and
`residual` usually says so; that is expected, not a failure.

In these cases **proximity to the host is not evidence**. Cables and mounting positions run
wherever the room allows. Fall back on detection quality, and on whether each candidate's
size and placement are plausible for the thing named.

## How the answer is scored

Your ids are converted into a 3D point cloud mask and compared against ground truth:

```
precision = |GT ∩ pred| / |pred|
AP50      = fraction of tasks whose precision ≥ 0.5
```

**Only precision is counted.** Adding an id you are unsure about enlarges the denominator
without necessarily enlarging the numerator. When genuinely torn, prefer fewer ids — but if
several detections are clearly parts of the same physical thing the user would grasp,
including them all is correct, not risky.

`[]` scores zero for that task, so it is only right when the candidate pool is empty or
contains nothing of the target class. **A low-confidence pick always beats it.**

## Output

Reason through it, then emit exactly one JSON object inside a ```json block:

```json
{"final": [0], "confidence": "high", "kind": "select", "note": "one short sentence"}
```

- `final` — array of integers, ids **of the target concept class** named in the
  `QUESTION:` line. Not host, container or landmark ids.
- `confidence` — exactly one of `"high"` / `"medium"` / `"low"`. Be honest; this is used
  to analyse where the method breaks.
- `kind` — exactly one of:
  `select` (an ordering constraint decided it) ·
  `relation` (a spatial constraint decided it) ·
  `containment` (the host's containment row decided it) ·
  `ordinal` (counting position in a sequence) ·
  `merged_host` (the host mask spanned several objects; resolved on target geometry) ·
  `detection_quality` (score / size / placement decided it) ·
  `fallback` (the mechanism could not run; this is a guess)
- `note` — one sentence stating the decisive evidence.

## Style

Work the constraints in order and commit:

1. one or two sentences — which landmark / container fixes the region
2. one or two sentences — which host that leaves, and what `select` picks among them
3. one or two sentences — which target(s) that host gives, and why competitors are out

That is the whole answer; around 150 words. Do not list every candidate's coordinates, and
do not re-derive a conclusion you already reached in order to double-check it — both cost
time and tend to talk you out of a correct first reading.

Detections are imperfect and some instructions are genuinely ambiguous. When the evidence
runs out, take the best available reading, mark `confidence: "low"`, and move on.
