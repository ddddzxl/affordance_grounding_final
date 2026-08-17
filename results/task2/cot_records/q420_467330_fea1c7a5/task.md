# q420_467330_fea1c7a5 - visit 467330 / desc fea1c7a5

## Instruction

> Turn on the TV using the remote on the blue couch

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
   "name": "couch",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "remote control",
   "b": "couch"
  }
 ],
 "select": [],
 "residual": "independent check on the train split (val untouched): handheld-device GT has a median of 478 points while fixed-furniture handles have 87-108, a factor of 4.4-5.5. The annotation therefore covers the whole device rather than an individual key: what a person grasps is the whole remote or controller, and which key the press lands on does not constitute a separate interactable entity. Fixed furniture is the opposite -- there you operate the handle itself."
}
```

## Selected frame

- `467330/45261600/53003.123`  (1920x1440)
- relaxation level **L0**, chosen from 207 frames (stride 10)
- top-8 alternative frames: `[['45261600', '53003.123'], ['45261600', '53000.124'], ['45261600', '53002.123'], ['45261600', '53004.122'], ['45261600', '53015.118'], ['45261600', '53014.119'], ['45261600', '53001.124'], ['45261600', '53005.122']]`

## Candidate counts (after NMS)

- `remote control` (target): **1**
- `couch` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
