# q12 — Kitchen_Task2 / frame 0074

## Instruction

> Plug in the Instant Pot using the nearest socket

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
   "name": "pressure cooker",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "near",
   "a": "socket",
   "b": "pressure cooker"
  }
 ],
 "select": [],
 "residual": "'nearest' as in q10; Instant Pot is a brand name, so the retrieval term is the generic pressure cooker"
}
```

## Frame selection

Chosen from 89 frames by "target detection count + concept completeness + confidence": frame 0074; 0 concepts missing, and 1 of the 1 spatial relations in the parse genuinely hold in this frame.
