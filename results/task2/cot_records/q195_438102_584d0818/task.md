# q195_438102_584d0818 - visit 438102 / desc 584d0818

## Instruction

> Open the under bed storage drawer

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
   "name": "bed",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "under",
   "a": "drawer",
   "b": "bed"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `438102/43896249/7572.099`  (1920x1440)
- relaxation level **L0**, chosen from 193 frames (stride 10)
- top-5 alternative frames: `[['43896249', '7572.099'], ['43896244', '7697.797'], ['43896244', '7699.796'], ['43896244', '7701.795'], ['43896244', '7636.306']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **7**
- `drawer` (host): **3**
- `bed` (landmark): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
