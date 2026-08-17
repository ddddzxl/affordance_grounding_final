# q133_434897_009cc1a0 - visit 434897 / desc 009cc1a0

## Instruction

> Open the right door of the wooden closet

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "closet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "closet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "closet",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "closet",
   "b": "closet door"
  }
 ],
 "select": [
  {
   "on": "closet door",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `434897/42899163/182680.731`  (1440x1920)
- relaxation level **L0**, chosen from 94 frames (stride 10)
- top-8 alternative frames: `[['42899163', '182680.731'], ['42899165', '182807.545'], ['42899163', '182685.745'], ['42899163', '182684.746'], ['42899165', '182853.543'], ['42899165', '182868.137'], ['42899165', '182816.441'], ['42899163', '182687.745']]`

## Candidate counts (after NMS)

- `door handle` (target): **9**
- `closet door` (host): **4**
- `closet` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
