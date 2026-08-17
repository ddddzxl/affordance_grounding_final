# q280_466437_3fc93181 - visit 466437 / desc 3fc93181

## Instruction

> Dial a number on the telephone on the nightstand

## Stage 0 parse

```json
{
 "target": {
  "concept": "telephone",
  "host": null
 },
 "entities": [
  {
   "name": "telephone",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "nightstand",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "telephone",
   "b": "nightstand"
  }
 ],
 "select": [],
 "residual": "independent check on the train split (val untouched): handheld-device GT has a median of 478 points while fixed-furniture handles have 87-108, a factor of 4.4-5.5. The annotation therefore covers the whole device rather than an individual key: what a person grasps is the whole remote or controller, and which key the press lands on does not constitute a separate interactable entity. Fixed furniture is the opposite -- there you operate the handle itself."
}
```

## Selected frame

- `466437/45260951/6177.106`  (1440x1920)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-2 alternative frames: `[['45260951', '6177.106'], ['45260952', '6037.112']]`

## Candidate counts (after NMS)

- `telephone` (target): **1**
- `nightstand` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
