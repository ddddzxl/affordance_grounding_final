# q042

**Instruction**: Plug the device in the socket next to the door

**target**: `socket`   **host**: `None`

## Reasoning

No host; the socket is located by `next_to(socket, door)`.

- Only `door#0` is credible (score 0.969, 29.8% of the image), spanning x[267,1063]. `door#1`
  at 0.36 and `#2` at 0.193 are weak detections.
- The three sockets, relative to `door#0`:
  - `#0` x[1059,1126] -- its left edge at 1059 **overlaps the door's right edge at 1063 by
    4 px**, i.e. flush against the frame
  - `#1` x[160,199] -- 68 px clear of the door on the left
  - `#2` x[1053,1066] -- also against the door edge, but with area **0.009%** (about 250 px)
    and score **0.21**
- Height corroboration: `#0` at cy 941 is 65% of the way down the image, consistent with socket
  height above the floor; `#2` at cy 424 is 29% down, too high for a socket and more likely a
  switch or a false detection.

`#0` is the only candidate satisfying all three of flush-to-the-door, strong detection, and
plausible height.

**FINAL: #0**
