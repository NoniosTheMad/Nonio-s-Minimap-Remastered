"""Routes between the crater and the island.

Route A, the Floating Stair: from the Landing on the south lip, one full turn clockwise (seen from above) around the
crater, rising from the Landing to the forecourt; a 4-wide ribbon of slab steps hung on stone roots, four lantern
landings (copper hoop gates, lantern posts, an instrument plinth each), bridge-head pylons at the top.
Route B, the Root Helix: from the root geode in the lake, a ribbon spiralling round the amethyst conduit up into the
Throat at the island's tip (the rest of the route is inside the island: Grotto -> Root Shaft -> Orrery Hall)."""
import math

import numpy as np

from tools.voxel import shapes
from tools.voxel.palette import Gradient, Mix

from .common import (C, CRATER_R, FLOOR, LAKE_Y, SEED, UNDERSIDE, at_polar, cu, helix_path, ramp, slab_states)
from .terrain import LANDING, LANDING_Y

STAIR_R0, STAIR_R1 = 52.0, 41.5      # radius at the Landing / at the forecourt
STAIR_W = 4.2
LANDING_TS = (0.2, 0.42, 0.62, 0.82)


def stair_path(n=1400):
    """Samples (x, z, h) of the floating stair: one clockwise turn from the south (90 deg) back to the south."""
    y0, y1 = LANDING_Y + 1, FLOOR + 1
    out = []
    for i in range(n + 1):
        t = i / n
        a = 90 + 360 * t
        rr = STAIR_R0 + (STAIR_R1 - STAIR_R0) * t
        x, z = at_polar(a, rr)
        # rise is eased at both ends (flat run-out onto the Landing and onto the forecourt) and pauses at landings
        e = t
        h = y0 + (y1 - y0) * e
        out.append((x, z, h))
    return out


def _flatten_at_landings(path):
    """Make the stair level for a short run at each landing (a pause in the climb): piecewise-linear remap of h."""
    P = np.array(path)
    n = len(P) - 1
    t = np.linspace(0, 1, n + 1)
    y0, y1 = P[0, 2], P[-1, 2]
    knots_t, knots_h = [0.0], [y0]
    flat = 0.022
    for lt in LANDING_TS:
        knots_t += [lt - flat, lt + flat]
    knots_t.append(1.0)
    # distribute the rise over the sloped segments only
    slopes = [(knots_t[i + 1] - knots_t[i]) for i in range(0, len(knots_t) - 1, 2)]
    total = sum(slopes)
    h = y0
    hs = [y0]
    for i in range(1, len(knots_t)):
        seg = knots_t[i] - knots_t[i - 1]
        if (i - 1) % 2 == 0:
            h += (y1 - y0) * seg / total
        hs.append(h)
    P[:, 2] = np.interp(t, knots_t, hs)
    return [tuple(p) for p in P]


def floating_stair(s, ctx):
    path = _flatten_at_landings(stair_path())
    full, slab = slab_states("polished_tuff")
    cells = ramp(s, path, STAIR_W, full, slab, thick=2, carve=4, chunk=60)
    # edge curb: calcite on the outer edge of the ribbon (a light line that draws the spiral at dusk)
    for x, top, z, d, k in cells:
        if d > STAIR_W / 2 - 0.75:
            if "slab" not in s.get(x, top, z):
                s.set(x, top, z, "calcite")
    # hanging stone roots under the ribbon every few blocks
    rng = np.random.default_rng(SEED + 300)
    P = np.array(path)
    for i in range(0, len(P), 9):
        x, z, h = P[i]
        L = rng.uniform(3, 8)
        s.fill(shapes.cylinder((x, 0, z), 0.5, h - 2 - L, h - 2, 1.7).displace(0.5, 3, seed=i), Gradient("y", [(h - 2 - L * 0.5, Mix({"tuff": 2, "dripstone_block": 1})), (999, Mix({"tuff": 2, "deepslate": 1}))]))
    # landings
    lands = []
    for j, lt in enumerate(LANDING_TS):
        i = int(lt * (len(P) - 1))
        x, z, h = P[i]
        a = math.atan2(z - C[1], x - C[0])
        ox, oz = x + math.cos(a) * 3.2, z + math.sin(a) * 3.2
        yt = int(round(h)) - 1
        s.fill(shapes.cylinder((ox, 0, oz), 4.6, yt - 0.5, yt + 0.5), Mix({"polished_tuff": 2, "calcite": 1, "tuff_bricks": 1}))
        s.fill(shapes.cylinder((ox, 0, oz), 4.6, yt - 1.5, yt - 0.5) - shapes.cylinder((ox, 0, oz), 3.6, 0, 999), "calcite")
        s.fill(shapes.cylinder((ox, 0, oz), 0.5, yt - 16, yt - 1, 4.4).displace(0.9, 3, seed=j), UNDERSIDE)
        # lantern posts on the outer rim
        for da in (-35, 35):
            px, pz = ox + math.cos(a + math.radians(da)) * 3.8, oz + math.sin(a + math.radians(da)) * 3.8
            for dy in range(1, 4):
                s.set(int(math.floor(px)), yt + dy, int(math.floor(pz)), "polished_tuff_wall" if dy < 3 else "calcite")
            s.set(int(math.floor(px)), yt + 4, int(math.floor(pz)), cu("", "lantern"))
        # copper hoop gate over the stair (a ring standing across the path)
        tx, tz = -math.sin(a), math.cos(a)           # stair tangent
        hoop = shapes.SDF(lambda X, Y, Z, x=x, z=z, y=yt + 1, tx=tx, tz=tz: np.maximum(
            np.abs((X - x) * tx + (Z - z) * tz) - 0.5,
            np.abs(np.sqrt(((X - x) * -tz + (Z - z) * tx) ** 2 + (Y - y) ** 2) - 3.6) - 0.6),
            ((x - 6, yt - 4, z - 6), (x + 6, yt + 6, z + 6)))
        ages = ("exposed", "weathered", "oxidized", "")
        s.fill(hoop & shapes.half_space("y", yt + 1.5, below=False), cu(ages[j], "cut"))
        lands.append(dict(c=(ox, oz), y=yt, a=math.degrees(a)))
    ctx["stair_cells"] = cells
    ctx["stair_landings"] = lands
    ctx["stair_path"] = path


def conduit(s, ctx):
    """The amethyst chain: floating shards from the root geode to the throat, tightening upwards."""
    y = LAKE_Y + 8
    k = 0
    while y < 50:
        R = 2.6 - 1.0 * (y - LAKE_Y) / (50 - LAKE_Y)
        oct_ = shapes.SDF(lambda X, Y, Z, y=y, R=R: (np.abs(X - C[0]) + np.abs(Y - y) * 0.55 + np.abs(Z - C[1])) - R * 1.4,
                          ((C[0] - 6, y - 7, C[1] - 6), (C[0] + 6, y + 7, C[1] + 6)))
        s.fill(oct_, "amethyst_block")
        y += 6 + (k % 2)
        k += 1


def root_helix(s, ctx):
    """Route B lower half: from the floor of the root geode up and round the conduit into the Throat."""
    from .island import GROTTO_FLOOR
    # the geode roof is broken open above the helix (oculus) so the climb is in the open
    s.fill(shapes.cylinder((C[0], 0, C[1]), 9.0, LAKE_Y + 12, LAKE_Y + 24), "air")
    full, slab = slab_states("smooth_quartz")
    path = helix_path(C, 6.6, 90, LAKE_Y + 2, GROTTO_FLOOR + 1, rise_per_block=0.5, direction=1, step=0.5)
    cells = ramp(s, path, 3.2, full, slab, thick=1, carve=4, chunk=40)
    ctx["root_helix"] = path


def shaft_helix(s, ctx):
    """Route B upper half: from the Root Grotto floor up the Root Shaft, coiling round the amethyst heart, out through
    the oculus onto the Orrery Hall floor. The open core of the helix is the deliberate fall (lethal from the top)."""
    from .island import GROTTO_FLOOR
    full, slab = slab_states("smooth_quartz")
    path = helix_path(C, 5.0, 270, GROTTO_FLOOR + 1, FLOOR + 1, rise_per_block=0.5, direction=1, step=0.5)
    ramp(s, path, 2.6, full, slab, thick=1, carve=3, chunk=40)
    ctx["shaft_helix"] = path


def build(s, ctx):
    root_helix(s, ctx)
    shaft_helix(s, ctx)
    conduit(s, ctx)
    floating_stair(s, ctx)
