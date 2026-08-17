# q278_466437_1501d8e7 - visit 466437 / desc 1501d8e7

## Instruction

> Open the rightmost closet door with the built-in mirror

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "closet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "closet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "closet",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "closet",
   "b": "closet door"
  }
 ],
 "select": [
  {
   "on": "closet door",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": "'with the built-in mirror' is a surface attribute of the door, not a separate spatial anchor"
}
```

## Selected frame

- `466437/45260951/6204.312`  (1440x1920)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['45260951', '6204.312'], ['45260952', '6060.919'], ['45260951', '6195.316'], ['45260951', '6193.317'], ['45260951', '6122.311'], ['45260957', '5936.018'], ['45260957', '5930.021'], ['45260952', '6001.909']]`

## Candidate counts (after NMS)

- `door handle` (target): **7**
- `closet door` (host): **4**
- `closet` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
