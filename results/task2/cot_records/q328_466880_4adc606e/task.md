# q328_466880_4adc606e - visit 466880 / desc 4adc606e

## Instruction

> Open the cabinet door directly above the microwave

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
   "name": "microwave",
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
   "rel": "above",
   "a": "cabinet door",
   "b": "microwave"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466880/47331711/11318.836`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-5 alternative frames: `[['47331711', '11318.836'], ['47331707', '11127.830'], ['47331711', '11260.726'], ['47331710', '11231.238'], ['47331710', '11228.239']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `cabinet door` (host): **7**
- `cabinet` (container): **5**
- `microwave` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
