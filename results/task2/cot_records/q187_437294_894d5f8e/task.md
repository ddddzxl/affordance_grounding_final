# q187_437294_894d5f8e - visit 437294 / desc 894d5f8e

## Instruction

> Open the left door of the closet near the window

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

- `437294/43649763/52433.144`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-4 alternative frames: `[['43649763', '52433.144'], ['43649767', '52372.053'], ['43649763', '52431.145'], ['43649767', '52389.046']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `closet door` (host): **2**
- `closet` (container): **1**
- `window` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
