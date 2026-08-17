# q394_467115_80b54aac - visit 467115 / desc 80b54aac

## Instruction

> Open the oven door

## Stage 0 parse

```json
{
 "target": {
  "concept": "oven handle",
  "host": "oven"
 },
 "entities": [
  {
   "name": "oven handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "oven",
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

- `467115/47333310/28302.762`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333310', '28302.762'], ['47333308', '28017.162'], ['47333308', '28018.162'], ['47333308', '28016.162'], ['47333319', '28482.855'], ['47333308', '28088.367'], ['47333310', '28230.659'], ['47333308', '28021.160']]`

## Candidate counts (after NMS)

- `oven handle` (target): **6**
- `oven` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
