# q033_421393_a30d9276 - visit 421393 / desc a30d9276

## Instruction

> Plug the device in the right socket between the radiator and the closet

## Stage 0 parse

```json
{
 "target": {
  "concept": "socket",
  "host": null
 },
 "entities": [
  {
   "name": "socket",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "radiator",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "closet",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "between",
   "a": "socket",
   "b": "radiator"
  },
  {
   "rel": "between",
   "a": "socket",
   "b": "closet"
  }
 ],
 "select": [
  {
   "on": "socket",
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

- `421393/42444923/220895.256`  (1440x1920)
- relaxation level **L1**, chosen from 137 frames (stride 10)
- top-2 alternative frames: `[['42444923', '220895.256'], ['42444923', '220894.257']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `radiator` (landmark): **1**
- `closet` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
