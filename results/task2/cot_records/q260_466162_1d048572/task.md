# q260_466162_1d048572 - visit 466162 / desc 1d048572

## Instruction

> Open the bottom drawer of the blue closet near the window

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
   "name": "closet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "closet",
   "b": "drawer"
  },
  {
   "rel": "near",
   "a": "closet",
   "b": "window"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "bottom",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `466162/44796576/16714.287`  (1920x1440)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['44796576', '16714.287'], ['44796575', '16888.181'], ['44796579', '16782.592'], ['44796579', '16781.592'], ['44796579', '16779.593'], ['44796576', '16711.288'], ['44796579', '16787.590'], ['44796579', '16777.594']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **4**
- `drawer` (host): **1**
- `closet` (container): **1**
- `window` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
