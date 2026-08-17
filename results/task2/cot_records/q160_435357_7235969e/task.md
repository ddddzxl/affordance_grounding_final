# q160_435357_7235969e - visit 435357 / desc 7235969e

## Instruction

> Adjust the intensity of the heater next to the blue couch

## Stage 0 parse

```json
{
 "target": {
  "concept": "heater knob",
  "host": "heater"
 },
 "entities": [
  {
   "name": "heater knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "heater",
   "role": "host",
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
   "rel": "next_to",
   "a": "heater",
   "b": "couch"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `435357/42899632/229995.176`  (1440x1920)
- relaxation level **L0**, chosen from 191 frames (stride 10)
- top-2 alternative frames: `[['42899632', '229995.176'], ['42899624', '230102.284']]`

## Candidate counts (after NMS)

- `heater knob` (target): **2**
- `heater` (host): **2**
- `couch` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
