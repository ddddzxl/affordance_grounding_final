# q103_423452_a50356e1 - visit 423452 / desc a50356e1

## Instruction

> Close the door that leads to the bedroom

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
 "residual": "'leads to the bedroom' room-level locator - ignored"
}
```

## Selected frame

- `423452/42897434/104293.439`  (1920x1440)
- relaxation level **L0**, chosen from 309 frames (stride 10)
- top-8 alternative frames: `[['42897434', '104293.439'], ['42897426', '104096.638'], ['42897422', '104033.148'], ['42897422', '104059.137'], ['42897426', '104144.735'], ['42897426', '104128.741'], ['42897434', '104333.839'], ['42897426', '104146.734']]`

## Candidate counts (after NMS)

- `door handle` (target): **6**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
