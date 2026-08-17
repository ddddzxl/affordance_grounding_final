# q319_466876_f1769f8c - visit 466876 / desc f1769f8c

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

- `466876/47331561/9782.142`  (1440x1920)
- relaxation level **L0**, chosen from 160 frames (stride 10)
- top-8 alternative frames: `[['47331561', '9782.142'], ['47331560', '9898.645'], ['47331560', '9897.646'], ['47331558', '9833.955'], ['47331560', '9901.644'], ['47331561', '9777.144'], ['47331561', '9767.149'], ['47331560', '9902.644']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
