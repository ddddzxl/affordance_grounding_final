# q007_421254_6afc3b66 - visit 421254 / desc 6afc3b66

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
 "residual": "'bedroom' is a room-level locator, not groundable"
}
```

## Selected frame

- `421254/42444758/80953.586`  (1440x1920)
- relaxation level **L0**, chosen from 170 frames (stride 10)
- top-8 alternative frames: `[['42444758', '80953.586'], ['42444754', '81018.476'], ['42444754', '80997.284'], ['42444754', '80999.284'], ['42444754', '81016.477'], ['42444758', '80944.173'], ['42444754', '80971.878'], ['42444754', '80970.879']]`

## Candidate counts (after NMS)

- `door handle` (target): **3**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
