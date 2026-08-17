# q290_466437_b7ade931 - visit 466437 / desc b7ade931

## Instruction

> Close the door that leads to the hallway

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
 "residual": "'leads to the hallway' is a room-level locator, not groundable"
}
```

## Selected frame

- `466437/45260957/5982.517`  (1440x1920)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['45260957', '5982.517'], ['45260957', '5983.516'], ['45260957', '5986.515'], ['45260957', '5984.516'], ['45260952', '6023.117'], ['45260957', '5985.515'], ['45260951', '6159.113'], ['45260951', '6208.311']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `door` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
