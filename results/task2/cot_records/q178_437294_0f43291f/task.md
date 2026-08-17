# q178_437294_0f43291f - visit 437294 / desc 0f43291f

## Instruction

> Open to the left window above the radiator

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
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `437294/43649767/52372.053`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-8 alternative frames: `[['43649767', '52372.053'], ['43649767', '52392.044'], ['43649762', '52548.846'], ['43649762', '52546.847'], ['43649767', '52388.046'], ['43649762', '52547.846'], ['43649767', '52393.144'], ['43649763', '52431.145']]`

## Candidate counts (after NMS)

- `window handle` (target): **4**
- `window` (host): **2**
- `radiator` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
