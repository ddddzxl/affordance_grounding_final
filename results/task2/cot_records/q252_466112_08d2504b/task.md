# q252_466112_08d2504b - visit 466112 / desc 08d2504b

## Instruction

> Turn on the tap in the bathtub

## Stage 0 parse

```json
{
 "target": {
  "concept": "faucet handle",
  "host": "faucet"
 },
 "entities": [
  {
   "name": "faucet handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "faucet",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "bathtub",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "faucet",
   "b": "bathtub"
  }
 ],
 "select": [],
 "residual": "'tap' and 'faucet' are the same object; unified to one concept so sibling descriptions share one candidate pool"
}
```

## Selected frame

- `466112/44796521/3987.918`  (1440x1920)
- relaxation level **L0**, chosen from 176 frames (stride 10)
- top-8 alternative frames: `[['44796521', '3987.918'], ['44796517', '3915.514'], ['44796517', '3895.222'], ['44796521', '3986.919'], ['44796520', '4034.217'], ['44796517', '3893.222'], ['44796521', '3957.414'], ['44796521', '3956.414']]`

## Candidate counts (after NMS)

- `faucet handle` (target): **4**
- `faucet` (host): **2**
- `bathtub` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
