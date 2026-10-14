"""Castle demo: a small weathered late-medieval border castle on a rocky spur.

Brief (playbook pass 1)
  Aesthetic : "Loarre-on-a-spur": a 15th-century border hold of tuff and deepslate masonry that grows out of its own
              crag, cut off from the approach ridge by a rock-hewn ditch; dark slate roofs, oak-black timber hoardings,
              one weathered-copper spire. Mood: late afternoon, quiet, lived in.
  References: Castillo de Loarre (keep on a rock), Bodiam (round corner towers, corbelled parapets),
              Eltz / Burg Rheinfels (timber hoardings, slate cones), Peñafiel (long curtain on a ridge).
  Scale     : footprint 128x128 (curtain ~70x70), keep walk at +24 over the yard, spire top ~y74.
  Palette   : cool stone ramp  cobbled_deepslate / deepslate_bricks -> tuff_bricks / tuff -> stone_bricks (mossy, cracked
              clusters) -> andesite / polished_andesite trim; polished_deepslate frames; roofs deepslate_tiles.
              Wood: dark_oak (beams, hoardings), spruce (floors, furniture).  Accent (10%): weathered copper + red carpet.
              Ground: rock ramp blackstone -> tuff -> andesite, soil rooted_dirt / coarse_dirt / grass / moss.

Passes are cumulative; CASTLE_PASS=<n> (env) stops after pass n so every pass can be rendered on its own:
  1 massing   2 secondary forms   3 wall depth   4 roofs   5 palette   6 interior   7 decoration   8 lighting

Run:  python -m tools.voxel render scenes/castle.py      (views in .mcdev/voxel/out/castle/)
      python -m tools.voxel place  scenes/castle.py --server castle --pristine
"""
import math
import os

import numpy as np

from tools.voxel import noise, shapes
from tools.voxel.palette import Gradient, Mix, Noise
from tools.voxel.scene import Scene

PASS = int(os.environ.get("CASTLE_PASS", "99"))

W, H, D = 128, 84, 128
SEED = 23
ORIGIN = (-64, 20, -64)            # world position of scene (0,0,0)

L0 = 18                            # meadow level around the spur
P = 34                             # courtyard standing level (floor blocks at P-1)
WALK = P + 10                      # curtain wall-walk standing level

# curtain polygon: tower centres, clockwise seen from above (x east, z south)
NW, NE, SE, GT, SW = (34, 30), (95, 26), (99, 78), (64, 92), (29, 80)
POLY = [NW, NE, SE, GT, SW]
WALL_T = 4                         # curtain thickness

# keep (inclusive box) and its stair turret
KX0, KX1, KZ0, KZ1 = 50, 76, 30, 48     # 27 x 19 outside
KT = 3                                  # keep wall thickness
K_FLOORS = (P - 8, P, P + 8, P + 16, P + 24)   # standing levels: cellar, hall, solar/library, chapel, roof walk
TUR = (79, 39)                          # turret newel (centre column); ring = the 8 cells around it
TUR_TOP = P + 31                        # turret roof-walk standing level

# towers: name, centre, kind, radius / half size, top standing level, roof
TOWERS = [
    ("nw", NW, "round", 6.2, P + 18, "cone"),
    ("ne", NE, "square", 5, P + 20, "hoard"),
    ("se", SE, "round", 5.6, P + 14, "open"),
    ("sw", SW, "round", 4.8, P + 15, "cone"),
]
GATE_X0, GATE_X1 = 62, 66               # gate passage (5 wide)
GH = (55, 73, 84, 96)                   # gatehouse block x0, x1, z0, z1
GH_TOP = P + 15
DT = [(58.5, 96.5), (69.5, 96.5)]       # D-tower fronts
DT_R = 4.6
DITCH = (101, 110)                      # rock-cut ditch across the neck (z range)

FACING = {(1, 0): "east", (-1, 0): "west", (0, 1): "south", (0, -1): "north"}

# ------------------------------------------------------------------ materials
ROCK = Gradient("y", [(L0 - 10, "blackstone"),
                      (L0 - 4, Mix({"cobbled_deepslate": 3, "blackstone": 1})),
                      (L0 + 3, Mix({"deepslate": 2, "tuff": 2})),
                      (L0 + 10, Mix({"tuff": 4, "andesite": 1})),
                      (P - 4, Mix({"tuff": 3, "andesite": 2, "stone": 1})),
                      (99, Mix({"andesite": 3, "tuff": 1, "stone": 2}))],
                jitter=3.5, jitter_scale=7, seed=SEED)


def masonry(seed=0):
    """Value ramp for all walls: dark heavy plinth -> tuff bricks -> stone bricks with mossy/cracked clusters -> light top."""
    mid = Noise([(-0.35, Mix({"tuff_bricks": 4, "tuff": 1})),
                 (0.05, Mix({"tuff_bricks": 3, "stone_bricks": 2, "polished_tuff": 1})),
                 (0.45, Mix({"stone_bricks": 5, "cracked_stone_bricks": 1, "tuff_bricks": 1})),
                 (1, Mix({"stone_bricks": 3, "mossy_stone_bricks": 2}))], scale=7, seed=seed)
    high = Noise([(-0.2, Mix({"stone_bricks": 4, "cracked_stone_bricks": 1})),
                  (0.4, Mix({"stone_bricks": 3, "andesite": 1})),
                  (1, Mix({"stone_bricks": 2, "polished_andesite": 1, "andesite": 1}))], scale=6, seed=seed + 1)
    return Gradient("y", [(P - 3, Mix({"cobbled_deepslate": 3, "deepslate_bricks": 2})),
                          (P + 1, Mix({"deepslate_bricks": 3, "cobbled_deepslate": 1, "tuff_bricks": 1})),
                          (P + 6, Mix({"tuff_bricks": 4, "deepslate_bricks": 1, "mossy_stone_bricks": 1})),
                          (P + 17, mid),
                          (99, high)], jitter=2.5, jitter_scale=6, seed=seed + 2)


MASON = "minecraft:stone_bricks"     # placeholder painted by masonry() in the palette pass
TRIM = "polished_deepslate"
ROOF = "deepslate_tiles"


def grid2():
    return np.meshgrid(np.arange(W) + 0.5, np.arange(D) + 0.5, indexing="ij")


def grid3():
    return np.meshgrid(np.arange(W) + 0.5, np.arange(H) + 0.5, np.arange(D) + 0.5, indexing="ij")


def ycol():
    return np.arange(H)[None, :, None]


# ------------------------------------------------------------------ geometry helpers
def poly_field():
    """Signed distance to the curtain polygon (negative inside), the edge index and the position along that edge."""
    X, Z = grid2()
    cx = sum(p[0] for p in POLY) / len(POLY); cz = sum(p[1] for p in POLY) / len(POLY)
    ds, ts, ns = [], [], []
    for i in range(len(POLY)):
        a = np.array(POLY[i], float); b = np.array(POLY[(i + 1) % len(POLY)], float)
        u = (b - a) / np.linalg.norm(b - a)
        n = np.array([u[1], -u[0]])
        if (np.array([cx, cz]) - a) @ n > 0:
            n = -n
        ds.append((X - a[0]) * n[0] + (Z - a[1]) * n[1])
        ts.append((X - a[0]) * u[0] + (Z - a[1]) * u[1])
        ns.append(n)
    ds = np.array(ds); k = np.argmax(ds, 0)
    sd = ds.max(0); t = np.take_along_axis(np.array(ts), k[None], 0)[0]
    return sd, k, t, ns


SD, EDGE, ALONG, NORMALS = poly_field()


def inward_facing(k):
    n = NORMALS[k]
    if abs(n[0]) > abs(n[1]):
        return "west" if n[0] > 0 else "east"
    return "north" if n[1] > 0 else "south"


def col_mask(m2, y0, y1):
    """2D column mask x [y0, y1] (inclusive) -> 3D bool."""
    m = np.zeros((W, H, D), bool)
    y0 = max(0, int(y0)); y1 = min(H - 1, int(y1))
    if y1 >= y0:
        m[:, y0:y1 + 1, :] = m2[:, None, :]
    return m


def stairify(s, mask, block, top_half=False):
    """Turn the exposed outer steps of a roof mass into stairs (high side toward the mass)."""
    idx = s.idx
    xs, ys, zs = np.nonzero(mask)
    st = {}
    for x, y, z in zip(xs, ys, zs):
        if y + 1 < H and idx[x, y + 1, z] != 0:
            continue
        for (dx, dz), name in FACING.items():
            nx, nz = x + dx, z + dz
            if 0 <= nx < W and 0 <= nz < D and idx[nx, y, nz] == 0 and (y == 0 or idx[nx, y - 1, nz] == 0 or True):
                opp = FACING[(-dx, -dz)]
                key = f"{block}_stairs[facing={opp},half={'top' if top_half else 'bottom'}]"
                st[(x, y, z)] = key
                break
    for (x, y, z), key in st.items():
        s.set(x, y, z, key)


# ------------------------------------------------------------------ pass 1: terrain + massing
def terrain(s):
    X, Z = grid2()
    r = np.hypot(X - 64, Z - 60)
    ang = np.arctan2(Z - 60, X - 64)
    coast = 58 + 5 * noise.fbm(np.cos(ang) * 3, np.sin(ang) * 3, 0.0, scale=1.6, octaves=3, seed=SEED)
    land = L0 + 2.5 * noise.fbm(X, Z, 1.0, scale=18, seed=SEED + 1) - np.clip(r - (coast - 10), 0, None) * 0.45
    # the spur: plateau a few blocks wider than the curtain, steep noisy cliffs
    gh = (X > GH[0] - 3) & (X < GH[1] + 3) & (Z > GH[2]) & (Z < GH[3] + 4)
    dp = SD - 5 - 2.2 * noise.fbm(X, Z, 3.0, scale=9, seed=SEED + 2)
    dp = np.where(gh, np.minimum(dp, -1), dp)
    rise = P - 1 - np.clip(dp, 0, None) * 2.4 + 1.6 * noise.fbm(X, Z, 5.0, scale=6, seed=SEED + 3) * (dp > 0)
    # the neck: a ridge running south from the gate, sloping down to the meadow
    nw = 6.5 + 1.5 * noise.fbm(Z, 0.0, 7.0, scale=8, seed=SEED + 4)
    neck_d = np.abs(X - 64.5) - nw
    neck = P - 1 - np.clip(Z - DITCH[1], 0, None) * 0.62 - np.clip(neck_d, 0, None) * 1.8
    h = np.maximum(land, np.where(dp <= 0, P - 1, rise))
    h = np.maximum(h, np.where(Z > GH[3], neck, -99))
    # rock-cut ditch: V-section across the neck, bottom below meadow level
    zc = (DITCH[0] + DITCH[1]) / 2
    half = (DITCH[1] - DITCH[0]) / 2
    ditch = (np.abs(Z - zc) < half + 0.5) & (np.abs(X - 64.5) < 20)
    dbot = L0 - 2 + np.abs(Z - zc) * 1.2 + 1.2 * noise.fbm(X, Z, 9.0, scale=4, seed=SEED + 5)
    h = np.where(ditch, np.minimum(h, dbot), h)
    h = np.where(r < coast, h, -1)
    h = np.round(h).astype(int)
    # underside: tapers to a point, sky-island style
    t = np.clip(1 - r / coast, 0, 1)
    bot = L0 - 3 - 20 * t ** 0.8 * (0.7 + 0.6 * (noise.fbm(X, Z, 11.0, scale=8, seed=SEED + 6) * 0.5 + 0.5))
    y = ycol()
    m = (y <= h[:, None, :]) & (y >= bot[:, None, :]) & (h[:, None, :] >= 0)
    s.fill(m, ROCK)
    # outcrops on the spur's cliffs: displaced lumps that make overhangs
    rng = np.random.default_rng(SEED)
    for k in range(16):
        a = rng.uniform(0, 2 * math.pi)
        px, pz = 64 + math.cos(a) * 42, 60 + math.sin(a) * 40
        if pz > 88 and abs(px - 64) < 16:
            continue
        lump = shapes.ellipsoid((px, P - 9 + rng.uniform(-3, 3), pz), (rng.uniform(4, 7), rng.uniform(5, 8), rng.uniform(4, 7)))
        lump = lump.displace(amp=2.2, scale=4.5, octaves=2, seed=SEED + 10 + k)
        s.fill(lump & shapes.half_space("y", P - 2, below=True), ROCK, replace="air")
    return h


def curtain(s, hm):
    """Curtain wall: 4 thick, from the rock to the wall-walk; parapet on the outer layer."""
    band = (SD > -WALL_T) & (SD <= 0)
    body = col_mask(band, P - 6, WALK - 1)
    outer = col_mask((SD > -1) & (SD <= 0), WALK, WALK + 1)
    s.fill(body | outer, MASON)
    # foot: wall runs down to the rock where the cliff edge is close
    for x, z in zip(*np.nonzero(band)):
        g = hm[x, z]
        if 0 <= g < P - 6:
            s.idx[x, g:P - 6, z] = s.id(MASON)


def tower_masks(name, c, kind, R, top):
    X, Z = grid2()
    if kind == "round":
        r = np.hypot(X - c[0] - 0.5, Z - c[1] - 0.5)
        return r <= R, r <= R - 2.0, r
    r = np.maximum(np.abs(X - c[0] - 0.5), np.abs(Z - c[1] - 0.5))
    return r <= R + 0.5, r <= R - 1.5, r


def towers(s, hm):
    for name, c, kind, R, top, roof in TOWERS:
        outer, inner, r = tower_masks(name, c, kind, R, top)
        s.fill(col_mask(outer, P - 8, top - 1), MASON)
        s.fill(col_mask(outer & ~inner, top, top + 1), MASON)
        s.fill(col_mask(inner, P, top - 1), "air")
        for x, z in zip(*np.nonzero(outer)):
            g = hm[x, z]
            if 0 <= g < P - 8:
                s.idx[x, g:P - 8, z] = s.id(MASON)


def keep(s):
    s.box((KX0, P - 10, KZ0), (KX1, P + 23, KZ1), MASON)
    s.box((KX0, P + 24, KZ0), (KX1, P + 25, KZ1), MASON)
    s.box((KX0 + 1, P + 24, KZ0 + 1), (KX1 - 1, P + 25, KZ1 - 1), "air")
    # turret: octagon around the newel
    X, Z = grid2()
    tx, tz = TUR[0] + 0.5, TUR[1] + 0.5
    oct_ = np.maximum(np.maximum(np.abs(X - tx), np.abs(Z - tz)), (np.abs(X - tx) + np.abs(Z - tz)) / 1.42) <= 3.6
    s.fill(col_mask(oct_, P - 10, TUR_TOP - 1), MASON)
    s.fill(col_mask(oct_, TUR_TOP, TUR_TOP + 1), MASON)
    return oct_


def gatehouse(s, hm):
    x0, x1, z0, z1 = GH
    s.box((x0, P - 8, z0), (x1, GH_TOP - 1, z1), MASON)
    X, Z = grid2()
    dts = np.zeros((W, D), bool)
    for cx, cz in DT:
        dts |= np.hypot(X - cx, Z - cz) <= DT_R
    s.fill(col_mask(dts, P - 8, GH_TOP - 1), MASON)
    for x, z in zip(*np.nonzero(dts)):
        g = hm[x, z]
        if 0 <= g < P - 8:
            s.idx[x, g:P - 8, z] = s.id(MASON)
    return dts


# ------------------------------------------------------------------ build
def build():
    s = Scene((W, H, D), "castle", seed=SEED)
    hm = terrain(s)
    curtain(s, hm)
    towers(s, hm)
    keep(s)
    gatehouse(s, hm)
    markers(s, hm)
    return s


def markers(s, hm):
    def stand(x, z):
        col = np.nonzero(s.idx[x, :, z])[0]
        return [x, int(col.max()) + 1 if len(col) else 0, z]
    s.mark("spawn_approach", stand(70, 124), look_at=[64, P + 10, 70])
    s.mark("cam_meadow_w", stand(10, 70), look_at=[60, P + 10, 50])
    s.meta["origin"] = list(ORIGIN)
