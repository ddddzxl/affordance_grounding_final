# q173_437157_cb3adce3 - visit 437157 / desc cb3adce3

## Instruction

> Turn on the bathroom light

## Stage 0 parse

```json
{
 "target": {
  "concept": "light switch",
  "host": null
 },
 "entities": [
  {
   "name": "light switch",
   "role": "target",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'bathroom' is a room-level locator, not groundable"
}
```

## Selected frame

- `437157/43649686/36214.277`  (1440x1920)
- relaxation level **L0**, chosen from 239 frames (stride 10)
- top-8 alternative frames: `[['43649686', '36214.277'], ['43649686', '36103.970'], ['43649686', '36104.970'], ['43649692', '36061.471'], ['43649692', '36039.679'], ['43649688', '36024.868'], ['43649686', '36108.069'], ['43649692', '36041.478']]`

## Candidate counts (after NMS)

- `light switch` (target): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
