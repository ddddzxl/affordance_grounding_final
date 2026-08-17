# q343_466880_d369d6fc - visit 466880 / desc d369d6fc

## Instruction

> Open the kitchen counter door with the coffee machine on top

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
   "name": "coffee machine",
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
   "b": "coffee machine"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466880/47331710/11239.335`  (1920x1440)
- relaxation level **L3**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['47331710', '11239.335'], ['47331711', '11254.729'], ['47331707', '11137.826'], ['47331711', '11318.836'], ['47331710', '11215.228'], ['47331711', '11247.748'], ['47331707', '11125.831'], ['47331707', '11132.828']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `counter door` (host): **0**
- `counter` (container): **2**
- `coffee machine` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
