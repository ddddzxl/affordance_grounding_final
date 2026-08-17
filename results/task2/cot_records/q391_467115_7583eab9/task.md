# q391_467115_7583eab9 - visit 467115 / desc 7583eab9

## Instruction

> Open the bottom counter door directly under the electric kettle

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
   "name": "electric kettle",
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
   "b": "electric kettle"
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

- `467115/47333310/28303.762`  (1440x1920)
- relaxation level **L3**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333310', '28303.762'], ['47333310', '28301.763'], ['47333308', '28032.156'], ['47333319', '28371.668'], ['47333310', '28315.757'], ['47333319', '28374.666'], ['47333319', '28392.659'], ['47333319', '28394.658']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `counter door` (host): **0**
- `counter` (container): **2**
- `electric kettle` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
