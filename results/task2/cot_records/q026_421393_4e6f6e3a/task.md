# q026_421393_4e6f6e3a - visit 421393 / desc 4e6f6e3a

## Instruction

> Open the left closet door

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
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "closet",
   "b": "closet door"
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

- `421393/42444924/220970.059`  (1440x1920)
- relaxation level **L0**, chosen from 137 frames (stride 10)
- top-8 alternative frames: `[['42444924', '220970.059'], ['42444924', '220969.060'], ['42444924', '220979.056'], ['42444924', '220975.057'], ['42444924', '220982.054'], ['42444923', '220901.254'], ['42444923', '220903.253'], ['42444923', '220906.169']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `closet door` (host): **3**
- `closet` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
