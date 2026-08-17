# q404_467115_d7e39642 - visit 467115 / desc d7e39642

## Instruction

> Open the bottom counter door directly under the microwave

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "counter door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "counter door",
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
   "b": "counter door"
  },
  {
   "rel": "under",
   "a": "counter door",
   "b": "microwave"
  }
 ],
 "select": [
  {
   "on": "counter door",
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

- `467115/47333308/28021.160`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-2 alternative frames: `[['47333308', '28021.160'], ['47333319', '28355.657']]`

## Candidate counts (after NMS)

- `door handle` (target): **7**
- `counter door` (host): **5**
- `counter` (container): **2**
- `microwave` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
