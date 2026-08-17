#!/usr/bin/env python3
"""Reading and projecting the iPhone 3D Scanner App exports, shared by the demo scripts.

The geometry (PLY reading, ARKit->OpenCV flip, pinhole projection) is carried over unchanged
from the closed-set line's demo, where the projection had already passed its self-check.

## Two things added on top of that

**1. EXIF orientation: project in the original frame, then rotate in 2D.**

The app stores its jpgs as 1920x1440 landscape with EXIF orientation=6 (needing a 90 degree
clockwise rotation to stand upright), while `intrinsics` is given relative to the **landscape
original** (verifiable from cx=964 ~ 1920/2 and cy=720 ~ 1440/2).

The closed-set demo only sampled DINOv2 features, and a ViT is insensitive to rotation, so it
never handled this. The instruction-level demo has to feed upright images to an
open-vocabulary segmenter -- a handle or switch lying on its side detects markedly worse --
so segmentation, masks and projection must all live in **the same coordinate system**.

See `rot_uv()`: the orientation **cannot** be handled by modifying K, because K cannot express
an axis swap. Project in the original landscape frame first, then apply a pure 2D transform to
the pixel coordinates. `project_frame()` does both in one call.

Self-check: correlation between the point cloud's own colour and the colour sampled at its
projected pixel. Before the fix -0.23; after, +0.89.

**2. z-buffer visibility.**

SceneFun3D ships depth maps, which the lift stage uses to decide whether a point is occluded.
The iPhone export has **no depth**. This approximates one from the point cloud itself: project
every point into the frame, record the nearest z per pixel cell, and mark a point occluded if
it lies more than `tol` metres beyond its cell's nearest z.

⚠️ A sparse cloud (50k-160k points in these scenes) has holes, and points on the far side can
   leak through them -- so this is only a **coarse filter**. The real guard is still the
   camera-frame front-layer step during lifting.
"""
import os, json, glob
import numpy as np
from PIL import Image, ImageOps

# ARKit camera (+y up, -z forward) -> OpenCV pinhole (+y down, +z forward): flip about x
ARKIT2CV = np.array([1, -1, -1], np.float64)


def read_ply(path):
    """ASCII PLY -> (xyz (N,3) f64, rgb (N,3) u8). Ignores the trailing 'element camera'
    section.

    The app's colored.ply is ascii and runs to well over a hundred thousand lines; parsing
    the body in one pass is an order of magnitude faster than splitting line by line.
    """
    with open(path, "r") as fh:
        nv, names, cur = None, [], None
        while True:
            l = fh.readline()
            if l == "":
                raise ValueError(f"{path}: no end_header found")
            if l.startswith("element"):
                # ⚠️ After the vertex section the header carries an `element camera` section
                #    with 21 properties. Only the vertex section's own properties may be
                #    collected, or the column count more than doubles.
                p = l.split(); cur = p[1]
                if cur == "vertex":
                    nv = int(p[2])
            elif l.startswith("property") and cur == "vertex":
                names.append(l.split()[-1])
            elif l.strip() == "end_header":
                break
        body = "".join(fh.readline() for _ in range(nv))
    ncol = len(names)
    arr = np.fromstring(body, sep=" ").reshape(nv, ncol)
    xyz = arr[:, :3].astype(np.float64)
    ci = [names.index(c) for c in ("red", "green", "blue") if c in names]
    rgb = (arr[:, ci].astype(np.uint8) if len(ci) == 3
           else np.full((nv, 3), 180, np.uint8))
    return xyz, rgb


def rot_uv(u, v, W0, H0, orient):
    """Transform **original landscape** image coordinates (u, v) into the EXIF-corrected
    upright coordinate system. Returns (u', v').

    ⚠️ **This step cannot be folded into the intrinsics matrix.** K expresses only per-axis
       scaling and translation; orient 6 and 8 swap the pixel u and v axes, which in 3D means
       the camera frame's X and Y have to swap with them. Changing only fx/fy/cx/cy leaves
       the 3D points projecting in the landscape frame while the image has been rotated
       upright -- a 90 degree discrepancy where the projected points still "look like they
       land on the image" while the whole thing is turned.

       So: project in the original frame first, then apply this pure 2D transform.

    EXIF: 6 = rotate 90 clockwise to upright, 8 = 90 counter-clockwise, 3 = 180.
    """
    if orient == 6:
        return H0 - 1.0 - v, u
    if orient == 8:
        return v, W0 - 1.0 - u
    if orient == 3:
        return W0 - 1.0 - u, H0 - 1.0 - v
    return u, v


def upright_size(W0, H0, orient):
    return (H0, W0) if orient in (6, 8) else (W0, H0)


def read_frames(scan_dir, upright=True):
    """frame_*.json + frame_*.jpg -> [dict(K, cam2world, rgb, W, H, orient)].

    With upright=True the returned K/W/H have already been rotated into the EXIF-corrected
    coordinate system, matching the image array read_rgb(..., upright=True) returns.
    """
    out = []
    for jf in sorted(glob.glob(os.path.join(scan_dir, "frame_*.json"))):
        jpg = jf.replace(".json", ".jpg")
        if not os.path.exists(jpg):
            continue
        d = json.load(open(jf))
        im = Image.open(jpg)
        W0, H0 = im.size
        orient = im.getexif().get(274, 1)
        K = np.array(d["intrinsics"], np.float64).reshape(3, 3)
        o = int(orient) if upright else 1          # upright=False keeps the original frame
        W, H = upright_size(W0, H0, o)
        out.append(dict(K=K, cam2world=np.array(d["cameraPoseARFrame"], np.float64).reshape(4, 4),
                        rgb=jpg, W=int(W), H=int(H), W0=int(W0), H0=int(H0), orient=o,
                        idx=int(d.get("frame_index", len(out)))))
    return out


def read_rgb(path, upright=True):
    """-> (H, W, 3) uint8. With upright=True the EXIF rotation is applied -- this flag must
    match the one given to read_frames."""
    im = Image.open(path)
    if upright:
        im = ImageOps.exif_transpose(im)
    return np.asarray(im.convert("RGB"), dtype=np.uint8)


def project_frame(xyz, fr):
    """world xyz -> (u, v, z) in **that frame's final coordinate system**.

    With read_frames(upright=True) the output is the EXIF-corrected upright coordinate system,
    corresponding exactly to the array read_rgb(upright=True) returns; with upright=False it
    is the original landscape coordinate system.

    Always call this rather than composing project + rot_uv yourself, so the two cannot fall
    out of sync.
    """
    u, v, z = project(xyz, fr["K"], fr["cam2world"])
    u, v = rot_uv(u, v, fr["W0"], fr["H0"], fr["orient"])
    return u, v, z


def project(xyz, K, cam2world):
    """world xyz -> (u, v, z) in the **original sensor coordinate frame**; z is camera-frame
    depth in metres.

    Note that this always returns pixel coordinates in the landscape original. For upright
    coordinates use project_frame().
    """
    w2c = np.linalg.inv(cam2world)
    Pc = (w2c[:3, :3] @ xyz.T + w2c[:3, 3:4]).T * ARKIT2CV
    z = Pc[:, 2]
    with np.errstate(divide="ignore", invalid="ignore"):
        u = K[0, 0] * Pc[:, 0] / z + K[0, 2]
        v = K[1, 1] * Pc[:, 1] / z + K[1, 2]
    return u, v, z


def visible(u, v, z, W, H, zbuf_tol=0.0, cell=4):
    """In-frustum test; with zbuf_tol > 0, additionally applies z-buffer occlusion (metres).

    cell: the side length in pixels of a depth-buffer cell. Larger cells are less likely to
    leak through holes in a sparse cloud, but more likely to flatten things that are close
    together in depth into one layer. 4 px is a compromise at this resolution.
    """
    ok = (z > 1e-6) & (u >= 0) & (u < W) & (v >= 0) & (v < H)
    if zbuf_tol <= 0 or not ok.any():
        return ok
    gu = (u[ok] / cell).astype(np.int64)
    gv = (v[ok] / cell).astype(np.int64)
    key = gv * (int(W // cell) + 2) + gu
    zz = z[ok]
    order = np.argsort(zz)                       # nearest written first; each cell keeps min z
    k_sorted, z_sorted = key[order], zz[order]
    uniq, first = np.unique(k_sorted, return_index=True)
    zmin = dict(zip(uniq.tolist(), z_sorted[first].tolist()))
    near = np.fromiter((zmin[k] for k in key.tolist()), np.float64, len(key))
    keep = zz <= near + zbuf_tol
    out = ok.copy()
    out[np.nonzero(ok)[0][~keep]] = False
    return out


def write_ply(path, xyz, rgb):
    """Binary PLY, so it opens directly in MeshLab or CloudCompare."""
    n = len(xyz)
    header = (f"ply\nformat binary_little_endian 1.0\nelement vertex {n}\n"
              "property float x\nproperty float y\nproperty float z\n"
              "property uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n")
    arr = np.empty(n, np.dtype([("x", "<f4"), ("y", "<f4"), ("z", "<f4"),
                                ("r", "u1"), ("g", "u1"), ("b", "u1")]))
    arr["x"], arr["y"], arr["z"] = xyz[:, 0], xyz[:, 1], xyz[:, 2]
    arr["r"], arr["g"], arr["b"] = rgb[:, 0], rgb[:, 1], rgb[:, 2]
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(header.encode()); fh.write(arr.tobytes())
