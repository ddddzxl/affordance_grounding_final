# q200_438102_c505333e - visit 438102 / desc c505333e

## Instruction

> Open the third cabinet drawer with the globe on top

## Stage 0 parse

```json
{
 "target": {
  "concept": "drawer handle",
  "host": "drawer"
 },
 "entities": [
  {
   "name": "drawer handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "drawer",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "globe",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "drawer"
  },
  {
   "rel": "has_on_top",
   "a": "cabinet",
   "b": "globe"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "ordinal",
   "value": null,
   "index": 3,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `438102/43896247/7608.601`  (1920x1440)
- relaxation level **L0**, chosen from 193 frames (stride 10)
- top-2 alternative frames: `[['43896247', '7608.601'], ['43896249', '7566.102']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **9**
- `drawer` (host): **8**
- `cabinet` (container): **3**
- `globe` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
