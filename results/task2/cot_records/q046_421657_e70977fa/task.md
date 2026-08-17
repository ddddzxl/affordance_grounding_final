# q046_421657_e70977fa - visit 421657 / desc e70977fa

## Instruction

> Turn on the table lamp on the nightstand next to the closet

## Stage 0 parse

```json
{
 "target": {
  "concept": "light switch",
  "host": "table lamp"
 },
 "entities": [
  {
   "name": "light switch",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "table lamp",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "nightstand",
   "role": "container",
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
   "rel": "on_top",
   "a": "table lamp",
   "b": "nightstand"
  },
  {
   "rel": "next_to",
   "a": "nightstand",
   "b": "closet"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `421657/42445642/58232.491`  (1920x1440)
- relaxation level **POOL-T**, chosen from 165 frames (stride 10)
- top-5 alternative frames: `[['42445642', '58232.491'], ['42445633', '58089.301'], ['42445639', '58298.014'], ['42445639', '58352.092'], ['42445639', '58333.883']]`

## Candidate counts (after NMS)

- `light switch` (target): **1**
- `table lamp` (host): **2**
- `nightstand` (container): **2**
- `closet` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
