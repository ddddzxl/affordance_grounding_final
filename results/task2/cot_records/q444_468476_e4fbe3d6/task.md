# q444_468476_e4fbe3d6 - visit 468476 / desc e4fbe3d6

## Instruction

> Open the left door of the cabinet located to the right of the mirror

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
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "mirror",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "cabinet door"
  },
  {
   "rel": "right_of",
   "a": "cabinet",
   "b": "mirror"
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

- `468476/45261682/3555.567`  (1440x1920)
- relaxation level **L0**, chosen from 222 frames (stride 10)
- top-5 alternative frames: `[['45261682', '3555.567'], ['45261681', '3608.062'], ['45261682', '3535.475'], ['45261682', '3556.566'], ['45261681', '3611.677']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `cabinet door` (host): **2**
- `cabinet` (container): **1**
- `mirror` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
