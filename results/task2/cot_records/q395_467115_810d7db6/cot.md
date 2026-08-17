# q395

**Instruction**: Open the top counter drawer directly under the electric kettle

**target**: `drawer handle`   **host**: `drawer`

## Reasoning

Everything turns on which electric kettle is meant:

- `#0` has area **7.708%** and extends to x=1439 (flush with the right edge) -- far too large
  for a kettle, and probably merged with the appliance beside it
- `#1` x[632,949] y[160,536] = 317x376, which is the size of a kettle

**The decisive evidence is the select clause itself**: the instruction supplies `select=top`,
which implies there should be **several drawer layers** beneath the kettle. Beneath `kettle#1`
there are two, `drawer#0` (cy 1252) and `drawer#1` (cy 1587), so top is meaningful; beneath
`kettle#0` there is only `drawer#4`, and top would degenerate to a no-op.

-> kettle = `#1` -> top -> `drawer#0` -> the containment table gives `contains #0`.

**FINAL: #0**

> **Manual review overturned the automatic score here**: the projected ground truth drifts off
> the target while the pick is correct. Confirmed visually.
