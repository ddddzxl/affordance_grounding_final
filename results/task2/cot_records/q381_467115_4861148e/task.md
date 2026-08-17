# q381_467115_4861148e - visit 467115 / desc 4861148e

## Instruction

> Open the top counter drawer directly under the microwave

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
   "name": "microwave",
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
   "b": "microwave"
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

- `467115/47333308/28099.362`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333308', '28099.362'], ['47333319', '28363.654'], ['47333308', '28026.158'], ['47333310', '28309.760'], ['47333319', '28358.656'], ['47333308', '28018.162'], ['47333310', '28315.757'], ['47333308', '28021.160']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **10**
- `drawer` (host): **7**
- `counter` (container): **3**
- `microwave` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
