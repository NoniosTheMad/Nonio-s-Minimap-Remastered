"""GRAND site: THE INVERTED SANCTUM.

Statement: a little upright chapel stands in a dream garden on a floating island; its reflection grew underneath the
island into a whole cathedral, hanging upside down into the void - door at the top, roof below, spire pointing at nothing.
Where the cathedral reaches past the island it kept a crust of the ground it was torn from.
Inside the hanging nave the world is the right way up again: a patterned floor (the inverted roof), upside-down pews
on the ceiling, and at the apse the Vault on its dais. Fly in through the great west door (just under the island rim,
floating steps lead down to the floor) or the broken lancet on the south side.

Layout (scene coords, x = nave axis, west = x small):
  island top y 72 (garden, chapel at the west end, beacon in the garden), cathedral attached at y 61.
  walls y 36..61 (door near the top), inverted roof y 35 -> ridge ~ y 24, crossing spire down to y ~ 3.
Render: python -m tools.voxel render scenes/dream/inverted_sanctum.py --mood dream
"""
import math

import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion

from scenes.dream._dream import (AMETHYST, GLOW_GREEN, GLOW_SEA, GLOW_WARM, SOIL, TURF, UNDERSIDE, beacon, deposit,
                                 finish, vault)
from tools.voxel import noise
from tools.voxel.palette import Gradient, Mix
from tools.voxel.scene import Scene

W, H, D = 64, 96, 64
CZ = 32                     # nave centre line (z)
TOP = 72                    # island turf level
G = 61                      # cathedral "ground" (inverted floor = nave ceiling), attached to the island underside
WT = 36                     # wall end / walkable floor of the nave (inverted roof springs below it)
NX0, NX1 = 10, 53           # nave outer x (west front .. start of apse)
NHW = 8                     # nave outer half width (z 24..40)
TX0, TX1 = 37, 45           # transept outer x
THW = 16                    # transept outer half width (z 16..48)
APX, APR = 53, 8            # apse centre x, outer radius
CROSS = (41, CZ)            # crossing (spire)
TB = 18                     # west towers' lowest course
SEED = 777

WALL = Gradient("y", [(WT + 3, Mix({"polished_diorite": 2, "calcite": 2, "quartz_bricks": 1})),
                      (G - 3, Mix({"quartz_bricks": 3, "calcite": 2, "polished_diorite": 1, "diorite": 1})),
                      (999, Mix({"calcite": 3, "polished_diorite": 1, "smooth_quartz": 1}))], jitter=1.5, jitter_scale=5, seed=SEED)
PILLAR = "quartz_pillar[axis=y]"
ROOF = Mix({"waxed_oxidized_cut_copper": 4, "waxed_oxidized_copper": 1, "waxed_weathered_cut_copper": 1}, seed=SEED + 1)
ROOF_BAND = "waxed_oxidized_copper"
COPPER_GRATE = "waxed_oxidized_copper_grate"
ROSE_GLASS = "purple_stained_glass"
CHAIN = "waxed_oxidized_copper_chain[axis=y]"

X = np.arange(W)[:, None, None] + 0.0
Y = np.arange(H)[None, :, None] + 0.0
Z = np.arange(D)[None, None, :] + 0.0
ZD = np.abs(Z - CZ)


def B(m):
    return np.broadcast_to(m, (W, H, D)).copy()


# ------------------------------------------------------------------ footprints (2D, x/z)
def footprints():
    x2 = np.arange(W)[:, None] + 0.0
    z2 = np.arange(D)[None, :] + 0.0
    zd = np.abs(z2 - CZ)
    nave = (x2 >= NX0) & (x2 <= NX1) & (zd <= NHW)
    trans = (x2 >= TX0) & (x2 <= TX1) & (zd <= THW)
    apse = (np.hypot(x2 - APX, z2 - CZ) <= APR) & (x2 >= APX)
    towers = (x2 >= NX0 - 3) & (x2 <= NX0 + 3) & (zd >= 7) & (zd <= 13)
    return nave, trans, apse, towers


NAVE2, TRANS2, APSE2, TOWERS2 = footprints()
BODY2 = NAVE2 | TRANS2 | APSE2
IN2 = binary_erosion(BODY2, iterations=2)


def _cols():
    return np.meshgrid(np.arange(W) + 0.5, np.arange(D) + 0.5, indexing="ij")


def island_r(gx, gz):
    ang = np.arctan2(gz - 32, gx - 33)
    wob = 1 + 0.07 * np.sin(3 * ang + 1.3) + 0.05 * np.sin(5 * ang + 0.4) + 0.04 * noise.fbm(gx, gz, 0.0, 6, 2, seed=SEED)
    return np.hypot((gx - 33) / 21.5, (gz - 32) / 16.5) / wob


def surface_y(s, x, z):
    col = np.nonzero(s.idx[x, :, z])[0]
    return int(col.max()) if len(col) else -1


# ------------------------------------------------------------------ island
def island(s):
    gx, gz = _cols()
    r = island_r(gx, gz)
    inside = r < 1
    top = TOP + np.round(1.2 * noise.fbm(gx, gz, 0.0, 10, 2, seed=SEED + 3)) - (r > 0.85) * 1
    bot = TOP - 3 - 9 * np.clip(1 - r, 0, 1) ** 0.6 - 3 * np.clip(noise.fbm(gx, gz, 0.0, 5, 2, seed=SEED + 4), 0, 1)
    bot = np.minimum(bot, np.where(BODY2 | TOWERS2, G - 1, 999))
    y = np.arange(H)[None, :, None]
    m = inside[:, None, :] & (y <= top[:, None, :]) & (y >= bot[:, None, :])
    s.fill(m, Gradient("depth", [(1, TURF), (3, SOIL), (6, Mix({"stone": 3, "calcite": 3, "andesite": 1}, seed=SEED)),
                                 (999, UNDERSIDE)], jitter=0.8, seed=SEED))
    # rock drips under the rim, away from the cathedral body
    rng = np.random.default_rng(SEED)
    near = binary_dilation(BODY2 | TOWERS2, iterations=1)
    for _ in range(40):
        a = rng.uniform(0, 2 * math.pi); rr = rng.uniform(0.6, 0.95)
        ix, iz = int(33 + 21.5 * rr * math.cos(a)), int(32 + 16.5 * rr * math.sin(a))
        if not (0 <= ix < W and 0 <= iz < D) or near[ix, iz]:
            continue
        col = np.nonzero(s.idx[ix, :, iz])[0]
        if not len(col):
            continue
        y0 = int(col.min()); L = int(rng.integers(3, 9)); rad = rng.uniform(1.2, 2.4)
        for k in range(L):
            rk = rad * (1 - k / L)
            for dx in range(-3, 4):
                for dz in range(-3, 4):
                    if dx * dx + dz * dz <= rk * rk and 0 <= ix + dx < W and 0 <= iz + dz < D and y0 - k >= 0:
                        if s.get(ix + dx, y0 - k, iz + dz) == "minecraft:air":
                            s.set(ix + dx, y0 - k, iz + dz, rng.choice(["calcite", "calcite", "amethyst_block", "stone"]))
        if y0 - L >= 0:
            s.set(ix, y0 - L, iz, "amethyst_cluster[facing=down]" if rng.random() < .6 else GLOW_GREEN)


# ------------------------------------------------------------------ garden on top
def garden(s):
    rng = np.random.default_rng(SEED + 9)
    for x in range(20, 56):
        for dz in (-1, 0, 1):
            z = CZ + dz + int(round(1.5 * math.sin(x / 6.0)))
            y = surface_y(s, x, z)
            if y >= TOP - 2 and s.get(x, y, z).split("[")[0] in ("minecraft:grass_block", "minecraft:moss_block"):
                s.set(x, y, z, rng.choice(["calcite", "polished_diorite", "moss_block", "calcite"]) if dz else "polished_diorite")
    # beacon court
    bx, bz = 40, CZ
    for x in range(bx - 6, bx + 7):
        for z in range(bz - 6, bz + 7):
            d = math.hypot(x - bx, z - bz)
            if d <= 5.5:
                if d < 2.5:
                    b = "calcite" if (x + z) % 2 else "polished_diorite"
                elif 3.2 < d < 4.0:
                    b = "prismarine_bricks"
                elif d > 4:
                    b = "moss_block" if rng.random() < .2 else "polished_diorite"
                else:
                    b = "calcite"
                s.set(x, TOP, z, b)
                for yy in range(TOP + 1, TOP + 6):
                    if s.get(x, yy, z) != "minecraft:air":
                        s.set(x, yy, z, "air")
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        x, z = int(round(bx + 5.5 * math.cos(a))), int(round(bz + 5.5 * math.sin(a)))
        s.set(x, TOP + 1, z, "waxed_oxidized_cut_copper")
        s.set(x, TOP + 2, z, "diorite_wall")
        s.set(x, TOP + 3, z, "lantern[hanging=false]")
    beacon(s, bx, TOP + 1, bz)
    for (ex, ez, f) in ((bx - 7, bz, "east"), (bx, bz - 7, "south"), (bx, bz + 7, "north")):
        for d in (-1, 0, 1):
            xx, zz = (ex, ez + d) if f == "east" else (ex + d, ez)
            yy = surface_y(s, xx, zz)
            if yy >= TOP - 1:
                s.set(xx, yy + 1, zz, f"birch_stairs[facing={f},half=bottom]")
        
    for x, z in ((bx - 1, bz - 1), (bx + 1, bz - 1), (bx - 1, bz + 1), (bx + 1, bz + 1)):
        s.set(x, TOP + 1, z, "amethyst_cluster[facing=up]")
    # flowering azalea trees with pale trunks
    for (tx, tz) in [(21, 25), (23, 40), (31, 19), (47, 20), (51, 40), (37, 45), (54, 31)]:
        y0 = surface_y(s, tx, tz)
        if y0 < TOP - 3:
            continue
        h = int(rng.integers(5, 8))
        for k in range(1, h + 1):
            s.set(tx, y0 + k, tz, "stripped_pale_oak_log[axis=y]")
        cy = y0 + h
        rr = rng.uniform(2.6, 3.6)
        for dx in range(-4, 5):
            for dy in range(-2, 3):
                for dz in range(-4, 5):
                    d = math.sqrt(dx * dx + (dy * 1.6) ** 2 + dz * dz)
                    if d <= rr + rng.uniform(-0.4, 0.4) and s.get(tx + dx, cy + dy, tz + dz) == "minecraft:air":
                        s.set(tx + dx, cy + dy, tz + dz, "pale_oak_leaves" if rng.random() < .6 else "flowering_azalea_leaves")
        s.set(tx, cy + 1, tz, "flowering_azalea_leaves")
        for dx in range(-4, 5):        # pale moss curtains under the canopy rim
            for dz in range(-4, 5):
                if rng.random() < 0.35 and s.get(tx + dx, cy - 2, tz + dz) == "minecraft:air" and                         "leaves" in s.get(tx + dx, cy - 1, tz + dz):
                    L = int(rng.integers(1, 3))
                    for k in range(L):
                        if s.get(tx + dx, cy - 2 - k, tz + dz) == "minecraft:air":
                            s.set(tx + dx, cy - 2 - k, tz + dz, "pale_hanging_moss[tip=" + ("true" if k == L - 1 else "false") + "]")
        for dx, dz in ((2, 0), (-2, 0), (0, 2), (0, -2)):
            if s.get(tx + dx, cy - 3, tz + dz) == "minecraft:air" and s.get(tx + dx, cy - 2, tz + dz) != "minecraft:air":
                if rng.random() < .4:
                    s.set(tx + dx, cy - 3, tz + dz, "spore_blossom")
    flowers = ["pink_petals[flower_amount=4,facing=north]", "wildflowers[flower_amount=3,facing=east]", "lily_of_the_valley",
               "allium", "short_grass", "short_grass", "firefly_bush", "torchflower", "azure_bluet"]
    for x in range(W):
        for z in range(D):
            y = surface_y(s, x, z)
            if y < TOP - 3 or s.get(x, y, z).split("[")[0] not in ("minecraft:grass_block", "minecraft:moss_block"):
                continue
            r = rng.random()
            if r < 0.30:
                s.set(x, y + 1, z, flowers[int(rng.integers(len(flowers)))])
            elif r < 0.33:
                s.set(x, y + 1, z, "moss_carpet")


def chapel(s):
    """Small upright chapel above the cathedral's west door: the 'original' of the reflection."""
    x0, x1, z0, z1 = 13, 21, CZ - 4, CZ + 4
    y0 = TOP + 1
    s.box((x0 - 1, TOP, z0 - 1), (x1 + 1, TOP, z1 + 1), "polished_diorite")
    s.box((x0, y0, z0), (x1, y0 + 6, z1), WALL, hollow=True)
    s.box((x0 + 1, y0, z0 + 1), (x1 - 1, y0 + 6, z1 - 1), "cave_air")
    s.box((x0 + 1, y0 - 1, z0 + 1), (x1 - 1, y0 - 1, z1 - 1), Mix({"quartz_bricks": 1, "calcite": 1}))
    for x in (x0, x1):
        for z in (z0, z1):
            s.box((x, y0, z), (x, y0 + 6, z), PILLAR)
    for dy in range(0, 5):
        for dz in range(-1, 2):
            if dy < 4 or dz == 0:
                s.set(x1, y0 + dy, CZ + dz, "cave_air")
    s.set(x1 + 1, y0 + 5, CZ, "smooth_quartz_stairs[facing=west,half=bottom]")
    s.set(x1 + 1, y0 + 5, CZ - 1, "smooth_quartz_stairs[facing=north,half=bottom]")
    s.set(x1 + 1, y0 + 5, CZ + 1, "smooth_quartz_stairs[facing=south,half=bottom]")
    for x in (15, 19):
        for z in (z0, z1):
            s.box((x, y0 + 2, z), (x, y0 + 4, z), "lime_stained_glass_pane")
            for dx in (-1, 1):
                f = "north" if z == z0 else "south"
                s.set(x + dx, y0 + 3, z + (-1 if z == z0 else 1), f"birch_trapdoor[facing={f},open=true,half=top]")
    for k in range(0, 6):
        zz0, zz1 = z0 - 1 + k, z1 + 1 - k
        if zz0 > zz1:
            break
        for z in range(zz0, zz1 + 1):
            for x in range(x0 - 1, x1 + 2):
                if z in (zz0, zz1):
                    f = "south" if z == zz0 else "north"
                    s.set(x, y0 + 7 + k, z, f"waxed_oxidized_cut_copper_stairs[facing={f},half=bottom]")
                elif k == 0 or x in (x0 - 1, x1 + 1):
                    s.set(x, y0 + 7 + k, z, "waxed_oxidized_cut_copper" if k else "smooth_quartz")
    for k in range(0, 5):
        for z in range(z0 + k, z1 - k + 1):
            for x in (x0, x1):
                if s.get(x, y0 + 7 + k, z) == "minecraft:air":
                    s.set(x, y0 + 7 + k, z, "calcite")
    s.set(x1, y0 + 9, CZ, "purple_stained_glass")
    s.set(x0, y0 + 9, CZ, "purple_stained_glass")
    sx = x0 + 1
    for k in range(0, 7):
        s.set(sx, y0 + 12 + k, CZ, "waxed_oxidized_copper" if k < 6 else "waxed_oxidized_lightning_rod[facing=up]")
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        s.box((sx + dx, y0 + 12, CZ + dz), (sx + dx, y0 + 14, CZ + dz), "waxed_oxidized_cut_copper")
        s.set(sx + dx, y0 + 15, CZ + dz, "waxed_oxidized_cut_copper_slab[type=bottom]")
    s.set(sx, y0 + 13, CZ, GLOW_WARM)
    s.box((x0 + 1, y0, CZ - 1), (x0 + 1, y0, CZ + 1), "chiseled_quartz_block")
    s.set(x0 + 1, y0 + 1, CZ, "amethyst_cluster[facing=up]")
    s.set(x0 + 1, y0 + 1, CZ - 1, "candle[candles=3,lit=true]")
    s.set(x0 + 1, y0 + 1, CZ + 1, "candle[candles=2,lit=true]")
    s.set(17, y0 + 6, CZ, CHAIN); s.set(17, y0 + 5, CZ, "lantern[hanging=true]")
    for x in (15, 17, 19):
        s.set(x, y0, CZ - 2, "birch_stairs[facing=west,half=bottom]")
        s.set(x, y0, CZ + 2, "birch_stairs[facing=west,half=bottom]")


# ------------------------------------------------------------------ the hanging cathedral
def cathedral(s):
    plinth2 = binary_dilation(BODY2 | TOWERS2, iterations=1)
    s.fill(B(plinth2[:, None, :]) & (Y >= G - 1) & (Y <= G + 1), Mix({"polished_diorite": 2, "calcite": 1}))
    # where the cathedral reaches past the island, it kept a crust of the ground it was torn from
    gx, gz = _cols()
    isl = island_r(gx, gz) < 1
    rng = np.random.default_rng(SEED + 40)
    nz = noise.fbm(gx, gz, 0.0, 4, 2, seed=SEED + 41)
    for x, z in zip(*np.nonzero(plinth2 & ~isl)):
        n = nz[x, z]
        if n > -0.35:
            top = G + 3 if n > 0.1 else G + 2
            s.set(x, G + 2, z, "dirt" if n > 0.2 else "rooted_dirt")
            s.set(x, top, z, "moss_block" if n < 0.3 else "grass_block")
            if rng.random() < 0.35:
                s.set(x, top + 1, z, rng.choice(["short_grass", "pink_petals[flower_amount=3,facing=south]", "moss_carpet", "allium"]))
        else:
            s.set(x, G + 2, z, rng.choice(["calcite", "polished_diorite", "smooth_quartz_slab[type=bottom]"]))
    s.fill(B(BODY2[:, None, :]) & (Y >= WT) & (Y <= G), WALL)
    # inverted roof: nave gable ridge along x, transept ridge along z, apse half cone
    slope = 1.3
    nave_roof = B(NAVE2[:, None, :]) & (Y < WT) & (Y >= WT - 1 - (NHW + 0.5 - ZD) * slope)
    trans_roof = B(TRANS2[:, None, :]) & (Y < WT) & (Y >= WT - 1 - (4.5 - np.abs(X - 41)) * slope)
    ad = np.hypot(X - APX, Z - CZ)
    apse_roof = B(APSE2[:, None, :]) & (Y < WT) & (Y >= WT - 1 - (APR + 0.5 - ad) * slope)
    roof = nave_roof | trans_roof | apse_roof
    s.fill(roof, ROOF)
    s.fill(roof & (np.mod(Y, 4) == 0), ROOF_BAND)
    s.fill(roof & (np.mod(X, 6) == 1) & ~TRANS2[:, None, :], "waxed_oxidized_cut_copper")
    corn2 = binary_dilation(BODY2, iterations=1) & ~BODY2
    s.fill(B(corn2[:, None, :]) & (Y == WT), "smooth_quartz_slab[type=top]")
    s.fill(B(corn2[:, None, :]) & (Y == WT + 1), "smooth_quartz")
    s.fill(B(corn2[:, None, :]) & (Y == G - 6), "waxed_oxidized_cut_copper")       # string course under the island
    s.fill(B(corn2[:, None, :]) & (Y == G - 7), "waxed_oxidized_cut_copper_slab[type=top]")
    s.fill(B(corn2[:, None, :]) & (Y == WT + 12) & (np.mod(X + Z, 2) == 0), "smooth_quartz_slab[type=top]")
    s.fill(B(corn2[:, None, :]) & (Y == WT + 13), "smooth_quartz")
    # pilaster strips on the outer face every 3 blocks, between the bays
    pil2 = corn2 & ((np.mod(np.arange(W)[:, None], 3) == 2) | ~NAVE2[:, :] & False)
    s.fill(B(pil2[:, None, :]) & (Y >= WT + 2) & (Y <= G - 8) & (Y != WT + 12) & (Y != WT + 13), PILLAR)
    # interior
    s.fill(B(IN2[:, None, :]) & (Y >= WT + 1) & (Y <= G - 2), "cave_air")
    fl = B(IN2[:, None, :]) & (Y == WT)
    s.fill(fl, Mix({"calcite": 2, "polished_diorite": 2, "smooth_quartz": 1}, seed=SEED + 5))
    s.fill(fl & (ZD <= 1.5) & (X < TX1), "prismarine_bricks")
    s.fill(fl & (ZD <= 0.5) & (np.mod(X, 4) == 0) & (X < TX1), GLOW_GREEN)
    s.fill(fl & (np.abs(ZD - 4) < 0.5) & (np.mod(X, 3) == 0), "dark_prismarine")
    cr = fl & (np.hypot(X - CROSS[0], Z - CZ) <= 3.5)
    s.fill(cr, "smooth_quartz")
    s.fill(cr & ((np.abs(X - CROSS[0]) < 0.5) | (np.abs(Z - CZ) < 0.5)), "prismarine_bricks")
    s.set(CROSS[0], WT, CZ, GLOW_GREEN)
    # ceiling = the cathedral's real floor, seen from below: checkerboard + upside-down pews
    ce = B(IN2[:, None, :]) & (Y == G - 1)
    s.fill(ce, Mix({"quartz_bricks": 2, "calcite": 1}, seed=SEED + 6))
    s.fill(ce & (np.mod(X + Z, 2) == 0), "polished_diorite")
    s.fill(ce & (ZD <= 1.5), "prismarine_bricks")
    for x in range(15, 35, 3):
        for z0, z1 in ((CZ - 5, CZ - 2), (CZ + 2, CZ + 5)):
            for z in range(z0, z1 + 1):
                s.set(x, G - 2, z, "birch_stairs[facing=west,half=top]")
            s.set(x - 1, G - 2, z0, "birch_slab[type=top]")
            s.set(x - 1, G - 2, z1, "birch_slab[type=top]")
    # upside-down altar on the ceiling over the apse (mirror of the real dais)
    s.box((APX - 1, G - 2, CZ - 2), (APX + 1, G - 2, CZ + 2), "smooth_quartz")
    s.box((APX, G - 3, CZ - 1), (APX, G - 3, CZ + 1), "chiseled_quartz_block")
    s.set(APX, G - 4, CZ, "amethyst_cluster[facing=down]")
    for x in range(NX0 + 4, NX1 + 1, 6):
        for z in range(CZ - NHW + 2, CZ + NHW - 1):
            if IN2[x, z]:
                s.set(x, G - 1, z, "quartz_pillar[axis=z]")
    bays = list(range(NX0 + 4, NX1 + 1, 6))          # 14, 20, 26, 32, 38, 44, 50
    for x in bays:
        if TX0 <= x <= TX1:
            continue
        for z in (CZ - NHW + 2, CZ + NHW - 2):
            s.box((x, WT + 1, z), (x, G - 2, z), PILLAR)
    # lancet windows (pointed DOWN) in the nave walls
    lancets = [b + 3 for b in bays if b + 3 < TX0 - 1 or TX1 + 1 < b + 3 < NX1]
    for x in lancets:
        for side in (-1, 1):
            zw = CZ + side * NHW
            for y in range(WT + 3, G - 3):
                v = (G - 4) - y
                for dx in (-1, 0, 1):
                    if v <= 16 or (v <= 18 and dx == 0):
                        s.set(x + dx, y, zw, "waxed_oxidized_copper_bars" if (dx == 0 and v % 6 != 0) else "lime_stained_glass")
                        s.set(x + dx, y, zw - side, "cave_air")
            for dx in (-1, 0, 1):    # head (top) sill and glowing drip at the point
                s.set(x + dx, G - 3, zw + side, "smooth_quartz_stairs[facing=" + ("north" if side < 0 else "south") + ",half=top]")
            s.set(x, G - 4 - 19, zw + side, "smooth_quartz_slab[type=top]")
            s.set(x, G - 4 - 20, zw + side, GLOW_GREEN)
            for y in range(WT + 2, G - 1):
                for dx in (-2, 2):
                    s.set(x + dx, y, zw + side, "smooth_quartz" if (y % 3) else "chiseled_quartz_block")
            s.set(x, WT + 2, zw + side, "smooth_quartz_stairs[facing=" + ("north" if side < 0 else "south") + ",half=top]")
    # broken lancet on the south side (second way in)
    bx = lancets[2]
    for y in range(WT + 3, G - 3):
        for dx in (-1, 0, 1):
            s.set(bx + dx, y, CZ + NHW, "cave_air")
    for dx, dy in ((-1, 0), (1, 1), (-1, 6), (0, 0)):
        s.set(bx + dx, WT + 3 + dy, CZ + NHW, "chiseled_quartz_block" if dy else "calcite")
    for side in (-1, 1):
        rose(s, (41, WT + 13, CZ + side * THW), side_axis="z", r=5.5, dir=side)
    west(s)
    for a in range(-60, 61, 30):
        ax = APX + (APR - 0.5) * math.cos(math.radians(a)); az = CZ + (APR - 0.5) * math.sin(math.radians(a))
        for y in range(WT + 4, G - 4):
            s.set(int(round(ax)), y, int(round(az)), "lime_stained_glass" if y % 5 else "smooth_quartz")
    for x in [b for b in bays if b < TX0 - 1 or b > TX1 + 1]:
        for side in (-1, 1):
            pier(s, x, CZ + side * (NHW + 4), side)
    for x in (TX0, TX1):
        for side in (-1, 1):
            pier(s, x, CZ + side * (THW + 3), side, wall_z=CZ + side * THW)
    roof_dressing(s, roof)
    spire(s)
    towers(s)
    interior_dressing(s)


def roof_dressing(s, roof):
    """Ridge cresting + downward finials on the nave ridge; glowing roof lights on the slopes."""
    for x in range(NX0, NX1 + 1):
        if TX0 - 1 <= x <= TX1 + 1:
            continue
        col = np.nonzero(roof[x, :, CZ])[0]
        if not len(col):
            continue
        yb = int(col.min())
        s.set(x, yb, CZ, "smooth_quartz")
        if x % 4 == 2:
            s.set(x, yb - 1, CZ, "waxed_oxidized_cut_copper_slab[type=top]")
            s.set(x, yb - 2, CZ, "end_rod[facing=down]")
        if x % 6 == 0:
            for side in (-1, 1):
                z = CZ + side * 4
                c2 = np.nonzero(roof[x, :, z])[0]
                if len(c2):
                    yy = int(c2.min())
                    for dy in (0, 1):
                        s.set(x, yy + dy, z, "lime_stained_glass")
                        s.set(x, yy + dy, z - side, GLOW_GREEN)


def rose(s, c, side_axis, r, dir):
    """Rose window disc set into a facade plane; glow behind."""
    cx, cy, cz = c
    R = int(r) + 2
    for u in range(-R, R + 1):
        for v in range(-R, R + 1):
            d = math.hypot(u, v)
            if d > r + 0.6:
                continue
            ang = math.degrees(math.atan2(v, u)) % 45
            if d > r - 0.4:
                b = "smooth_quartz"
            elif d < 1.2:
                b = "amethyst_block"
            elif abs(ang - 22.5) < 7 and d > 2:
                b = "lime_stained_glass"
            elif d < 2.2:
                b = "purple_stained_glass"
            else:
                b = ROSE_GLASS if (int(d) % 2) else "magenta_stained_glass"
            if side_axis == "z":
                s.set(cx + u, cy + v, cz, b)
                if d <= r - 0.4:
                    s.set(cx + u, cy + v, cz - dir, GLOW_SEA if d > 1.5 else "amethyst_block")
            else:
                s.set(cx, cy + v, cz + u, b)
                if d <= r - 0.4:
                    s.set(cx - dir, cy + v, cz + u, GLOW_SEA if d > 1.5 else "amethyst_block")
    for k in range(0, 360, 10):
        u = (r + 1.2) * math.cos(math.radians(k)); v = (r + 1.2) * math.sin(math.radians(k))
        st = "smooth_quartz_slab[type=top]" if v > 0 else "smooth_quartz_slab[type=bottom]"
        if side_axis == "z":
            s.set(int(round(cx + u)), int(round(cy + v)), cz + dir, st)
        else:
            s.set(cx + dir, int(round(cy + v)), int(round(cz + u)), st)


def _inv_arch(u, v, hw, depth):
    """Inverted pointed arch: v = distance down from the top line. Full width near the top, point at the bottom."""
    u = abs(u)
    if u > hw:
        return False
    spring = depth - hw * 1.4
    if v <= spring:
        return True
    return (v - spring) <= hw * 1.4 * (1 - (u / (hw + 0.5)) ** 1.6)


def west(s):
    xw = NX0
    top_y = G - 2
    # 3 nested arch layers proud of the wall (x = 9, 8, 7), the densest element
    for layer, (xo, hw, depth) in enumerate(((xw - 1, 5, 14), (xw - 2, 4.5, 13), (xw - 3, 4, 12))):
        for z in range(CZ - int(hw) - 3, CZ + int(hw) + 4):
            for y in range(top_y - depth - 3, G + 1):
                u = z - CZ; v = top_y - y
                if _inv_arch(u, v, hw + 1, depth + 1) and not _inv_arch(u, v, hw, depth):
                    s.set(xo, y, z, ["chiseled_quartz_block", "smooth_quartz", "quartz_bricks"][layer] if (y + layer) % 4
                          else "waxed_oxidized_cut_copper")
    for x in range(xw - 3, xw + 3):
        for z in range(CZ - 4, CZ + 5):
            for y in range(WT + 1, G):
                if _inv_arch(z - CZ, top_y - y, 3.5, 11):
                    s.set(x, y, z, "cave_air")
    s.box((xw - 3, top_y + 1, CZ - 4), (xw + 2, top_y + 1, CZ + 4), "polished_diorite")
    for z in (CZ - 3, CZ + 3):     # lanterns hang at the door's head
        s.set(xw - 3, top_y, z, "lantern[hanging=true]")
    # inverted gable on the west front: the big rose window
    rose(s, (xw, WT - 5, CZ), side_axis="x", r=4.5, dir=-1)
    s.set(xw - 2, top_y - 14, CZ, "amethyst_cluster[facing=down]")


def pier(s, x, zp, side, wall_z=None):
    """Buttress pier hanging from the island: 2x2 shaft G..y_bot, copper bands, downward pinnacle, strut to the wall."""
    y_bot = WT + 3
    for dx in (0, 1):
        for dz in (0, -side):
            for y in range(y_bot, G + 1):
                s.set(x + dx, y, zp + dz, PILLAR if (dx == 0 and dz == 0) else ("polished_diorite" if y % 2 else "calcite"))
            for yb in (y_bot + 4, y_bot + 12):
                s.set(x + dx, yb, zp + dz, "waxed_oxidized_cut_copper")
            s.set(x + dx, y_bot, zp + dz, "smooth_quartz")
    for k in range(1, 7):
        for dx in (0, 1):
            for dz in (0, -side):
                if k < 3 or (dx == 0 and dz == 0):
                    s.set(x + dx, y_bot - k, zp + dz, "waxed_oxidized_copper" if k < 3 else "waxed_oxidized_cut_copper")
    s.set(x, y_bot - 7, zp, "end_rod[facing=down]")
    wz = wall_z if wall_z is not None else CZ + side * NHW
    n = abs(zp - wz)
    for k in range(0, n + 1):
        z = zp - side * k
        y = y_bot + 2 - int(round(k * 0.5))
        s.set(x, y, z, "polished_diorite")
        s.set(x, y - 1, z, "smooth_quartz_slab[type=top]")


def spire(s):
    """Octagonal verdigris spire hanging from the crossing down into the void, a glowing lantern stage, amethyst tip."""
    cx, cz = CROSS
    y_top = WT - 7
    y_tip = 3
    for y in range(y_tip, y_top + 1):
        t = (y - y_tip) / (y_top - y_tip)
        r = 0.6 + 4.6 * t ** 0.9
        for dx in range(-6, 7):
            for dz in range(-6, 7):
                d8 = max(abs(dx), abs(dz), (abs(dx) + abs(dz)) / 1.42)
                if d8 <= r:
                    edge = d8 > r - 1.0
                    rib = (abs(dx) == abs(dz) or dx == 0 or dz == 0) and edge
                    blk = "smooth_quartz" if rib else ("waxed_oxidized_copper" if y % 5 == 0 else "waxed_oxidized_cut_copper")
                    if not edge:
                        blk = "calcite"
                    s.set(cx + dx, y, cz + dz, blk)
    for y in (y_top - 4, y_top - 5, y_top - 6):
        for dx in range(-5, 6):
            for dz in range(-5, 6):
                d8 = max(abs(dx), abs(dz), (abs(dx) + abs(dz)) / 1.42)
                if 3.2 < d8 <= 4.2:
                    s.set(cx + dx, y, cz + dz, COPPER_GRATE if (dx + dz) % 2 else "smooth_quartz")
                elif d8 <= 3.2:
                    s.set(cx + dx, y, cz + dz, GLOW_GREEN if d8 < 1.5 else GLOW_SEA)
    s.set(cx, y_tip, cz, AMETHYST)
    s.set(cx, y_tip - 1, cz, GLOW_GREEN)
    s.set(cx, y_tip - 2, cz, "amethyst_cluster[facing=down]")
    for dx, dz in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
        for k in range(0, 5):
            s.set(cx + dx, y_top + 2 - k, cz + dz, "smooth_quartz" if k < 2 else "waxed_oxidized_cut_copper")
        s.set(cx + dx, y_top - 3, cz + dz, "end_rod[facing=down]")


def towers(s):
    """Twin west towers hanging lower than the nave, belfries glowing, pyramidal copper caps aiming down."""
    for side in (-1, 1):
        zc = CZ + side * 10
        x0, x1 = NX0 - 3, NX0 + 3
        z0, z1 = zc - 3, zc + 3
        s.box((x0, TB, z0), (x1, G, z1), WALL)
        s.box((x0 + 1, TB + 1, z0 + 1), (x1 - 1, G - 2, z1 - 1), "cave_air")
        for yl in (G - 3, WT + 6, TB + 14):
            s.set(x0 + 3, yl + 1, zc, CHAIN); s.set(x0 + 3, yl, zc, "waxed_oxidized_copper_lantern[hanging=true]")
        for x in (x0, x1):
            for z in (z0, z1):
                s.box((x, TB, z), (x, G, z), PILLAR)
        for y in (WT + 1, TB + 9, TB + 1, G - 6):
            s.box((x0 - 1, y, z0 - 1), (x1 + 1, y, z1 + 1), "smooth_quartz", hollow=True)
        for y in range(TB + 2, TB + 7):
            for k in (-1, 0, 1):
                s.set(x0, y, zc + k, "cave_air"); s.set(x1, y, zc + k, "cave_air")
                s.set(x0 + 3 + k, y, z0, "cave_air"); s.set(x0 + 3 + k, y, z1, "cave_air")
        s.box((x0 + 2, TB + 3, z0 + 2), (x1 - 2, TB + 5, z1 - 2), GLOW_GREEN)
        s.box((x0 + 1, TB + 2, z0 + 1), (x1 - 1, TB + 2, z1 - 1), COPPER_GRATE)
        for y in list(range(TB + 11, TB + 17)) + list(range(WT + 4, G - 8)):
            if y % 7 == 0:
                continue
            s.set(x0, y, zc, "lime_stained_glass"); s.set(x1, y, zc, "lime_stained_glass")
            s.set(x0 + 3, y, z0, "lime_stained_glass"); s.set(x0 + 3, y, z1, "lime_stained_glass")
        for k in range(0, 9):
            rr = 3.5 - k * 0.42
            if rr < 0:
                break
            for dx in range(-4, 5):
                for dz in range(-4, 5):
                    if max(abs(dx), abs(dz)) <= rr:
                        s.set(x0 + 3 + dx, TB - 1 - k, zc + dz,
                              "waxed_oxidized_cut_copper" if max(abs(dx), abs(dz)) >= rr - 1 else "calcite")
        tip = TB - 10
        s.set(x0 + 3, tip, zc, "waxed_oxidized_copper")
        s.set(x0 + 3, tip - 1, zc, "waxed_oxidized_lightning_rod[facing=down]")
        for x in (x0, x1):
            for z in (z0, z1):
                s.set(x, TB - 1, z, "smooth_quartz")
                s.set(x, TB - 2, z, "end_rod[facing=down]")


def interior_dressing(s):
    # floating stepping stones: door landing -> nave floor along the north side (and back up)
    land_y = G - 14
    s.box((NX0 + 1, land_y, CZ - 3), (NX0 + 3, land_y, CZ + 3), "polished_diorite")
    s.box((NX0 + 1, land_y - 1, CZ - 3), (NX0 + 3, land_y - 1, CZ + 3), "smooth_quartz_slab[type=top]")
    for z in range(CZ - 3, CZ + 4):
        if z not in (CZ - 3,):
            s.set(NX0 + 3, land_y + 1, z, "birch_fence")
    y, x = land_y, NX0 + 4
    while y > WT + 1:
        st = "smooth_quartz_slab[type=top]" if (x // 2) % 2 else "polished_diorite_slab[type=top]"
        for dz in (-5, -4):
            s.set(x, y - 1, CZ + dz, st)
            s.set(x + 1, y - 1, CZ + dz, st)
        if (x - NX0) % 8 == 4:
            s.set(x, y - 2, CZ - 5, "amethyst_cluster[facing=down]")
        y -= 1
        x += 2
    # dais + vault at the apse focal end
    dx0 = APX - 4
    s.box((dx0, WT + 1, CZ - 4), (APX + 3, WT + 1, CZ + 4), "polished_diorite", replace="cave_air")
    s.box((dx0 + 1, WT + 2, CZ - 3), (APX + 2, WT + 2, CZ + 3), "smooth_quartz", replace="cave_air")
    for z in range(CZ - 3, CZ + 4):
        s.set(dx0, WT + 2, z, "smooth_quartz_stairs[facing=west,half=bottom]")
    for z in range(CZ - 4, CZ + 5):
        s.set(dx0 - 1, WT + 1, z, "polished_diorite_stairs[facing=west,half=bottom]")
    vault(s, APX - 1, WT + 3, CZ, facing="west")
    for z in (CZ - 3, CZ + 3):
        s.box((APX - 1, WT + 3, z), (APX - 1, WT + 7, z), "waxed_oxidized_copper")
        s.set(APX - 1, WT + 8, z, AMETHYST)
        s.set(APX - 1, WT + 9, z, "amethyst_cluster[facing=up]")
        s.set(APX - 2, WT + 3, z, "waxed_oxidized_copper_lantern[hanging=false]")
    s.set(APX + 1, WT + 3, CZ, GLOW_WARM)
    s.set(APX + 1, WT + 4, CZ, "amethyst_cluster[facing=up]")
    # candelabra posts down the nave
    for x in range(NX0 + 5, TX0, 6):
        for z in (CZ - 3, CZ + 3):
            s.set(x, WT + 1, z, "polished_diorite")
            s.set(x, WT + 2, z, "diorite_wall")
            s.set(x, WT + 3, z, "lantern[hanging=false]")
    # chandelier at the crossing
    cx, cz = CROSS
    for y in range(G - 2, G - 10, -1):
        s.set(cx, y, cz, CHAIN)
    s.box((cx - 1, G - 10, cz - 1), (cx + 1, G - 10, cz + 1), COPPER_GRATE)
    s.set(cx, G - 10, cz, GLOW_GREEN)
    for ddx, ddz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        s.set(cx + ddx, G - 11, cz + ddz, "waxed_oxidized_copper_lantern[hanging=true]")
    # transept side chapels: planters + lectern
    for side in (-1, 1):
        zc = CZ + side * 10
        for x in (39, 43):
            s.set(x, WT + 1, zc, "moss_block")
            s.set(x, WT + 2, zc, "flowering_azalea")
        s.set(41, WT + 1, zc, "lectern[facing=" + ("south" if side < 0 else "north") + "]")
        for x in (39, 43):
            s.set(x, WT + 1, zc + side * 3, "polished_diorite")
            s.set(x, WT + 2, zc + side * 3, "waxed_oxidized_copper_lantern[hanging=false]")
        s.set(41, G - 2, zc, CHAIN); s.set(41, G - 3, zc, CHAIN); s.set(41, G - 4, zc, "lantern[hanging=true]")
        # props: decorated pots and candles along the chapel walls
        for x in (38, 44):
            s.set(x, WT + 1, zc - side, "decorated_pot")
            s.set(x, WT + 1, zc + side, "flower_pot")
    for x in range(NX0 + 6, TX0 - 1, 6):
        for z in (CZ - 5, CZ + 5):
            if s.get(x, WT + 1, z) == "minecraft:cave_air":
                s.set(x, WT + 1, z, "candle[candles=4,lit=true]")
    for x in range(16, 36, 6):
        s.set(x, G - 2, CZ, CHAIN)
        s.set(x, G - 3, CZ, "lantern[hanging=true]")


def deposits(s):
    """10 regrowing veins: 4 in crystal outcrops in the garden, 6 as seams in the transept floors inside."""
    rng = np.random.default_rng(SEED + 21)
    for (ox, oz) in ((25, 22), (46, 42), (28, 42), (50, 24)):
        y0 = surface_y(s, ox, oz)
        if y0 < TOP - 3:
            continue
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                if abs(dx) + abs(dz) > 3:
                    continue
                h = 2 - (abs(dx) + abs(dz)) // 2
                for k in range(0, h + 1):
                    s.set(ox + dx, y0 + k, oz + dz, rng.choice(["calcite", "calcite", "amethyst_block", "tuff"]))
                if s.get(ox + dx, y0 + h + 1, oz + dz) != "minecraft:air" and (dx or dz):
                    s.set(ox + dx, y0 + h + 1, oz + dz, "air")
        top = y0 + 2
        for yy in range(top + 1, top + 4):
            s.set(ox, yy, oz, "air")
        deposit(s, ox, top, oz)
        s.set(ox + 1, top, oz, "amethyst_cluster[facing=up]")
    for side in (-1, 1):
        for x in (38, 41, 44):
            z = CZ + side * 13
            s.set(x, WT, z - side, AMETHYST)
            deposit(s, x, WT, z)
            s.set(x, WT + 1, z, "cave_air")


def build():
    s = Scene((W, H, D), name="inverted_sanctum", seed=SEED)
    island(s)
    cathedral(s)
    chapel(s)
    garden(s)
    deposits(s)
    from tools.voxel.stability import fix_soil
    fix_soil(s)
    s.mark("cam_below", (62, 4, 62), look_at=(34, 34, 30))
    s.mark("cam_side", (63, 52, 63), look_at=(30, 40, 30))
    s.mark("cam_nave", (14, WT + 1, CZ + 2), look_at=(APX, WT + 6, CZ))
    s.mark("cam_door", (0, G - 10, CZ), look_at=(NX0 + 8, G - 8, CZ))
    s.mark("eye_garden", (52, TOP + 2, CZ + 2), look_at=(18, TOP + 6, CZ))
    s.meta["mood"] = "dream"
    return finish(s, tier="grand", kind="sky", anchor=(32, TOP + 1, 32))
