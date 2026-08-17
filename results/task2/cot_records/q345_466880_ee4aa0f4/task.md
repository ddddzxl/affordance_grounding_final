# q345_466880_ee4aa0f4 - visit 466880 / desc ee4aa0f4

## Instruction

> Open the top drawer of the white cabinet under the telephone mounted on the wall

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
   "name": "telephone",
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
   "rel": "under",
   "a": "cabinet",
   "b": "telephone"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "top",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `466880/47331707/11162.133`  (1920x1440)
- relaxation level **L2**, chosen from 179 frames (stride 10)
- top-1 alternative frames: `[['47331707', '11162.133']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **3**
- `drawer` (host): **2**
- `cabinet` (container): **3**
- `telephone` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
