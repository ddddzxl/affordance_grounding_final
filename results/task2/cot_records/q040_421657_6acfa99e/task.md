# q040_421657_6acfa99e - visit 421657 / desc 6acfa99e

## Instruction

> Close the bedroom door

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'bedroom' room-level locator - ignored"
}
```

## Selected frame

- `421657/42445639/58315.290`  (1920x1440)
- relaxation level **L0**, chosen from 165 frames (stride 10)
- top-8 alternative frames: `[['42445639', '58315.290'], ['42445639', '58314.291'], ['42445633', '58120.488'], ['42445633', '58117.489'], ['42445633', '58121.487'], ['42445633', '58131.700'], ['42445633', '58133.699'], ['42445642', '58279.688']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
