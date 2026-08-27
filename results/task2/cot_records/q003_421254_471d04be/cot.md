# q003

**Instruction**: Open the top left drawer of the cabinet located to the left of the TV

**target**: `drawer handle`   **host**: `drawer`

## Reasoning

**Step 1 - fix the cabinet**

    cabinet 0: x 692-1439, cx 1057.1, 23.2% of the image
    cabinet 1: x 282- 819, cx  513.4, 10.8%
    TV       : x 781-1439, cx 1123.3

cabinet 0's x interval almost entirely overlaps the TV's (692-1439 vs 781-1439) and their
centres differ by only 66 px, so it is **the cabinet underneath the TV**, not the one to its
left. cabinet 1 is what satisfies left_of(cabinet, TV).

**The criterion has to be overlap *and* centre, not centre alone** -- comparing cx by itself
would pick cabinet 0.

**Step 2 - the handles inside cabinet 1** (x 282-819, y 742-1728): 13 of them, forming two
columns by cx.

    left  column cx~357-394: #12(cy 852) #14(978) #15(1098) #17(1213) #16(1324) #18(1431)
    right column cx~550-569: #1 (cy 915) #8 (1062) #10(1197) #7 (1329) #11(1454) #13(1575)

A 2 x 6 array. The left column's cy values are systematically smaller than the right's -- a
perspective effect from the cabinet being at an angle -- so **the columns cannot be cut along
the image axis**, but the vertical ordering within each column is clean.

**Step 3 - select**: top + left -> topmost of the left column -> #12.

Consistency check: #12 falls inside drawer 2 (x 285-457, y 786-946), which is indeed the
topmost drawer of cabinet 1.

## FINAL

`FINAL: #12`   confidence **high**
