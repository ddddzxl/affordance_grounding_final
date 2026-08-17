# q286_466437_9bf8909e - visit 466437 / desc 9bf8909e

## Instruction

> Adjust the temperature using the radiator dial next to the bathroom door

## Stage 0 parse

```json
{
 "target": {
  "concept": "radiator knob",
  "host": null
 },
 "entities": [
  {
   "name": "radiator knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "radiator knob",
   "b": "door"
  }
 ],
 "select": [],
 "residual": "'bathroom door' uses a room name to pick the door; treated as an unqualified door"
}
```

## Selected frame

- `466437/45260951/6142.120`  (1440x1920)
- relaxation level **L1**, chosen from 257 frames (stride 10)
- top-2 alternative frames: `[['45260951', '6142.120'], ['45260957', '5960.109']]`

## Candidate counts (after NMS)

- `radiator knob` (target): **2**
- `door` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
