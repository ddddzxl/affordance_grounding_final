# q07 — Kitchen_Task2 / frame 0019

## Instruction

> Open the left door of the cabinet above the refrigerator

## Stage 0 parse

```json
{
 "target": {
  "concept": "cabinet knob",
  "host": "cabinet door"
 },
 "entities": [
  {
   "name": "cabinet knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "cabinet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "refrigerator",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "cabinet door"
  },
  {
   "rel": "above",
   "a": "cabinet",
   "b": "refrigerator"
  }
 ],
 "select": [
  {
   "on": "cabinet door",
   "axis": "horizontal",
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Frame selection

Chosen from 89 frames by "target detection count + concept completeness + confidence": frame 0019; 0 concepts missing, and 2 of the 2 spatial relations in the parse genuinely hold in this frame.

> ⚠️ The frame for this question was **specified manually**. Automatic selection returned frame 0048 (the most knob detections, with every relation individually satisfied), but in that frame the refrigerator shows only a strip at the far left and there is no knob above it at all -- each relation holding individually is not the same as the whole target -> host -> container -> landmark chain landing on one set of instances. In frame 0019 the refrigerator scores 0.952 at 28.9% area with exactly two knobs directly above it, which is the frame this question can actually be reasoned on. Specified manually, with the limitation of automatic frame selection recorded as observed.
