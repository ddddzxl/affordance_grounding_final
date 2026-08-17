# q005_421254_55b56254 - visit 421254 / desc 55b56254

## Instruction

> Open the bottom drawer of the nightstand with the red table lamp on top

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

- `421254/42444754/80977.876`  (1440x1920)
- relaxation level **L0**, chosen from 170 frames (stride 10)
- top-8 alternative frames: `[['42444754', '80977.876'], ['42444754', '80976.876'], ['42444755', '80848.679'], ['42444755', '80841.681'], ['42444755', '80854.676'], ['42444758', '80920.183'], ['42444754', '80986.872'], ['42444758', '80907.371']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **3**
- `drawer` (host): **3**
- `nightstand` (container): **1**
- `table lamp` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
