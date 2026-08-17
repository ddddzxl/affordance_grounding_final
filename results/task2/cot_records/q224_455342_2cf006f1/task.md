# q224_455342_2cf006f1 - visit 455342 / desc 2cf006f1

## Instruction

> Open the middle drawer of the wooden TV stand

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
   "name": "TV stand",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "TV stand",
   "b": "drawer"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "horizontal",
   "value": "middle",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `455342/44358472/46611.090`  (1920x1440)
- relaxation level **L0**, chosen from 97 frames (stride 10)
- top-8 alternative frames: `[['44358472', '46611.090'], ['44358471', '46556.395'], ['44358472', '46614.089'], ['44358471', '46586.300'], ['44358472', '46607.092'], ['44358472', '46608.091'], ['44358471', '46550.398'], ['44358471', '46572.989']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **3**
- `drawer` (host): **3**
- `TV stand` (container): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
