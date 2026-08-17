# q201_438102_cd9901ab - visit 438102 / desc cd9901ab

## Instruction

> Open the top right cabinet drawer with the globe on top

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
   "value": "top",
   "index": null,
   "from": null
  },
  {
   "on": "drawer",
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

- `438102/43896244/7649.300`  (1920x1440)
- relaxation level **L0**, chosen from 193 frames (stride 10)
- top-6 alternative frames: `[['43896244', '7649.300'], ['43896247', '7616.597'], ['43896247', '7615.598'], ['43896249', '7566.102'], ['43896247', '7608.601'], ['43896244', '7648.301']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **5**
- `drawer` (host): **5**
- `cabinet` (container): **1**
- `globe` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
