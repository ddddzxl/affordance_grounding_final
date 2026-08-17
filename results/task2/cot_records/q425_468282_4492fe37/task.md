# q425_468282_4492fe37 - visit 468282 / desc 4492fe37

## Instruction

> Open the washing machine door

## Stage 0 parse

```json
{
 "target": {
  "concept": "washing machine door",
  "host": "washing machine"
 },
 "entities": [
  {
   "name": "washing machine door",
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
 "residual": "the drum door is opened by its rim/recess, there is no separate handle noun in the sentence"
}
```

## Selected frame

- `468282/47331279/14319.317`  (1440x1920)
- relaxation level **L0**, chosen from 215 frames (stride 10)
- top-8 alternative frames: `[['47331279', '14319.317'], ['47331279', '14320.316'], ['47331279', '14307.705'], ['47331279', '14254.710'], ['47331279', '14237.717'], ['47331279', '14236.717'], ['47331279', '14238.716'], ['47331279', '14239.716']]`

## Candidate counts (after NMS)

- `washing machine door` (target): **1**
- `washing machine` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
