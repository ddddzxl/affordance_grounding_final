# q427_468282_9b5e7fa7 - visit 468282 / desc 9b5e7fa7

## Instruction

> Activate the socket between the mirrors

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
   "rel": "between",
   "a": "socket",
   "b": "mirror"
  }
 ],
 "select": [],
 "residual": "'between the mirrors' — both anchors are the same concept 'mirror', so the relation cannot separate them"
}
```

## Selected frame

- `468282/47331279/14259.708`  (1440x1920)
- relaxation level **L0**, chosen from 215 frames (stride 10)
- top-2 alternative frames: `[['47331279', '14259.708'], ['47331281', '14165.013']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `mirror` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
