# q09 — Kitchen_Task2 / frame 0011

## Instruction

> Open the door of the pantry to the left of the refrigerator

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "pantry",
   "role": "container",
   "instanceable": false
  },
  {
   "name": "refrigerator",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "left_of",
   "a": "door",
   "b": "refrigerator"
  }
 ],
 "select": [],
 "residual": "pantry is not instanceable (it is a space, not an object), so the relation attaches to the door"
}
```

## Frame selection

Chosen from 89 frames by "target detection count + concept completeness + confidence": frame 0011; 0 concepts missing, and 1 of the 1 spatial relations in the parse genuinely hold in this frame.
