# q056_422356_e41bf377 - visit 422356 / desc e41bf377

## Instruction

> Open the right drawer of the center table

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
   "name": "table",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "table",
   "b": "drawer"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `422356/42446579/205813.464`  (1920x1440)
- relaxation level **L0**, chosen from 115 frames (stride 10)
- top-3 alternative frames: `[['42446579', '205813.464'], ['42446579', '205815.463'], ['42446579', '205814.463']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **1**
- `drawer` (host): **2**
- `table` (container): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
