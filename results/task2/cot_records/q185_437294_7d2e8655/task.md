# q185_437294_7d2e8655 - visit 437294 / desc 7d2e8655

## Instruction

> Open the right door of the closet near the window

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

- `437294/43649767/52372.053`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-8 alternative frames: `[['43649767', '52372.053'], ['43649763', '52433.144'], ['43649763', '52431.145'], ['43649762', '52547.846'], ['43649767', '52389.046'], ['43649767', '52391.045'], ['43649762', '52546.847'], ['43649767', '52392.044']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `closet door` (host): **2**
- `closet` (container): **1**
- `window` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
