# q11 — Kitchen_Task2 / frame 0039

## Instruction

> Plug in the Ninja blender using the nearest socket

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
   "name": "blender",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "near",
   "a": "socket",
   "b": "blender"
  }
 ],
 "select": [],
 "residual": "'nearest' as in q10; the brand name Ninja is not detectable, so only blender is kept"
}
```

## Frame selection

Chosen from 89 frames by "target detection count + concept completeness + confidence": frame 0039; 0 concepts missing, and 1 of the 1 spatial relations in the parse genuinely hold in this frame.
