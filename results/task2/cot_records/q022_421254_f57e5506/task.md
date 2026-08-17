# q022_421254_f57e5506 - visit 421254 / desc f57e5506

## Instruction

> Turn on the red table lamp next to the bed

## Stage 0 parse

```json
{
 "target": {
  "concept": "light switch",
  "host": "table lamp"
 },
 "entities": [
  {
   "name": "light switch",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "table lamp",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "bed",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "table lamp",
   "b": "bed"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `421254/42444758/80907.371`  (1440x1920)
- relaxation level **L1**, chosen from 170 frames (stride 10)
- top-3 alternative frames: `[['42444758', '80907.371'], ['42444758', '80915.185'], ['42444758', '80921.182']]`

## Candidate counts (after NMS)

- `light switch` (target): **1**
- `table lamp` (host): **2**
- `bed` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
