# q043_421657_a831b29a - visit 421657 / desc a831b29a

## Instruction

> Open the bottom drawer of the blue nightstand to the right of the bed

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
   "name": "nightstand",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "bed",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "nightstand",
   "b": "drawer"
  },
  {
   "rel": "right_of",
   "a": "nightstand",
   "b": "bed"
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

- `421657/42445633/58089.301`  (1920x1440)
- relaxation level **L0**, chosen from 165 frames (stride 10)
- top-6 alternative frames: `[['42445633', '58089.301'], ['42445639', '58300.996'], ['42445633', '58091.300'], ['42445633', '58093.299'], ['42445639', '58298.014'], ['42445642', '58232.491']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **5**
- `drawer` (host): **4**
- `nightstand` (container): **2**
- `bed` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
