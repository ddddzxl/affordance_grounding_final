# q165_435357_bbd764f1 - visit 435357 / desc bbd764f1

## Instruction

> Turn on the heater next to the blue couch

## Stage 0 parse

```json
{
 "target": {
  "concept": "heater switch",
  "host": "heater"
 },
 "entities": [
  {
   "name": "heater switch",
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
 "residual": "may be the same physical control as the intensity knob in the sibling description"
}
```

## Selected frame

- `435357/42899632/229995.176`  (1440x1920)
- relaxation level **L0**, chosen from 191 frames (stride 10)
- top-2 alternative frames: `[['42899632', '229995.176'], ['42899624', '230102.284']]`

## Candidate counts (after NMS)

- `heater switch` (target): **3**
- `heater` (host): **2**
- `couch` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
