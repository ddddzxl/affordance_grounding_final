# q346_466880_f3db9fb1 - visit 466880 / desc f3db9fb1

## Instruction

> Open the cabinet door directly above the fridge

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
   "name": "fridge",
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
   "rel": "above",
   "a": "cabinet door",
   "b": "fridge"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466880/47331711/11269.339`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-3 alternative frames: `[['47331711', '11269.339'], ['47331710', '11231.238'], ['47331711', '11271.339']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `cabinet door` (host): **6**
- `cabinet` (container): **6**
- `fridge` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
