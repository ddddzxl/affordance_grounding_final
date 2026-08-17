# q407

**Instruction**: Open the bottom, left cabinet drawer located to the left of the dining table

**target**: `drawer handle`   **host**: `drawer`

## Reasoning

The drawers form **two columns**:

- left column cx ~ 520-532: `#5` (cy 479), `#1` (862), `#3` (1037)
- right column cx ~ 614-641: `#4` (cy 529), `#0` (1004), `#2` (1225)

1. `dining table#0` cx 1230 -> `cabinet#0` (cx 702) is to its left.
2. select = bottom + left -> the lowest of the left column = `drawer#3` (cx 532, cy 1037).
3. The containment table gives `contains #2, #6`, but their cy values of 919 and 1031 differ by
   112 px, so this is **two layers detected as one drawer** (`drawer#3` is 272 px tall). They
   are not equivalent, so bottom takes the lower one -> `#2`.

**FINAL: #2**
