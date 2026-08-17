# q191_437294_cfc4b964 - visit 437294 / desc cfc4b964

## Instruction

> Plug the device in one of the sockets behind the nightstand next to he door

## Stage 0 parse

```json
{
 "target": {
  "concept": "socket",
  "host": null
 },
 "entities": [
  {
   "name": "socket",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "nightstand",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "behind",
   "a": "socket",
   "b": "nightstand"
  },
  {
   "rel": "next_to",
   "a": "nightstand",
   "b": "door"
  }
 ],
 "select": [],
 "residual": "'one of the sockets' — any instance satisfying the relation is acceptable"
}
```

## Selected frame

- `437294/43649762/52534.852`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-7 alternative frames: `[['43649762', '52534.852'], ['43649767', '52381.049'], ['43649763', '52449.254'], ['43649762', '52533.852'], ['43649767', '52382.048'], ['43649767', '52380.049'], ['43649763', '52448.254']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `nightstand` (landmark): **1**
- `door` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
