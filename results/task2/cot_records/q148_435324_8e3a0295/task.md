# q148_435324_8e3a0295 - visit 435324 / desc 8e3a0295

## Instruction

> Open the second drawer of the wooden cabinet in the corner

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
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "drawer"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "ordinal",
   "value": null,
   "index": 2,
   "from": null
  }
 ],
 "residual": "'in the corner' is a room-level locator, not groundable"
}
```

## Selected frame

- `435324/42899220/188313.107`  (1920x1440)
- relaxation level **L0**, chosen from 161 frames (stride 10)
- top-3 alternative frames: `[['42899220', '188313.107'], ['42899220', '188272.508'], ['42899221', '188350.009']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **13**
- `drawer` (host): **5**
- `cabinet` (container): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
