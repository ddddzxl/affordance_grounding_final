# q11 - Plug in the Ninja blender using the nearest socket

## Reasoning

**This question exposes a boundary of the method.** `blender` is detected in only 2 of all 89
frames, and in this frame it scores just 0.466; `food processor` / `juicer` / `mixer` all
return zero, and only the generic term `kitchen appliance` detects anything (5.7 per frame on
average), which cannot distinguish which appliance is which.

In other words: **the open-vocabulary detector does not recognise this branded, irregularly
shaped small appliance.**

Granting the detection for the sake of argument, the distance to `socket #0` is 276 against 428
to `#1` -> **socket 0**. But that premise is itself unreliable, so this is recorded as
`low` / `detection_quality`.

```json
{"final": [0], "confidence": "low", "kind": "detection_quality"}
```
