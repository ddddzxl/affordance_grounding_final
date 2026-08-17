# q072_422842_8e0dad90 - visit 422842 / desc 8e0dad90

## Instruction

> Control the light intensity using the dimmer on the wall

## Stage 0 parse

```json
{
 "target": {
  "concept": "switch",
  "host": null
 },
 "entities": [
  {
   "name": "switch",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "wall",
   "role": "landmark",
   "instanceable": false
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'wall' not instanceable; no disambiguation cue"
}
```

## Selected frame

- `422842/42897547/473311.215`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-8 alternative frames: `[['42897547', '473311.215'], ['42897547', '473314.214'], ['42897547', '473306.217'], ['42897547', '473313.214'], ['42897547', '473317.212'], ['42897547', '473312.215'], ['42897547', '473322.210'], ['42897547', '473308.216']]`

## Candidate counts (after NMS)

- `switch` (target): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
