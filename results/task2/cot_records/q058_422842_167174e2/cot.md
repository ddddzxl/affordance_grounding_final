# q058

**Instruction**: Open the top drawer of the nightstand to the left of the bed

**target**: `drawer handle`   **host**: `drawer`

## Reasoning

1. `bed#0` x[112,1439] cx 744 -> `nightstand#0` (cx 82) is to its left.
2. `nightstand#0` contains only `drawer#0` x[0,162] y[855,1052].
3. select = top applied to a single-element set -> no-op -> still `drawer#0`.

**But `drawer#0` is 197 px tall and holds two vertically separated handles** (`#1` cy 894.5 and
`#0` cy 987.9, 93 px apart) -- this is **two drawer layers detected as one drawer** (the same
pattern as q067/q068). The two handles belong to different layers and are **not equivalent**,
so the "emit all" rule does not apply. select=top points at the upper layer -> `#1`.

**FINAL: #1**
