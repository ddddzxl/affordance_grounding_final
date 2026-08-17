# q134_434897_11427387 - visit 434897 / desc 11427387

## Instruction

> Adjust the room's temperature using the dial next to the door

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

- `434897/42899165/182807.545`  (1440x1920)
- relaxation level **L0**, chosen from 94 frames (stride 10)
- top-8 alternative frames: `[['42899165', '182807.545'], ['42899163', '182680.731'], ['42899163', '182718.132'], ['42899163', '182720.131'], ['42899165', '182809.544'], ['42899165', '182806.545'], ['42899163', '182681.730'], ['42899163', '182684.746']]`

## Candidate counts (after NMS)

- `radiator knob` (target): **9**
- `door` (landmark): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
