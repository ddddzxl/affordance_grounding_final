# q160

**Instruction**: Adjust the intensity of the heater next to the blue couch

**target**: `heater knob`   **host**: `heater`

## Reasoning

heater#0 contains two knobs with nearly identical cx (428 / 429) and cy differing by 85 px, and
#1 is only 20x19 px -- more likely an attached part of #0 than a second valve. Emit the main
body, #0 (78x119, score 0.544).

**FINAL: #0**
