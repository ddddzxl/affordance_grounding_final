# q176_437294_037f432a - visit 437294 / desc 037f432a

## Instruction

> Open the top drawer of the nightstand with the lamp on top

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
   "name": "lamp",
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
   "b": "lamp"
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

- `437294/43649767/52398.358`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-4 alternative frames: `[['43649767', '52398.358'], ['43649767', '52397.359'], ['43649767', '52393.144'], ['43649762', '52549.846']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **2**
- `drawer` (host): **3**
- `nightstand` (container): **1**
- `lamp` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
