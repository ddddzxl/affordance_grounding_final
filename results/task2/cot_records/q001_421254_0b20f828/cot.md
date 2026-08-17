# q001

**Instruction**: Open the left window behind the shutters

**target**: `window handle`   **host**: `window`

## Reasoning

shutters#0 x[387,996] and window#0 x[380,997] almost exactly coincide, so `behind` carries no
information here. window w=617 is a merged detection; the two handles at cx 660 / 972 sit left
and right of each other, and the instruction asks for the left one -> #0 (which also has the
stronger detection, score 0.573 vs 0.195).

**FINAL: #0**
