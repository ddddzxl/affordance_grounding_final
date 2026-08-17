# q421_468282_16725785 - visit 468282 / desc 16725785

## Instruction

> Open the detergent drawer of the washing machine

## Stage 0 parse

```json
{
 "target": {
  "concept": "detergent drawer",
  "host": "washing machine"
 },
 "entities": [
  {
   "name": "detergent drawer",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "washing machine",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "the detergent tray has no separate handle; the tray front itself is the interactable surface"
}
```

## Selected frame

- `468282/47331279/14319.317`  (1440x1920)
- relaxation level **L0**, chosen from 215 frames (stride 10)
- top-8 alternative frames: `[['47331279', '14319.317'], ['47331279', '14307.705'], ['47331279', '14238.716'], ['47331279', '14239.716'], ['47331279', '14241.715'], ['47331279', '14240.716'], ['47331279', '14321.316'], ['47331279', '14322.316']]`

## Candidate counts (after NMS)

- `detergent drawer` (target): **1**
- `washing machine` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
