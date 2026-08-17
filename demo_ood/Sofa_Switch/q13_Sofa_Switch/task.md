# q13 — Sofa_Switch / frame 0014

## Instruction

> Turn on the light using the switch near the sofa

## Stage 0 parse

```json
{
 "target": {
  "concept": "light switch",
  "host": null
 },
 "entities": [
  {
   "name": "light switch",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "sofa",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "near",
   "a": "light switch",
   "b": "sofa"
  }
 ],
 "select": [],
 "residual": "the light being operated (a ceiling light) is not co-located with the switch and may not be within the scanned volume at all, so it is not made an entity"
}
```

## Frame selection

Chosen from 40 frames by "target detection count + concept completeness + confidence": frame 0014; 0 concepts missing, and 1 of the 1 spatial relations in the parse genuinely hold in this frame.
