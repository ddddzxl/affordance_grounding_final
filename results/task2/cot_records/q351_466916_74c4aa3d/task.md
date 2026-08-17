# q351_466916_74c4aa3d - visit 466916 / desc 74c4aa3d

## Instruction

> Open the left door of the TV stand

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "cabinet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "cabinet door",
   "role": "host",
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
   "rel": "contains",
   "a": "TV stand",
   "b": "cabinet door"
  }
 ],
 "select": [
  {
   "on": "cabinet door",
   "axis": "horizontal",
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `466916/47331617/18258.296`  (1920x1440)
- relaxation level **L0**, chosen from 306 frames (stride 10)
- top-5 alternative frames: `[['47331617', '18258.296'], ['47331617', '18257.296'], ['47331615', '18056.894'], ['47331618', '18003.899'], ['47331618', '18011.896']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `cabinet door` (host): **3**
- `TV stand` (container): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
