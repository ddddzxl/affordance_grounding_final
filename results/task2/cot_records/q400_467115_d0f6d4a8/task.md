# q400_467115_d0f6d4a8 - visit 467115 / desc d0f6d4a8

## Instruction

> Plug the device in one of the sockets next to the dish drainer

## Stage 0 parse

```json
{
 "target": {
  "concept": "socket",
  "host": null
 },
 "entities": [
  {
   "name": "socket",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "dish drainer",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "socket",
   "b": "dish drainer"
  }
 ],
 "select": [],
 "residual": "'one of the sockets' — any instance satisfying the relation is acceptable"
}
```

## Selected frame

- `467115/47333310/28288.768`  (1440x1920)
- relaxation level **L3**, chosen from 608 frames (stride 10)
- top-2 alternative frames: `[['47333310', '28288.768'], ['47333308', '28047.267']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `dish drainer` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
