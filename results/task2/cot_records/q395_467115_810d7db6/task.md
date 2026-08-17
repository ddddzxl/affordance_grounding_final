# q395_467115_810d7db6 - visit 467115 / desc 810d7db6

## Instruction

> Open the top counter drawer directly under the electric kettle

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
   "name": "electric kettle",
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
   "b": "electric kettle"
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

- `467115/47333310/28301.763`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-7 alternative frames: `[['47333310', '28301.763'], ['47333310', '28303.762'], ['47333319', '28392.659'], ['47333319', '28384.662'], ['47333319', '28393.659'], ['47333308', '28039.270'], ['47333319', '28385.662']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **5**
- `drawer` (host): **5**
- `counter` (container): **5**
- `electric kettle` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
