# q371_467115_1632fe22 - visit 467115 / desc 1632fe22

## Instruction

> Open the cabinet door directly to the right of the range hood

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
   "name": "range hood",
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
   "rel": "right_of",
   "a": "cabinet door",
   "b": "range hood"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333308/28030.157`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-3 alternative frames: `[['47333308', '28030.157'], ['47333319', '28386.661'], ['47333310', '28260.763']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `cabinet door` (host): **2**
- `cabinet` (container): **2**
- `range hood` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
