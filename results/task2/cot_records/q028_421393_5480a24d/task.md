# q028_421393_5480a24d - visit 421393 / desc 5480a24d

## Instruction

> Open the bottom drawer of the nightstand

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
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "nightstand",
   "b": "drawer"
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

- `421393/42444923/220905.152`  (1440x1920)
- relaxation level **L0**, chosen from 137 frames (stride 10)
- top-4 alternative frames: `[['42444923', '220905.152'], ['42444924', '220990.168'], ['42444923', '220913.166'], ['42444923', '220914.165']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **6**
- `drawer` (host): **4**
- `nightstand` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
