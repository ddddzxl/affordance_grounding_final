# q059_422842_28af664b - visit 422842 / desc 28af664b

## Instruction

> Close the door that leads to the stairway

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
 "residual": "'leads to the stairway' is a semantic/room-level locator - ignored"
}
```

## Selected frame

- `422842/42897547/473306.217`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-8 alternative frames: `[['42897547', '473306.217'], ['42897547', '473241.610'], ['42897547', '473255.605'], ['42897547', '473308.216'], ['42897560', '473383.802'], ['42897547', '473265.717'], ['42897547', '473271.715'], ['42897547', '473148.815']]`

## Candidate counts (after NMS)

- `door handle` (target): **4**
- `door` (host): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
