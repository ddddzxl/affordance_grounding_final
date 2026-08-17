# q034

**Instruction**: Close the wooden bedroom door

**target**: `door handle`   **host**: `door`

## Reasoning

The only `door#0` x[673,965] `contains (none)` -- **every handle is at x <= 528, completely
separate from the door**.

The handles fall into two classes:

- `#1`-`#4`: x ~ 310-528 (w ~ 210), cy 1246 / 1344 / 1439 / 1533, **evenly spaced vertically**
  -> a row of **drawer pulls** detected as door handles
- `#0` (w=29, cy 955) and `#5` (w=24, cy 721): the right size for a door handle, but at
  x ~ 490-520, more than 150 px to the left of door#0

Conclusion: **the handle of that door was never detected**, so the mechanism cannot run. As a
fallback, take the candidate that is shaped like a door handle and at a plausible height: `#0`
(cy 955, mid-height on the door).

**FINAL: #0**
