# q025_421393_3e2820ab - visit 421393 / desc 3e2820ab

## Instruction

> Open the right closet door

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
   "value": "right",
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
- top-8 alternative frames: `[['42444924', '220970.059'], ['42444924', '220969.060'], ['42444924', '220974.058'], ['42444924', '221012.159'], ['42444923', '220901.254'], ['42444923', '220896.256'], ['42444923', '220897.256'], ['42444924', '220971.059']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `closet door` (host): **3**
- `closet` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
