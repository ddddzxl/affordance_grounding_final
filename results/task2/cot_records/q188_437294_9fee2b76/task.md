# q188_437294_9fee2b76 - visit 437294 / desc 9fee2b76

## Instruction

> Plug the device in the socket next to the table lamp

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
   "name": "table lamp",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "socket",
   "b": "table lamp"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `437294/43649762/52587.746`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-8 alternative frames: `[['43649762', '52587.746'], ['43649763', '52438.259'], ['43649762', '52588.746'], ['43649767', '52398.358'], ['43649762', '52549.846'], ['43649763', '52437.259'], ['43649762', '52550.845'], ['43649767', '52397.359']]`

## Candidate counts (after NMS)

- `socket` (target): **2**
- `table lamp` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
