# q130_434888_ba8873b2 - visit 434888 / desc ba8873b2

## Instruction

> Unplug the right lamp on the vanity table

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": "lamp"
 },
 "entities": [
  {
   "name": "plug",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "lamp",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "vanity table",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "lamp",
   "b": "vanity table"
  }
 ],
 "select": [
  {
   "on": "lamp",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": "the plug sits at the socket end, not on the lamp; 'right' orders the lamps"
}
```

## Selected frame

- `434888/42899184/184459.299`  (1440x1920)
- relaxation level **L0**, chosen from 105 frames (stride 10)
- top-3 alternative frames: `[['42899184', '184459.299'], ['42899184', '184442.805'], ['42899185', '184318.307']]`

## Candidate counts (after NMS)

- `plug` (target): **4**
- `lamp` (host): **2**
- `vanity table` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
