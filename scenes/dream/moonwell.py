"""Minor Dream site: THE MOONWELL.

A round wishing well of calcite and verdigris whose water glows from below (froglights, sea pickles = the wishes).
A giant copper-stemmed dripleaf curls over it like an umbrella, glow berries dripping from its rim and a bell hung
under it to ring for a wish. The offering (loot chest) waits in a little calcite alcove facing the well.
Render: python -m tools.voxel render scenes/dream/moonwell.py --mood dream
"""
import math

import numpy as np

from scenes.dream._dream import deposit, finish, loot_chest
from scenes.dream._minor import disc, scatter
from tools.voxel.palette import Mix
from tools.voxel.scene import Scene
from tools.voxel.stability import fix_soil

W, H, D = 17, 26, 17
C = 8
A = 8
WX, WZ = 9, 9          # well centre (slightly off-centre: the alcove gets the west side)
LEAF_Y = A + 11
SEED = 977


def build():
    s = Scene((W, H, D), name="moonwell", seed=SEED)
    fp = disc(s, A, seed=SEED)
    gx, gz = np.meshgrid(np.arange(W), np.arange(D), indexing="ij")
    rw = np.hypot(gx - WX, gz - WZ)

    # ---------------------------------------------------------------- the well: shaft, glowing floor, water
    for x in range(W):
        for z in range(D):
            r = rw[x, z]
            if r < 4.0:
                for y in range(A - 4, A):
                    s.set(x, y, z, "calcite" if (x + y + z) % 3 else "prismarine_bricks")
            if r < 2.9:
                s.set(x, A - 4, z, "verdant_froglight" if (x + z) % 2 else "sea_lantern")
                for y in range(A - 3, A + 1):
                    s.set(x, y, z, "water")
            # rim: knee-high, calcite with a verdigris cap
            if 2.9 <= r < 4.0:
                s.set(x, A, z, "calcite" if (x * 7 + z * 3) % 4 else "polished_diorite")
                s.set(x, A + 1, z, "waxed_oxidized_cut_copper_slab[type=bottom]")
            if 4.0 <= r < 4.8 and fp[x, z]:   # a ring of mossy flagstones round the rim
                s.set(x, A - 1, z, "mossy_cobblestone" if (x + z) % 3 == 0 else "calcite")
    # the wishes: sea pickles on the floor, lily pads on the surface
    for (x, z, n) in [(WX - 1, WZ, 3), (WX + 1, WZ + 1, 2), (WX, WZ - 1, 4), (WX + 1, WZ - 2, 1)]:
        s.set(x, A - 3, z, f"sea_pickle[pickles={n},waterlogged=true]")
    for (x, z) in [(WX - 2, WZ + 1), (WX + 1, WZ - 1), (WX + 2, WZ + 1)]:
        s.set(x, A + 1, z, "lily_pad")

    # ---------------------------------------------------------------- giant dripleaf: copper stalk + leaf umbrella
    # stalk rises from the north-east edge and leans over the well
    p0 = np.array([WX + 5.0, A - 1.0, WZ - 4.0]); p1 = np.array([WX + 4.0, A + 6.0, WZ - 3.0]); p2 = np.array([WX + 0.5, LEAF_Y - 1.0, WZ - 0.5])
    pts = []
    for i in range(80):
        t = i / 79
        q = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t * t * p2
        pts.append(q)
        rad = 1.1 - 0.6 * t
        for dx in range(-2, 3):
            for dy in range(-1, 2):
                for dz in range(-2, 3):
                    c = np.round(q + [dx, dy, dz]).astype(int)
                    if np.linalg.norm(c - q) <= rad + 0.35:
                        st = "waxed_oxidized_copper_grate" if (c[1] % 4 == 0) else "waxed_oxidized_copper"
                        s.set(*c, st)
    # the leaf: a domed lime disc with a notch, darker veins, rim drooping, glow-berry drips from the rim
    lc = (WX, WZ)
    for x in range(W):
        for z in range(D):
            dx, dz = x - lc[0] - 0.3, z - lc[1] + 0.2
            ang = math.atan2(dz, dx)
            notch = abs(math.atan2(math.sin(ang - 2.4), math.cos(ang - 2.4)))
            R = 6.2 * (1 + 0.05 * math.sin(5 * ang)) - (2.5 * max(0, 1 - notch / 0.35))
            r = math.hypot(dx, dz)
            if r > R:
                continue
            y = LEAF_Y - (1 if r > R - 1.3 else 0)      # rim droops one block
            vein = (abs(math.sin(ang * 3.5)) < 0.16 and r > 1.5) or r < 1.0
            edge = r > R - 1.3
            st = "green_wool" if vein else ("lime_wool" if (x * 3 + z * 5) % 4 else "lime_concrete")
            if edge:
                st = "green_wool" if (x + z) % 3 == 0 else "lime_wool"
            s.set(x, y, z, st)
            if r > R - 1.0 and (x * 5 + z * 3) % 6 == 0:
                L = 2 + (x + z) % 3
                for k in range(1, L):
                    s.set(x, y - k, z, "cave_vines_plant[berries=true]" if k % 2 else "cave_vines_plant[berries=false]")
                s.set(x, y - L, z, "cave_vines[age=25,berries=true]")
    s.set(WX, LEAF_Y + 1, WZ, "green_wool")          # the leaf's crown where the stalk meets it
    # little dripleaves at the stalk's foot echo the giant (scale cue)
    for (x, z, f, h) in [(WX + 3, WZ - 5, "south", 1), (WX + 6, WZ - 2, "west", 2), (WX + 6, WZ - 5, "west", 0), (WX + 2, WZ - 6, "east", 1)]:
        if s.idx[x, A, z] == 0:
            for k in range(h):
                s.set(x, A + k, z, f"big_dripleaf_stem[facing={f}]")
            s.set(x, A + h, z, f"big_dripleaf[facing={f},tilt=none]")
    # wish bell under the leaf, over the water
    s.set(WX, LEAF_Y - 1, WZ, "iron_chain[axis=y]")
    s.set(WX, LEAF_Y - 2, WZ, "iron_chain[axis=y]")
    s.set(WX, LEAF_Y - 3, WZ, "bell[attachment=ceiling,facing=north]")
    # spore blossom glow on the leaf underside
    s.set(WX - 3, LEAF_Y - 1, WZ + 2, "spore_blossom")
    s.set(WX + 2, LEAF_Y - 1, WZ + 3, "spore_blossom")

    # ---------------------------------------------------------------- the alcove (west), chest faces the well
    ax, az = 2, WZ
    s.box((ax - 1, A, az - 2), (ax, A + 3, az + 2), Mix({"calcite": 3, "diorite": 1}, seed=SEED + 1))
    s.box((ax + 1, A, az - 2), (ax + 1, A + 2, az - 2), "quartz_pillar[axis=y]")
    s.box((ax + 1, A, az + 2), (ax + 1, A + 2, az + 2), "quartz_pillar[axis=y]")
    s.box((ax, A, az - 1), (ax + 1, A + 2, az + 1), "cave_air")
    s.box((ax, A - 1, az - 1), (ax + 1, A - 1, az + 1), "smooth_quartz")
    for z in range(az - 2, az + 3):
        s.set(ax + 2, A + 3, z, "waxed_oxidized_cut_copper_stairs[facing=west,half=bottom]")
        s.set(ax + 1, A + 3, z, "waxed_oxidized_cut_copper")
        s.set(ax, A + 3, z, "waxed_oxidized_cut_copper")
        s.set(ax - 1, A + 4, z, "waxed_oxidized_cut_copper_slab[type=bottom]")
        s.set(ax, A + 4, z, "waxed_oxidized_cut_copper_stairs[facing=west,half=bottom]")
    s.set(ax + 2, A + 3, az - 2, "waxed_oxidized_cut_copper_slab[type=bottom]")
    s.set(ax + 2, A + 3, az + 2, "waxed_oxidized_cut_copper_slab[type=bottom]")
    s.set(ax - 1, A + 2, az, "verdant_froglight")
    loot_chest(s, ax, A, az, "minor", facing="east")
    s.set(ax, A, az - 1, "potted_blue_orchid")
    s.set(ax, A, az + 1, "candle[candles=3,lit=true]")
    s.set(ax + 1, A + 2, az, "lantern[hanging=true]")

    # ---------------------------------------------------------------- ground: boulders with ore seams, path, flowers
    for (x, z, h) in [(13, 2, 2), (14, 13, 1), (5, 15, 1)]:
        for y in range(A, A + h):
            s.set(x, y, z, "calcite")
        s.set(x - 1, A, z, "amethyst_block")
        s.set(x - 1, A + 1, z, "amethyst_cluster[facing=up]")
        deposit(s, x, A + h - 1, z)
    for z in range(13, D):   # stepping stones from the south
        s.set(C + (z % 2), A - 1, z, "calcite")
    clear = (rw < 4.9)
    clear[ax - 1:ax + 3, az - 2:az + 3] = True
    scatter(s, A, fp, chance=0.5, seed=SEED, keep_clear=clear)

    s.mark("cam_front", (C, A, D - 1), look_at=(WX, A + 4, WZ))
    fix_soil(s)   # grass under covers -> dirt
    return finish(s, tier="minor", kind="ground", anchor=(C, A, C))
