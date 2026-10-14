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
    neck = P - 1 - np.clip(Z - DITCH[1] - 1, 0, None) * 0.7 - np.clip(neck_d, 0, None) * 1.8
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


# ------------------------------------------------------------------ pass 2: secondary forms
RING = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]   # clockwise from above
SPIRAL_Y0 = P - 16                                                               # stair k sits at y0+k in RING[k%8]
SPIRAL_K = range(7, 48)                                                          # cellar (P-9) .. lookout (P+31)


def crenels(s):
    """Merlons (2 on, 1 off) on the curtain parapet."""
    outer = (SD > -1) & (SD <= 0)
    on = (np.floor(ALONG) % 3) != 0
    s.fill(col_mask(outer & on, WALK + 2, WALK + 2), MASON)


def tower_tops(s):
    for name, c, kind, R, top, roof in TOWERS:
        outer, inner, r = tower_masks(name, c, kind, R, top)
        X, Z = grid2()
        ang = np.degrees(np.arctan2(Z - c[1] - 0.5, X - c[0] - 0.5)) % 360
        rim = outer & ~(r <= (R - 1.0 if kind == "round" else R - 0.5))
        if roof in ("open", "cone"):
            on = (ang // (360 / (round(R * 2.2) * 2))) % 2 == 0 if kind == "round" else ((np.floor(X) + np.floor(Z)) % 3 != 0)
            s.fill(col_mask(rim & on, top + 2, top + 2), MASON)


def gate(s):
    x0, x1, z0, z1 = GH
    # passage through the gatehouse and curtain, rounded head
    s.box((GATE_X0, P, z0 - 6), (GATE_X1, P + 4, z1 + 6), "air", replace=MASON)
    s.box((GATE_X0 + 1, P + 5, z0 - 6), (GATE_X1 - 1, P + 5, z1 + 6), "air", replace=MASON)
    s.box((GATE_X0, P - 1, z0 - 6), (GATE_X1, P - 1, z1 + 2), "cobbled_deepslate")
    # gatehouse top: parapet + merlons
    s.box((x0 + 1, GH_TOP, z0 + 1), (x1 - 1, GH_TOP + 1, z1 - 1), MASON)
    s.box((x0 + 2, GH_TOP, z0 + 2), (x1 - 2, GH_TOP + 1, z1 - 2), "air")
    X, Z = grid2()
    for cx, cz in DT:
        r = np.hypot(X - cx, Z - cz)
        rim = (r <= DT_R) & (r > DT_R - 1.2)
        s.fill(col_mask(rim, GH_TOP, GH_TOP + 1), MASON)
        ang = np.degrees(np.arctan2(Z - cz, X - cx)) % 360
        s.fill(col_mask(rim & ((ang // 30) % 2 == 0), GH_TOP + 2, GH_TOP + 2), MASON)
    # drawbridge over the ditch: stripped dark oak rails, spruce deck
    for z in range(z1 + 1, DITCH[1] + 2):
        for x in range(GATE_X0, GATE_X1 + 1):
            s.set(x, P - 1, z, "stripped_dark_oak_log[axis=z]" if x in (GATE_X0, GATE_X1) else "spruce_planks")
            for y in range(P, P + 4):
                if s.idx[x, y, z] != 0 and z > z1 + 1:
                    s.idx[x, y, z] = 0
        s.set(GATE_X0, P, z, "dark_oak_fence"); s.set(GATE_X1, P, z, "dark_oak_fence")


def keep_body(s, oct_):
    ix0, ix1, iz0, iz1 = KX0 + KT, KX1 - KT, KZ0 + KT, KZ1 - KT
    # hollow storeys, floors at F-1
    s.box((ix0, P - 9, iz0), (ix1, P + 22, iz1), "air")
    for F in K_FLOORS:
        s.box((ix0, F - 1, iz0), (ix1, F - 1, iz1), "spruce_planks" if P < F < P + 24 else "polished_tuff")
    # roof walk: wall top at P+23, parapet ring at P+24..25 (built in massing), merlons
    s.box((KX0 + 1, P + 24, KZ0 + 1), (KX1 - 1, P + 25, KZ1 - 1), "air")
    X, Z = grid2()
    ring = (X >= KX0) & (X < KX1 + 1) & (Z >= KZ0) & (Z < KZ1 + 1)
    ring &= ~((X >= KX0 + 1) & (X < KX1) & (Z >= KZ0 + 1) & (Z < KZ1))
    on = ((np.floor(X) + np.floor(Z)) % 3) != 0
    s.fill(col_mask(ring & on, P + 26, P + 26), MASON)
    # main door (south), 3 wide x 4 high + head, a flight of steps outside
    s.box((62, P, KZ1 - KT), (64, P + 3, KZ1), "air")
    s.set(63, P + 4, KZ1 - 1, "air"); s.set(63, P + 4, KZ1, "air")
    # chimney stack on the west face
    s.box((KX0 - 2, P - 1, 37), (KX0 - 1, P + 30, 41), MASON)
    s.box((KX0 - 2, P + 31, 38), (KX0 - 1, P + 31, 40), "air")
    # clasping corner buttresses, stepped
    for cx, cz, sx, sz in ((KX0, KZ1, -1, 1), (KX1, KZ1, 1, 1), (KX0, KZ0, -1, -1)):
        for step, top in ((2, P + 8), (1, P + 16)):
            s.box((cx + sx * step, P - 1, cz - sz * 2), (cx + sx * step, top, cz + sz * step), MASON, replace="air")
            s.box((cx - sx * 2, P - 1, cz + sz * step), (cx + sx * step, top, cz + sz * step), MASON, replace="air")


def stair_turret(s, oct_):
    tx, tz = TUR
    ring_cells = [(tx + dx, tz + dz) for dx, dz in RING]
    # carve the shaft and keep the newel
    for x, z in ring_cells:
        s.idx[x, P - 9:P + 34, z] = 0
    s.box((tx, P - 10, tz), (tx, P + 31, tz), "polished_deepslate")
    for x, z in ring_cells:
        s.set(x, P - 10, z, "polished_tuff")
    for k in SPIRAL_K:
        i = k % 8
        x, z = ring_cells[i]
        nx, nz = ring_cells[(i + 1) % 8]
        face = FACING[(int(np.sign(nx - x)), int(np.sign(nz - z)))]
        s.set(x, SPIRAL_Y0 + k, z, f"stone_brick_stairs[facing={face}]")
    # lookout floor
    for x, z in ring_cells:
        if s.idx[x, P + 31, z] == 0:
            s.set(x, P + 31, z, "spruce_slab[type=top]")
    # doors west into the keep at every storey (ring cell 7 = west of the newel)
    for F in K_FLOORS[:-1]:
        s.box((KX1 - KT + 1, F, tz), (tx - 2, F + 2, tz), "air")
        s.box((KX1 - KT + 1, F - 1, tz), (tx - 2, F - 1, tz), "polished_tuff")
    s.box((KX1, P + 24, tz), (tx - 2, P + 26, tz), "air")
    s.box((KX1, P + 23, tz), (tx - 2, P + 23, tz), "polished_tuff")
    # turret rises above the keep: lookout with 8 openings, walls to P+34
    s.fill(col_mask(oct_, P + 26, P + 34), MASON)
    for x, z in ring_cells + [(tx, tz)]:
        s.idx[x, P + 32:P + 35, z] = 0
    for dx, dz in ((0, -3), (0, 3), (-3, 0), (3, 0)):
        s.box((tx + dx, P + 32, tz + dz), (tx + dx, P + 33, tz + dz), "air")


def courtyard_stairs(s):
    """Two flights from the yard to the wall-walk, against the inner face of the west and east curtains."""
    for zr, edge in ((range(48, 58), 4), (range(50, 60), 1)):
        for k, z in enumerate(zr):
            xs = [x for x in range(W) if -6 < SD[x, z] <= -4 and EDGE[x, z] == edge]
            for x in xs:
                y = P + k
                s.idx[x, P - 1:y, z] = s.id(MASON)
                s.set(x, y, z, "stone_brick_stairs[facing=north]")
                s.idx[x, y + 1:y + 5, z] = 0


def lean_to(s):
    """Service range against the west curtain: stone ground storey, jettied dark-oak/spruce upper storey, pent roof."""
    zs, ze = 62, 76
    inside = (SD > -11) & (SD <= -4) & (EDGE == 4)
    X, Z = grid2()
    m2 = inside & (Z >= zs) & (Z <= ze + 1)
    body = m2 & (SD <= -4) & (SD > -10)
    s.fill(col_mask(body, P - 1, P + 4), MASON)
    s.fill(col_mask(body & (SD > -9) & (Z > zs) & (Z < ze + 1), P, P + 3), "air")
    s.fill(col_mask(body & (SD > -9) & (Z > zs) & (Z < ze + 1), P - 1, P - 1), "spruce_planks")
    s.fill(col_mask(body & (SD > -9) & (Z > zs) & (Z < ze + 1), P + 4, P + 4), "spruce_planks")
    # upper storey: jettied 1 toward the yard, timber frame
    up = m2 & (SD > -11)
    edge_ = up & (SD <= -10)
    s.fill(col_mask(edge_, P + 4, P + 4), "dark_oak_slab[type=top]")
    frame = up & ((SD <= -10) | (Z == zs) | (Z == ze + 1))
    s.fill(col_mask(frame, P + 5, P + 7), Gradient("z", [(zs + 0.5, "dark_oak_log"), (ze + 0.5, Mix({"spruce_planks": 3, "stripped_spruce_log": 1})), (99, "dark_oak_log")]))
    for z in range(zs, ze + 2, 4):
        s.fill(col_mask(frame & (Z > z) & (Z < z + 1), P + 5, P + 7), "dark_oak_log")
    for z in range(zs + 2, ze, 4):
        s.fill(col_mask(frame & (SD <= -10) & (Z > z) & (Z < z + 1), P + 6, P + 6), "spruce_trapdoor[facing=east,open=true]")
    # pent roof: rises from the yard edge to the curtain
    for x, z in zip(*np.nonzero(m2 | (inside & (SD <= -11 + 1e-6) & (Z >= zs) & (Z <= ze + 1)))):
        y = P + 8 + int((SD[x, z] + 11) // 2.4)
        s.set(x, y, z, "deepslate_tile_stairs[facing=west]")
        s.idx[x, P + 5:y, z] = np.where(s.idx[x, P + 5:y, z] == 0, s.id("spruce_planks") if SD[x, z] > -9 else 0, s.idx[x, P + 5:y, z])
    return zs, ze


def well(s):
    cx, cz = 70, 68
    X, Z = grid2()
    r = np.hypot(X - cx - 0.5, Z - cz - 0.5)
    s.fill(col_mask(r <= 2.2, P - 1, P), "cobblestone")
    s.fill(col_mask(r <= 1.2, P - 6, P), "air")
    s.fill(col_mask(r <= 1.2, P - 6, P - 4), "water")


# ------------------------------------------------------------------ pass 3: wall depth
def no_depth_zone():
    X, Z = grid2()
    return (X > GH[0] - 2) & (X < GH[1] + 2) & (Z > GH[2] - 3) & (Z < GH[3] + 8)


def curtain_depth(s, hm):
    """Layer 1: batter + pilasters every 7; layer 2: corbel table carrying a projecting parapet; sub-block: stair caps."""
    ok = ~no_depth_zone()
    out1 = (SD > 0) & (SD <= 1) & ok
    pil = out1 & ((np.floor(ALONG) % 7) < 2)
    for x, z in zip(*np.nonzero((SD > 0) & (SD <= 2) & ok)):
        g = max(0, hm[x, z])
        ytop = P + (1 if SD[x, z] <= 1 else -2)
        s.fill(((x, g, z), (x, ytop, z)), MASON, replace="air")
    for x, z in zip(*np.nonzero(pil)):
        s.fill(((x, P, z), (x, WALK - 4, z)), MASON, replace="air")
        if s.idx[x, WALK - 3, z] == 0:
            s.set(x, WALK - 3, z, f"stone_brick_stairs[facing={inward_facing(EDGE[x, z])}]")
    for x, z in zip(*np.nonzero(out1)):
        if s.idx[x, WALK - 1, z] == 0:
            s.set(x, WALK - 1, z, f"stone_brick_stairs[facing={inward_facing(EDGE[x, z])},half=top]")
        s.fill(((x, WALK, z), (x, WALK + 1, z)), MASON, replace="air")
        if np.floor(ALONG[x, z]) % 3 != 0:
            s.fill(((x, WALK + 2, z), (x, WALK + 2, z)), MASON, replace="air")
    on = (SD > -1) & (SD <= 1) & ((np.floor(ALONG) % 3) != 0) & ok
    for x, z in zip(*np.nonzero(on)):
        if s.idx[x, WALK + 2, z] != 0 and s.idx[x, WALK + 3, z] == 0:
            s.set(x, WALK + 3, z, "stone_brick_slab")


def tower_depth(s, hm):
    X, Z = grid2()
    for name, c, kind, R, top, roof in TOWERS:
        cx, cz = c[0] + 0.5, c[1] + 0.5
        r = np.hypot(X - cx, Z - cz) if kind == "round" else np.maximum(np.abs(X - cx), np.abs(Z - cz))
        Rr = R if kind == "round" else R + 0.5
        for x, z in zip(*np.nonzero((r > Rr) & (r <= Rr + 1.6))):
            g = max(0, hm[x, z])
            s.fill(((x, g, z), (x, P + (2 if r[x, z] <= Rr + 0.8 else -1), z)), MASON, replace="air")
        ring = (r > Rr) & (r <= Rr + 1.0)
        if roof in ("open", "cone"):
            for x, z in zip(*np.nonzero(ring)):
                dx, dz = cx - (x + 0.5), cz - (z + 0.5)
                face = FACING[(int(np.sign(dx)), 0)] if abs(dx) > abs(dz) else FACING[(0, int(np.sign(dz)))]
                s.set(x, top - 2, z, f"stone_brick_stairs[facing={face},half=top]")
                s.fill(((x, top - 1, z), (x, top + 1, z)), MASON, replace="air")
                if roof == "open":
                    a = math.degrees(math.atan2(-dz, -dx)) % 360
                    if (a // 24) % 2 == 0:
                        s.set(x, top + 2, z, MASON)
                        s.set(x, top + 3, z, "stone_brick_slab")
        # arrow slits, 1x3, on the outward half
        for lvl, y0 in enumerate((P + 2, WALK + 3)):
            for a in range(0, 360, 60):
                a2 = math.radians(a + 30 * lvl)
                vx, vz = math.cos(a2), math.sin(a2)
                if (cx - 64) * vx + (cz - 60) * vz < 0:
                    continue  # facing the yard
                for t in np.linspace(R - 2.5, Rr + 0.6, 10):
                    px, pz = int(cx + vx * t), int(cz + vz * t)
                    for yy in range(y0, y0 + 3):
                        if s.idx[px, yy, pz] == s.id(MASON):
                            s.idx[px, yy, pz] = 0


def keep_depth(s):
    """String courses at each storey, pilaster strips, corbelled parapet at the top, deep window reveals."""
    X, Z = grid2()
    inbox = (X >= KX0) & (X < KX1 + 1) & (Z >= KZ0) & (Z < KZ1 + 1)
    out1 = (X >= KX0 - 1) & (X < KX1 + 2) & (Z >= KZ0 - 1) & (Z < KZ1 + 2) & ~inbox
    mx, mz = (KX0 + KX1) / 2, (KZ0 + KZ1) / 2
    for x, z in zip(*np.nonzero(out1)):
        dx, dz = x - mx, z - mz
        ax, az = abs(dx) / ((KX1 - KX0) / 2 + 1), abs(dz) / ((KZ1 - KZ0) / 2 + 1)
        face = FACING[(-int(np.sign(dx)), 0)] if ax > az else FACING[(0, -int(np.sign(dz)))]
        for y in (P + 7, P + 15):
            if s.idx[x, y, z] == 0:
                s.set(x, y, z, f"polished_deepslate_stairs[facing={face},half=top]")
        along = x if az > ax else z
        if along % 6 == 0:
            s.fill(((x, P, z), (x, P + 20, z)), MASON, replace="air")
            if s.idx[x, P + 21, z] == 0:
                s.set(x, P + 21, z, f"stone_brick_stairs[facing={face}]")
        if s.idx[x, P + 22, z] == 0:
            s.set(x, P + 22, z, f"stone_brick_stairs[facing={face},half=top]")
        s.fill(((x, P + 23, z), (x, P + 25, z)), MASON, replace="air")
        if (x + z) % 3 != 0:
            s.fill(((x, P + 26, z), (x, P + 26, z)), MASON, replace="air")
            s.set(x, P + 27, z, "stone_brick_slab")

    def window(cells, y0, y1, axis, outer, inward):
        for a in cells:
            for y in range(y0, y1 + 1):
                for d in range(0, 4):
                    c = outer + inward * d
                    x, z = (c, a) if axis == "x" else (a, c)
                    s.idx[x, y, z] = 0
                c = outer + inward * 2
                x, z = (c, a) if axis == "x" else (a, c)
                s.set(x, y, z, "gray_stained_glass_pane")
            c = outer
            x, z = (c, a) if axis == "x" else (a, c)
            s.set(x, y0 - 1, z, "polished_deepslate_slab[type=top]")
    for y0, y1 in [(P + 1, P + 5), (P + 10, P + 12), (P + 18, P + 21)]:
        for pair in ((56, 57), (69, 70)):
            window(pair, y0, y1, "z", KZ1 + 1, -1)
        for pair in ((34, 35), (43, 44)):
            window(pair, y0, y1, "x", KX0 - 1, 1)
    for pair in ((57, 58), (68, 69)):
        window(pair, P + 18, P + 21, "z", KZ0 - 1, 1)
    # door frame: deepslate jambs + arch, threshold
    for y in range(P, P + 4):
        s.set(61, y, KZ1 + 1, TRIM); s.set(65, y, KZ1 + 1, TRIM)
    s.set(62, P + 4, KZ1 + 1, "polished_deepslate_stairs[facing=east,half=top]")
    s.set(64, P + 4, KZ1 + 1, "polished_deepslate_stairs[facing=west,half=top]")
    s.set(63, P + 5, KZ1 + 1, "chiseled_stone_bricks")
    for x in range(62, 65):
        s.set(x, P - 1, KZ1 + 1, TRIM)


# ------------------------------------------------------------------ pass 4: roofs
def cone(s, cx, cz, R, y0, h, block, stair, shell=2.0):
    X, Z = grid2()
    r = np.hypot(X - cx, Z - cz)
    m = np.zeros((W, H, D), bool)
    for k in range(int(h) + 1):
        rr = R * (1 - k / h)
        if rr < 0.6:
            m[int(cx), y0 + k, int(cz)] = True
            continue
        m[:, y0 + k, :] = (r <= rr) & (r > rr - shell - 1.0)
    s.fill(m, block)
    stairify(s, m, stair)
    s.set(int(cx), y0 + int(h) + 1, int(cz), "lightning_rod")


def roofs(s):
    for name, c, kind, R, top, roof in TOWERS:
        cx, cz = c[0] + 0.5, c[1] + 0.5
        if roof == "cone":
            cone(s, cx, cz, R + 1.7, top, round((R + 1.7) * 1.8), ROOF, "deepslate_tile")
        elif roof == "hoard":
            hoarding(s, c, R, top)
    # keep: hipped roof inside the wall-walk
    x0, x1, z0, z1 = KX0 + 3, KX1 - 3, KZ0 + 3, KZ1 - 3
    m = np.zeros((W, H, D), bool)
    for k in range(0, 8):
        if x0 + k > x1 - k or z0 + k > z1 - k:
            break
        m[x0 + k:x1 - k + 1, P + 24 + 2 * k:P + 26 + 2 * k, z0 + k:z1 - k + 1] = True
    s.fill(m, ROOF)
    stairify(s, m, "deepslate_tile")
    # stair turret: weathered copper cone
    cone(s, TUR[0] + 0.5, TUR[1] + 0.5, 4.9, P + 35, 11, "waxed_weathered_cut_copper", "waxed_weathered_cut_copper", shell=1.5)
    # chimney cap
    s.box((KX0 - 3, P + 31, 36), (KX0, P + 31, 42), "polished_deepslate_slab")
    s.box((KX0 - 2, P + 31, 38), (KX0 - 1, P + 31, 40), "air")


def hoarding(s, c, R, top):
    """Timber hoarding on the NE tower: corbels, dark-oak post-and-plank gallery, pyramid slate roof."""
    cx, cz = c[0] + 0.5, c[1] + 0.5
    X, Z = grid2()
    r = np.maximum(np.abs(X - cx), np.abs(Z - cz))
    Rr = R + 0.5
    s.fill(col_mask(r <= Rr, top, top + 2), "air", replace=MASON)
    s.fill(col_mask(r <= Rr - 1.5, top - 1, top - 1), "spruce_planks")
    ring = (r > Rr) & (r <= Rr + 1)
    for x, z in zip(*np.nonzero(ring)):
        dx, dz = cx - (x + 0.5), cz - (z + 0.5)
        face = FACING[(int(np.sign(dx)), 0)] if abs(dx) > abs(dz) else FACING[(0, int(np.sign(dz)))]
        s.set(x, top - 2, z, f"stone_brick_stairs[facing={face},half=top]")
        s.set(x, top - 1, z, "spruce_planks")
        corner = abs(abs(dx) - abs(dz)) < 0.1
        post = corner or (x + z) % 3 == 0
        for y in range(top, top + 3):
            s.set(x, y, z, "dark_oak_log" if post else ("spruce_planks" if y != top + 1 else "spruce_trapdoor[half=top,open=true,facing=" + FACING[(-int(np.sign(dx)), 0)] + "]" if abs(dx) > abs(dz) else ("spruce_planks" if y != top + 1 else "air")))
        s.set(x, top + 3, z, "dark_oak_log[axis=x]" if abs(dz) > abs(dx) else "dark_oak_log[axis=z]")
    # pyramid roof
    m = np.zeros((W, H, D), bool)
    for k in range(0, 10):
        rr = Rr + 2 - k
        if rr < 0:
            break
        m[:, top + 4 + 2 * k, :] = (r <= rr) & (r > rr - 2)
        m[:, top + 5 + 2 * k, :] = (r <= rr) & (r > rr - 2)
    s.fill(m, ROOF)
    stairify(s, m, "deepslate_tile")
    s.set(int(cx), top + 4 + 2 * int(Rr + 2) + 2, int(cz), "lightning_rod")


# ------------------------------------------------------------------ build
def build():
    s = Scene((W, H, D), "castle", seed=SEED)
    hm = terrain(s)
    curtain(s, hm)
    towers(s, hm)
    oct_ = keep(s)
    dts = gatehouse(s, hm)
    if PASS >= 2:
        crenels(s)
        tower_tops(s)
        keep_body(s, oct_)
        stair_turret(s, oct_)
        gate(s)
        courtyard_stairs(s)
        lean_to(s)
        well(s)
    if PASS >= 3:
        curtain_depth(s, hm)
        tower_depth(s, hm)
        keep_depth(s)
    if PASS >= 4:
        roofs(s)
    if PASS >= 5:
        palette(s, hm)
    if PASS >= 6:
        interior(s)
    if PASS >= 7:
        decorate(s, hm)
    if PASS >= 8:
        lighting(s)
    markers(s, hm)
    return s


def markers(s, hm):
    def stand(x, z):
        col = np.nonzero(s.idx[x, :, z])[0]
        return [x, int(col.max()) + 1 if len(col) else 0, z]
    s.mark("spawn_approach", [64, P, 108], look_at=[64, P + 9, 80])
    s.mark("cam_meadow_sw", stand(36, 104), look_at=[56, P + 12, 56])
    s.mark("cam_yard", [63, P, 76], look_at=[63, P + 14, 40])
    if PASS >= 6:
        s.mark("cam_hall", [63, P, 45], look_at=[63, P + 2, 33])
        s.mark("cam_library", [61, P + 8, 44], look_at=[54, P + 9, 35])
        s.mark("cam_chapel", [70, P + 16, 39], look_at=[53, P + 18, 39])
        s.mark("cam_cellar", [64, P - 8, 44], look_at=[60, P - 6, 34])
        wx = [x for x in range(W) if -3 < SD[x, 64] <= -2 and EDGE[x, 64] == 1][0]
        s.mark("cam_walk", [wx, WALK, 64], look_at=[63, P + 20, 40])
        s.mark("cam_keeptop", [KX0 + 2, P + 24, KZ1 - 2], look_at=[79, P + 36, 39])
    s.meta["origin"] = list(ORIGIN)


# ------------------------------------------------------------------ pass 5: palette
ROCKS = ["minecraft:tuff", "minecraft:andesite", "minecraft:stone", "minecraft:deepslate", "minecraft:cobbled_deepslate", "minecraft:blackstone"]


def palette(s, hm):
    s.replace(MASON, masonry(SEED + 40))
    X, Z = grid2()
    # courtyard ground: worn earth and cobbles, a cobbled road from the gate to the keep door
    yard = col_mask(SD <= -4, P - 1, P - 1) & s.match(ROCKS)
    road = col_mask((np.abs(X - 63.5) < 3 + noise.fbm(X, Z, 2.0, scale=5, seed=SEED + 41)) & (Z > KZ1) & (Z < GH[2]), P - 1, P - 1)
    s.fill(yard, Noise([(-0.35, "packed_mud"), (0.0, "coarse_dirt"), (0.3, Mix({"dirt_path": 2, "coarse_dirt": 1})),
                        (0.55, "mossy_cobblestone"), (1, "cobblestone")], scale=6, seed=SEED + 42))
    s.fill(road & s.match(["minecraft:packed_mud", "minecraft:coarse_dirt", "minecraft:dirt_path", "minecraft:mossy_cobblestone", "minecraft:cobblestone"]),
           Noise([(-0.2, "cobblestone"), (0.3, Mix({"stone_bricks": 1, "cobblestone": 2})), (1, "mossy_cobblestone")], scale=4, seed=SEED + 43))
    soil(s)
    # moss sheets on flattish rock tops
    rock = s.match(["minecraft:tuff", "minecraft:andesite", "minecraft:stone", "minecraft:deepslate"])
    s.fill(rock, Gradient("up", [(0.5, None), (2, Noise([(-0.1, "moss_block"), (1, None)], scale=5, seed=SEED + 44))]))


def soil(s):
    hm = s.surface("solid")
    pad = np.pad(hm, 1, mode="edge")
    slope = np.max([np.abs(hm - pad[1:-1, :-2]), np.abs(hm - pad[1:-1, 2:]), np.abs(hm - pad[:-2, 1:-1]), np.abs(hm - pad[2:, 1:-1])], 0)
    top = np.zeros(s.shape, bool); sub = np.zeros(s.shape, bool)
    for x, z in zip(*np.nonzero((slope <= 1) & (hm > 0) & (SD > 0.5))):
        y = hm[x, z]
        if s.palette[s.idx[x, y, z]] not in ROCKS:
            continue
        top[x, y, z] = True
        sub[x, max(0, y - 2):y, z] = True
    sub &= s.match(ROCKS)
    s.fill(sub, Noise([(-0.3, "rooted_dirt"), (0.4, "dirt"), (1, "coarse_dirt")], scale=5, seed=SEED + 45))
    s.fill(top, Noise([(-0.45, "moss_block"), (0.55, "grass_block"), (0.68, "coarse_dirt"), (1, "grass_block")], scale=7, seed=SEED + 46))


# ------------------------------------------------------------------ pass 6: interior
IX0, IX1, IZ0, IZ1 = KX0 + KT, KX1 - KT, KZ0 + KT, KZ1 - KT     # 53..73 x 33..45


def interior(s):
    great_hall(s)
    solar_and_library(s)
    chapel(s)
    cellar(s)
    tower_rooms(s)
    gate_room(s)


def great_hall(s):
    F = P
    s.box((IX0, F - 1, IZ0), (IX1, F - 1, IZ1), Noise([(-0.2, "polished_tuff"), (0.35, "tuff_bricks"), (1, "polished_andesite")], scale=5, seed=SEED + 50))
    # ceiling beams (dark oak, every 4) under the solar floor
    for z in range(IZ0 + 1, IZ1, 4):
        s.box((IX0, F + 6, z), (IX1, F + 6, z), "stripped_dark_oak_log[axis=x]")
    s.box((IX0, F + 7, IZ0), (IX1, F + 7, IZ1), "dark_oak_planks")
    # dais at the north end, high table, lord's chair
    s.box((IX0 + 2, F, IZ0), (IX1 - 2, F, IZ0 + 2), "dark_oak_planks")
    for x in range(IX0 + 2, IX1 - 1):
        s.set(x, F, IZ0 + 3, "dark_oak_stairs[facing=north]")
    s.box((57, F + 1, IZ0 + 1), (69, F + 1, IZ0 + 1), "dark_oak_slab[type=top]")
    for x in range(58, 69, 2):
        s.set(x, F + 1, IZ0, "spruce_stairs[facing=north]")
    s.set(63, F + 1, IZ0, "dark_oak_stairs[facing=north]")
    s.set(63, F + 2, IZ0, "dark_oak_trapdoor[facing=south,half=bottom,open=true]")
    # two long tables with benches
    for tx in (58, 68):
        s.box((tx, F, 38), (tx, F, 44), "dark_oak_slab[type=top]")
        s.box((tx - 1, F, 38), (tx - 1, F, 44), "spruce_stairs[facing=west]")
        s.box((tx + 1, F, 38), (tx + 1, F, 44), "spruce_stairs[facing=east]")
        for z in (39, 42):
            s.set(tx, F + 1, z, "candle[candles=3,lit=true]")
    # red runner from the door to the dais
    s.box((62, F, IZ0 + 4), (64, F, IZ1), "red_carpet")
    # fireplace in the west wall
    s.box((IX0 - 1, F, 38), (IX0 - 1, F + 2, 40), "air")
    s.box((IX0 - 2, F, 38), (IX0 - 2, F + 3, 40), "bricks")
    s.set(IX0 - 1, F, 39, "campfire[lit=true,facing=east]")
    s.set(IX0 - 1, F, 38, "polished_deepslate"); s.set(IX0 - 1, F, 40, "polished_deepslate")
    for z in range(37, 42):
        s.set(IX0, F + 3, z, "polished_deepslate_stairs[facing=west,half=top]")
    s.set(IX0, F + 4, 39, "chiseled_tuff_bricks")
    s.set(IX0, F, 37, "polished_deepslate"); s.set(IX0, F, 41, "polished_deepslate")
    s.set(IX0, F + 1, 37, "polished_deepslate_wall"); s.set(IX0, F + 1, 41, "polished_deepslate_wall")
    s.set(IX0, F + 2, 37, "polished_deepslate_wall"); s.set(IX0, F + 2, 41, "polished_deepslate_wall")
    # chandeliers on chains from the beams
    for cx, cz in ((58, 41), (68, 41), (63, 37)):
        s.set(cx, F + 5, cz, "iron_chain[axis=y]")
        s.set(cx, F + 4, cz, "lantern[hanging=true]")
    # sideboards and barrels along the east wall
    for z in (34, 36, 44):
        s.set(IX1, F, z, "barrel[facing=up]")
    s.box((IX1, F, 41), (IX1, F, 43), "spruce_slab[type=top]")
    s.set(IX1, F + 1, 42, "decorated_pot")


def solar_and_library(s):
    F = P + 8
    for z in range(IZ0 + 1, IZ1, 4):
        s.box((IX0, F + 6, z), (IX1, F + 6, z), "stripped_dark_oak_log[axis=x]")
    s.box((IX0, F + 7, IZ0), (IX1, F + 7, IZ1), "spruce_planks")
    # timber partition at x=63 with a door gap
    s.box((63, F, IZ0), (63, F + 5, IZ1), Mix({"spruce_planks": 3, "stripped_spruce_log": 1}, seed=3))
    for z in (IZ0, 37, 41, IZ1):
        s.box((63, F, z), (63, F + 5, z), "dark_oak_log")
    s.box((63, F, 39), (63, F + 2, 39), "air")
    # library (west half)
    s.box((IX0, F, 37), (IX0, F + 3, 41), "bookshelf")
    s.box((IX0 + 1, F, IZ0), (62, F + 2, IZ0), Mix({"bookshelf": 4, "chiseled_bookshelf": 1}))
    s.box((IX0 + 1, F + 3, IZ0), (62, F + 3, IZ0), "spruce_slab")
    s.box((56, F, 39), (59, F, 41), "spruce_slab[type=top]")
    for x in (56, 58):
        s.set(x, F, 38, "spruce_stairs[facing=north]"); s.set(x + 1, F, 42, "spruce_stairs[facing=south]")
    s.set(57, F + 1, 40, "lectern[facing=south]")
    s.set(59, F + 1, 39, "candle[candles=2,lit=true]")
    s.box((IX0 + 1, F - 0, 43), (60, F, 45), "brown_carpet")
    # lord's chamber (east half): bed, chest, wardrobe, rug
    s.set(70, F, 34, "red_bed[facing=north,part=head]"); s.set(70, F, 35, "red_bed[facing=north,part=foot]")
    s.set(71, F, 34, "red_bed[facing=north,part=head]"); s.set(71, F, 35, "red_bed[facing=north,part=foot]")
    s.set(69, F, 33, "spruce_slab[type=top]"); s.set(72, F, 33, "spruce_slab[type=top]")
    s.set(69, F + 1, 33, "lantern"); s.set(72, F + 1, 33, "candle[candles=1,lit=true]")
    s.set(66, F, IZ1, "chest[facing=north]")
    s.box((IX1, F, 43), (IX1, F + 2, 45), "spruce_planks")
    s.box((IX1 - 1, F, 43), (IX1 - 1, F + 2, 45), "spruce_trapdoor[facing=west,open=true]")
    s.box((66, F, 37), (71, F, 42), "red_carpet")
    s.box((67, F, 38), (70, F, 41), "brown_carpet")
    s.set(65, F, 42, "spruce_stairs[facing=east]")


def chapel(s):
    F = P + 16
    s.box((IX0, F - 1, IZ0), (IX1, F - 1, IZ1), Noise([(0, "polished_tuff"), (1, "tuff_bricks")], scale=4, seed=SEED + 51))
    # altar at the west end on a step
    s.box((IX0, F, 35), (IX0 + 2, F, 43), "polished_deepslate")
    for z in range(35, 44):
        s.set(IX0 + 3, F, z, "polished_deepslate_stairs[facing=west]")
    s.box((IX0, F + 1, 37), (IX0, F + 1, 41), "chiseled_tuff_bricks")
    s.box((IX0 + 1, F + 1, 37), (IX0 + 1, F + 1, 41), "polished_deepslate_slab[type=top]")
    for z in (37, 39, 41):
        s.set(IX0 + 1, F + 2, z, "candle[candles=4,lit=true]")
    s.box((IX0, F + 2, 38), (IX0, F + 5, 40), "air")
    s.box((IX0 - 1, F + 2, 38), (IX0 - 1, F + 5, 40), "yellow_stained_glass")
    s.set(IX0, F + 3, 39, "lightning_rod")
    # pews facing the altar, aisle down the middle
    for x in range(58, 71, 2):
        for z in list(range(34, 38)) + list(range(41, 45)):
            s.set(x, F, z, "spruce_stairs[facing=east]")
    s.box((58, F, 38), (72, F, 40), "red_carpet")
    # vaulted feel: stepped corbels along the long walls
    for x in range(IX0, IX1 + 1, 4):
        for z, f in ((IZ0, "south"), (IZ1, "north")):
            s.box((x, F, z), (x, F + 6, z), "tuff_bricks")
            s.set(x, F + 5, z + (1 if f == "south" else -1), f"tuff_brick_stairs[facing={'north' if f == 'south' else 'south'},half=top]")
    s.box((IX0, F + 6, IZ0), (IX1, F + 6, IZ1), "spruce_planks")
    for x in range(IX0, IX1 + 1, 4):
        s.box((x, F + 6, IZ0), (x, F + 6, IZ1), "stripped_dark_oak_log[axis=z]")


def cellar(s):
    F = P - 8
    s.box((IX0, F - 1, IZ0), (IX1, F - 1, IZ1), Noise([(-0.1, "cobbled_deepslate"), (0.4, "packed_mud"), (1, "mossy_cobblestone")], scale=4, seed=SEED + 52))
    # vault springers along the walls and two piers
    for x in range(IX0, IX1 + 1):
        s.set(x, F + 6, IZ0, "deepslate_brick_stairs[facing=north,half=top]")
        s.set(x, F + 6, IZ1, "deepslate_brick_stairs[facing=south,half=top]")
    for px in (59, 67):
        s.box((px, F, 38), (px + 1, F + 6, 40), "deepslate_bricks")
        for dx, f in ((-1, "east"), (2, "west")):
            s.box((px + dx, F + 6, 38), (px + dx, F + 6, 40), f"deepslate_brick_stairs[facing={f},half=top]")
    # casks along the north wall (two high), barrels and sacks
    s.box((IX0 + 1, F, IZ0), (IX1 - 1, F + 1, IZ0), "barrel[facing=south]")
    for x in range(IX0 + 1, IX1, 3):
        s.box((x, F, IZ0), (x, F + 1, IZ0), "spruce_planks")
    s.box((IX0, F, IZ0 + 3), (IX0, F, IZ1 - 1), "barrel[facing=up]")
    s.box((IX0 + 1, F, IZ1), (IX0 + 4, F, IZ1), "brown_wool")
    s.box((IX0 + 1, F + 1, IZ1), (IX0 + 2, F + 1, IZ1), "brown_wool")
    s.box((IX1 - 4, F, IZ1), (IX1 - 1, F, IZ1), "hay_block")
    s.set(IX0, F + 5, IZ0, "cobweb"); s.set(IX1, F + 5, IZ1, "cobweb")
    for x, z in ((56, 39), (63, 36), (63, 43), (70, 39)):
        s.set(x, F + 5, z, "iron_chain[axis=y]"); s.set(x, F + 4, z, "lantern[hanging=true]")


def ladder_up(s, cx, cz, y0, y1):
    """Ladder on the north inner wall of a tower from y0 to y1 (through the floors)."""
    z = cz
    while s.idx[cx, y0 + 1, z - 1] == 0:
        z -= 1
    for y in range(y0, y1 + 1):
        s.set(cx, y, z, "ladder[facing=south]")
    return z


def tower_rooms(s):
    X, Z = grid2()
    for name, c, kind, R, top, roof in TOWERS:
        outer, inner, r = tower_masks(name, c, kind, R, top)
        cx, cz = c
        # floors: walk level and top
        s.fill(col_mask(inner, WALK - 1, WALK - 1), "spruce_planks")
        if roof != "hoard":
            s.fill(col_mask(inner, top - 1, top - 1), "spruce_planks")
        s.fill(col_mask(inner, P - 1, P - 1), Mix({"cobbled_deepslate": 2, "tuff": 1}))
        # doorways onto the wall-walks and into the yard
        ring = outer & ~inner
        s.fill(col_mask(ring & (SD > -4) & (SD <= -0.5), WALK, WALK + 2), "air")
        vx, vz = 64 - cx, 60 - cz
        n = math.hypot(vx, vz); vx, vz = vx / n, vz / n
        for t in np.arange(R - 2.5, R + 1.5, 0.5):
            px, pz = int(cx + 0.5 + vx * t), int(cz + 0.5 + vz * t)
            for py in range(P, P + 3):
                s.set(px, py, pz, "air")
        lz = ladder_up(s, cx, cz, P, top - 1 if roof != "hoard" else top - 2)
        # light + furnishing per floor
        for F in (P, WALK, top):
            s.set(cx + 1, F, cz + 1, "lantern")
            s.set(cx - 1, F, cz + 1, "barrel[facing=up]")
        if name == "ne":   # armoury store
            for dx in (-3, -2, 2, 3):
                s.set(cx + dx, P, cz - 3, "lightning_rod")
            s.set(cx + 3, P, cz, "anvil[facing=north]")
            s.set(cx + 3, P, cz + 2, "grindstone[face=floor,facing=north]")
            s.set(cx - 3, P, cz + 3, "smithing_table")
            s.set(cx - 3, P, cz, "chest[facing=east]")
            s.set(cx - 3, P, cz - 1, "chest[facing=east]")


def gate_room(s):
    """Guard room / armoury over the gate passage, level with the wall-walks."""
    x0, x1, z0, z1 = GH
    F = WALK
    s.box((x0 + 2, F, z0 + 2), (x1 - 2, F + 3, z1 - 3), "air")
    s.box((x0 + 2, F - 1, z0 + 2), (x1 - 2, F - 1, z1 - 3), "spruce_planks")
    s.box((x0, F, 89), (x1, F + 2, 90), "air")       # through to both wall-walks
    s.box((x0 + 2, F + 4, z0 + 2), (x1 - 2, F + 4, z1 - 3), "dark_oak_planks")
    # portcullis winch over the passage: chains down to raised iron bars
    for x in range(GATE_X0, GATE_X1 + 1):
        s.set(x, P + 4, 94, "iron_bars")
        s.set(x, P + 5, 94, "iron_bars")
    s.box((GATE_X0, F, 92), (GATE_X1, F, 92), "stripped_spruce_log[axis=x]")
    # weapon racks: lightning-rod spears, shields = trapdoors, barrels of arrows
    for x in range(x0 + 2, x1 - 1, 2):
        s.set(x, F, z0 + 2, "lightning_rod")
    s.box((x0 + 2, F, 92), (x0 + 3, F, 93), "barrel[facing=up]")
    s.set(x1 - 2, F, 93, "anvil[facing=east]")
    s.set(x1 - 3, F, 93, "smithing_table")
    s.box((x0 + 5, F, 88), (x0 + 5, F, 90), "dark_oak_slab[type=top]")
    for x, z in ((59, 88), (69, 88)):
        s.set(x, F + 3, z, "lantern[hanging=true]")


# ------------------------------------------------------------------ pass 7: decoration
def decorate(s, hm):
    s.decorate("grass_block", Mix({"short_grass": 6, "fern": 2, "poppy": 0.2, "cornflower": 0.2}), chance=0.3, seed=SEED + 70)
    s.decorate("moss_block", Mix({"moss_carpet": 3, "short_grass": 1}), chance=0.35, seed=SEED + 71)
    # rubble and fallen stones at the foot of the walls, outside
    rng = np.random.default_rng(SEED + 72)
    frags = ["cobblestone", "mossy_cobblestone", "stone_brick_slab", "mossy_stone_brick_slab", "tuff_brick_slab", "cobblestone_wall"]
    surf = s.surface("solid")
    cand = np.argwhere((SD > 2.5) & (SD < 7) & (surf > 0))
    for x, z in cand[rng.random(len(cand)) < 0.05]:
        y = surf[x, z]
        if s.palette[s.idx[x, y, z]].split("[")[0].endswith(("slab", "stairs", "wall", "carpet", "grass", "fern")):
            continue
        s.set(x, y + 1, z, frags[rng.integers(len(frags))])
    # yard life: hay, barrels, a cart of crates by the lean-to; a well with a timber hood
    for x, z, b in ((48, 66, "hay_block"), (48, 67, "hay_block"), (48, 68, "barrel[facing=up]"), (49, 66, "hay_block"),
                    (80, 70, "barrel[facing=up]"), (81, 70, "barrel[facing=up]"), (80, 71, "spruce_planks"),
                    (55, 52, "barrel[facing=up]"), (71, 52, "barrel[facing=up]")):
        s.set(x, P, z, b)
    s.set(48, P + 1, 66, "hay_block")
    for dx, dz in ((-2, 0), (2, 0)):
        s.box((70 + dx, P + 1, 68 + dz), (70 + dx, P + 2, 68 + dz), "spruce_fence")
    s.box((68, P + 3, 68), (72, P + 3, 68), "stripped_spruce_log[axis=x]")
    s.box((68, P + 4, 67), (72, P + 4, 69), "deepslate_tile_slab")
    s.set(70, P + 2, 68, "iron_chain[axis=y]")
    vines(s)


def vines(s):
    from tools.voxel.connect import sturdy
    rng = np.random.default_rng(SEED + 73)
    solid = sturdy(s)
    air = s.match("air")
    X, Y, Z = s.shape
    dirs = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
    out_ok = (SD > 0.5)[:, None, :]
    for name, (ddx, ddz) in dirs.items():
        nb = np.zeros_like(solid)
        xs = slice(max(0, ddx), X + min(0, ddx)); xd = slice(max(0, -ddx), X + min(0, -ddx))
        zs = slice(max(0, ddz), Z + min(0, ddz)); zd = slice(max(0, -ddz), Z + min(0, -ddz))
        nb[xd, :, zd] = solid[xs, :, zs]
        c = air & nb & out_ok
        c[:, :L0 - 6] = False
        c[:, P + 8:] = False
        pts = np.argwhere(c)
        keep = noise.fbm(pts[:, 0], pts[:, 1], pts[:, 2], scale=6, octaves=1, seed=SEED + 74 + len(name)) > 0.4
        pts = pts[keep]
        st = s.id(f"minecraft:vine[{name}=true]")
        for x, y, z in pts[rng.random(len(pts)) < 0.1]:
            for k in range(int(rng.integers(2, 7))):
                yy = y - k
                if yy < 0 or s.idx[x, yy, z] != 0 or not solid[x + ddx, yy, z + ddz]:
                    break
                s.idx[x, yy, z] = st


# ------------------------------------------------------------------ pass 8: lighting
def lighting(s):
    # wall-walk lanterns on the inner edge every ~9 blocks
    walk = (SD > -4) & (SD <= -3) & ((np.floor(ALONG) % 9) == 4) & ~no_depth_zone()
    for x, z in zip(*np.nonzero(walk)):
        if s.idx[x, WALK, z] == 0 and s.idx[x, WALK - 1, z] != 0:
            s.set(x, WALK, z, "lantern")
    # yard: lantern posts
    for x, z in ((58, 60), (69, 60), (58, 75), (69, 75), (50, 52), (77, 52)):
        s.box((x, P, z), (x, P + 1, z), "dark_oak_fence")
        s.set(x, P + 2, z, "lantern")
    # keep door: hanging lanterns on brackets
    for x in (60, 66):
        s.set(x, P + 4, KZ1 + 2, "dark_oak_fence")
        s.set(x, P + 3, KZ1 + 2, "lantern[hanging=true]")
        s.set(x, P + 4, KZ1 + 1, "dark_oak_fence")
    # gate passage
    for x in (GATE_X0, GATE_X1):
        for z in (86, 92):
            s.set(x, P + 2, z, "wall_torch[facing=" + ("east" if x == GATE_X0 else "west") + "]")
    # stair turret: a torch every revolution on the north wall
    tx, tz = TUR
    for k in SPIRAL_K:
        if k % 8 == 1:
            y = SPIRAL_Y0 + k + 2
            if s.idx[tx, y, tz - 1] == 0 and s.idx[tx, y, tz - 2] != 0:
                s.set(tx, y, tz - 1, "wall_torch[facing=south]")
    # solar / library / chapel / roof walk
    for F in (P + 8, P + 16):
        for x, z in ((55, 44), (61, 34), (65, 44), (71, 37)):
            s.set(x, F + 5, z, "iron_chain[axis=y]") if s.idx[x, F + 5, z] == 0 else None
            if s.idx[x, F + 4, z] == 0:
                s.set(x, F + 4, z, "lantern[hanging=true]")
    for x, z in ((KX0 + 1, KZ0 + 1), (KX1 - 1, KZ0 + 1), (KX0 + 1, KZ1 - 1), (KX1 - 1, KZ1 - 1)):
        s.set(x, P + 24, z, "lantern")
    # lean-to and towers are lit in their own functions; tunnels in the lean-to
    for z in (65, 70, 74):
        xs = [x for x in range(W) if -8 < SD[x, z] <= -7 and EDGE[x, z] == 4]
        if xs:
            s.set(xs[0], P + 3, z, "lantern[hanging=true]")
