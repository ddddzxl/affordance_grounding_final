# q127_434888_80872139 - visit 434888 / desc 80872139

## Instruction

> Open the lamp on the nightstand near the painting

## Stage 0 parse

```json
{
 "target": {
  "concept": "lamp chain",
  "host": "lamp"
 },
 "entities": [
  {
   "name": "lamp chain",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "lamp",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "nightstand",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "painting",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "lamp",
   "b": "nightstand"
  },
  {
   "rel": "near",
   "a": "nightstand",
   "b": "painting"
  }
 ],
 "select": [],
 "residual": "train: 'open the lamp' is pinch_pull in 41/42 annotations — it is a pull-chain switch, not a press switch (note 'turn on the lamp' IS push 46/54, so the verb carries the distinction)."
}
```

## Selected frame

- `434888/42899187/184405.904`  (1440x1920)
- relaxation level **POOL-T**, chosen from 105 frames (stride 10)
- top-8 alternative frames: `[['42899187', '184405.904'], ['42899187', '184357.807'], ['42899184', '184443.805'], ['42899187', '184406.904'], ['42899184', '184441.806'], ['42899185', '184320.306'], ['42899187', '184358.807'], ['42899184', '184442.805']]`

## Candidate counts (after NMS)

- `lamp chain` (target): **2**
- `lamp` (host): **2**
- `nightstand` (container): **1**
- `painting` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
