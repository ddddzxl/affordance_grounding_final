# q192_437294_e4da865c - visit 437294 / desc e4da865c

## Instruction

> Open the right window above the radiator

## Stage 0 parse

```json
{
 "target": {
  "concept": "window handle",
  "host": "window"
 },
 "entities": [
  {
   "name": "window handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "radiator",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "above",
   "a": "window",
   "b": "radiator"
  }
 ],
 "select": [
  {
   "on": "window",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `437294/43649762/52548.846`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-8 alternative frames: `[['43649762', '52548.846'], ['43649762', '52546.847'], ['43649767', '52377.051'], ['43649767', '52388.046'], ['43649767', '52387.046'], ['43649767', '52393.144'], ['43649762', '52525.856'], ['43649767', '52372.053']]`

## Candidate counts (after NMS)

- `window handle` (target): **1**
- `window` (host): **2**
- `radiator` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
