# q159_435357_69de1094 - visit 435357 / desc 69de1094

## Instruction

> Turn on the TV using the remote on the glass coffee table

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
 "residual": "independent check on the train split (val untouched): handheld-device GT has a median of 478 points while fixed-furniture handles have 87-108, a factor of 4.4-5.5. The annotation therefore covers the whole device rather than an individual key: what a person grasps is the whole remote or controller, and which key the press lands on does not constitute a separate interactable entity. Fixed furniture is the opposite -- there you operate the handle itself."
}
```

## Selected frame

- `435357/42899624/230107.282`  (1440x1920)
- relaxation level **L0**, chosen from 191 frames (stride 10)
- top-8 alternative frames: `[['42899624', '230107.282'], ['42899624', '230113.280'], ['42899624', '230106.282'], ['42899624', '230101.284'], ['42899624', '230112.280'], ['42899624', '230111.280'], ['42899624', '230114.279'], ['42899624', '230118.278']]`

## Candidate counts (after NMS)

- `remote control` (target): **1**
- `coffee table` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
