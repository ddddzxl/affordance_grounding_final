# q440_468476_90bbb7bd - visit 468476 / desc 90bbb7bd

## Instruction

> Open the left cabinet door under the TV

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "cabinet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "cabinet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "TV",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "cabinet door"
  },
  {
   "rel": "under",
   "a": "cabinet door",
   "b": "TV"
  }
 ],
 "select": [
  {
   "on": "cabinet door",
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

- `468476/45261686/3806.463`  (1440x1920)
- relaxation level **L0**, chosen from 222 frames (stride 10)
- top-8 alternative frames: `[['45261686', '3806.463'], ['45261681', '3607.062'], ['45261686', '3805.463'], ['45261681', '3608.062'], ['45261686', '3807.462'], ['45261682', '3535.475'], ['45261682', '3553.568'], ['45261686', '3828.470']]`

## Candidate counts (after NMS)

- `door handle` (target): **4**
- `cabinet door` (host): **2**
- `cabinet` (container): **3**
- `TV` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
