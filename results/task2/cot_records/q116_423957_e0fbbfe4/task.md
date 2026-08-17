# q116_423957_e0fbbfe4 - visit 423957 / desc e0fbbfe4

## Instruction

> Open the right door of the closet next to the radiator

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
   "name": "radiator",
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
   "b": "radiator"
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

- `423957/42898343/508273.525`  (1920x1440)
- relaxation level **L0**, chosen from 106 frames (stride 10)
- top-4 alternative frames: `[['42898343', '508273.525'], ['42898343', '508278.523'], ['42898343', '508281.522'], ['42898343', '508276.524']]`

## Candidate counts (after NMS)

- `door handle` (target): **4**
- `closet door` (host): **3**
- `closet` (container): **1**
- `radiator` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
