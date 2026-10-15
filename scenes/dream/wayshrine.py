"""Minor Dream site: THE WAYSHRINE.

A small pale shrine on a stepped octagonal plinth holds the offering (the loot chest). Far above it, with nothing holding
it up, hangs the Dream's heart: a green glass gem with a froglight core, circled by a tilted ring of drifting stones.
Read from afar: the glowing gem + stone halo; up close: the verdigris-domed niche and its offering.
Render: python -m tools.voxel render scenes/dream/wayshrine.py --mood dream
"""
import math

import numpy as np

from scenes.dream._dream import DREAMSTONE, deposit, finish, loot_chest
from scenes.dream._minor import disc, scatter
from tools.voxel.palette import Mix
from tools.voxel.scene import Scene
from tools.voxel.stability import fix_soil

W, H, D = 17, 30, 17
C = 8
A = 8            # first air above terrain (anchor y)
HEART_Y = A + 17
SEED = 311


def octa(dx, dz):
    return max(abs(dx), abs(dz), (abs(dx) + abs(dz)) * 0.72)


def build():
    s = Scene((W, H, D), name="wayshrine", seed=SEED)
    fp = disc(s, A, seed=SEED)

    # ---------------------------------------------------------------- plinth: two octagonal tiers
    for x in range(W):
        for z in range(D):
            o = octa(x - C, z - C)
            if o <= 5.6:
                s.set(x, A, z, "polished_diorite_slab[type=bottom]" if o > 4.8 else "polished_diorite")
            if o <= 3.9:
                s.set(x, A + 1, z, "quartz_slab[type=bottom]" if o > 3.1 else "smooth_quartz")
    s.fill(((C - 4, A, C - 4), (C + 4, A, C + 4)), DREAMSTONE, replace="polished_diorite")
    # front steps (south = +z)
    for x in range(C - 1, C + 2):
        s.set(x, A, C + 6, "polished_diorite_stairs[facing=north,half=bottom]")
        s.set(x, A, C + 5, "polished_diorite")
        s.set(x, A + 1, C + 4, "quartz_stairs[facing=north,half=bottom]")
        s.set(x, A + 1, C + 3, "smooth_quartz")

    # ---------------------------------------------------------------- the shrine (5 x 5 aedicule, open to the south)
    x0, x1, z0, z1 = C - 2, C + 2, C - 2, C + 2
    y0 = A + 2
    for y in range(y0, y0 + 5):
        for (x, z) in [(x0, z0), (x1, z0), (x0, z1), (x1, z1)]:
            s.set(x, y, z, "quartz_pillar[axis=y]")
    s.box((x0 + 1, y0, z0), (x1 - 1, y0 + 4, z0), Mix({"calcite": 3, "polished_diorite": 1}, seed=SEED))   # back wall
    for x in (x0, x1):                                                                                      # side walls
        s.box((x, y0, z0 + 1), (x, y0 + 4, z1 - 1), Mix({"calcite": 3, "diorite": 1}, seed=SEED + 1))
        s.set(x, y0 + 2, C, "lime_stained_glass_pane")
        s.set(x, y0 + 1, C, "diorite_wall")
    # back wall: inset glowing heart echo
    s.set(C, y0 + 2, z0, "verdant_froglight")
    s.set(C, y0 + 1, z0, "waxed_oxidized_chiseled_copper")
    s.set(C, y0 + 3, z0, "waxed_oxidized_chiseled_copper")
    # front pointed arch (south face)
    s.set(x0 + 1, y0 + 3, z1, "quartz_stairs[facing=east,half=top]")
    s.set(x1 - 1, y0 + 3, z1, "quartz_stairs[facing=west,half=top]")
    s.set(C, y0 + 4, z1, "chiseled_quartz_block")
    s.set(x0 + 1, y0 + 4, z1, "smooth_quartz"); s.set(x1 - 1, y0 + 4, z1, "smooth_quartz")
    # verdigris frieze + roof
    yr = y0 + 5
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 - 1, z1 + 2):
            edge = x in (x0 - 1, x1 + 1) or z in (z0 - 1, z1 + 1)
            corner = x in (x0 - 1, x1 + 1) and z in (z0 - 1, z1 + 1)
            if corner:
                s.set(x, yr, z, "quartz_slab[type=bottom]")
            elif edge:
                f = "south" if z == z0 - 1 else "north" if z == z1 + 1 else "east" if x == x0 - 1 else "west"
                s.set(x, yr, z, f"waxed_oxidized_cut_copper_stairs[facing={f},half=bottom]")
            else:
                s.set(x, yr, z, "waxed_oxidized_cut_copper")
    s.box((x0, yr - 1, z0), (x1, yr - 1, z1), "smooth_quartz", hollow=False)
    s.box((x0 + 1, yr - 1, z0 + 1), (x1 - 1, yr - 1, z1 - 1), "cave_air")
    s.set(C, yr - 1, C, "smooth_quartz")
    # dome
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            d = max(abs(x - C), abs(z - C))
            if d == 2:
                f = "south" if z == z0 else "north" if z == z1 else "east" if x == x0 else "west"
                if abs(x - C) == 2 and abs(z - C) == 2:
                    s.set(x, yr + 1, z, "waxed_oxidized_cut_copper_slab[type=bottom]")
                else:
                    s.set(x, yr + 1, z, f"waxed_oxidized_cut_copper_stairs[facing={f},half=bottom]")
            elif d == 1:
                s.set(x, yr + 1, z, "waxed_oxidized_copper")
                f = "south" if z == C - 1 and x == C else "north" if z == C + 1 and x == C else "east" if x == C - 1 and z == C else "west" if x == C + 1 and z == C else None
                s.set(x, yr + 2, z, f"waxed_oxidized_cut_copper_stairs[facing={f},half=bottom]" if f else "waxed_oxidized_cut_copper_slab[type=bottom]")
    s.set(C, yr + 1, C, "waxed_oxidized_copper")
    s.set(C, yr + 2, C, "waxed_oxidized_copper_bulb[lit=true]")
    s.set(C, yr + 3, C, "end_rod[facing=up]")
    # interior: offering chest, lantern, pots, amethyst
    s.box((x0 + 1, y0, z0 + 1), (x1 - 1, y0 + 4, z1), "cave_air")
    s.box((x0 + 1, y0 - 1, z0 + 1), (x1 - 1, y0 - 1, z1 - 1), Mix({"smooth_quartz": 1, "polished_diorite": 1}, seed=SEED + 2))
    s.set(C, y0 - 1, C, "waxed_oxidized_chiseled_copper")
    loot_chest(s, C, y0, z0 + 1, "minor", facing="south")
    s.set(C - 1, y0, z0 + 1, "potted_azure_bluet")
    s.set(C + 1, y0, z0 + 1, "amethyst_cluster[facing=up]")
    s.set(C, y0 + 4, C, "lantern[hanging=true]")
    for x in (C - 2, C + 2):   # paired fixtures flanking the niche
        s.set(x, y0, C + 3, "waxed_oxidized_copper_lantern" )

    # ---------------------------------------------------------------- the heart (hovering gem) + drifting stone ring
    for dx in range(-2, 3):
        for dy in range(-3, 4):
            for dz in range(-2, 3):
                m = abs(dx) + abs(dy) * 0.75 + abs(dz)
                if m <= 1.0:
                    s.set(C + dx, HEART_Y + dy, C + dz, "verdant_froglight")
                elif m <= 2.3:
                    s.set(C + dx, HEART_Y + dy, C + dz, "lime_stained_glass")
    s.set(C, HEART_Y + 4, C, "amethyst_cluster[facing=up]")
    s.set(C, HEART_Y - 4, C, "amethyst_cluster[facing=down]")
    # halo: a tilted, segmented band of drifting stones (16 segments, every other one present)
    tilt = math.radians(14)
    for x in range(W):
        for z in range(D):
            for y in range(HEART_Y - 6, HEART_Y + 6):
                dx, dy, dz = x - C, y - HEART_Y, z - C
                # rotate about the x axis so the ring tilts towards the south
                ry = dy * math.cos(tilt) - dz * math.sin(tilt)
                rz = dy * math.sin(tilt) + dz * math.cos(tilt)
                r = math.hypot(dx, rz)
                if abs(r - 6.6) > 0.62 or abs(ry) > 0.55:
                    continue
                seg = int(((math.atan2(rz, dx) + math.pi) / (2 * math.pi)) * 16) % 16
                if seg % 2:
                    continue
                s.set(x, y, z, "amethyst_block" if seg % 8 == 0 else ("calcite" if (x + z) % 3 else "polished_diorite"))
    # stones still rising to join the halo: a loose spiral from the plinth up
    for k, (ang, y) in enumerate([(200, A + 4), (250, A + 7), (300, A + 10), (350, A + 13)]):
        t_ = math.radians(ang)
        x = int(round(C + 6.8 * math.cos(t_))); z = int(round(C + 6.8 * math.sin(t_)))
        s.set(x, y, z, "calcite")
        s.set(x, y - 1, z, "small_amethyst_bud[facing=down]" if k % 2 else "pointed_dripstone[thickness=tip,vertical_direction=down]")

    # ---------------------------------------------------------------- ground: path, lamp posts, boulders, flowers
    for z in range(C + 7, D):
        s.set(C, A - 1, z, "calcite")
        s.set(C + (1 if z % 2 else -1), A - 1, z, "polished_diorite")
    for x in (C - 3, C + 3):
        z = C + 7
        s.set(x, A, z, "diorite_wall")
        s.set(x, A + 1, z, "diorite_wall")
        s.set(x, A + 2, z, "lantern")
    for (x, z, h) in [(2, 3, 2), (14, 4, 1), (3, 12, 1), (13, 13, 2)]:
        for y in range(A, A + h):
            s.set(x, y, z, "calcite" if y == A else "diorite")
        s.set(x + 1, A, z, "moss_block")
        s.set(x, A + h, z, "amethyst_cluster[facing=up]" if h == 2 else "moss_carpet")
    for (x, z, h) in [(2, 3, 2), (14, 4, 1), (13, 13, 2)]:   # ore seams: the boulder tops (open above, mineable)
        s.set(x, A + h, z, "cave_air")
        deposit(s, x, A + h - 1, z)
    clear = np.zeros((W, D), bool)
    clear[C - 1:C + 2, C + 5:] = True
    scatter(s, A, fp, chance=0.45, seed=SEED, keep_clear=clear)

    s.mark("cam_front", (C, A, D - 1), look_at=(C, A + 6, C))
    fix_soil(s)   # grass under covers -> dirt
    return finish(s, tier="minor", kind="ground", anchor=(C, A, C))
