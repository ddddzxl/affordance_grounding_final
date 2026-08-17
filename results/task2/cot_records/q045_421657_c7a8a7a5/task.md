# q045_421657_c7a8a7a5 - visit 421657 / desc c7a8a7a5

## Instruction

> Open the left door of the wooden closet

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
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `421657/42445642/58279.688`  (1920x1440)
- relaxation level **L0**, chosen from 165 frames (stride 10)
- top-8 alternative frames: `[['42445642', '58279.688'], ['42445633', '58117.489'], ['42445633', '58132.699'], ['42445639', '58338.897'], ['42445633', '58118.489'], ['42445642', '58252.500'], ['42445639', '58312.292'], ['42445642', '58251.500']]`

## Candidate counts (after NMS)

- `door handle` (target): **4**
- `closet door` (host): **2**
- `closet` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
