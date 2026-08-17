# q236_466092_1f30aca2 - visit 466092 / desc 1f30aca2

## Instruction

> Lock the door

## Stage 0 parse

```json
{
 "target": {
  "concept": "door lock",
  "host": "door"
 },
 "entities": [
  {
   "name": "door lock",
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
 "residual": "'lock' vs 'close' distinguishes the lock/keyhole from the handle on the same door"
}
```

## Selected frame

- `466092/44796568/16165.188`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['44796568', '16165.188'], ['44796568', '16164.188'], ['44796568', '16176.200'], ['44796562', '15971.401'], ['44796562', '16009.402'], ['44796562', '16005.404'], ['44796562', '15970.402'], ['44796562', '15967.403']]`

## Candidate counts (after NMS)

- `door lock` (target): **2**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
