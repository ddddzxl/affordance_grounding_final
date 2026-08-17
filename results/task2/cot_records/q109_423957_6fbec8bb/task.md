# q109_423957_6fbec8bb - visit 423957 / desc 6fbec8bb

## Instruction

> Unplug the table lamp on top of the nightstand

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": null
 },
 "entities": [
  {
   "name": "plug",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "table lamp",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "nightstand",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "near",
   "a": "plug",
   "b": "table lamp"
  },
  {
   "rel": "on_top",
   "a": "table lamp",
   "b": "nightstand"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `423957/42898340/508428.312`  (1920x1440)
- relaxation level **L1**, chosen from 106 frames (stride 10)
- top-1 alternative frames: `[['42898340', '508428.312']]`

## Candidate counts (after NMS)

- `plug` (target): **1**
- `table lamp` (landmark): **1**
- `nightstand` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
