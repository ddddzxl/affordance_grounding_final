# q002_421254_4668a5f5 - visit 421254 / desc 4668a5f5

## Instruction

> Open the right window behind the shutters

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
   "name": "shutters",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "behind",
   "a": "window",
   "b": "shutters"
  }
 ],
 "select": [
  {
   "on": "window",
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

- `421254/42444758/80941.174`  (1440x1920)
- relaxation level **L0**, chosen from 170 frames (stride 10)
- top-8 alternative frames: `[['42444758', '80941.174'], ['42444758', '80942.174'], ['42444755', '80863.672'], ['42444755', '80864.672'], ['42444754', '81009.279'], ['42444754', '81006.281'], ['42444755', '80865.672'], ['42444754', '81011.279']]`

## Candidate counts (after NMS)

- `window handle` (target): **3**
- `window` (host): **1**
- `shutters` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
