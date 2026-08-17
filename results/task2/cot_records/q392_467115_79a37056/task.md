# q392_467115_79a37056 - visit 467115 / desc 79a37056

## Instruction

> Plug the device in the socket next to the stereo system

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
   "name": "stereo system",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "socket",
   "b": "stereo system"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333319/28418.765`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-7 alternative frames: `[['47333319', '28418.765'], ['47333310', '28273.758'], ['47333308', '28047.267'], ['47333319', '28417.765'], ['47333310', '28272.758'], ['47333310', '28274.757'], ['47333319', '28422.763']]`

## Candidate counts (after NMS)

- `socket` (target): **2**
- `stereo system` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
