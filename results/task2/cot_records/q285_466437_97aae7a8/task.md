# q285_466437_97aae7a8 - visit 466437 / desc 97aae7a8

## Instruction

> Open the left drawer of the wooden valet stand

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
   "name": "valet stand",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "valet stand",
   "b": "drawer"
  }
 ],
 "select": [
  {
   "on": "drawer",
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

- `466437/45260957/5944.115`  (1440x1920)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['45260957', '5944.115'], ['45260951', '6140.121'], ['45260952', '6016.120'], ['45260952', '6017.120'], ['45260951', '6141.121'], ['45260951', '6142.120'], ['45260951', '6138.122'], ['45260951', '6145.119']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **5**
- `drawer` (host): **2**
- `valet stand` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
