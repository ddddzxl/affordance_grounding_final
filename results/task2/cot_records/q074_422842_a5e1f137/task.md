# q074_422842_a5e1f137 - visit 422842 / desc a5e1f137

## Instruction

> Open the right door of the white closet between the doors

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "closet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "closet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "closet",
   "role": "container",
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
   "rel": "contains",
   "a": "closet",
   "b": "closet door"
  },
  {
   "rel": "between",
   "a": "closet",
   "b": "door"
  }
 ],
 "select": [
  {
   "on": "closet door",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": "'between the doors' - both landmarks are the same noun 'door'"
}
```

## Selected frame

- `422842/42897547/473286.209`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-8 alternative frames: `[['42897547', '473286.209'], ['42897547', '473289.207'], ['42897547', '473152.813'], ['42897547', '473186.816'], ['42897547', '473180.819'], ['42897547', '473217.104'], ['42897560', '473472.715'], ['42897547', '473168.807']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `closet door` (host): **4**
- `closet` (container): **3**
- `door` (landmark): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
