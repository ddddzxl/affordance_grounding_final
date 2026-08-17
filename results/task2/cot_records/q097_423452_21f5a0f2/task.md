# q097_423452_21f5a0f2 - visit 423452 / desc 21f5a0f2

## Instruction

> Open the top drawer of the wooden cabinet with the lamp on top

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
   "name": "lamp",
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

- `423452/42897434/104173.339`  (1920x1440)
- relaxation level **L0**, chosen from 309 frames (stride 10)
- top-8 alternative frames: `[['42897434', '104173.339'], ['42897434', '104176.338'], ['42897434', '104174.339'], ['42897434', '104175.339'], ['42897434', '104177.338'], ['42897426', '104131.740'], ['42897434', '104168.341'], ['42897434', '104167.342']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **2**
- `drawer` (host): **2**
- `cabinet` (container): **2**
- `lamp` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
