# q168_437157_05447a27 - visit 437157 / desc 05447a27

## Instruction

> Open the top drawer of the bedside table to the left of the bed

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
   "name": "bed",
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
   "rel": "left_of",
   "a": "bedside table",
   "b": "bed"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "top",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `437157/43649686/36206.280`  (1440x1920)
- relaxation level **L0**, chosen from 239 frames (stride 10)
- top-5 alternative frames: `[['43649686', '36206.280'], ['43649686', '36205.280'], ['43649686', '36197.267'], ['43649686', '36155.567'], ['43649686', '36207.280']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **1**
- `drawer` (host): **1**
- `bedside table` (container): **1**
- `bed` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
