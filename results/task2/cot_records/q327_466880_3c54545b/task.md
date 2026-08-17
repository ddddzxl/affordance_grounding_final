# q327_466880_3c54545b - visit 466880 / desc 3c54545b

## Instruction

> Turn on the kitchen light

## Stage 0 parse

```json
{
 "target": {
  "concept": "light switch",
  "host": null
 },
 "entities": [
  {
   "name": "light switch",
   "role": "target",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'kitchen' is a room-level locator, not groundable"
}
```

## Selected frame

- `466880/47331711/11278.935`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['47331711', '11278.935'], ['47331711', '11324.833'], ['47331711', '11270.339'], ['47331707', '11115.035'], ['47331710', '11236.236'], ['47331710', '11231.238'], ['47331710', '11182.641'], ['47331711', '11283.334']]`

## Candidate counts (after NMS)

- `light switch` (target): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
