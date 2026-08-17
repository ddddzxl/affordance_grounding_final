# q429_468282_9f874491 - visit 468282 / desc 9f874491

## Instruction

> Lock the bathroom door

## Stage 0 parse

```json
{
 "target": {
  "concept": "lock",
  "host": "door"
 },
 "entities": [
  {
   "name": "lock",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'bathroom' is a room-level locator; 'lock' vs 'close' distinguishes the lock from the handle on the same door"
}
```

## Selected frame

- `468282/47331279/14310.704`  (1440x1920)
- relaxation level **L0**, chosen from 215 frames (stride 10)
- top-8 alternative frames: `[['47331279', '14310.704'], ['47331279', '14258.708'], ['47331279', '14255.710'], ['47331281', '14173.010'], ['47331279', '14308.704'], ['47331279', '14235.718'], ['47331279', '14330.312'], ['47331281', '14158.016']]`

## Candidate counts (after NMS)

- `lock` (target): **2**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
