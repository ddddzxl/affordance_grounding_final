# q081_422842_da35d971 - visit 422842 / desc da35d971

## Instruction

> Open the cabinet door to the right of the nightstand

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
   "name": "nightstand",
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
   "b": "nightstand"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `422842/42897547/473205.908`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-2 alternative frames: `[['42897547', '473205.908'], ['42897547', '473181.818']]`

## Candidate counts (after NMS)

- `door handle` (target): **8**
- `cabinet door` (host): **8**
- `cabinet` (container): **11**
- `nightstand` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
