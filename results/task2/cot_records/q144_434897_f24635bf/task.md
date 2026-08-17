# q144_434897_f24635bf - visit 434897 / desc f24635bf

## Instruction

> Plug the device in the one of the sockets next to the mirror

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
   "name": "mirror",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "socket",
   "b": "mirror"
  }
 ],
 "select": [],
 "residual": "'one of the sockets' — any instance satisfying the relation is acceptable"
}
```

## Selected frame

- `434897/42899163/182703.738`  (1440x1920)
- relaxation level **L0**, chosen from 94 frames (stride 10)
- top-6 alternative frames: `[['42899163', '182703.738'], ['42899163', '182691.743'], ['42899163', '182706.737'], ['42899163', '182690.743'], ['42899163', '182704.738'], ['42899163', '182689.744']]`

## Candidate counts (after NMS)

- `socket` (target): **2**
- `mirror` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
