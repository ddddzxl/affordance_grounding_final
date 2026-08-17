# q204_438775_1ce048ec - visit 438775 / desc 1ce048ec

## Instruction

> Dial a number using the telephone next to the table lamp

## Stage 0 parse

```json
{
 "target": {
  "concept": "telephone",
  "host": null
 },
 "entities": [
  {
   "name": "telephone",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "table lamp",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "telephone",
   "b": "table lamp"
  }
 ],
 "select": [],
 "residual": "independent check on the train split (val untouched): handheld-device GT has a median of 478 points while fixed-furniture handles have 87-108, a factor of 4.4-5.5. The annotation therefore covers the whole device rather than an individual key: what a person grasps is the whole remote or controller, and which key the press lands on does not constitute a separate interactable entity. Fixed furniture is the opposite -- there you operate the handle itself."
}
```

## Selected frame

- `438775/44358173/62406.749`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-8 alternative frames: `[['44358173', '62406.749'], ['44358173', '62407.749'], ['44358173', '62403.751'], ['44358173', '62405.750'], ['44358173', '62404.750'], ['44358170', '62337.560'], ['44358173', '62402.751'], ['44358170', '62336.561']]`

## Candidate counts (after NMS)

- `telephone` (target): **1**
- `table lamp` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
