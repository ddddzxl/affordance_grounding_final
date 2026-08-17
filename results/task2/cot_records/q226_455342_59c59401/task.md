# q226_455342_59c59401 - visit 455342 / desc 59c59401

## Instruction

> Control the volume on the mini music system under the TV stand

## Stage 0 parse

```json
{
 "target": {
  "concept": "volume knob",
  "host": "music system"
 },
 "entities": [
  {
   "name": "volume knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "music system",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "TV stand",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "under",
   "a": "music system",
   "b": "TV stand"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `455342/44358471/46554.396`  (1920x1440)
- relaxation level **L0**, chosen from 97 frames (stride 10)
- top-5 alternative frames: `[['44358471', '46554.396'], ['44358472', '46610.091'], ['44358472', '46627.101'], ['44358472', '46629.100'], ['44358472', '46626.101']]`

## Candidate counts (after NMS)

- `volume knob` (target): **3**
- `music system` (host): **3**
- `TV stand` (landmark): **4**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
