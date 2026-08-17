# q101

**Instruction**: Adjust the intensity of the floor lamp light next to the dining table

**target**: `dimmer switch`   **host**: `floor lamp`

## Reasoning

**Step 1 - landmark**: dining table #0 x[0,793] y[1177,1439] score 0.960, unique.

**Step 2 - host: next_to(floor lamp, dining table)**

    floor lamp #0 x[327,479] y[549,1129] score 0.886 -> x lies entirely within the dining
                                                        table's [0,793], and its base at 1129
                                                        is close to the table top at 1177
    floor lamp #1 x[0,72] y[521,719] score 0.281     -> low score, at the far left edge
    => host = floor lamp #0

**Step 3 - target**

containment: floor lamp #0 contains #2.

    dimmer switch #0 x[1833,1885] cx 1858.4 cy 970.8 score 0.533
    dimmer switch #1 x[1882,1919] cx 1902.5 cy 972.4 score 0.512
    dimmer switch #2 x[373,412] y[906,979] cx 392.9 cy 943.0 score 0.236

#0 and #1 score higher (0.533 / 0.512 against 0.236), but:

- their centres at cx 1858 and 1902 are at the far right edge, over 1400 px from floor lamp#0
  (x 327-479)
- their cy values are nearly identical (970.8 / 972.4) and their x intervals adjacent -- this
  is a two-gang switch plate on the wall, unrelated to the floor lamp

#2's cx of 392.9 falls inside floor lamp#0 (327-479), and cy 943 is mid-way up the lamp
stem -- a floor lamp's dimmer is normally on the stem or the cable, so the position is
plausible.

The containment table, which is a mask test, assigns #2 to floor lamp#0. Follow the containment
table rather than the score.

**Uncertainty**: #2 scores only 0.236 while the excluded #0/#1 score more than twice that; if
the ground truth annotates the wall dimmer that controls the floor lamp, the answer should be
#0 or #1. Hence medium.

**FINAL: #2**   confidence **medium**
