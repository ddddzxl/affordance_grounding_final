# q296_466437_e225590d - visit 466437 / desc e225590d

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

- `466437/45260951/6208.311`  (1440x1920)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['45260951', '6208.311'], ['45260951', '6158.114'], ['45260951', '6207.311'], ['45260952', '6053.922'], ['45260957', '5984.516'], ['45260957', '5985.515'], ['45260952', '6030.114'], ['45260951', '6191.317']]`

## Candidate counts (after NMS)

- `light switch` (target): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
