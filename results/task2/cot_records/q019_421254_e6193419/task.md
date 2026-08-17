# q019_421254_e6193419 - visit 421254 / desc e6193419

## Instruction

> Turn on the ceiling light using the switch next to the TV

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
  },
  {
   "name": "TV",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "light switch",
   "b": "TV"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `421254/42444758/80953.586`  (1440x1920)
- relaxation level **L0**, chosen from 170 frames (stride 10)
- top-1 alternative frames: `[['42444758', '80953.586']]`

## Candidate counts (after NMS)

- `light switch` (target): **1**
- `TV` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
