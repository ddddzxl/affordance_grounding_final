# q248_466092_d2f1a848 - visit 466092 / desc d2f1a848

## Instruction

> Turn on the TV using one of the remotes on the coffee table

## Stage 0 parse

```json
{
 "target": {
  "concept": "remote control",
  "host": null
 },
 "entities": [
  {
   "name": "remote control",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "coffee table",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "remote control",
   "b": "coffee table"
  }
 ],
 "select": [],
 "residual": "'one of the remotes' — any instance satisfying the relation is acceptable | independent check on the train split (val untouched): handheld-device GT has a median of 478 points while fixed-furniture handles have 87-108, a factor of 4.4-5.5. The annotation therefore covers the whole device rather than an individual key: what a person grasps is the whole remote or controller, and which key the press lands on does not constitute a separate interactable entity. Fixed furniture is the opposite -- there you operate the handle itself."
}
```

## Selected frame

- `466092/44796568/16149.195`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['44796568', '16149.195'], ['44796568', '16150.194'], ['44796568', '16148.195'], ['44796568', '16151.194'], ['44796562', '15962.405'], ['44796562', '15951.293'], ['44796568', '16152.193'], ['44796562', '16003.405']]`

## Candidate counts (after NMS)

- `remote control` (target): **1**
- `coffee table` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
