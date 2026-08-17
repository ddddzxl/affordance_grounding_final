# q269_466162_a9d2acb5 - visit 466162 / desc a9d2acb5

## Instruction

> Open the right blue closet door near the window

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "closet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "closet door",
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
   "b": "closet door"
  },
  {
   "rel": "near",
   "a": "closet",
   "b": "window"
  }
 ],
 "select": [
  {
   "on": "closet door",
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

- `466162/44796579/16778.593`  (1920x1440)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['44796579', '16778.593'], ['44796575', '16889.181'], ['44796576', '16714.287'], ['44796575', '16888.181'], ['44796579', '16782.592'], ['44796579', '16781.592'], ['44796579', '16779.593'], ['44796579', '16788.589']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `closet door` (host): **2**
- `closet` (container): **1**
- `window` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
