# q266_466162_8ede1872 - visit 466162 / desc 8ede1872

## Instruction

> Adjust the lighting using the dimmer switch next to the door

## Stage 0 parse

```json
{
 "target": {
  "concept": "dimmer switch",
  "host": null
 },
 "entities": [
  {
   "name": "dimmer switch",
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
   "a": "dimmer switch",
   "b": "door"
  }
 ],
 "select": [],
 "residual": "reverted: 'dimmer dial' is semantically right (GT label is rotate) but SAM3 detects it in 0/5 descriptions, while 'dimmer switch' at least builds a candidate pool. Retrieval failure is a harder failure than a form mismatch — you score 0 either way, but with no pool there is nothing to reason over."
}
```

## Selected frame

- `466162/44796575/16856.994`  (1920x1440)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-2 alternative frames: `[['44796575', '16856.994'], ['44796576', '16704.291']]`

## Candidate counts (after NMS)

- `dimmer switch` (target): **2**
- `door` (landmark): **4**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
