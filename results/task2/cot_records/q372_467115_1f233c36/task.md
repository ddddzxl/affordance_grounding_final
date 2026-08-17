# q372_467115_1f233c36 - visit 467115 / desc 1f233c36

## Instruction

> Open the counter door directly under the kitchen sink

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
   "name": "sink",
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
   "b": "sink"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333310/28301.763`  (1440x1920)
- relaxation level **L3**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333310', '28301.763'], ['47333319', '28400.656'], ['47333319', '28372.667'], ['47333319', '28398.657'], ['47333308', '28042.269'], ['47333319', '28392.659'], ['47333319', '28399.656'], ['47333319', '28394.658']]`

## Candidate counts (after NMS)

- `door handle` (target): **8**
- `counter door` (host): **0**
- `counter` (container): **5**
- `sink` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
