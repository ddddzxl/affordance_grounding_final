# q373_467115_212b657b - visit 467115 / desc 212b657b

## Instruction

> Open the bottom counter drawer directly under the teacups

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
   "value": "bottom",
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
- top-6 alternative frames: `[['47333319', '28363.654'], ['47333308', '28026.158'], ['47333308', '28027.158'], ['47333310', '28294.766'], ['47333319', '28398.657'], ['47333319', '28396.657']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **4**
- `drawer` (host): **5**
- `counter` (container): **1**
- `teacups` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
