# q111_423957_76768416 - visit 423957 / desc 76768416

## Instruction

> Adjust the light intensity using the dial next to the door

## Stage 0 parse

```json
{
 "target": {
  "concept": "dimmer dial",
  "host": null
 },
 "entities": [
  {
   "name": "dimmer dial",
   "role": "target",
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
   "rel": "next_to",
   "a": "dimmer dial",
   "b": "door"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `423957/42898340/508389.328`  (1920x1440)
- relaxation level **POOL**, chosen from 106 frames (stride 10)
- top-8 alternative frames: `[['42898340', '508389.328'], ['42898340', '508390.311'], ['42898340', '508391.310'], ['42898340', '508392.310'], ['42898340', '508393.309'], ['42898340', '508394.326'], ['42898340', '508395.325'], ['42898340', '508396.325']]`

## Candidate counts (after NMS)

- `dimmer dial` (target): **0**
- `door` (landmark): **0**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
