"""
lift/data_io.py — SceneFun3D data loading + projection (Phase 1, step 1).

Goal of this module:
  - Reuse the OFFICIAL toolkit DataParser (never hand-parse .traj/.pincam).
  - Load the cropped laser scan (in FULL-laser-scan index space) + per-frame
    {K, cam2world, depth, rgb}, associated by timestamp.
  - Provide project(), and a __main__ sanity check that VERIFIES the coordinate
    convention before we build the lift.

Verified conventions (from scenefun3d/utils/data_parser.py):
  - .traj line = 7 cols: ts, axis-angle rotation (3, rad, world->cam),
    translation (3, m, world->cam). TrajStringToMatrix() returns inv(extrinsics),
    i.e. get_camera_trajectory() yields **cam2world** 4x4. To project a world
    point we need world->cam = inv(cam2world).
  - .pincam = "w h fx fy cx cy"; read_camera_intrinsics(format="matrix") -> K.
  - depth PNG is uint16 millimetres; read_depth_frame() divides by 1000 -> metres.
  - annotation indices & crop_mask index into the FULL laser scan, so we keep
    observed_idx in full-index space (crop first, then map local->full).

Module name: data_io (NOT io). Naming this file `io.py` shadowed the stdlib `io`:
elsewhere `from io import load_scene` resolves to the stdlib io that is already in
sys.modules at interpreter startup (so a later sys.path insert cannot override it)
and fails with ImportError. Renamed to data_io.py to remove that trap for good.
"""

import os
import sys
import numpy as np

# --- Make the official toolkit DataParser importable (reuse it; don't reimplement) ---
TOOLKIT = os.environ.get(
    "SF3D_TOOLKIT", TOOLKIT
)
if TOOLKIT not in sys.path:
    sys.path.insert(0, TOOLKIT)
from utils.data_parser import DataParser  # noqa: E402

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import SCENEFUN3D, TOOLKIT  # noqa: E402

# Max time gap (s) allowed between a frame and its nearest COLMAP pose before we drop
# the frame. hires=10 FPS -> 0.1s spacing; nearest-pose worst case = 0.05s (half-frame).
# ~0.06 leaves float/alignment slack while still rejecting frames whose pose is a real
# mismatch (COLMAP gaps). Set to np.inf to restore the old "always accept" behaviour.
POSE_TIME_TOL = 0.06  # seconds


def load_pointcloud(data_root, visit_id):
    """Load the FULL laser scan + crop mask for one visit (scene-level geometry).
    It is IDENTICAL across the visit's videos (get_laser_scan/get_crop_mask key on
    visit_id, not video_id), so read this ONCE per scene -- not per video.

    Returns dict(parser, P_full (N,3), C_full (N,3) in [0,1], kept_idx (M,) into full,
                 P_keep (M,3) == P_full[kept_idx], C_keep (M,3)).
    """
    dp = DataParser(data_root)
    pcd = dp.get_laser_scan(visit_id)
    P_full = np.asarray(pcd.points)                       # (N,3)
    C_full = np.asarray(pcd.colors)                       # (N,3) in [0,1]
    kept_idx = dp.get_crop_mask(visit_id, return_indices=True)  # (M,) into full
    return dict(parser=dp, P_full=P_full, C_full=C_full, kept_idx=kept_idx,
                P_keep=P_full[kept_idx], C_keep=C_full[kept_idx])


def load_frames(data_root, visit_id, video_id, parser=None):
    """Per-frame assets for ONE video: list of dict(ts, rgb, depth, K(3x3),
    cam2world(4x4)), associated by timestamp. Frames missing depth/intrinsics, or
    whose nearest COLMAP pose is farther than POSE_TIME_TOL, are dropped (never feed
    a mismatched pose into the lift). Pass `parser` to reuse a DataParser instance.

    Returns dict(parser, frames).
    """
    dp = parser or DataParser(data_root)
    rgb_map = dp.get_rgb_frames(visit_id, video_id)              # {ts: path}
    depth_map = dp.get_depth_frames(visit_id, video_id)          # {ts: path}
    intr_map = dp.get_camera_intrinsics(visit_id, video_id)      # {ts: .pincam path}
    poses = dp.get_camera_trajectory(visit_id, video_id, pose_source="colmap")  # {ts: cam2world}

    frames = []
    n_skip_meta, n_skip_pose = 0, 0
    for ts in sorted(rgb_map.keys(), key=float):
        if ts not in depth_map or ts not in intr_map:
            n_skip_meta += 1
            continue
        # hires=10 FPS -> 0.1s spacing; nearest pose worst case 0.05s. POSE_TIME_TOL
        # rejects frames whose nearest pose is a real (COLMAP-gap) mismatch.
        cam2world = dp.get_nearest_pose(ts, poses, time_distance_threshold=POSE_TIME_TOL)
        if cam2world is None:
            n_skip_pose += 1
            continue
        K = dp.read_camera_intrinsics(intr_map[ts], format="matrix")  # 3x3
        frames.append(
            dict(ts=ts, rgb=rgb_map[ts], depth=depth_map[ts], K=K, cam2world=cam2world)
        )

    if n_skip_meta or n_skip_pose:
        # Many dropped frames = sparse/poor COLMAP poses -> worse coverage; surface it.
        print(f"[load_frames {visit_id}/{video_id}] kept {len(frames)} frames; "
              f"skipped {n_skip_meta} (missing depth/intr), {n_skip_pose} (no pose within "
              f"{POSE_TIME_TOL}s)")
    return dict(parser=dp, frames=frames)


def load_scene(data_root, visit_id, video_id):
    """Back-compat: pointcloud + ONE video's frames in a single dict (used by this
    file's __main__ and dinov2_extract's smoke test). The lift uses load_pointcloud
    (once) + load_frames (per video) directly to avoid re-reading the scan."""
    pc = load_pointcloud(data_root, visit_id)
    fr = load_frames(data_root, visit_id, video_id, parser=pc["parser"])
    return dict(parser=pc["parser"], P_full=pc["P_full"], C_full=pc["C_full"],
                kept_idx=pc["kept_idx"], P_keep=pc["P_keep"], C_keep=pc["C_keep"],
                frames=fr["frames"])


def project(P_world, K, cam2world, depth, eps=0.03):
    """Project world points into one frame + occlusion test against GT depth.

    Convention: parser gives cam2world; projection needs world->cam = inv(cam2world).
    Pinhole (OpenCV/COLMAP): u = fx*X/Z + cx, v = fy*Y/Z + cy, camera looks down +Z.

    Args:
        P_world  : (N,3) world coords (laser scan).
        K        : (3,3) intrinsics.
        cam2world: (4,4) camera->world.
        depth    : (H,W) GT depth in metres.
        eps      : occlusion tolerance in metres (a point is visible iff its
                   projected camera-depth matches the GT depth map within eps).

    Returns dict:
        u,v      : (N,) pixel coords (float)
        z        : (N,) camera-frame depth
        ui,vi    : (N,) rounded int pixel coords
        in_view  : (N,) bool, in front of camera & inside image bounds
        visible  : (N,) bool, in_view AND passes occlusion test
    """
    world2cam = np.linalg.inv(cam2world)
    R, t = world2cam[:3, :3], world2cam[:3, 3]
    Pc = P_world @ R.T + t                       # (N,3) camera coords
    z = Pc[:, 2]

    fx, fy, cx, cy = K[0, 0], K[1, 1], K[0, 2], K[1, 2]
    with np.errstate(divide="ignore", invalid="ignore"):
        u = fx * Pc[:, 0] / z + cx
        v = fy * Pc[:, 1] / z + cy

    H, W = depth.shape
    ui = np.round(u).astype(np.int64)
    vi = np.round(v).astype(np.int64)
    in_view = (z > 1e-6) & (ui >= 0) & (ui < W) & (vi >= 0) & (vi < H)

    visible = np.zeros(len(P_world), dtype=bool)
    idx = np.where(in_view)[0]
    d = depth[vi[idx], ui[idx]]                  # GT depth (m) at projected pixel
    ok = (d > 1e-6) & (np.abs(z[idx] - d) < eps)
    visible[idx[ok]] = True

    return dict(u=u, v=v, z=z, ui=ui, vi=vi, in_view=in_view, visible=visible)


if __name__ == "__main__":
    # ---- Coordinate-system sanity check (headless-safe, saves a PNG) ----
    import argparse
    import matplotlib
    matplotlib.use("Agg")  # no display needed
    import matplotlib.pyplot as plt

    ap = argparse.ArgumentParser()
    ap.add_argument("--data_root", default=SCENEFUN3D)
    ap.add_argument("--visit_id", default="420683")
    ap.add_argument("--video_id", default="42445137")
    ap.add_argument("--frame", type=int, default=0, help="which frame index to test")
    ap.add_argument("--eps", type=float, default=0.03, help="occlusion tolerance (m)")
    ap.add_argument("--out", default="./debug_lift")
    ap.add_argument("--plot_max", type=int, default=50000, help="cap scatter points")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    S = load_scene(args.data_root, args.visit_id, args.video_id)
    print(f"[scene] full_pts={len(S['P_full'])}  kept_pts={len(S['P_keep'])}  frames={len(S['frames'])}")

    fr = S["frames"][args.frame]
    depth = S["parser"].read_depth_frame(fr["depth"])  # (H,W) metres
    rgb = S["parser"].read_rgb_frame(fr["rgb"])        # (H,W,3) uint8
    dpos = depth[depth > 0]
    print(f"[frame {args.frame}] ts={fr['ts']}  rgb={rgb.shape}  depth={depth.shape}  "
          f"depth=[{dpos.min():.2f},{dpos.max():.2f}] m")
    print(f"[K]\n{fr['K']}")
    print(f"[cam2world]\n{fr['cam2world']}")

    P, C = S["P_keep"], S["C_keep"]
    out = project(P, fr["K"], fr["cam2world"], depth, eps=args.eps)
    n_view, n_vis = int(out["in_view"].sum()), int(out["visible"].sum())
    print(f"[proj] in_view={n_view} ({100*n_view/len(P):.1f}%)  "
          f"visible_after_occlusion={n_vis} ({100*n_vis/len(P):.1f}%)")

    if n_vis == 0:
        print("[!] 0 visible points -> convention is almost certainly wrong "
              "(check cam2world inversion / image orientation).")
        sys.exit(1)

    # --- Decisive check: paint VISIBLE laser points with THEIR OWN color onto the
    #     RGB frame. If the convention is right, the colored dots line up with the
    #     underlying image content (no offset / rotation / mirror). ---
    vis = np.where(out["visible"])[0]
    if len(vis) > args.plot_max:
        vis = np.random.default_rng(0).choice(vis, args.plot_max, replace=False)

    fig, ax = plt.subplots(1, 2, figsize=(14, 9))
    ax[0].imshow(rgb); ax[0].set_title("RGB"); ax[0].axis("off")
    ax[1].imshow(rgb)
    ax[1].scatter(out["u"][vis], out["v"][vis], s=1, c=np.clip(C[vis], 0, 1), marker=".")
    ax[1].set_title(f"reprojected visible laser pts (n={n_vis})"); ax[1].axis("off")
    png = os.path.join(args.out, f"reproj_{args.visit_id}_{fr['ts']}.png")
    fig.savefig(png, dpi=120, bbox_inches="tight")
    print(f"[saved] {png}")

    # --- Quantitative convention test: RGB sampled at the reprojected pixel vs the
    #     laser point's own color. Same physical surface -> should agree.
    #     Right convention: clearly small (lighting/exposure floor ~0.1).
    #     Wrong convention: ~random (~0.3+). ---
    rgbf = rgb.astype(np.float32) / 255.0
    allvis = out["visible"]
    samp = rgbf[out["vi"][allvis], out["ui"][allvis]]
    diff = float(np.abs(samp - np.clip(C[allvis], 0, 1)).mean())
    print(f"[check] mean |reproj_RGB - laser_RGB| = {diff:.3f}  "
          f"(small ~<0.15 => convention OK; ~0.3 => wrong)")