# q388_467115_6aba2172 - visit 467115 / desc 6aba2172

## Instruction

> Open the fridge

## Stage 0 parse

```json
{
 "target": {
  "concept": "fridge handle",
  "host": "fridge"
 },
 "entities": [
  {
   "name": "fridge handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "fridge",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333310/28221.562`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333310', '28221.562'], ['47333308', '28013.164'], ['47333308', '28098.362'], ['47333319', '28500.865'], ['47333308', '28099.362'], ['47333319', '28501.864'], ['47333310', '28219.563'], ['47333319', '28348.660']]`

## Candidate counts (after NMS)

- `fridge handle` (target): **9**
- `fridge` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
