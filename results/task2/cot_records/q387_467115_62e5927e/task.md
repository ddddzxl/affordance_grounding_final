# q387_467115_62e5927e - visit 467115 / desc 62e5927e

## Instruction

> Open the cabinet door above the microwave

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "cabinet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "cabinet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "microwave",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "cabinet door"
  },
  {
   "rel": "above",
   "a": "cabinet door",
   "b": "microwave"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333319/28360.655`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333319', '28360.655'], ['47333308', '28020.161'], ['47333319', '28354.658'], ['47333308', '28021.160'], ['47333310', '28241.654'], ['47333310', '28243.653'], ['47333310', '28308.760'], ['47333308', '28032.156']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `cabinet door` (host): **4**
- `cabinet` (container): **5**
- `microwave` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
