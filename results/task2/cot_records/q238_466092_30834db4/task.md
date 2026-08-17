# q238_466092_30834db4 - visit 466092 / desc 30834db4

## Instruction

> Close the door

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "door"
 },
 "entities": [
  {
   "name": "door handle",
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
 "residual": null
}
```

## Selected frame

- `466092/44796568/16165.188`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['44796568', '16165.188'], ['44796568', '16164.188'], ['44796568', '16180.198'], ['44796568', '16171.202'], ['44796562', '15986.395'], ['44796562', '15997.391'], ['44796562', '15996.391'], ['44796568', '16176.200']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
