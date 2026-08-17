# q227_455342_5ac9f10b - visit 455342 / desc 5ac9f10b

## Instruction

> Turn on the TV using the remote on the coffee table

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

- `455342/44358472/46650.391`  (1920x1440)
- relaxation level **L0**, chosen from 97 frames (stride 10)
- top-8 alternative frames: `[['44358472', '46650.391'], ['44358472', '46637.097'], ['44358471', '46587.300'], ['44358472', '46651.391'], ['44358472', '46645.093'], ['44358472', '46638.096'], ['44358472', '46652.391'], ['44358472', '46626.101']]`

## Candidate counts (after NMS)

- `remote control` (target): **2**
- `coffee table` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
