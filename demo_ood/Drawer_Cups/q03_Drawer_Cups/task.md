# q03 — Drawer_Cups / frame 0017

## Instruction

> Open the third drawer from the top of the cabinet with cups directly on top

## Stage 0 parse

```json
{
 "target": {
  "concept": "drawer handle",
  "host": "drawer"
 },
 "entities": [
  {
   "name": "drawer handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "drawer",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "cup",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "drawer"
  },
  {
   "rel": "has_on_top",
   "a": "cabinet",
   "b": "cup"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "ordinal",
   "value": null,
   "index": 3,
   "from": "top"
  }
 ],
 "residual": null
}
```

## Frame selection

Chosen from 32 frames by "target detection count + concept completeness + confidence": frame 0017; 0 concepts missing, and 2 of the 2 spatial relations in the parse genuinely hold in this frame.
