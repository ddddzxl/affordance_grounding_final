# q408_467115_f84ded76 - visit 467115 / desc f84ded76

## Instruction

> Open the top counter drawer directly under the teacups

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
   "name": "counter",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "teacups",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "counter",
   "b": "drawer"
  },
  {
   "rel": "under",
   "a": "drawer",
   "b": "teacups"
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

- `467115/47333319/28363.654`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333319', '28363.654'], ['47333308', '28026.158'], ['47333319', '28371.668'], ['47333310', '28293.766'], ['47333319', '28394.658'], ['47333319', '28393.659'], ['47333310', '28294.766'], ['47333319', '28398.657']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **4**
- `drawer` (host): **5**
- `counter` (container): **1**
- `teacups` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
