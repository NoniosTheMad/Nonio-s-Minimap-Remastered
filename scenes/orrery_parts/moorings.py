"""The moorings: three giant copper chains that hold the summit over its crater.

Each chain hangs from an iron-banded hawse (a copper eye set into the rock under a bastion) in a shallow catenary down to
a capstan anchor on the crater's outer slope. The links alternate their plane (real chain), are big enough to read from
the far highland (5 blocks wide, a hole you can see the sky through) and are climbable: a deliberate, risky third route
between the crater and the island. Built after the floating stair (angles chosen so no link comes near it)."""
import math

import numpy as np

from tools.voxel import shapes
from tools.voxel.palette import Mix

from .common import C, FLOOR, SEED, at_polar, cu

MOORINGS = [(300, 70.0), (15, 72.0), (105, 69.0)]      # angle (deg), anchor radius
LINK_H, LINK_R, LINK_T = 1.5, 2.0, 0.72                 # half straight length, loop radius, bar radius
PITCH = 2 * LINK_H + 2 * LINK_R - 2 * LINK_T + 0.3


def _link(p, d, n, mat):
    m = np.cross(d, n)

    def f(X, Y, Z):
        rx, ry, rz = X - p[0], Y - p[1], Z - p[2]
        a = rx * d[0] + ry * d[1] + rz * d[2]
        b = rx * n[0] + ry * n[1] + rz * n[2]
        c = rx * m[0] + ry * m[1] + rz * m[2]
        ac = a - np.clip(a, -LINK_H, LINK_H)
        dp = np.sqrt(ac ** 2 + b ** 2) - LINK_R
        return np.sqrt(dp ** 2 + c ** 2) - LINK_T
    e = LINK_H + LINK_R + LINK_T + 1
    return shapes.SDF(f, ((p[0] - e, p[1] - e, p[2] - e), (p[0] + e, p[1] + e, p[2] + e)))


def _top(s, x, z, below=250):
    col = s.idx[int(x), :below, int(z)]
    nz = np.nonzero(col)[0]
    return int(nz.max()) if len(nz) else 0


def _underside(s, x, z):
    """Lowest solid cell of the island above y 60 in this column."""
    col = s.idx[int(x), 60:FLOOR, int(z)]
    nz = np.nonzero(col)[0]
    return int(nz.min()) + 60 if len(nz) else FLOOR - 6


def chain(s, A, B, sag, age, k):
    A, B = np.array(A, float), np.array(B, float)
    pts = []
    for t in np.linspace(0, 1, 400):
        p = A + (B - A) * t
        p[1] -= sag * 4 * t * (1 - t)
        pts.append(p)
    P = np.array(pts)
    seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
    L = np.concatenate([[0], np.cumsum(seg)])
    n_links = int(L[-1] // PITCH)
    up = np.array([0, 1.0, 0])
    links = []
    for i in range(n_links + 1):
        li = min(i * PITCH, L[-1])
        j = int(np.searchsorted(L, li))
        j = min(max(j, 1), len(P) - 1)
        p = P[j]
        d = P[j] - P[j - 1]
        d /= np.linalg.norm(d)
        e1 = np.cross(d, up)
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(d, e1)
        n = e1 if i % 2 == 0 else e2
        mat = cu(age, "cut") if i % 5 else cu("", "chiseled")
        s.fill(_link(p, d, n, mat), mat)
        links.append(p)
    return links


def hawse(s, p, a):
    """Where the chain enters the rock: a copper eye collar and a calcite-lined socket."""
    x, y, z = p
    s.fill(shapes.sphere((x, y + 1.5, z), 3.6), Mix({"calcite": 2, "polished_tuff": 1}), replace="solid")
    s.fill(shapes.torus((x, y - 0.5, z), 2.8, 0.9), cu("", "chiseled"))
    s.fill(shapes.cylinder((x, 0, z), 1.6, y - 1.5, y + 2.5), "air")


def capstan(s, p, a, age):
    """Ground anchor: a squat drum of tuff banded with copper on a paved pad, two bollards and a lantern."""
    x, y, z = p
    pad = shapes.cylinder((x, 0, z), 6.5, y - 3, y + 0.5)
    s.fill(pad, Mix({"polished_tuff": 3, "tuff_bricks": 2, "cracked_stone_bricks": 0.5}))
    s.fill(shapes.cylinder((x, 0, z), 6.5, y + 0.5, y + 14), "air")
    drum = shapes.cylinder((x, 0, z), 3.4, y + 0.5, y + 6.5)
    s.fill(drum, Mix({"tuff_bricks": 2, "polished_tuff": 1}))
    for yy in (y + 2, y + 5):
        s.fill(shapes.cylinder((x, 0, z), 3.7, yy - 0.5, yy + 0.5) - shapes.cylinder((x, 0, z), 2.0, 0, 999), cu(age, "cut"))
    s.fill(shapes.cylinder((x, 0, z), 2.6, y + 6.5, y + 7.5), cu("", "chiseled"))
    ua = math.radians(a + 90)
    for sgn in (-1, 1):
        bx, bz = x + math.cos(ua) * 5.0 * sgn, z + math.sin(ua) * 5.0 * sgn
        for dy in (1, 2):
            s.set(int(bx), y + dy, int(bz), "polished_tuff_wall")
        s.set(int(bx), y + 3, int(bz), cu(age, "lantern"))


def build(s, ctx):
    stair_P = np.array(ctx.get("stair_path", [(0, -999, 0)]))
    out = []
    ages = ("weathered", "oxidized", "exposed")
    for k, (a, ra) in enumerate(MOORINGS):
        from .island import edge_r
        e = float(edge_r(np.array([a]))[0])
        hx, hz = at_polar(a, e - 14.0)            # deep under the belly: the chain passes the rim > 23 below it
        hy = _underside(s, hx, hz)
        ax, az = at_polar(a, ra)
        gy = _top(s, ax, az, below=80)
        capstan(s, (ax, gy, az), a, ages[k])
        top = (hx, hy + 1.0, hz)
        bot = (ax, gy + 7.5, az)
        links = chain(s, top, bot, sag=9.0, age=ages[k], k=k)
        hawse(s, (hx, hy, hz), a)
        d = np.min(np.linalg.norm(stair_P[None, :, [0, 2, 1]] - np.array(links)[:, None, :], axis=2)) if len(stair_P) > 1 else 99
        out.append(dict(a=a, hawse=(round(hx, 1), hy, round(hz, 1)), anchor=(round(ax, 1), gy, round(az, 1)), links=len(links),
                        stair_clear=round(float(d), 1)))
    ctx["moorings"] = out
