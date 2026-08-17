# q06 — Kitchen_Task2 / frame 0008

## Instruction

> Open the right door of the refrigerator

## Stage 0 parse

```json
{
 "target": {
  "concept": "refrigerator door handle",
  "host": "refrigerator door"
 },
 "entities": [
  {
   "name": "refrigerator door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "refrigerator door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "refrigerator",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "refrigerator",
   "b": "refrigerator door"
  }
 ],
 "select": [
  {
   "on": "refrigerator door",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Frame selection

Chosen from 89 frames by "target detection count + concept completeness + confidence": frame 0008; 0 concepts missing, and 1 of the 1 spatial relations in the parse genuinely hold in this frame.
