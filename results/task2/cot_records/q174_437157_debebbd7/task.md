# q174_437157_debebbd7 - visit 437157 / desc debebbd7

## Instruction

> Open the right closet door next to the nightstand

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
   "name": "nightstand",
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
   "rel": "next_to",
   "a": "closet",
   "b": "nightstand"
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

- `437157/43649686/36212.278`  (1440x1920)
- relaxation level **L0**, chosen from 239 frames (stride 10)
- top-3 alternative frames: `[['43649686', '36212.278'], ['43649686', '36140.573'], ['43649688', '36008.075']]`

## Candidate counts (after NMS)

- `door handle` (target): **4**
- `closet door` (host): **2**
- `closet` (container): **1**
- `nightstand` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
