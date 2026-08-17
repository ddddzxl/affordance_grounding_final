# q070_422842_8480581d - visit 422842 / desc 8480581d

## Instruction

> Open the door located to the left of the closet

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "closet",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "left_of",
   "a": "door",
   "b": "closet"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `422842/42897547/473241.610`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-8 alternative frames: `[['42897547', '473241.610'], ['42897547', '473255.605'], ['42897547', '473168.807'], ['42897547', '473215.904'], ['42897547', '473169.806'], ['42897547', '473162.809'], ['42897547', '473289.207'], ['42897547', '473292.206']]`

## Candidate counts (after NMS)

- `door handle` (target): **4**
- `door` (host): **5**
- `closet` (landmark): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
