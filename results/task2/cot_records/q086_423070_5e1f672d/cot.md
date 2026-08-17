# q086

**Instruction**: Control the water flow in the bathtub using the drain control dial

**target**: `drain control dial`   **host**: `bathtub`

## Reasoning

`drain control dial` on `bathtub`, no select, so the containment table settles it directly.

- `bathtub#0` x[151,772] score **0.928** is the actual bathtub; `bathtub#1` scores 0.633.
- Containment: `bathtub#0 contains #1`, `bathtub#1 contains (none)`.
- `dial#0` (cx 1460) falls outside both bathtubs.

Both dials score low (0.229 / 0.181), so detection quality is poor -- but that affects the
precision of the lift, not which one to select.

**FINAL: #1**
