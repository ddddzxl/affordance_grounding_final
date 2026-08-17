# q064_422842_5e1d5350 - visit 422842 / desc 5e1d5350

## Instruction

> Open the left door of the wall cabinet located above the glass cabinet decorated with pictures

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
   "name": "glass cabinet",
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
   "b": "glass cabinet"
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
 "residual": "'decorated with pictures' is a surface attribute - ignored"
}
```

## Selected frame

- `422842/42897547/473171.806`  (1440x1920)
- relaxation level **L2**, chosen from 236 frames (stride 10)
- top-1 alternative frames: `[['42897547', '473171.806']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `cabinet door` (host): **3**
- `wall cabinet` (container): **4**
- `glass cabinet` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
