# q243_466092_8989704f - visit 466092 / desc 8989704f

## Instruction

> Control the light intensity with the dimmer switch next to the door

## Stage 0 parse

```json
{
 "target": {
  "concept": "switch",
  "host": null
 },
 "entities": [
  {
   "name": "switch",
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
   "a": "switch",
   "b": "door"
  }
 ],
 "select": [],
 "residual": "reverted: 'dimmer dial' is semantically right (GT label is rotate) but SAM3 detects it in 0/5 descriptions, while 'dimmer switch' at least builds a candidate pool. Retrieval failure is a harder failure than a form mismatch — you score 0 either way, but with no pool there is nothing to reason over."
}
```

## Selected frame

- `466092/44796562/15964.404`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-5 alternative frames: `[['44796562', '15964.404'], ['44796562', '15984.396'], ['44796562', '15966.404'], ['44796562', '15965.404'], ['44796562', '15963.405']]`

## Candidate counts (after NMS)

- `switch` (target): **2**
- `door` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
