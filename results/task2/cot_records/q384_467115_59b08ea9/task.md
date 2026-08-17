# q384_467115_59b08ea9 - visit 467115 / desc 59b08ea9

## Instruction

> Open the drawer under the oven

## Stage 0 parse

```json
{
 "target": {
  "concept": "drawer handle",
  "host": "drawer"
 },
 "entities": [
  {
   "name": "drawer handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "drawer",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "oven",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "under",
   "a": "drawer",
   "b": "oven"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333319/28354.658`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333319', '28354.658'], ['47333308', '28020.161'], ['47333310', '28302.762'], ['47333319', '28481.856'], ['47333308', '28017.162'], ['47333308', '28099.362'], ['47333308', '28021.160'], ['47333308', '28018.162']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **4**
- `drawer` (host): **2**
- `oven` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
