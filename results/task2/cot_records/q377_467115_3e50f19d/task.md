# q377_467115_3e50f19d - visit 467115 / desc 3e50f19d

## Instruction

> Unplug the stereo system on the shelf

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": "stereo system"
 },
 "entities": [
  {
   "name": "plug",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "stereo system",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "shelf",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "stereo system",
   "b": "shelf"
  }
 ],
 "select": [],
 "residual": "the plug sits at the socket end, not on the stereo system"
}
```

## Selected frame

- `467115/47333319/28418.765`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-1 alternative frames: `[['47333319', '28418.765']]`

## Candidate counts (after NMS)

- `plug` (target): **4**
- `stereo system` (host): **2**
- `shelf` (container): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
