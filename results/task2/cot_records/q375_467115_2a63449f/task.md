# q375_467115_2a63449f - visit 467115 / desc 2a63449f

## Instruction

> Turn on the TV using the remote on the dining table

## Stage 0 parse

```json
{
 "target": {
  "concept": "remote control button",
  "host": null
 },
 "entities": [
  {
   "name": "remote control button",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "dining table",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "remote control button",
   "b": "dining table"
  }
 ],
 "select": [],
 "residual": "independent check on the train split (val untouched): handheld-device GT has a median of 478 points while fixed-furniture handles have 87-108, a factor of 4.4-5.5. The annotation therefore covers the whole device rather than an individual key: what a person grasps is the whole remote or controller, and which key the press lands on does not constitute a separate interactable entity. Fixed furniture is the opposite -- there you operate the handle itself."
}
```

## Selected frame

- `467115/47333319/28504.063`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333319', '28504.063'], ['47333319', '28509.161'], ['47333308', '28084.368'], ['47333310', '28239.655'], ['47333310', '28235.657'], ['47333308', '28097.363'], ['47333319', '28462.864'], ['47333319', '28484.855']]`

## Candidate counts (after NMS)

- `remote control button` (target): **11**
- `dining table` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
