# q385_467115_5ebfe643 - visit 467115 / desc 5ebfe643

## Instruction

> Unplug the table lamp on the side table next to the couch

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": "table lamp"
 },
 "entities": [
  {
   "name": "plug",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "table lamp",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "side table",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "couch",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "table lamp",
   "b": "side table"
  },
  {
   "rel": "next_to",
   "a": "side table",
   "b": "couch"
  }
 ],
 "select": [],
 "residual": "the plug sits at the socket end, not on the lamp"
}
```

## Selected frame

- `467115/47333310/28170.966`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-3 alternative frames: `[['47333310', '28170.966'], ['47333319', '28609.553'], ['47333310', '28164.969']]`

## Candidate counts (after NMS)

- `plug` (target): **3**
- `table lamp` (host): **2**
- `side table` (container): **2**
- `couch` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
