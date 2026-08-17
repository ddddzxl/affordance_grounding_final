# q363_466916_c49b3990 - visit 466916 / desc c49b3990

## Instruction

> Adjust the power of the humidifier

## Stage 0 parse

```json
{
 "target": {
  "concept": "humidifier knob",
  "host": "humidifier"
 },
 "entities": [
  {
   "name": "humidifier knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "humidifier",
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

- `466916/47331618/17979.192`  (1920x1440)
- relaxation level **L0**, chosen from 306 frames (stride 10)
- top-8 alternative frames: `[['47331618', '17979.192'], ['47331617', '18167.699'], ['47331617', '18165.700'], ['47331617', '18164.700'], ['47331615', '18092.096'], ['47331617', '18173.697'], ['47331615', '18088.098'], ['47331617', '18258.296']]`

## Candidate counts (after NMS)

- `humidifier knob` (target): **3**
- `humidifier` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
