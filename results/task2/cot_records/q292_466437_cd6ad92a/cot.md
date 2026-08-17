# q292

**Instruction**: Open the window next to the closet

**target**: `window handle`   **host**: `window`

## Reasoning

The only `window#0` (w=243) contains **five** handles -- a 243 px wide window cannot have five
handles, so most are false detections.

- `#1` (cx 729, cy 978) and `#7` (cx 734, cy 982) almost coincide -> one object split in two
- `#0` scores **0.513**, well above the next best at 0.329, and has the largest area
- `#0`'s cy of 1076 is 87% of the way down the window, consistent with a window handle at hand
  height

`next_to(window, closet)` is automatically satisfied because there is only one window, so it
adds no information.

**FINAL: #0**
