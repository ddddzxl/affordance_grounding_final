# q228

**Instruction**: Turn on the ceiling light

**target**: `light switch`   **host**: `None`

## Reasoning

**Step 1 - structure**: host = None, no relation, no select.

**Step 2 - candidates**

    #0 x[927,987] y[685,764]   60x79 px    area 0.146% score 0.879
    #1 x[0,306]   y[695,1439]  306x744 px  area 0.057% score 0.194
    #2 x[0,26]    y[1357,1439] 26x82       area 0.047% score 0.181

**Step 3 - excluding #1 and #2**

#1's bbox is 306x744, a considerable fraction of the frame, yet its mask area is only 0.057% --
an enormous box with almost no actual pixels, the classic signature of scattered pixels merged
into one instance (the candidate table's own note warns about exactly this). #2 sits at
x[0,26] y[1357,1439], hard against the lower-left corner, 26x82 px at score 0.181 -- an edge
fragment.

**Step 4 - positive evidence for #0**

Score 0.879 is 4.5x the runner-up (0.194) -- very strong discrimination. Geometrically:

    60x79 px, a vertical rectangle: the standard shape of a single switch plate
    cy 721 is 50% of the way down the frame, corresponding to a wall height of about 1.2-1.4 m
    area 0.146% against a bbox area of 60x79 = 4740 px (0.171%) -- a high fill ratio, so this
      is a solid object rather than scattered pixels

Both the score gap and the geometric evidence are far stronger here than on comparable
questions, and both competitors can be positively identified as false detections -> high.

**FINAL: #0**   confidence **high**

> Flagged as a question defect (`unanswerable`) on review, despite the confident reasoning.
