# q061_422842_4112a6d8 - visit 422842 / desc 4112a6d8

## Instruction

> Open the left door of the wall cabinet located above the bed and near the door

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
   "name": "wall cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "bed",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "wall cabinet",
   "b": "cabinet door"
  },
  {
   "rel": "above",
   "a": "wall cabinet",
   "b": "bed"
  },
  {
   "rel": "near",
   "a": "wall cabinet",
   "b": "door"
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

- `422842/42897547/473286.209`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-3 alternative frames: `[['42897547', '473286.209'], ['42897547', '473254.605'], ['42897547', '473288.208']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `cabinet door` (host): **4**
- `wall cabinet` (container): **3**
- `bed` (landmark): **1**
- `door` (landmark): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
