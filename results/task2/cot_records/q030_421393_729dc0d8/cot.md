# q030

**Instruction**: Adjust the room's temperature using the radiator dial

**target**: `radiator knob`   **host**: `radiator`

## Reasoning

The containment table lists only #0, but #1 (cx 600, cy 662) also falls inside radiator#0
x[570,891] y[648,1605] -- the containment table is not always complete. A radiator's top
fitting is usually a bleed valve while the temperature valve sits lower: #0 at cy 1058 is 43%
of the way down, whereas #1 hugs the top. #0 also has the higher score and larger area.

**FINAL: #0**
