# q006_421254_609f3c02 - visit 421254 / desc 609f3c02

## Instruction

> Unplug the TV from the power supply

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": null
 },
 "entities": [
  {
   "name": "plug",
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
   "rel": "near",
   "a": "plug",
   "b": "TV"
  }
 ],
 "select": [],
 "residual": "'power supply' is generic; the plug is inferred to be the TV's"
}
```

## Selected frame

- `421254/42444754/81018.476`  (1440x1920)
- relaxation level **L0**, chosen from 170 frames (stride 10)
- top-1 alternative frames: `[['42444754', '81018.476']]`

## Candidate counts (after NMS)

- `plug` (target): **1**
- `TV` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
