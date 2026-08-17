# q362_466916_be3f2542 - visit 466916 / desc be3f2542

## Instruction

> Play a game using the left joystick on the shelf of the TV stand

## Stage 0 parse

```json
{
 "target": {
  "concept": "joystick",
  "host": null
 },
 "entities": [
  {
   "name": "joystick",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "shelf",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "TV stand",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "joystick",
   "b": "shelf"
  },
  {
   "rel": "contains",
   "a": "TV stand",
   "b": "shelf"
  }
 ],
 "select": [
  {
   "on": "joystick",
   "axis": "horizontal",
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": "train: 'play a game' is a key_press affordance, so the target is a button on the joystick | independent check on the train split (val untouched): handheld-device GT has a median of 478 points while fixed-furniture handles have 87-108, a factor of 4.4-5.5. The annotation therefore covers the whole device rather than an individual key: what a person grasps is the whole remote or controller, and which key the press lands on does not constitute a separate interactable entity. Fixed furniture is the opposite -- there you operate the handle itself."
}
```

## Selected frame

- `466916/47331617/18249.299`  (1920x1440)
- relaxation level **POOL-T**, chosen from 306 frames (stride 10)
- top-3 alternative frames: `[['47331617', '18249.299'], ['47331618', '18010.896'], ['47331618', '18011.896']]`

## Candidate counts (after NMS)

- `joystick` (target): **3**
- `shelf` (container): **4**
- `TV stand` (landmark): **4**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
