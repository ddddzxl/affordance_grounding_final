# q242_466092_7891492c - visit 466092 / desc 7891492c

## Instruction

> Open the window behind the table with the flower vase

## Stage 0 parse

```json
{
 "target": {
  "concept": "window handle",
  "host": "window"
 },
 "entities": [
  {
   "name": "window handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "table",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "flower vase",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "behind",
   "a": "window",
   "b": "table"
  },
  {
   "rel": "has_on_top",
   "a": "table",
   "b": "flower vase"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466092/44796562/15980.398`  (1920x1440)
- relaxation level **L1**, chosen from 179 frames (stride 10)
- top-2 alternative frames: `[['44796562', '15980.398'], ['44796562', '15983.396']]`

## Candidate counts (after NMS)

- `window handle` (target): **5**
- `window` (host): **5**
- `table` (landmark): **2**
- `flower vase` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
