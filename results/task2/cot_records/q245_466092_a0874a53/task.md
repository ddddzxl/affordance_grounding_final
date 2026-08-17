# q245_466092_a0874a53 - visit 466092 / desc a0874a53

## Instruction

> Open the left drawer of the desk with the laptop on top

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
   "name": "desk",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "laptop",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "desk",
   "b": "drawer"
  },
  {
   "rel": "has_on_top",
   "a": "desk",
   "b": "laptop"
  }
 ],
 "select": [
  {
   "on": "drawer",
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

- `466092/44796562/16011.402`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-6 alternative frames: `[['44796562', '16011.402'], ['44796568', '16125.204'], ['44796568', '16120.990'], ['44796568', '16122.989'], ['44796568', '16119.990'], ['44796568', '16121.989']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **2**
- `drawer` (host): **1**
- `desk` (container): **1**
- `laptop` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
