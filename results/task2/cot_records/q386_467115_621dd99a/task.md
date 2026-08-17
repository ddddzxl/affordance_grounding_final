# q386_467115_621dd99a - visit 467115 / desc 621dd99a

## Instruction

> Turn on the tap in the sink

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
 "residual": "'tap' and 'faucet' are the same object; unified to one concept so sibling descriptions share one candidate pool"
}
```

## Selected frame

- `467115/47333319/28393.659`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-7 alternative frames: `[['47333319', '28393.659'], ['47333319', '28394.658'], ['47333308', '28039.270'], ['47333310', '28288.768'], ['47333319', '28396.657'], ['47333319', '28406.653'], ['47333310', '28296.765']]`

## Candidate counts (after NMS)

- `faucet handle` (target): **6**
- `faucet` (host): **1**
- `sink` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
