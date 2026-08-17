# q366_466916_f30f1ae6 - visit 466916 / desc f30f1ae6

## Instruction

> Turn on the TV using one of the remotes on the TV stand

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
   "name": "TV stand",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "remote control",
   "b": "TV stand"
  }
 ],
 "select": [],
 "residual": "'one of the remotes' — any instance satisfying the relation is acceptable | independent check on the train split (val untouched): handheld-device GT has a median of 478 points while fixed-furniture handles have 87-108, a factor of 4.4-5.5. The annotation therefore covers the whole device rather than an individual key: what a person grasps is the whole remote or controller, and which key the press lands on does not constitute a separate interactable entity. Fixed furniture is the opposite -- there you operate the handle itself."
}
```

## Selected frame

- `466916/47331617/18258.296`  (1920x1440)
- relaxation level **L0**, chosen from 306 frames (stride 10)
- top-8 alternative frames: `[['47331617', '18258.296'], ['47331615', '18055.894'], ['47331615', '18056.894'], ['47331618', '18003.899'], ['47331618', '18011.896'], ['47331617', '18257.296'], ['47331617', '18249.299'], ['47331615', '18065.890']]`

## Candidate counts (after NMS)

- `remote control` (target): **4**
- `TV stand` (container): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
