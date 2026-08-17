# q013_421254_ae4aa9fa - visit 421254 / desc ae4aa9fa

## Instruction

> Turn on the TV using the right remote on the nightstand

## Stage 0 parse

```json
{
 "target": {
  "concept": "remote control",
  "host": null
 },
 "entities": [
  {
   "name": "remote control",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "nightstand",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "remote control",
   "b": "nightstand"
  }
 ],
 "select": [
  {
   "on": "remote control",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": "independent check on the train split (val untouched): handheld-device GT median 478 points vs 87-108 for fixed-furniture handles, a factor of 4.4-5.5 -> the annotation covers the whole device"
}
```

## Selected frame

- `421254/42444754/80977.876`  (1440x1920)
- relaxation level **L0**, chosen from 170 frames (stride 10)
- top-8 alternative frames: `[['42444754', '80977.876'], ['42444755', '80834.684'], ['42444754', '80981.874'], ['42444754', '80985.872'], ['42444754', '80984.873'], ['42444754', '80980.874'], ['42444754', '80978.875'], ['42444754', '80979.875']]`

## Candidate counts (after NMS)

- `remote control` (target): **3**
- `nightstand` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
