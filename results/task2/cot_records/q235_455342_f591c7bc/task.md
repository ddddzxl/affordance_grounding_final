# q235_455342_f591c7bc - visit 455342 / desc f591c7bc

## Instruction

> Open the right drawer of the wooden TV stand

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
   "name": "TV stand",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "TV stand",
   "b": "drawer"
  }
 ],
 "select": [
  {
   "on": "drawer",
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

- `455342/44358471/46592.298`  (1920x1440)
- relaxation level **L0**, chosen from 97 frames (stride 10)
- top-8 alternative frames: `[['44358471', '46592.298'], ['44358472', '46655.389'], ['44358472', '46615.089'], ['44358471', '46590.299'], ['44358471', '46570.990'], ['44358472', '46637.097'], ['44358472', '46611.090'], ['44358471', '46572.989']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **2**
- `drawer` (host): **5**
- `TV stand` (container): **4**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
