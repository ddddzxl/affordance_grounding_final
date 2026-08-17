# q330_466880_5cdd0cac - visit 466880 / desc 5cdd0cac

## Instruction

> Open the kitchen counter door with the paper towel holder on top

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "counter door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "counter door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "counter",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "paper towel holder",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "counter",
   "b": "counter door"
  },
  {
   "rel": "has_on_top",
   "a": "counter",
   "b": "paper towel holder"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466880/47331711/11307.840`  (1920x1440)
- relaxation level **L3**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['47331711', '11307.840'], ['47331711', '11254.729'], ['47331711', '11252.729'], ['47331707', '11137.826'], ['47331710', '11215.228'], ['47331711', '11313.838'], ['47331711', '11248.731'], ['47331710', '11217.227']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `counter door` (host): **0**
- `counter` (container): **3**
- `paper towel holder` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
