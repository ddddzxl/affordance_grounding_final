# q170_437157_163b76b3 - visit 437157 / desc 163b76b3

## Instruction

> Open the drawer of the bedside table with the telephone on top

## Stage 0 parse

```json
{
 "target": {
  "concept": "drawer handle",
  "host": "drawer"
 },
 "entities": [
  {
   "name": "drawer handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "drawer",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "bedside table",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "telephone",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "bedside table",
   "b": "drawer"
  },
  {
   "rel": "has_on_top",
   "a": "bedside table",
   "b": "telephone"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `437157/43649686/36162.281`  (1440x1920)
- relaxation level **L0**, chosen from 239 frames (stride 10)
- top-8 alternative frames: `[['43649686', '36162.281'], ['43649686', '36160.565'], ['43649686', '36158.565'], ['43649686', '36159.565'], ['43649686', '36163.280'], ['43649686', '36157.566'], ['43649686', '36156.566'], ['43649686', '36152.568']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **1**
- `drawer` (host): **1**
- `bedside table` (container): **1**
- `telephone` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
