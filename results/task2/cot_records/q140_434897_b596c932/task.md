# q140_434897_b596c932 - visit 434897 / desc b596c932

## Instruction

> Plug the device in the one of the sockets next to the wooden closet

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
   "name": "closet",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "socket",
   "b": "closet"
  }
 ],
 "select": [],
 "residual": "'one of the sockets' — any instance satisfying the relation is acceptable"
}
```

## Selected frame

- `434897/42899163/182706.737`  (1440x1920)
- relaxation level **L0**, chosen from 94 frames (stride 10)
- top-1 alternative frames: `[['42899163', '182706.737']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `closet` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
