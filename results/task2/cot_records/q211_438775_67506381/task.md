# q211_438775_67506381 - visit 438775 / desc 67506381

## Instruction

> Close the left glass door under the TV screen

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "TV screen",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "under",
   "a": "door",
   "b": "TV screen"
  }
 ],
 "select": [
  {
   "on": "door",
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

- `438775/44358170/62317.152`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-7 alternative frames: `[['44358170', '62317.152'], ['44358176', '62260.457'], ['44358176', '62273.452'], ['44358170', '62370.347'], ['44358173', '62385.758'], ['44358173', '62428.557'], ['44358170', '62327.148']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `door` (host): **1**
- `TV screen` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
