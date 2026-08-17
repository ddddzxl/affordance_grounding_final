# q262_466162_56fc664c - visit 466162 / desc 56fc664c

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

- `466162/44796575/16863.991`  (1920x1440)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['44796575', '16863.991'], ['44796575', '16865.991'], ['44796579', '16778.593'], ['44796576', '16707.290'], ['44796575', '16918.186'], ['44796576', '16752.688'], ['44796576', '16753.687'], ['44796579', '16819.793']]`

## Candidate counts (after NMS)

- `door handle` (target): **6**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
