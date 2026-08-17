# q275_466162_f23d6d03 - visit 466162 / desc f23d6d03

## Instruction

> Open the left blue closet door near the window

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
   "value": "left",
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
- top-8 alternative frames: `[['44796576', '16714.287'], ['44796579', '16778.593'], ['44796579', '16779.593'], ['44796576', '16715.286'], ['44796575', '16892.180'], ['44796575', '16889.181'], ['44796575', '16888.181'], ['44796579', '16782.592']]`

## Candidate counts (after NMS)

- `door handle` (target): **4**
- `closet door` (host): **2**
- `closet` (container): **1**
- `window` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
