# q221_455342_03ce1755 - visit 455342 / desc 03ce1755

## Instruction

> Set the temperature using the thermostat above the couch

## Stage 0 parse

```json
{
 "target": {
  "concept": "thermostat",
  "host": null
 },
 "entities": [
  {
   "name": "thermostat",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "couch",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "above",
   "a": "thermostat",
   "b": "couch"
  }
 ],
 "select": [],
 "residual": "the sentence names no sub-part; inferring a dial from train's verb->affordance statistics was not supported, so the neutral noun from the sentence is kept"
}
```

## Selected frame

- `455342/44358471/46568.990`  (1920x1440)
- relaxation level **L0**, chosen from 97 frames (stride 10)
- top-1 alternative frames: `[['44358471', '46568.990']]`

## Candidate counts (after NMS)

- `thermostat` (target): **1**
- `couch` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
