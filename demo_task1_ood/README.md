# Zero-shot demo of the closed-set line on phone scans

The PointTransformerV3 head from the closed-set line
([`../docs/task1_closed_set.md`](../docs/task1_closed_set.md)), run directly on iPhone scans
with **no retraining and no fine-tuning**.

The lift pipeline is reused unchanged: the app's reconstructed point cloud is projected back
into the RGB frames, DINOv2 features are sampled, and the trained head runs on top. No depth is
used, so occlusion is not handled. The ARKit camera convention (+y up, −z forward) is converted
to OpenCV (+y down, +z forward) by flipping Y and Z; the projection self-check placed
8770 / 8770 points in frame.

## Three scenes, deliberately spanning the quality range

| Scene | Points | Frames | Content | Result |
|---|---:|---:|---|---|
| `wall` | 8,770 | — | an untextured flat wall | **0 instances** |
| `piano` | — | — | piano, door, fittings | plausible predictions |
| `kitchen` | 185,000 | 17 | door, switch, socket, piano | plausible predictions, roughly **80% visual precision** |

**The good case includes a genuine generalisation**: piano keys are predicted as `key_press`,
a class-instance pairing the model never saw in training. Sockets go to `plug_in` and switches
to `tip_push` -- the right family, confused within it.

**The bad case is informative too.** On the untextured wall, DINOv2 features are grid noise
with nothing semantic to grasp, and the geometric head is out of distribution on a sparse
plane, so nothing fires at all. That is the honest failure mode rather than a hidden one.

## What this establishes, and what it does not

**The feature backbone transfers.** Phone RGB is close enough to the RGB the features were
lifted from during training.

**The geometric head is the bottleneck.** Training clouds are 5 mm laser scans; iPhone LiDAR is
nominally 5 mm but materially worse. This is the concrete evidence behind "the frozen backbone
carries over, the trained geometric head is what needs replacing with a backend that does not
depend on dense geometry".

**Capture quality decides the outcome** -- density, texture, multiple frames, close range.

**The out-of-distribution prior mismatch is severe.** SceneFun3D's extremely sparse foreground
prior (1300:1) crushes a household scene dense in functional parts: calibrated inference leaves
88 foreground points against 5561 raw. Out-of-distribution inference therefore uses raw logits
plus a confidence threshold rather than the calibrated prior — the opposite of what is correct
in-distribution, which is itself a finding.

Outputs also have some non-determinism (GPU floating point plus voxel-boundary flips): high
confidence predictions are stable, low confidence ones drift.

## Files

```
<scene>/pred.ply         predicted instances, colour coded — open in MeshLab or CloudCompare
<scene>/feat_pca.ply     the lifted DINOv2 features as PCA-RGB, for judging whether the
                         features carry anything semantic in this scene
<scene>/labels_2D/       predictions projected back onto RGB frames
<scene>/points_2D/       the same as points rather than filled labels
<scene>/feat_2D/         per-patch DINOv2 features as PCA-RGB, per frame
```

Reproduced by [`../code/demo/iphone_demo.py`](../code/demo/iphone_demo.py), whose `--la_scale`
and `--conf_thresh` flags are the out-of-distribution controls discussed above.
