# q194_438102_43e0f3a2 - visit 438102 / desc 43e0f3a2

## Instruction

> Open the bottom cabinet drawer with the globe on top

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
   "axis": "vertical",
   "value": "bottom",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `438102/43896249/7563.103`  (1920x1440)
- relaxation level **L0**, chosen from 193 frames (stride 10)
- top-3 alternative frames: `[['43896249', '7563.103'], ['43896249', '7566.102'], ['43896247', '7608.601']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **8**
- `drawer` (host): **6**
- `cabinet` (container): **1**
- `globe` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
