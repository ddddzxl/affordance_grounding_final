# q304_466841_4dd5f1bc - visit 466841 / desc 4dd5f1bc

## Instruction

> Open the bottom drawer of the cabinet with the printer on top

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
  },
  {
   "name": "printer",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "drawer"
  },
  {
   "rel": "has_on_top",
   "a": "cabinet",
   "b": "printer"
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

- `466841/47331589/15956.993`  (1920x1440)
- relaxation level **L3**, chosen from 135 frames (stride 10)
- top-4 alternative frames: `[['47331589', '15956.993'], ['47331587', '16007.206'], ['47331591', '16063.300'], ['47331589', '15954.994']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **3**
- `drawer` (host): **0**
- `cabinet` (container): **3**
- `printer` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
