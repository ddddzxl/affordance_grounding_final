# q378

**Instruction**: Open the freezer

**target**: `freezer handle`   **host**: `freezer`

## Reasoning

The two freezer detections are in fact the fridge's upper and lower compartments:

- `freezer#1` y[487,924], height **437**
- `freezer#0` y[940,1804], height **864**

Small above, large below -> a **top-freezer layout** (the freezer compartment is on top and is
about 33% of the unit, matching 437/1317 = 33%); in a bottom-freezer layout the lower
compartment would be the smaller one.

So the freezer is the upper compartment, `freezer#1` -> the containment table gives
`contains #0`.

(`#1` at cx 1219 and `#3` at cx 1187 are 32 px apart with cy differing by 2 -- the lower
compartment's handle split into two pieces; `#2` x[1315,1439] falls outside both freezers.)

This relies on general knowledge of fridge layouts rather than pure geometry, so it is marked
medium.

**FINAL: #0**   confidence **medium**
