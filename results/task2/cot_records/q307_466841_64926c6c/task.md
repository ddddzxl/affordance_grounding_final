# q307_466841_64926c6c - visit 466841 / desc 64926c6c

## Instruction

> Open the third drawer of the cabinet with the bird cage and the toys on top

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
   "name": "bird cage",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "toys",
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
   "b": "bird cage"
  },
  {
   "rel": "has_on_top",
   "a": "cabinet",
   "b": "toys"
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

- `466841/47331589/15931.004`  (1920x1440)
- relaxation level **L1**, chosen from 135 frames (stride 10)
- top-1 alternative frames: `[['47331589', '15931.004']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **5**
- `drawer` (host): **7**
- `cabinet` (container): **5**
- `bird cage` (landmark): **2**
- `toys` (landmark): **14**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
