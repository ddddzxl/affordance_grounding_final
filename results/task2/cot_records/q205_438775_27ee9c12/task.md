# q205_438775_27ee9c12 - visit 438775 / desc 27ee9c12

## Instruction

> Open the top drawer of the cabinet located on the left side of the couch

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
   "name": "couch",
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
   "rel": "left_of",
   "a": "cabinet",
   "b": "couch"
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

- `438775/44358176/62241.448`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-3 alternative frames: `[['44358176', '62241.448'], ['44358170', '62310.154'], ['44358170', '62311.154']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **5**
- `drawer` (host): **4**
- `cabinet` (container): **6**
- `couch` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
