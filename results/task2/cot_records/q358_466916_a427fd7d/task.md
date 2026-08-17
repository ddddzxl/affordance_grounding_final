# q358_466916_a427fd7d - visit 466916 / desc a427fd7d

## Instruction

> Regulate the temperature using the radiator dial next to the glass door

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
 "residual": null
}
```

## Selected frame

- `466916/47331615/18094.096`  (1920x1440)
- relaxation level **L0**, chosen from 306 frames (stride 10)
- top-1 alternative frames: `[['47331615', '18094.096']]`

## Candidate counts (after NMS)

- `radiator knob` (target): **4**
- `door` (landmark): **4**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
