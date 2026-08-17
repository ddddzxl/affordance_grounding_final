# q233_455342_d7a0c1c7 - visit 455342 / desc d7a0c1c7

## Instruction

> Play a game using the joystick on the TV stand

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
   "name": "TV stand",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "joystick",
   "b": "TV stand"
  }
 ],
 "select": [],
 "residual": "train: 'play a game' is a key_press affordance, so the target is a button on the joystick, not the joystick body | independent check on the train split (val untouched): handheld-device GT has a median of 478 points while fixed-furniture handles have 87-108, a factor of 4.4-5.5. The annotation therefore covers the whole device rather than an individual key: what a person grasps is the whole remote or controller, and which key the press lands on does not constitute a separate interactable entity. Fixed furniture is the opposite -- there you operate the handle itself."
}
```

## Selected frame

- `455342/44358472/46626.101`  (1920x1440)
- relaxation level **L0**, chosen from 97 frames (stride 10)
- top-8 alternative frames: `[['44358472', '46626.101'], ['44358472', '46629.100'], ['44358472', '46652.391'], ['44358471', '46592.298'], ['44358472', '46630.199'], ['44358472', '46638.096'], ['44358472', '46655.389'], ['44358472', '46627.101']]`

## Candidate counts (after NMS)

- `joystick` (target): **2**
- `TV stand` (container): **4**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
