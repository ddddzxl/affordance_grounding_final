# q102_423452_9b3a2dbf - visit 423452 / desc 9b3a2dbf

## Instruction

> Turn on the TV using one of the remotes in front of the TV

## Stage 0 parse

```json
{
 "target": {
  "concept": "remote control",
  "host": null
 },
 "entities": [
  {
   "name": "remote control",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "TV",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "in_front_of",
   "a": "remote control",
   "b": "TV"
  }
 ],
 "select": [],
 "residual": "'one of the remotes' - any instance is acceptable | independent check on the train split (val untouched): handheld-device GT median 478 points vs 87-108 for fixed-furniture handles, a factor of 4.4-5.5 -> the annotation covers the whole device"
}
```

## Selected frame

- `423452/42897434/104280.445`  (1920x1440)
- relaxation level **L0**, chosen from 309 frames (stride 10)
- top-8 alternative frames: `[['42897434', '104280.445'], ['42897426', '104116.746'], ['42897434', '104288.441'], ['42897422', '104003.143'], ['42897434', '104289.441'], ['42897434', '104287.442'], ['42897422', '104064.235'], ['42897426', '104117.746']]`

## Candidate counts (after NMS)

- `remote control` (target): **8**
- `TV` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
