"""Minor Dream site: THE LANTERN TREE.

A pale, twisting dream-tree standing on five arching roots. Its crown is a wide azalea cap like a mushroom's, its
underside studded with glowing gold fruit (shroomlight / ochre froglight) and hung with lanterns on chains of every
length. Under the roots, in a mossy hollow you can see into from every side, sits the offering (loot chest).
Render: python -m tools.voxel render scenes/dream/lantern_tree.py --mood dream
"""
import math

import numpy as np

from scenes.dream._dream import deposit, finish, loot_chest
from scenes.dream._minor import disc, scatter
from tools.voxel.palette import Mix, Noise
from tools.voxel.scene import Scene
from tools.voxel.stability import fix_soil

W, H, D = 17, 34, 17
C = 8
A = 8
BASE_Y = A + 5          # trunk bottom (roots spring from here)
CAP_Y = A + 19          # cap underside centre
SEED = 1531
BARK = Mix({"birch_wood[axis=y]": 4, "stripped_birch_wood[axis=y]": 0.4}, seed=1531)


_G = np.indices((W, H, D))


def blob(s, p, r, spec):
    s.fill(((_G[0] - p[0]) ** 2 + (_G[1] - p[1]) ** 2 + (_G[2] - p[2]) ** 2) <= r * r, spec)


def curve(p0, p1, p2, n=60):
    p0, p1, p2 = (np.array(v, float) for v in (p0, p1, p2))
    for i in range(n):
        t = i / (n - 1)
        yield t, (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t * t * p2


def build():
    s = Scene((W, H, D), name="lantern_tree", seed=SEED)
    fp = disc(s, A, seed=SEED)
    rng = np.random.default_rng(SEED)

    # ---------------------------------------------------------------- roots: five arches down to the turf
    feet = []
    for k in range(5):
        a = math.radians(k * 72 + 20 + rng.uniform(-10, 10))
        R = 6.2
        foot = (C + R * math.cos(a), A - 1.0, C + R * math.sin(a))
        mid = (C + 4.2 * math.cos(a), BASE_Y + 1.0, C + 4.2 * math.sin(a))
        feet.append((foot, a))
        for t, q in curve((C, BASE_Y + 1, C), mid, foot):
            blob(s, q, 1.0 - 0.4 * t, BARK)
    # ---------------------------------------------------------------- trunk: twisting, tapering
    top = None
    for i in range(60):
        t = i / 59
        y = BASE_Y + t * (CAP_Y - BASE_Y)
        sw = 1.1 * math.sin(t * math.pi * 1.3)
        x = C + sw * math.cos(t * 4.0); z = C + sw * math.sin(t * 4.0)
        blob(s, (x, y, z), 1.9 - 0.8 * t, BARK)
        top = (x, y, z)
    # hollow under the trunk: clear head room for the offering
    for x in range(C - 2, C + 3):
        for z in range(C - 2, C + 3):
            for y in range(A, BASE_Y - 1):
                if (x - C) ** 2 + (z - C) ** 2 <= 5:
                    s.set(x, y, z, "cave_air")
    # ---------------------------------------------------------------- the cap: a mushroom-like azalea dome
    cap = Noise([(-0.45, "flowering_azalea_leaves"), (0.5, "cherry_leaves"), (1, Mix({"cherry_leaves": 2, "flowering_azalea_leaves": 1}))],
                scale=3, seed=SEED)
    capm = np.zeros(s.shape, bool)
    under = []
    for x in range(W):
        for z in range(D):
            r = math.hypot(x - C, z - C)
            ang = math.atan2(z - C, x - C)
            Rr = 8.4 * (1 + 0.07 * math.sin(4 * ang + 1.0))
            if r > Rr:
                continue
            u = r / Rr
            y_top = CAP_Y + 4.5 * math.sqrt(max(0.0, 1 - u ** 2.2))   # dome
            y_bot = CAP_Y + 1.5 * u ** 2 - 0.5 * (1 - u)                 # underside rises gently towards the rim
            y_bot = min(y_bot, y_top - 1)
            for y in range(int(round(y_bot)), int(round(y_top)) + 1):
                capm[x, y, z] = True
            under.append((x, int(round(y_bot)), z, u))
    s.fill(capm, cap)
    # the gills: a darker ring band under the cap edge, gold fruit studded in the underside
    for (x, yb, z, u) in under:
        if u > 0.84:   # the glowing gill ring at the rim, readable from the side
            s.set(x, yb, z, "shroomlight" if (x + z) % 2 else "ochre_froglight")
        elif u > 0.7:
            s.set(x, yb, z, "azalea_leaves")
        elif (x * 7 + z * 11) % 9 == 0 and u > 0.25:
            s.set(x, yb, z, "shroomlight" if (x + z) % 2 else "ochre_froglight")
    # crown buds on top of the cap
    for (dx, dz) in [(0, 0), (3, -2), (-3, 2), (-2, -3), (2, 4)]:
        x, z = C + dx, C + dz
        ys = np.nonzero(capm[x, :, z])[0]
        if len(ys):
            yt = ys.max() + 1
            s.set(x, yt, z, "pink_petals[flower_amount=4,facing=north]" if (dx + dz) % 2 else "flowering_azalea")
    yt = np.nonzero(capm[C, :, C])[0].max()
    s.set(C, yt + 1, C, "pearlescent_froglight")
    s.set(C, yt + 2, C, "end_rod[facing=up]")
    # ---------------------------------------------------------------- lanterns on chains of every length
    for (dx, dz, L) in [(5, 1, 3), (-5, 2, 2), (2, 6, 4), (-1, -6, 3), (4, -4, 1), (-4, -3, 4), (-3, 5, 2), (6, -1, 2)]:
        x, z = C + dx, C + dz
        ys = np.nonzero(capm[x, :, z])[0]
        if not len(ys):
            continue
        y = ys.min() - 1
        for k in range(L):
            s.set(x, y - k, z, "iron_chain[axis=y]")
        s.set(x, y - L, z, "lantern[hanging=true]")
    # pale hanging moss from the roots' arches
    for (foot, a) in feet:
        x = int(round(C + 3.6 * math.cos(a))); z = int(round(C + 3.6 * math.sin(a)))
        for y in range(BASE_Y + 3, A, -1):
            if s.idx[x, y, z] != 0 and s.idx[x, y - 1, z] == 0:
                s.set(x, y - 1, z, "pale_hanging_moss[tip=true]")
                break
    # ---------------------------------------------------------------- the hollow: mossy floor, offering, candles
    for x in range(C - 2, C + 3):
        for z in range(C - 2, C + 3):
            if (x - C) ** 2 + (z - C) ** 2 <= 5:
                s.set(x, A - 1, z, "moss_block" if (x + z) % 3 else "rooted_dirt")
    loot_chest(s, C, A, C, "minor", facing="south")
    s.set(C - 1, A, C + 1, "candle[candles=3,lit=true]")
    s.set(C + 1, A, C - 1, "moss_carpet")
    s.set(C + 1, A, C + 1, "potted_flowering_azalea_bush")
    s.set(C - 1, A, C - 1, "glow_lichen[down=true]")
    # ---------------------------------------------------------------- ground: calcite outcrops (ore seams), path, flowers
    for (x, z, h) in [(2, 8, 2), (14, 11, 1), (11, 2, 1)]:
        if s.idx[x, A, z] != 0:
            continue
        for y in range(A, A + h):
            s.set(x, y, z, "calcite")
        deposit(s, x, A + h - 1, z)
        if s.idx[x, A, z + 1] == 0:
            s.set(x, A, z + 1, "amethyst_block")
    scatter(s, A, fp, chance=0.5, seed=SEED)
    for (x, z) in [(3, 12), (13, 5), (6, 2)]:     # a few fallen lantern-fruit glowing in the grass
        if s.idx[x, A, z] == 0:
            s.set(x, A, z, "shroomlight" if x % 2 else "ochre_froglight")

    s.mark("cam_front", (C + 5, A, D - 3), look_at=(C, A + 9, C))
    fix_soil(s)   # grass under covers -> dirt
    return finish(s, tier="minor", kind="ground", anchor=(C, A, C))
