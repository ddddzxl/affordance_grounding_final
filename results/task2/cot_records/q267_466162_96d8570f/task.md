# q267_466162_96d8570f - visit 466162 / desc 96d8570f

## Instruction

> Turn on the faucet

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
  }
 ],
 "relations": [],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466162/44796575/16939.494`  (1920x1440)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['44796575', '16939.494'], ['44796576', '16747.690'], ['44796579', '16810.580'], ['44796575', '16908.190'], ['44796576', '16746.690'], ['44796579', '16836.786'], ['44796576', '16729.281'], ['44796576', '16730.680']]`

## Candidate counts (after NMS)

- `faucet handle` (target): **3**
- `faucet` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
