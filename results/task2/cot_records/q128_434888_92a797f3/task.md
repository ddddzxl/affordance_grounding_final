# q128_434888_92a797f3 - visit 434888 / desc 92a797f3

## Instruction

> Open the top right drawer of the closet next to the door

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
   "name": "closet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "closet",
   "b": "drawer"
  },
  {
   "rel": "next_to",
   "a": "closet",
   "b": "door"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "top",
   "index": null,
   "from": null
  },
  {
   "on": "drawer",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `434888/42899187/184385.613`  (1440x1920)
- relaxation level **L2**, chosen from 105 frames (stride 10)
- top-8 alternative frames: `[['42899187', '184385.613'], ['42899184', '184413.801'], ['42899185', '184273.609'], ['42899187', '184347.828'], ['42899185', '184290.602'], ['42899187', '184393.709'], ['42899185', '184292.701'], ['42899187', '184392.710']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **5**
- `drawer` (host): **3**
- `closet` (container): **1**
- `door` (landmark): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
