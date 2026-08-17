# q027

**Instruction**: Open the door that you will find on your left when exiting the room towards
the hallway

**target**: `door handle`   **host**: `door`

## Reasoning

**Step 1 - residual**: the phrasing is egocentric ("on your left when exiting") plus a
room-level locator, neither of which can be grounded. There is no relation, no select, and a
single door.

**Step 2 - the host chain is broken**

door #0 x[673,965] y[628,1686] w=292 score 0.735 -- the only door detection.
containment: door #0 contains (none). All six handles fall outside the door's mask:

    #0 x[490,519] y[920,987]   -> 154 px to the left of the door
    #1 x[311,524] y[1327,1359] -> further left
    #2 x[310,524] y[1227,1259]
    #3 x[317,526] y[1420,1454]
    #4 x[320,528] y[1513,1552]
    #5 x[480,504] y[693,750]

All are in the band x < 530 while the door occupies x[673,965]. The host-target chain is
broken.

**Step 3 - shape analysis of the handles**

#1/#2/#3/#4 have nearly identical x intervals ([310,524] / [311,524] / [317,526] /
[320,528]), all about 210 px wide and 32-39 px tall -- **horizontal bars**. Their cy values run
1245.7 / 1343.7 / 1438.7 / 1533.1, evenly spaced about 95 px apart. That is a stack of long
horizontal bars: window-blind slats, a stair rail, or drawer pulls -- not door handles. All
score between 0.184 and 0.230, extremely low.

    #0 x[490,519] y[920,987] 29x67 px score 0.239 -> a **vertical bar**, the right shape for a
                                                     door handle
    #5 x[480,504] y[693,750] 24x57 px score 0.173 -> also vertical, but smaller and weaker

**Step 4 - decision**

Every candidate scores low (0.239 at best), so score offers no discrimination. Shape is still a
valid criterion: a door handle should be vertical or compact, not a 210 px horizontal bar. #0
and #5 are the only vertical bars, and #0 has both the higher score (0.239 vs 0.173) and the
larger size.

Positional corroboration: #0's cy of 955.1 sits 31% of the way down door #0's y interval
[628,1686] -- a plausible door-handle height if the handle belongs to another door that was
never detected.

Broken host chain + uniformly very low scores + an unverifiable egocentric locator -> low.

**FINAL: #0**   confidence **low**
