# q445_468476_edcb0a76 - visit 468476 / desc edcb0a76

## Instruction

> Turn on the TV using the remote on the white cabinet

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
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "remote control",
   "b": "cabinet"
  }
 ],
 "select": [],
 "residual": "independent check on the train split (val untouched): handheld-device GT has a median of 478 points while fixed-furniture handles have 87-108, a factor of 4.4-5.5. The annotation therefore covers the whole device rather than an individual key: what a person grasps is the whole remote or controller, and which key the press lands on does not constitute a separate interactable entity. Fixed furniture is the opposite -- there you operate the handle itself."
}
```

## Selected frame

- `468476/45261681/3642.664`  (1440x1920)
- relaxation level **L0**, chosen from 222 frames (stride 10)
- top-8 alternative frames: `[['45261681', '3642.664'], ['45261686', '3806.463'], ['45261686', '3805.463'], ['45261686', '3807.462'], ['45261682', '3535.475'], ['45261686', '3828.470'], ['45261686', '3804.464'], ['45261682', '3536.475']]`

## Candidate counts (after NMS)

- `remote control` (target): **1**
- `cabinet` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
