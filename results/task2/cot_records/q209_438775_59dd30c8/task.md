# q209_438775_59dd30c8 - visit 438775 / desc 59dd30c8

## Instruction

> Unplug the lamp on the cabinet next to the glass door

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": "lamp"
 },
 "entities": [
  {
   "name": "plug",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "lamp",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "lamp",
   "b": "cabinet"
  },
  {
   "rel": "next_to",
   "a": "cabinet",
   "b": "door"
  }
 ],
 "select": [],
 "residual": "the plug sits at the socket end, not on the lamp"
}
```

## Selected frame

- `438775/44358170/62311.154`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-1 alternative frames: `[['44358170', '62311.154']]`

## Candidate counts (after NMS)

- `plug` (target): **2**
- `lamp` (host): **1**
- `cabinet` (container): **3**
- `door` (landmark): **7**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
