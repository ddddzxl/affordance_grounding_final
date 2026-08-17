# q047

**Instruction**: Open the window

**target**: `window handle`   **host**: `window`

## Reasoning

window#0 contains two handles, but their cy differs by 354 px, so they are not equivalent and
the "emit all" rule does not apply. #0 is 26x14 px at cy 552 (52% of the window's height),
consistent with a window handle; #1 is 139x30 px, a horizontal bar more like window-frame trim,
and scores only 0.245.

**FINAL: #0**
