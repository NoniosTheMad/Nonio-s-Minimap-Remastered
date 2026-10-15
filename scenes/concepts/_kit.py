"""Massing kit shared by the castle concepts (scenes/concepts/*.py): bbox-bounded SDFs for the shapes the concepts need
and a few terrain helpers. Everything is in scene-local block coordinates; SDFs are negative inside.

    from scenes.concepts._kit import *
    s.fill(ring_band((96, 140, 96), R=58, half_w=2, half_t=1, tilt_x=15), "oxidized_cut_copper")
"""
import math

import numpy as np
from scipy.spatial import cKDTree

from tools.voxel import noise, shapes
from tools.voxel.shapes import SDF


def _bb(c, r):
    return (tuple(v - r for v in c), tuple(v + r for v in c))


def _rot(tilt_x=0.0, tilt_z=0.0, yaw=0.0):
    """World -> local rotation matrix (inverse of yaw * rz * rx)."""
    ax, az, ay = (math.radians(v) for v in (tilt_x, tilt_z, yaw))
    rx = np.array([[1, 0, 0], [0, math.cos(ax), -math.sin(ax)], [0, math.sin(ax), math.cos(ax)]])
    rz = np.array([[math.cos(az), -math.sin(az), 0], [math.sin(az), math.cos(az), 0], [0, 0, 1]])
    ry = np.array([[math.cos(ay), 0, math.sin(ay)], [0, 1, 0], [-math.sin(ay), 0, math.cos(ay)]])
    return (ry @ rz @ rx).T


def ring_band(c, R, half_w, half_t, tilt_x=0.0, tilt_z=0.0, yaw=0.0, gaps=(), gap_w=0.0):
    """Flat band (armillary ring): radius R, half width along its axis half_w, half radial thickness half_t.
    gaps: angles (deg, in the ring's own plane) where a segment of angular width gap_w (deg) is missing."""
    M = _rot(tilt_x, tilt_z, yaw)
    cx, cy, cz = c

    def f(x, y, z):
        dx, dy, dz = x - cx, y - cy, z - cz
        lx = M[0, 0] * dx + M[0, 1] * dy + M[0, 2] * dz
        ly = M[1, 0] * dx + M[1, 1] * dy + M[1, 2] * dz
        lz = M[2, 0] * dx + M[2, 1] * dy + M[2, 2] * dz
        q = np.sqrt(lx ** 2 + lz ** 2) - R
        d = np.maximum(np.abs(q) - half_t, np.abs(ly) - half_w)
        if gaps:
            a = np.degrees(np.arctan2(lz, lx))
            for g in gaps:
                da = np.abs((a - g + 180) % 360 - 180)
                d = np.where(da < gap_w / 2, np.maximum(d, 1.0), d)
        return d
    return SDF(f, _bb(c, R + half_t + half_w + 1))


def helix_rib(c, y0, y1, r0, r1, turns, phase_deg, thick, flat=1.0):
    """A rib winding around a vertical axis: at height y it sits at radius r(y) and angle phase + turns*360*t.
    Distance is approximate (good for steep helices). flat > 1 widens the rib along the tangent."""
    cx, _, cz = c
    ph = math.radians(phase_deg)

    def f(x, y, z):
        t = np.clip((y - y0) / (y1 - y0), 0, 1)
        r = r0 + (r1 - r0) * t
        a = ph + 2 * math.pi * turns * t
        dx, dz = x - cx, z - cz
        rho = np.sqrt(dx ** 2 + dz ** 2)
        th = np.arctan2(dz, dx)
        da = (th - a + math.pi) % (2 * math.pi) - math.pi
        d = np.sqrt((rho - r) ** 2 + (rho * da / flat) ** 2) - thick
        return np.maximum(d, np.maximum(y0 - y, y - y1))
    R = max(r0, r1) + thick + 1
    return SDF(f, ((cx - R, y0, cz - R), (cx + R, y1, cz + R)))


def star_prism(c, y0, y1, n, r_out0, r_in0, r_out1, r_in1, twist_deg=0.0, phase_deg=0.0, power=1.0):
    """Vertical star-section prism (n points) that tapers from (r_out0, r_in0) at y0 to (r_out1, r_in1) at y1 and
    twists by twist_deg over its height. power > 1 bows the taper (stays fat longer, then needles)."""
    cx, _, cz = c

    def f(x, y, z):
        t = np.clip((y - y0) / (y1 - y0), 0, 1) ** power
        ro = r_out0 + (r_out1 - r_out0) * t
        ri = r_in0 + (r_in1 - r_in0) * t
        dx, dz = x - cx, z - cz
        rho = np.sqrt(dx ** 2 + dz ** 2)
        th = np.arctan2(dz, dx) - math.radians(phase_deg) - math.radians(twist_deg) * np.clip((y - y0) / (y1 - y0), 0, 1)
        seg = 2 * math.pi / n
        u = np.abs(((th % seg) / seg) * 2 - 1)        # 1 at a point, 0 in a valley
        redge = ri + (ro - ri) * u
        d = (rho - redge) * 0.8
        return np.maximum(d, np.maximum(y0 - y, y - y1))
    R = max(r_out0, r_out1) + 1
    return SDF(f, ((cx - R, y0, cz - R), (cx + R, y1, cz + R)))


def bezier(pts, n=32):
    P = np.array(pts, float)
    t = np.linspace(0, 1, n)[:, None]
    B = [np.broadcast_to(p, (n, len(p))) for p in P]
    while len(B) > 1:
        B = [B[i] * (1 - t) + B[i + 1] * t for i in range(len(B) - 1)]
    return B[0]


def tube(path, r0, r1, power=1.0):
    """Union of capsules along a polyline (e.g. bezier(...)) whose radius goes from r0 to r1 -> list of SDFs."""
    path = np.asarray(path, float)
    n = len(path) - 1
    out = []
    for i in range(n):
        t = ((i + 0.5) / n) ** power
        r = r0 + (r1 - r0) * t
        out.append(shapes.capsule(path[i], path[i + 1], max(0.45, r)))
    return out


def union(sdfs):
    u = sdfs[0]
    for s in sdfs[1:]:
        u = u | s
    return u


def cone(c, r, y0, y1, r_top=0.0):
    return shapes.cylinder(c, r, y0, y1, r_top)


def pointed_arch_2d(u, v, half_span, spring, rise_k=1.0):
    """Inside test for a pointed (equilateral) arch opening in a plane: u = across (centred), v = up from the floor.
    spring = height of the springing line. Returns bool."""
    R = 2 * half_span * rise_k
    below = (np.abs(u) <= half_span) & (v <= spring)
    vv = v - spring
    left = np.sqrt((u + half_span - R) ** 2 + vv ** 2) <= R      # circle centred at the far side
    right = np.sqrt((u - half_span + R) ** 2 + vv ** 2) <= R
    return below | ((vv >= 0) & left & right & (np.abs(u) <= half_span))


def grid(shape):
    X, Y, Z = shape
    return np.ogrid[0:X, 0:Y, 0:Z]


def cols2d(shape):
    X, _, Z = shape
    return np.meshgrid(np.arange(X) + 0.5, np.arange(Z) + 0.5, indexing="ij")


def heightmask(shape, h, bot=None):
    """Bool grid: y <= h[x,z] (and >= bot[x,z] if given)."""
    y = np.arange(shape[1])[None, :, None]
    m = y <= np.asarray(h)[:, None, :]
    if bot is not None:
        m &= y >= np.asarray(bot)[:, None, :]
    return m


def basalt_cells(shape, region2d, spacing=3.2, seed=0):
    """Voronoi 'organ pipe' cells over a 2D region -> (cell id grid, n cells, centres)."""
    X, _, Z = shape
    rng = np.random.default_rng(seed)
    pts = []
    for j, z in enumerate(np.arange(0, Z, spacing * 0.866)):
        for x in np.arange((j % 2) * spacing / 2, X, spacing):
            pts.append((x + rng.uniform(-0.6, 0.6), z + rng.uniform(-0.6, 0.6)))
    pts = np.array(pts)
    gx, gz = cols2d(shape)
    tree = cKDTree(pts)
    _, cid = tree.query(np.stack([gx.ravel(), gz.ravel()], 1))
    cid = cid.reshape(X, Z)
    return np.where(region2d, cid, -1), len(pts), pts


def wrap_deg(a):
    return (a + 180) % 360 - 180


def polar(shape, c):
    gx, gz = cols2d(shape)
    dx, dz = gx - c[0], gz - c[1]
    return np.hypot(dx, dz), np.degrees(np.arctan2(dz, dx))


def fbm2(gx, gz, scale, seed, octaves=3):
    return noise.fbm(gx, gz, 0.0, scale=scale, octaves=octaves, seed=seed)
