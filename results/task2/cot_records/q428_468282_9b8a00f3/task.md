# q428_468282_9b8a00f3 - visit 468282 / desc 9b8a00f3

## Instruction

> Close the shower door

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "shower door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "shower door",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": null
}
```

## Selected frame

- `468282/47331279/14235.718`  (1440x1920)
- relaxation level **L0**, chosen from 215 frames (stride 10)
- top-8 alternative frames: `[['47331279', '14235.718'], ['47331279', '14342.307'], ['47331281', '14183.006'], ['47331281', '14171.011'], ['47331279', '14344.307'], ['47331281', '14164.014'], ['47331279', '14234.718'], ['47331279', '14258.708']]`

## Candidate counts (after NMS)

- `door handle` (target): **3**
- `shower door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
