# q376_467115_31d64faf - visit 467115 / desc 31d64faf

## Instruction

> Plug the device in the socket to the right of the couch

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
   "name": "couch",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "right_of",
   "a": "socket",
   "b": "couch"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333308/28142.361`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-1 alternative frames: `[['47333308', '28142.361']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `couch` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
