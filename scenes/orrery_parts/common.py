"""Shared constants, palettes and helpers for the Orrery of Ast.

Axes: x east, y up, z south (scene-local). Polar angles are atan2(dz, dx) in degrees: 0 = east, 90 = south (the axis
of approach), 180 = west, -90 = north. All copper is waxed (copper oxidises in game; a protected build would restore
it forever)."""
import math

import numpy as np
from scipy.spatial import cKDTree

from tools.voxel import noise, shapes
from tools.voxel.palette import Gradient, Mix, Noise

W, H, D = 208, 250, 208
C = (104.0, 104.0)                  # plan centre (x, z)
SEED = 4242

GROUND = 30                         # highland mean level
CRATER_R = 50                       # crater lip radius
LAKE_Y = 15                         # lake surface (top water block)
FLOOR = 108                         # island deck / court floor: top solid block (feet at FLOOR + 1)
ISLAND_R = 36
ISLAND_TIP = 56
WALL_R = 30                         # ring wall centre radius
SPIRE_TOP = 242
HUB_Y = 160                         # centre of the armillary (ring centre, axle height)
RING_C = (C[0], float(HUB_Y), C[1])

# ------------------------------------------------------------------ copper (always waxed)
AGES = ("", "exposed", "weathered", "oxidized")


def cu(age, kind="block", **props):
    """Waxed copper state. age: '' | exposed | weathered | oxidized. kind: block, cut, chiseled, grate, slab, stairs,
    bulb, bars, chain, lantern, trapdoor, door, rod (lightning rod), statue."""
    a = f"{age}_" if age else ""
    if kind == "block":
        n = f"waxed_{age}_copper" if age else "waxed_copper_block"
    elif kind == "rod":
        n = f"waxed_{a}lightning_rod"
    elif kind == "statue":
        n = f"waxed_{a}copper_golem_statue"
    else:
        n = {"cut": "cut_copper", "chiseled": "chiseled_copper", "grate": "copper_grate", "slab": "cut_copper_slab",
             "stairs": "cut_copper_stairs", "bulb": "copper_bulb", "bars": "copper_bars", "chain": "copper_chain",
             "lantern": "copper_lantern", "trapdoor": "copper_trapdoor", "door": "copper_door"}[kind]
        n = f"waxed_{a}{n}"
    if props:
        n += "[" + ",".join(f"{k}={v}" for k, v in props.items()) + "]"
    return n


# ------------------------------------------------------------------ palettes (roles: art-direction sheet scenes/orrery.md)
GRASS = Noise([(-0.3, Mix({"moss_block": 2, "grass_block": 3})), (0.35, "grass_block"),
               (1, Mix({"grass_block": 4, "coarse_dirt": 1}))], scale=11, seed=SEED)
SOIL = Mix({"dirt": 3, "coarse_dirt": 1, "rooted_dirt": 1})
ROCK = Gradient("y", [(GROUND - 24, Mix({"deepslate": 3, "cobbled_deepslate": 1})),
                      (GROUND - 10, Mix({"tuff": 3, "deepslate": 1, "andesite": 0.5})),
                      (999, Mix({"tuff": 3, "andesite": 1.2, "calcite": 0.6, "stone": 0.6}))], jitter=4, jitter_scale=7, seed=SEED)
UNDERSIDE = Gradient("y", [(ISLAND_TIP + 12, Mix({"deepslate": 3, "cobbled_deepslate": 1, "tuff": 1})),
                           (FLOOR - 26, Mix({"tuff": 3, "deepslate": 1.2, "calcite": 0.4})),
                           (FLOOR - 8, Mix({"tuff": 3, "andesite": 1, "calcite": 0.8})),
                           (999, Mix({"calcite": 1, "tuff": 2, "dripstone_block": 0.4}))],
                     jitter=4, jitter_scale=6, seed=SEED + 1)
MASONRY = Gradient("y", [(FLOOR + 3, Mix({"deepslate_bricks": 3, "polished_deepslate": 1, "cracked_deepslate_bricks": 0.4})),
                         (FLOOR + 14, Mix({"tuff_bricks": 3, "polished_tuff": 1, "deepslate_bricks": 0.6})),
                         (FLOOR + 36, Mix({"tuff_bricks": 2, "polished_tuff": 1, "calcite": 0.5})),
                         (999, Mix({"calcite": 2, "tuff_bricks": 1, "smooth_quartz": 0.4}))], jitter=3, jitter_scale=6, seed=SEED + 2)
SPIRE_BODY = Gradient("y", [(FLOOR + 10, Mix({"polished_deepslate": 2, "deepslate_tiles": 1, "deepslate_bricks": 1})),
                            (142, Mix({"deepslate_bricks": 2, "tuff_bricks": 1.2, "polished_deepslate": 0.5})),
                            (170, Mix({"tuff_bricks": 2, "polished_tuff": 1, "calcite": 0.6})),
                            (999, Mix({"calcite": 2, "quartz_bricks": 1, "polished_tuff": 0.4}))], jitter=4, jitter_scale=8, seed=SEED + 3)
TRIM = Mix({"calcite": 4, "polished_diorite": 0.0001, "smooth_quartz": 1})   # pilasters, linings, crowns
TRIM_SOLID = "calcite"
PAVING = Mix({"polished_tuff": 3, "tuff_bricks": 2, "polished_deepslate": 1, "tuff": 0.5})
FEATURE = "amethyst_block"
GLASS_V = "purple_stained_glass"
GLASS_V_PANE = "purple_stained_glass_pane"


# ------------------------------------------------------------------ geometry helpers
def wrap_deg(a):
    return (a + 180) % 360 - 180


def polar_xz(x, z):
    dx, dz = x - C[0], z - C[1]
    return np.hypot(dx, dz), np.degrees(np.arctan2(dz, dx))


def at_polar(a_deg, r, c=C):
    a = math.radians(a_deg)
    return c[0] + math.cos(a) * r, c[1] + math.sin(a) * r


def cols2d(shape=(W, H, D)):
    X, _, Z = shape
    return np.meshgrid(np.arange(X) + 0.5, np.arange(Z) + 0.5, indexing="ij")


def fbm2(gx, gz, scale, seed, octaves=3):
    return noise.fbm(gx, gz, 0.0, scale=scale, octaves=octaves, seed=seed)


def heightmask(shape, h, bot=None):
    y = np.arange(shape[1])[None, :, None]
    m = y <= np.asarray(h)[:, None, :]
    if bot is not None:
        m &= y >= np.asarray(bot)[:, None, :]
    return m


class Box:
    """Sub-box of the scene grid [lo, hi) clipped to the scene, with voxel-centre coordinate grids."""

    def __init__(self, s, lo, hi):
        self.s = s
        self.lo = [max(0, int(math.floor(v))) for v in lo]
        self.hi = [min(n, int(math.ceil(v))) for v, n in zip(hi, s.shape)]
        self.ok = all(h > l for l, h in zip(self.lo, self.hi))
        x, y, z = np.ogrid[self.lo[0]:self.hi[0], self.lo[1]:self.hi[1], self.lo[2]:self.hi[2]]
        self.x, self.y, self.z = x + 0.5, y + 0.5, z + 0.5
        self.xi, self.yi, self.zi = x, y, z

    @property
    def shape(self):
        return tuple(h - l for l, h in zip(self.lo, self.hi))

    def full(self, m):
        out = np.zeros(self.s.shape, bool)
        if self.ok:
            out[self.lo[0]:self.hi[0], self.lo[1]:self.hi[1], self.lo[2]:self.hi[2]] = np.broadcast_to(m, self.shape)
        return out

    def fill(self, m, spec, replace=None):
        if not self.ok:
            return 0
        return self.s.fill(self.full(m), spec, replace=replace)

    def view(self):
        return self.s.idx[self.lo[0]:self.hi[0], self.lo[1]:self.hi[1], self.lo[2]:self.hi[2]]


def box_around(s, c, r, y0, y1):
    return Box(s, (c[0] - r - 1, y0, c[1] - r - 1), (c[0] + r + 2, y1 + 1, c[1] + r + 2))


def column_top(s, x, z, below=None):
    col = s.idx[int(x), : (below if below is not None else s.shape[1]), int(z)]
    nz = np.nonzero(col)[0]
    return int(nz.max()) if len(nz) else -1


def solid_mask(s, names=("air", "water", "cave_air")):
    """True where the cell is not air/water."""
    air_ids = [i for i, p in enumerate(s.palette) if p.split("[")[0].split(":")[-1] in names]
    lut = np.ones(len(s.palette), bool)
    lut[air_ids] = False
    return lut[s.idx]


# ------------------------------------------------------------------ walking surfaces
def slab_states(material):
    """(full block, bottom slab) for a stone family name, e.g. 'polished_tuff' -> ('polished_tuff', 'polished_tuff_slab')."""
    slab = {"tuff_bricks": "tuff_brick_slab", "deepslate_bricks": "deepslate_brick_slab",
            "deepslate_tiles": "deepslate_tile_slab", "stone_bricks": "stone_brick_slab",
            "polished_blackstone_bricks": "polished_blackstone_brick_slab", "mud_bricks": "mud_brick_slab",
            "quartz_bricks": "quartz_slab"}.get(material, material + "_slab")
    return material, slab + "[type=bottom]"


def ramp(s, path, width, full, slab, thick=2, carve=0, edge=None, edge_h=0, chunk=40):
    """Walkable ribbon along `path` = [(x, z, h), ...] (dense, ~0.5 block apart; h = surface height in blocks, rounded to
    halves). Columns within width/2 of the path get the height of the nearest sample: a bottom slab when the surface is
    at .5, else a full block, plus `thick`-1 blocks below. carve > 0 clears that many cells of air above the surface.
    edge: state for a parapet/curb on cells whose distance is in the outer half block of the ribbon (edge_h high).
    The path is processed in chunks (of `chunk` samples, keep < 0.8 turn for tight helices) so stacked turns don't fight.
    Returns [(x, y_top_cell, z, distance_to_path, path_index)] for every column written."""
    P = np.asarray(path, float)
    out = []
    n = len(P)
    for c0 in range(0, n, chunk):
        Q = P[max(0, c0 - 2): min(n, c0 + chunk + 2)]
        lo = Q[:, [0, 1]].min(0) - width; hi = Q[:, [0, 1]].max(0) + width
        xs, zs = np.meshgrid(np.arange(int(lo[0]), int(hi[0]) + 1), np.arange(int(lo[1]), int(hi[1]) + 1), indexing="ij")
        xs, zs = xs.ravel(), zs.ravel()
        tree = cKDTree(Q[:, :2])
        d, k = tree.query(np.stack([xs + 0.5, zs + 0.5], 1))
        # only claim columns nearest to THIS chunk's core samples (no double writes at chunk seams)
        core = (k >= (2 if c0 > 0 else 0)) & (k < len(Q) - (2 if c0 + chunk < n else 0))
        sel = (d <= width / 2) & core
        for x, z, dd, kk in zip(xs[sel], zs[sel], d[sel], k[sel]):
            if not (0 <= x < s.shape[0] and 0 <= z < s.shape[2]):
                continue
            h = round(Q[kk, 2] * 2) / 2
            yb = int(math.floor(h))
            if h - yb >= 0.5:      # slab surface
                s.set(x, yb, z, slab)
                top_cell = yb
                for t in range(1, thick):
                    s.set(x, yb - t, z, full)
                feet = yb + 1
            else:
                for t in range(1, thick + 1):
                    s.set(x, yb - t, z, full)
                top_cell = yb - 1
                feet = yb
            for t in range(carve):
                if 0 <= feet + t < s.shape[1]:
                    s.set(x, feet + t, z, "air")
            if edge is not None and dd > width / 2 - 1.0:
                for t in range(edge_h):
                    s.set(x, feet + t, z, edge)
            out.append((int(x), int(top_cell), int(z), float(dd), int(max(0, c0 - 2) + kk)))
    return out


def helix_path(c, r, a0_deg, y0, y1, rise_per_block=0.5, direction=1, step=0.5, r1=None):
    """Samples of a helix (x, z, h) around c=(x, z) from height y0 to y1 rising rise_per_block per block of arc.
    direction +1 = increasing angle (clockwise seen from above, since z points south). r1: end radius (taper)."""
    L = (y1 - y0) / rise_per_block
    n = max(2, int(L / step))
    out = []
    for i in range(n + 1):
        t = i / n
        rr = r + ((r1 if r1 is not None else r) - r) * t
        arc = L * t
        a = math.radians(a0_deg) + direction * arc / max(rr, 1e-3)
        out.append((c[0] + math.cos(a) * rr, c[1] + math.sin(a) * rr, y0 + (y1 - y0) * t))
    return out


# ------------------------------------------------------------------ rotations (rings, tilted things)
def rot(tilt_x=0.0, tilt_z=0.0, yaw=0.0):
    """local -> world rotation matrix = Ry(yaw) Rz(tilt_z) Rx(tilt_x)."""
    ax, az, ay = (math.radians(v) for v in (tilt_x, tilt_z, yaw))
    rx = np.array([[1, 0, 0], [0, math.cos(ax), -math.sin(ax)], [0, math.sin(ax), math.cos(ax)]])
    rz = np.array([[math.cos(az), -math.sin(az), 0], [math.sin(az), math.cos(az), 0], [0, 0, 1]])
    ry = np.array([[math.cos(ay), 0, math.sin(ay)], [0, 1, 0], [-math.sin(ay), 0, math.cos(ay)]])
    return ry @ rz @ rx


def to_local(M, c, x, y, z):
    """World voxel-centre coords -> local (lx, ly, lz) for local->world matrix M around centre c."""
    dx, dy, dz = x - c[0], y - c[1], z - c[2]
    Mt = M.T
    lx = Mt[0, 0] * dx + Mt[0, 1] * dy + Mt[0, 2] * dz
    ly = Mt[1, 0] * dx + Mt[1, 1] * dy + Mt[1, 2] * dz
    lz = Mt[2, 0] * dx + Mt[2, 1] * dy + Mt[2, 2] * dz
    return lx, ly, lz


def facing_of(dx, dz):
    """Horizontal facing name for a direction vector."""
    if abs(dx) >= abs(dz):
        return "east" if dx > 0 else "west"
    return "south" if dz > 0 else "north"


OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}
