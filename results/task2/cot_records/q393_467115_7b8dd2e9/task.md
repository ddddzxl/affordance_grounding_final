# q393_467115_7b8dd2e9 - visit 467115 / desc 7b8dd2e9

## Instruction

> Select a function on the kitchen range hood

## Stage 0 parse

```json
{
 "target": {
  "concept": "range hood panel",
  "host": "range hood"
 },
 "entities": [
  {
   "name": "range hood panel",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "range hood",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "no disambiguating cue — any of the range hood controls is acceptable"
}
```

## Selected frame

- `467115/47333308/28094.364`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333308', '28094.364'], ['47333319', '28371.668'], ['47333319', '28410.652'], ['47333319', '28385.662'], ['47333319', '28386.661'], ['47333310', '28300.763'], ['47333319', '28540.265'], ['47333310', '28204.553']]`

## Candidate counts (after NMS)

- `range hood panel` (target): **2**
- `range hood` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
