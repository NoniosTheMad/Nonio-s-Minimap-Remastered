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


def palette(s, hm):
    pass


def interior(s):
    pass


def decorate(s, hm):
    pass


def lighting(s):
    pass


def markers(s, hm):
    def stand(x, z):
        col = np.nonzero(s.idx[x, :, z])[0]
        return [x, int(col.max()) + 1 if len(col) else 0, z]
    s.mark("spawn_approach", stand(67, 117), look_at=[64, P + 8, 80])
    s.mark("cam_meadow_sw", stand(36, 104), look_at=[56, P + 12, 56])
    s.mark("cam_yard", [63, P, 76], look_at=[63, P + 14, 40])
    s.meta["origin"] = list(ORIGIN)
