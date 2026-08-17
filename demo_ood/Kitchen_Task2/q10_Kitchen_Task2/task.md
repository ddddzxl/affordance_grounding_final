# q10 — Kitchen_Task2 / frame 0081

## Instruction

> Plug in the air fryer using the nearest socket

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
   "name": "air fryer",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "near",
   "a": "socket",
   "b": "air fryer"
  }
 ],
 "select": [],
 "residual": "'nearest' requires taking the closest socket by distance to the air fryer -- the schema has no distance axis, so this is left to the reasoning stage"
}
```

## Frame selection

Chosen from 89 frames by "target detection count + concept completeness + confidence": frame 0081; 0 concepts missing, and 1 of the 1 spatial relations in the parse genuinely hold in this frame.
