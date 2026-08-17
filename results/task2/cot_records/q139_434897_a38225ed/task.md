# q139_434897_a38225ed - visit 434897 / desc a38225ed

## Instruction

> Open the left door of the wooden closet

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

- `434897/42899163/182723.147`  (1440x1920)
- relaxation level **L0**, chosen from 94 frames (stride 10)
- top-8 alternative frames: `[['42899163', '182723.147'], ['42899163', '182721.131'], ['42899163', '182724.146'], ['42899163', '182680.731'], ['42899165', '182826.437'], ['42899165', '182807.545'], ['42899165', '182870.136'], ['42899163', '182725.146']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `closet door` (host): **4**
- `closet` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
