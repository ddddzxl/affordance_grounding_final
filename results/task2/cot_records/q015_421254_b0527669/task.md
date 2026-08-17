# q015_421254_b0527669 - visit 421254 / desc b0527669

## Instruction

> Open the first drawer of the nightstand with the red table lamp on top

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
   "name": "table lamp",
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
   "rel": "has_on_top",
   "a": "nightstand",
   "b": "table lamp"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "ordinal",
   "value": null,
   "index": 1,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `421254/42444754/80977.876`  (1440x1920)
- relaxation level **L0**, chosen from 170 frames (stride 10)
- top-6 alternative frames: `[['42444754', '80977.876'], ['42444754', '80976.876'], ['42444755', '80848.679'], ['42444755', '80841.681'], ['42444758', '80907.371'], ['42444758', '80919.183']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **3**
- `drawer` (host): **3**
- `nightstand` (container): **1**
- `table lamp` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
