# q125  (auto-filled, no reasoning)

**Instruction**: Close the bedroom door

**target concept**: `door handle`   candidates: **1**

## Why no reasoning was performed

There is only one candidate, so `select` can only ever land on `#0` however it is resolved. The
information gain from reasoning here is exactly zero -- the score is determined entirely by the
quality of the 2D mask and by the lift.

**FINAL: #0**

> **The projection-based hit test does not apply here.** The ground truth and the prediction
> have the same shape, but the projected ground truth is displaced out of bounds -- an offset
> caused by pose accuracy, not a wrong selection. This question is scored by centre distance
> instead, and the strict score is reported alongside, so the criterion cannot flatter the
> headline number.
