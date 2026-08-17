# q315_466876_0239b344 - visit 466876 / desc 0239b344

## Instruction

> Turn on the faucet in the sink

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
   "name": "sink",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "faucet",
   "b": "sink"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466876/47331560/9900.645`  (1440x1920)
- relaxation level **L0**, chosen from 160 frames (stride 10)
- top-8 alternative frames: `[['47331560', '9900.645'], ['47331560', '9898.645'], ['47331560', '9901.644'], ['47331558', '9834.954'], ['47331561', '9783.142'], ['47331561', '9784.142'], ['47331561', '9767.149'], ['47331561', '9743.042']]`

## Candidate counts (after NMS)

- `faucet handle` (target): **2**
- `faucet` (host): **1**
- `sink` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
