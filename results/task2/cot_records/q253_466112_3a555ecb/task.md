# q253_466112_3a555ecb - visit 466112 / desc 3a555ecb

## Instruction

> Close the bathroom door

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
 "residual": "'bathroom' is a room-level locator, not groundable"
}
```

## Selected frame

- `466112/44796517/3926.526`  (1440x1920)
- relaxation level **L0**, chosen from 176 frames (stride 10)
- top-8 alternative frames: `[['44796517', '3926.526'], ['44796517', '3897.221'], ['44796517', '3925.526'], ['44796521', '3959.413'], ['44796521', '3958.413'], ['44796521', '3957.414'], ['44796517', '3893.222'], ['44796517', '3896.221']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
