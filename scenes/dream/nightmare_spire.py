"""Emerald Dream NIGHTMARE site: the Nightmare Spire (user #81: mega-hard PvE, Wardens, Exodia claim).

Statement: "A broken black tooth hanging in the dream: a sculk-rotted keep that gets WIDER as it climbs, three stacked
arenas twisting up its spine, crowned by a ring of claws around a red beam."
Mood: the Dream gone sick. Black/grey stone (blackstone, deepslate), sick teal (sculk, dark prismarine), crying-obsidian
violet as the feature (<5%), soul-blue light only, one warm sick note (shroomlight) in the summit braziers.
References: Barad-dur's top-heavy mass, Bloodborne's Cainhurst gate, inverted ziggurats, the Deep Dark.

Route: land on the gate court (south) -> great gate -> ARENA 1 (y31, 18 wide; vindicators + evokers) -> ramp east->north
through the ceiling -> ARENA 2 (y41, 24 wide; wither skeletons + breezes + a ravager) -> ramp west->south ->
ARENA 3 summit sanctum (y53, 30 wide; 2 wardens) -> dais: Exodia altar + beacon under a barred oculus.
Every window is barred; the roof is closed except the barred oculus (beam column), so there's no shortcut onto the altar.

Render: python -m tools.voxel render scenes/dream/nightmare_spire.py --mood dream   (or --mood night)
"""
import math

import numpy as np

from scenes.dream._dream import beacon, deposit, exodia_altar, finish, guard
from tools.voxel import noise
from tools.voxel.palette import Gradient, Mix, Noise
from tools.voxel.scene import Scene

W, H, D = 64, 96, 64
SEED = 6613
KX, KZ = 32.5, 28.5          # keep axis (cell 32, 28 is the centre column)
CXI, CZI = 32, 28
IX, IZ = 32.5, 35.0          # island centre
TOP = 30                     # island / court surface block y; arena 1 floor block

# tiers: (floor block y, first air y, last air y, outer inradius, wall thickness, rotation deg)
T1 = dict(f=30, a0=31, a1=38, R=11, t=2, rot=0.0)
T2 = dict(f=40, a0=41, a1=50, R=14, t=2, rot=15.0)
T3 = dict(f=52, a0=53, a1=62, R=17, t=2, rot=30.0)
ROOF0 = 63

# ------------------------------------------------------------------ materials (4 families: black stone, sick teal, violet, soul light)
WALL = Gradient("y", [
    (36, Noise([(-0.3, Mix({"deepslate_bricks": 3, "cracked_deepslate_bricks": 2, "deepslate_tiles": 1})),
                (1, Mix({"deepslate_bricks": 3, "deepslate_tiles": 2, "cracked_deepslate_tiles": 1}))], scale=5, seed=SEED)),
    (50, Noise([(-0.2, Mix({"deepslate_tiles": 2, "polished_blackstone_bricks": 2, "cracked_deepslate_tiles": 1})),
                (1, Mix({"polished_blackstone_bricks": 3, "deepslate_bricks": 1, "cracked_polished_blackstone_bricks": 1}))],
               scale=5, seed=SEED + 1)),
    (99, Noise([(-0.2, Mix({"polished_blackstone_bricks": 3, "cracked_polished_blackstone_bricks": 2})),
                (1, Mix({"polished_blackstone_bricks": 4, "blackstone": 1}))], scale=5, seed=SEED + 2)),
], jitter=2.5, jitter_scale=5, seed=SEED + 3)
TRIM = Mix({"polished_blackstone": 3, "polished_deepslate": 2})
TRIM_DARK = "polished_blackstone"
BAND = Mix({"dark_prismarine": 2, "prismarine_bricks": 2, "prismarine": 1})
ROOF = Noise([(-0.1, Mix({"deepslate_tiles": 3, "cracked_deepslate_tiles": 1})), (1, Mix({"blackstone": 2, "deepslate_tiles": 2}))],
             scale=4, seed=SEED + 4)
ROCK_TOP = Noise([(-0.35, "sculk"), (-0.05, Mix({"blackstone": 2, "deepslate": 2, "tuff": 1})),
                  (0.35, Mix({"deepslate": 3, "cobbled_deepslate": 1, "sculk": 1})), (1, Mix({"blackstone": 3, "basalt": 1}))],
                 scale=5, seed=SEED + 5)
ROCK = Gradient("y", [(8, Mix({"blackstone": 3, "basalt": 2, "crying_obsidian": 0.15})),
                      (18, Mix({"deepslate": 3, "blackstone": 2, "tuff": 1})),
                      (99, Mix({"deepslate": 3, "cobbled_deepslate": 2, "tuff": 1}))], jitter=3, jitter_scale=6, seed=SEED + 6)
PAVE = Noise([(-0.3, Mix({"polished_blackstone_bricks": 3, "cracked_polished_blackstone_bricks": 1})),
              (0.3, Mix({"deepslate_tiles": 3, "polished_deepslate": 1})),
              (1, Mix({"sculk": 2, "deepslate_tiles": 1}))], scale=4, seed=SEED + 7)


def grid():
    return np.meshgrid(np.arange(W) + 0.5, np.arange(H) + 0.5, np.arange(D) + 0.5, indexing="ij")


X, Y, Z = grid()
YI = np.arange(H)[None, :, None]


def octd(rot, x=None, z=None):
    """Octagon 'radius' (inradius metric) around the keep axis, rotated by rot degrees."""
    x = X if x is None else x
    z = Z if z is None else z
    a = math.radians(rot)
    dx, dz = x - KX, z - KZ
    u = dx * math.cos(a) + dz * math.sin(a)
    v = -dx * math.sin(a) + dz * math.cos(a)
    return np.maximum(np.maximum(np.abs(u), np.abs(v)), (np.abs(u) + np.abs(v)) / math.sqrt(2))


def theta():
    return np.degrees(np.arctan2(Z - KZ, X - KX))


RHO = np.hypot(X - KX, Z - KZ)
TH = theta()


# ------------------------------------------------------------------ island
def island(s):
    gx, gz = np.meshgrid(np.arange(W) + 0.5, np.arange(D) + 0.5, indexing="ij")
    ang = np.arctan2(gz - IZ, gx - IX)
    r = np.hypot(gx - IX, gz - IZ)
    # jagged coastline: sharp notches (ridged noise along the angle)
    jag = noise.ridged(np.cos(ang) * 6, np.sin(ang) * 6, 0.0, scale=1.6, octaves=2, seed=SEED)
    R = 24.0 * (0.82 + 0.28 * jag) + 2.0 * np.sin(5 * ang + 1.3)
    d = r / R
    inside = d < 1
    # top: flat at TOP over the court/keep, rocky teeth rising at the rim
    teeth = np.clip((d - 0.72) / 0.28, 0, 1) ** 1.5 * (2 + 6 * noise.ridged(gx, gz, 0.0, scale=5, octaves=2, seed=SEED + 1))
    top = TOP + np.where(d > 0.72, teeth, 0)
    # keep the south court + gate path flat (no teeth on the landing side), and the west bridge head
    court = (np.abs(gx - KX) < 12) & (gz > KZ + 8)
    top = np.where(court & (d < 0.97), TOP, top)
    top = np.where((gx < 22) & (np.abs(gz - 50) < 3), TOP, top)
    # underside: one big inverted fang plus lesser fangs
    fang = TOP - 2 - 27 * np.clip(1 - d, 0, 1) ** 1.25 * (0.75 + 0.35 * noise.fbm(gx, gz, 0.0, scale=7, octaves=2, seed=SEED + 2))
    for (fx, fz, fr, fd) in [(22, 24, 6, 12), (44, 42, 5, 10), (30, 48, 4, 8), (46, 20, 4, 9)]:
        fd2 = np.hypot(gx - fx, gz - fz) / fr
        fang = np.minimum(fang, np.where(fd2 < 1, TOP - 6 - fd * np.clip(1 - fd2, 0, 1) ** 0.7, 99))
    bot = np.maximum(fang, 1)
    m = inside[:, None, :] & (YI <= top[:, None, :]) & (YI >= bot[:, None, :])
    s.fill(m, ROCK)
    # surface skin
    surf = m & ~np.roll(m, -1, axis=1)
    s.fill(surf, ROCK_TOP)
    return inside, top


def shard(s, cx, cz, ty, r, depth, seed):
    gx, gz = np.meshgrid(np.arange(W) + 0.5, np.arange(D) + 0.5, indexing="ij")
    ang = np.arctan2(gz - cz, gx - cx)
    rr = np.hypot(gx - cx, gz - cz) / (r * (1 + 0.25 * np.sin(3 * ang + seed)))
    inside = rr < 1
    bot = ty - depth * np.clip(1 - rr, 0, 1) ** 0.6
    top = ty + np.where(rr > 0.6, 3 * noise.ridged(gx, gz, 0.0, scale=3, octaves=1, seed=seed), 0)
    m = inside[:, None, :] & (YI <= top[:, None, :]) & (YI >= bot[:, None, :])
    s.fill(m, ROCK)
    s.fill(m & ~np.roll(m, -1, axis=1), ROCK_TOP)


# ------------------------------------------------------------------ keep
def outer_R(y):
    """Outer inradius + rotation of the keep skin at height y: flares outward under each wider tier (corbelled funnels)."""
    if y <= 34:
        return T1["R"], T1["rot"]
    if y <= 39:
        return T1["R"] + (T2["R"] - T1["R"]) * (y - 34) / 5.0, T2["rot"]
    if y <= 46:
        return T2["R"], T2["rot"]
    if y <= 51:
        return T2["R"] + (T3["R"] - T2["R"]) * (y - 46) / 5.0, T3["rot"]
    if y <= 62:
        return T3["R"], T3["rot"]
    return None, T3["rot"]


def keep(s):
    solid = np.zeros(s.shape, bool)
    for y in range(T1["f"] - 3, ROOF0):
        R, rot = outer_R(y)
        d = octd(rot)[:, y, :]
        solid[:, y, :] = d <= R
    # roof: stepped octagonal pyramid
    for y in range(ROOF0, 78):
        R = T3["R"] - 1.5 * (y - ROOF0)
        if R <= 0.4:
            break
        solid[:, y, :] = octd(T3["rot"])[:, y, :] <= R
    s.fill(solid, WALL)
    # corner ribs (octagon corners): trim on the outer skin
    for rot, y0, y1, R, mat in [(T1["rot"], 27, 34, T1["R"], TRIM), (T2["rot"], 35, 46, T2["R"], TRIM),
                                (T3["rot"], 47, 62, T3["R"], "bone_block[axis=y]")]:
        a = math.radians(rot)
        dx, dz = X - KX, Z - KZ
        u = dx * math.cos(a) + dz * math.sin(a)
        v = -dx * math.sin(a) + dz * math.cos(a)
        corner = np.abs(np.abs(u) - np.abs(v)) < 2.2
        rib = solid & corner & (octd(rot) > R - 1.2) & (Y >= y0) & (Y < y1 + 1)
        s.fill(rib, mat)
    # lips: teal bands where each funnel meets the next tier, crying obsidian studs
    for y in (34, 40, 46, 52, 62):
        R, rot = outer_R(y)
        lip = (np.abs(Y - (y + 0.5)) < 0.5) & solid & (octd(rot) > R - 1.1)
        s.fill(lip, BAND)
    # roof edge trim + ridge
    s.fill(solid & (Y >= ROOF0) & (Y < ROOF0 + 1) & (octd(T3["rot"]) > T3["R"] - 1.2), TRIM_DARK)
    s.fill(solid & (Y >= ROOF0) & (np.abs(np.abs(X - KX) - np.abs(Z - KZ)) < 0.6), "polished_blackstone_bricks")
    return solid


def cornices(s):
    """Shadow lines between tiers: a projecting cornice (+1) on each lip with corbel teeth under it, every 2nd block."""
    for y, T in ((39, T2), (51, T3), (62, T3)):
        R, rot = T["R"], T["rot"]
        d = octd(rot)
        a = np.degrees(np.arctan2(Z - KZ, X - KX))
        per = (np.floor((a + 180) / 360 * (2 * math.pi * R) / 1.0) % 2 == 0)
        s.fill((YI == y) & (d > R - 0.5) & (d <= R + 1.0), Mix({"polished_blackstone": 2, "polished_deepslate": 1}))
        s.fill((YI == y - 1) & (d > R - 0.5) & (d <= R + 1.0) & per, "polished_blackstone_brick_wall")
        s.fill((YI == y + 1) & (d > R - 0.2) & (d <= R + 1.0) & per, "polished_blackstone_brick_slab[type=bottom]")


def turrets(s):
    """Eight corner turrets on the sanctum, spiked caps: they punctuate the roof line around the claws."""
    from scenes.concepts._kit import cone
    for k in range(8):
        a = math.radians(T3["rot"] + 22.5 + 45 * k)
        rr = T3["R"] / math.cos(math.radians(22.5)) - 0.5
        cx, cz = KX + rr * math.cos(a), KZ + rr * math.sin(a)
        y1 = 66 + (k % 2) * 3
        body = (np.hypot(X - cx, Z - cz) < 2.4) & (Y >= 47) & (Y < y1)
        s.fill(body, WALL)
        s.fill(body & (np.abs(Y - 58.5) < 0.5), BAND)
        s.fill(cone((cx, 0, cz), 2.9, y1, y1 + 8 + (k % 2) * 3).mask(s.shape), Mix({"blackstone": 2, "polished_blackstone": 1}))
        s.fill((np.hypot(X - cx, Z - cz) < 3.0) & (np.hypot(X - cx, Z - cz) >= 2.3) & (YI == y1), "polished_blackstone_brick_slab[type=bottom]")
        # corbel cone under the turret
        s.fill(cone((cx, 0, cz), 0.6, 42, 47, 2.4).mask(s.shape), TRIM)
        x, z = int(math.floor(cx)), int(math.floor(cz))
        s.fill(cone((cx, 0, cz), 1.4, y1 + 5 + (k % 2) * 2, y1 + 8 + (k % 2) * 3).mask(s.shape), "bone_block[axis=y]")


def facade_craft(s):
    """Pilasters (wall-block fins) flanking every face centre, hanging soul lanterns under the cornices, a slab plinth."""
    for T, y0, y1 in ((T1, 31, 34), (T2, 41, 46), (T3, 53, 61)):
        R, rot = T["R"], T["rot"]
        for k in range(8):
            a = math.radians(rot + 45 * k)
            nx, nz = math.cos(a), math.sin(a)
            tx, tz = -nz, nx
            for off in (-3.5, 3.5):
                x = int(math.floor(KX + (R + 0.5) * nx + off * tx))
                z = int(math.floor(KZ + (R + 0.5) * nz + off * tz))
                for y in range(y0, y1 + 1):
                    if s.get(x, y, z) == "minecraft:air":
                        s.set(x, y, z, "polished_blackstone_brick_wall")
                if s.get(x, y1 + 1, z) == "minecraft:air":
                    s.set(x, y1 + 1, z, "polished_blackstone_brick_slab[type=bottom]")
    # lanterns hanging off the cornices, at each face centre
    for y, R, rot in ((39, T2["R"], T2["rot"]), (51, T3["R"], T3["rot"]), (62, T3["R"], T3["rot"])):
        for k in range(8):
            a = math.radians(rot + 45 * k)
            x = int(math.floor(KX + (R + 0.6) * math.cos(a)))
            z = int(math.floor(KZ + (R + 0.6) * math.sin(a)))
            if s.get(x, y - 1, z) == "minecraft:air" and s.get(x, y - 2, z) == "minecraft:air":
                s.set(x, y - 1, z, "iron_chain[axis=y]")
                s.set(x, y - 2, z, "soul_lantern[hanging=true]")
    # plinth ring around arena 1
    d = octd(T1["rot"])
    s.fill((YI == TOP + 1) & (d > T1["R"] - 0.5) & (d <= T1["R"] + 1.0), "polished_blackstone_slab[type=bottom]", replace="air")


def banners(s):
    """Black banners on arena 1's west and east inner faces (south = gate, north = ramp)."""
    k = T1["R"] - T1["t"] - 1          # last air cell from the axis along a cardinal
    for (dx, dz, facing, offs) in [(-1, 0, "east", (0,)), (1, 0, "west", (-2, 2))]:   # north wall carries the ramp
        for off in offs:
            x = CXI + dx * k + (off if dz else 0)
            z = CZI + dz * k + (off if dx else 0)
            if s.get(x, 35, z) == "minecraft:cave_air":
                s.set(x, 35, z, f"black_wall_banner[facing={facing}]")
    # A2: cages with skull trophies against the outer ring, chains from the ceiling
    for ang in (335, 45, 68):
        a = math.radians(ang)
        x = int(math.floor(KX + 10.0 * math.cos(a)))
        z = int(math.floor(KZ + 10.0 * math.sin(a)))
        s.box((x - 1, T2["a0"], z - 1), (x + 1, T2["a0"] + 2, z + 1), "iron_bars", replace="cave_air")
        s.set(x, T2["a0"], z, "wither_skeleton_skull")
        s.set(x, T2["a0"] + 1, z, "cave_air")
        s.box((x - 1, T2["a0"] + 3, z - 1), (x + 1, T2["a0"] + 3, z + 1), "polished_blackstone_slab[type=bottom]", replace="cave_air")


def interiors(s):
    for T, ceil_top in [(T1, T2["f"]), (T2, T3["f"]), (T3, None)]:
        Ri = T["R"] - T["t"]
        d = octd(T["rot"])
        if ceil_top is None:
            # summit: stepped vault into the roof
            air = (d < Ri) & (Y >= T["a0"]) & (Y < T["a1"] + 1)
            for y in range(ROOF0, 72):
                air[:, y, :] |= d[:, y, :] < Ri - 1.6 * (y - T["a1"])
        else:
            air = (d < Ri) & (Y >= T["a0"]) & (Y < T["a1"] + 1)
        s.fill(air, "cave_air")
        # floor pattern: concentric octagon rings + a crying-obsidian star in arena 3
        fl = (d < Ri) & (np.abs(Y - (T["f"] + 0.5)) < 0.5)
        ring = (np.floor(d) % 4 == 0)
        s.fill(fl, PAVE)
        s.fill(fl & ring, "polished_deepslate")
        s.fill(fl & (np.floor(d) % 4 == 2) & (np.abs(np.abs(X - KX) - np.abs(Z - KZ)) < 0.7), "chiseled_polished_blackstone")


def ramp(s, T_from, T_to, th_start, sweep, r_in, r_out):
    """Helical slab ramp inside T_from, climbing (th decreasing) from its floor to T_to's floor; hole in the ceiling."""
    t = ((th_start - TH) % 360) / sweep
    band = (RHO >= r_in) & (RHO <= r_out) & (t <= 1.0)
    rise = T_to["f"] - T_from["f"]
    h = T_from["f"] + 0.5 + rise * np.clip(t, 0, 1)          # surface height (blocks, top)
    yb = np.floor(h)
    half = (h - yb) >= 0.5
    m_solid = band & (Y >= T_from["a0"]) & (Y < yb)
    m_slab = band & half & (YI == yb)
    # ceiling hole where the ramp surface comes within 3 of the ceiling
    hole = band & (h > T_from["a1"] - 2.5) & (Y >= T_from["a1"] + 1) & (Y <= T_to["f"] + 0.5) & (Y >= h + 0.0)
    s.fill(hole, "cave_air")
    s.fill(m_solid, Mix({"polished_blackstone_bricks": 3, "polished_deepslate": 1}))
    s.fill(m_slab, "polished_blackstone_brick_slab[type=bottom]")
    # parapet on the inner edge (low wall, broken by the start)
    edge = band & (RHO < r_in + 0.9) & (t > 0.15) & (YI == (yb + 1))
    s.fill(edge & ~m_slab, "polished_blackstone_brick_wall")
    # rail on the hole edge so you can't walk off into arena below by accident: chains hang there
    return band


def gate(s):
    """Great gate on the south face of arena 1: 3 nested arches (outer projecting portal is the densest element)."""
    zf = KZ + T1["R"]            # outer face plane of arena 1 (south)
    u = X - KX
    v_floor = Y - (TOP + 1)
    layers = [(6.5, 3.0, 9, WALL), (5.2, 2.0, 7.5, TRIM), (4.2, 1.0, 6.4, "crying_obsidian")]
    for hs, depth, spring, mat in layers:
        from scenes.concepts._kit import pointed_arch_2d
        frame = pointed_arch_2d(u, v_floor, hs + 1.6, spring, 1.0) & (Z > zf - 2) & (Z < zf + depth) & (Y >= TOP + 1)
        s.fill(frame, mat)
    from scenes.concepts._kit import pointed_arch_2d
    opening = pointed_arch_2d(u, v_floor, 3.2, 4.5, 1.0) & (Z > zf - 3) & (Z < zf + 4) & (Y >= TOP + 1)
    s.fill(opening, "cave_air")
    # portcullis teeth hanging in the arch top
    teeth = opening & (v_floor >= 4.5) & (np.floor(X) % 2 == 0) & (np.abs(Z - (zf + 0.5)) < 0.5)
    s.fill(teeth, "iron_bars")
    # flanking claw pillars with soul lanterns
    for sx in (-8, 8):
        x = CXI + sx
        z = int(zf) + 2
        s.box((x - 1, TOP + 1, z - 1), (x + 1, TOP + 2, z + 1), TRIM)
        s.box((x, TOP + 3, z), (x, TOP + 9, z), "polished_blackstone_wall")
        s.box((x - 1, TOP + 10, z - 1), (x + 1, TOP + 10, z + 1), "polished_blackstone_brick_slab[type=bottom]")
        s.set(x, TOP + 11, z, "crying_obsidian")
        s.set(x, TOP + 12, z, "polished_blackstone_wall")
        for dz in (-1, 1):
            s.set(x, TOP + 9, z + dz, "iron_chain[axis=y]")
            s.set(x, TOP + 8, z + dz, "soul_lantern[hanging=true]")
    # paving in front + steps down to the court
    return zf


def windows(s, solid):
    """Barred slits on arenas 1-2 (face centres), barred 'eye' rose windows on arena 3."""
    for T, ys, n in [(T1, (32, 36), 8), (T2, (42, 48), 8)]:
        a0 = T["rot"]
        for k in range(n):
            ang = math.radians(a0 + 45 * k)
            if T is T1 and k == 2:      # south face = gate
                continue
            for off in ((-1.6, 1.6) if T is T2 else (0,)):
                px = KX + (T["R"] - 1) * math.cos(ang) - off * math.sin(ang)
                pz = KZ + (T["R"] - 1) * math.sin(ang) + off * math.cos(ang)
                for rr in (-1.0, 0.0, 1.0):
                    x = int(math.floor(px + rr * math.cos(ang)))
                    z = int(math.floor(pz + rr * math.sin(ang)))
                    for y in range(ys[0], ys[1] + 1):
                        s.set(x, y, z, "iron_bars")
                x = int(math.floor(px + 1.6 * math.cos(ang)))
                z = int(math.floor(pz + 1.6 * math.sin(ang)))
                s.set(x, ys[0] - 1, z, "polished_blackstone_brick_slab[type=top]")
    # arena 3: four great eyes (bars ring, crying obsidian pupil) on the diagonal faces
    for k in range(4):
        ang = math.radians(T3["rot"] + 22.5 + 45 + 90 * k)
        ang = math.radians(T3["rot"] + 45 * (2 * k + 1))
        nx, nz = math.cos(ang), math.sin(ang)
        tx, tz = -nz, nx
        cy = 58.0
        for depth in (0.5, 1.5, 2.5):
            for a in np.arange(-3.5, 3.6, 0.5):
                for b in np.arange(-3.5, 3.6, 0.5):
                    rr = math.hypot(a, b)
                    if rr > 3.4:
                        continue
                    x = int(math.floor(KX + (T3["R"] - depth) * nx + a * tx))
                    z = int(math.floor(KZ + (T3["R"] - depth) * nz + a * tz))
                    y = int(math.floor(cy + b))
                    if depth > 2:
                        continue
                    if rr < 1.1:
                        s.set(x, y, z, "crying_obsidian" if depth < 1 else "cave_air")
                    elif rr < 2.6:
                        s.set(x, y, z, "iron_bars" if depth < 1 else "cave_air")
                    else:
                        s.set(x, y, z, "chiseled_polished_blackstone" if depth < 1 else "polished_blackstone")


def crown(s):
    """Eight claws rising off the roof rim, bending out then hooking in around the beam."""
    from scenes.concepts._kit import bezier, tube, union
    claws = []
    for k in range(8):
        a = math.radians(T3["rot"] + 22.5 + 45 * k)
        c, sn = math.cos(a), math.sin(a)
        hgt = 90 if k % 2 == 0 else 82
        pts = [(KX + 15.5 * c, ROOF0 - 1, KZ + 15.5 * sn), (KX + 20.5 * c, ROOF0 + 9, KZ + 20.5 * sn),
               (KX + 17.5 * c, hgt - 8, KZ + 17.5 * sn), (KX + 11.0 * c, hgt, KZ + 11.0 * sn)]
        claws += tube(bezier(pts, 18), 2.4, 0.5)
    m = union(claws).mask(s.shape)
    s.fill(m, Gradient("y", [(ROOF0 + 4, WALL), (ROOF0 + 9, Mix({"blackstone": 2, "bone_block[axis=y]": 1})),
                             (99, "bone_block[axis=y]")], jitter=2, jitter_scale=4, seed=SEED + 9))
    # crying-obsidian tips
    tips = m & (Y > 84)
    s.fill(tips & (Y > 87), "crying_obsidian")
    # chains + soul lanterns hanging off each claw's outer bend
    for k in range(8):
        a = math.radians(T3["rot"] + 22.5 + 45 * k)
        x = int(math.floor(KX + 21.5 * math.cos(a)))
        z = int(math.floor(KZ + 21.5 * math.sin(a)))
        ytop = ROOF0 + 6
        n = 5 + (k % 3) * 2
        for y in range(ytop - n, ytop):
            if s.get(x, y, z) in ("minecraft:air",):
                s.set(x, y, z, "iron_chain[axis=y]")
        if s.get(x, ytop - n - 1, z) == "minecraft:air":
            s.set(x, ytop - n - 1, z, "soul_lantern[hanging=true]")


def oculus_and_dais(s):
    """Summit: raised dais, the beacon on it, the Exodia altar before it, under a barred oculus."""
    top = T3["f"]
    d = np.hypot(X - KX, Z - KZ)
    s.fill((d < 6.6) & (YI == top + 1), Mix({"polished_blackstone_bricks": 3, "polished_deepslate": 1}))
    s.fill((d < 4.8) & (YI == top + 2), "polished_blackstone")
    s.fill((d < 6.6) & (d >= 5.6) & (YI == top + 1), "polished_blackstone_brick_slab[type=top]")
    s.fill((d < 6.6) & (d >= 5.6) & (YI == top + 1), "polished_blackstone_bricks")
    # crying obsidian star inlay in the arena floor (feature colour)
    star = (YI == top) & (d > 7) & (d < 13.5) & (np.abs(np.abs(X - KX) - np.abs(Z - KZ)) < 0.6)
    s.fill(star, "crying_obsidian")
    # oculus: open column above the dais, barred
    ocu = (d < 3.6) & (Y >= ROOF0 - 1)
    s.fill(ocu, "cave_air")
    s.fill((d < 3.6) & (YI == 72), "iron_bars")
    s.fill((d < 4.6) & (d >= 3.6) & (YI == 73), "polished_blackstone_wall")
    # beacon at the centre, altar on its south side
    beacon(s, CXI, top + 3, CZI, glass="red_stained_glass", base="crying_obsidian")
    exodia_altar(s, CXI, top + 3, CZI + 3)
    s.set(CXI, top + 3, CZI + 2, "air")
    # black candles + soul campfires at the dais corners
    for k in range(4):
        a = math.radians(45 + 90 * k)
        x = int(math.floor(KX + 5.2 * math.cos(a)))
        z = int(math.floor(KZ + 5.2 * math.sin(a)))
        s.set(x, top + 2, z, "polished_blackstone_wall")
        s.set(x, top + 3, z, "soul_campfire[lit=true]")
    for (dx, dz) in [(-2, 4), (2, 4), (-3, 2), (3, 2)]:
        s.set(CXI + dx, top + 3, CZI + dz, "black_candle[candles=3,lit=true]")


def pillars(s):
    """Arena 3: ring of 8 piers (2x2) carrying the vault; arena 2: broken columns."""
    for k in range(8):
        a = math.radians(T3["rot"] + 22.5 + 45 * k)
        x = int(math.floor(KX + 11.5 * math.cos(a)))
        z = int(math.floor(KZ + 11.5 * math.sin(a)))
        s.box((x, T3["a0"], z), (x + 1, 70, z + 1), TRIM, replace="cave_air")
        s.box((x, T3["a0"], z), (x + 1, T3["a0"], z + 1), "chiseled_polished_blackstone")
        # sconce: chain + soul lantern hanging off the inner face
    for k in range(8):
        a = math.radians(T2["rot"] + 45 * k + 22.5)
        x = int(math.floor(KX + 8.5 * math.cos(a)))
        z = int(math.floor(KZ + 8.5 * math.sin(a)))
        if k in (5, 6):   # keep the A1->A2 arrival clear
            continue
        hgt = 2 + (k * 3) % 6
        s.box((x, T2["a0"], z), (x, T2["a0"] + hgt, z), "polished_blackstone_wall" if hgt < 4 else TRIM, replace="cave_air")
        s.set(x, T2["a0"] + hgt + 1, z, "wither_skeleton_skull" if k % 2 else "skeleton_skull")


def hang_lanterns(s):
    """Chains + soul lanterns from each arena ceiling (designed fixtures, ring layout)."""
    for T, r, n, length in [(T1, 5.5, 6, 3), (T2, 8.0, 8, 4), (T3, 8.5, 8, 6)]:
        top = T["a1"]
        for k in range(n):
            a = math.radians(T["rot"] + 360 / n * k + 10)
            x = int(math.floor(KX + r * math.cos(a)))
            z = int(math.floor(KZ + r * math.sin(a)))
            # find the ceiling above
            yc = top + 1
            while yc < H - 1 and s.get(x, yc, z) == "minecraft:cave_air":
                yc += 1
            if s.get(x, yc, z) in ("minecraft:cave_air", "minecraft:air"):
                continue
            for y in range(yc - length, yc):
                if s.get(x, y, z) == "minecraft:cave_air":
                    s.set(x, y, z, "iron_chain[axis=y]")
            if s.get(x, yc - length - 1, z) == "minecraft:cave_air":
                s.set(x, yc - length - 1, z, "soul_lantern[hanging=true]")


def props(s):
    """Furnish each arena by its job: a guardroom (A1), a killing pit (A2), the sanctum (A3)."""
    f1 = T1["a0"]
    # A1: weapon/skull clusters by the walls, bone piles, two hanging cages, braziers
    for (x, z) in [(26, 24), (39, 33), (25, 32)]:
        s.set(x, f1, z, "bone_block[axis=x]")
        s.set(x + 1, f1, z, "skeleton_skull")
        s.set(x, f1 + 1, z, "skeleton_skull")
        s.set(x, f1, z + 1, "cobweb")
    for (x, z) in [(27, 34), (38, 34)]:
        s.box((x - 1, f1, z - 1), (x + 1, f1, z + 1), "polished_blackstone_brick_wall")
        s.set(x, f1, z, "soul_soil")
        s.set(x, f1 + 1, z, "soul_fire")
    for (x, z) in [(25, 25), (25, 31)]:
        s.box((x - 1, 35, z - 1), (x + 1, 37, z + 1), "iron_bars")
        s.box((x, 36, z), (x, 36, z), "cave_air")
        s.box((x - 1, 34, z - 1), (x + 1, 34, z + 1), "polished_blackstone_slab[type=top]")
        s.set(x, 38, z, "iron_chain[axis=y]")
        s.set(x, 35, z, "skeleton_skull")
    # A2: soul-fire pits in a ring, bones
    f2 = T2["a0"]
    for k in range(4):
        a = math.radians(T2["rot"] + 90 * k + 45)
        x = int(math.floor(KX + 5 * math.cos(a)))
        z = int(math.floor(KZ + 5 * math.sin(a)))
        s.set(x, f2 - 1, z, "soul_soil")
        s.set(x, f2, z, "soul_fire")
        s.set(x + 1, f2, z, "bone_block[axis=z]")
        s.set(x, f2, z + 1, "wither_skeleton_skull")
    # sculk catalysts (glow) by the sanctum walls
    for k in range(8):
        a = math.radians(T3["rot"] + 45 * k)
        x = int(math.floor(KX + 13.2 * math.cos(a)))
        z = int(math.floor(KZ + 13.2 * math.sin(a)))
        s.set(x, T3["a0"], z, "sculk_catalyst")


def sculk_rot(s):
    """Sculk creeping up from the island over the lower keep and onto floors (by noise)."""
    n = noise.fbm(X, Y * 0.7, Z, scale=6, octaves=2, seed=SEED + 11) if hasattr(noise, "fbm") else 0
    mask_names = ("deepslate_bricks", "cracked_deepslate_bricks", "deepslate_tiles", "cracked_deepslate_tiles",
                  "polished_blackstone_bricks", "cracked_polished_blackstone_bricks", "blackstone", "deepslate",
                  "cobbled_deepslate", "tuff")
    m = np.zeros(s.shape, bool)
    for nm in mask_names:
        m |= s.match(nm)
    above_air = np.roll(s.idx == 0, -1, axis=1) | np.roll(s.match("cave_air"), -1, axis=1)
    reach = 40 - 9 * (Y - TOP) / 30.0
    rot = m & (n > 0.25 + (Y - TOP) / 40.0) & (Y < 50)
    s.fill(rot & (above_air | (Y < TOP + 12)), "sculk")


def court(s, inside, top):
    """Gate court (landing): flat paving, guard obelisks, a straight processional path, broken wall stubs."""
    gx, gz = np.meshgrid(np.arange(W) + 0.5, np.arange(D) + 0.5, indexing="ij")
    area = inside & (np.abs(gx - KX) < 13) & (gz > KZ + 11) & (gz < 61)
    m = area[:, None, :] & (YI == TOP)
    s.fill(m, PAVE)
    path = area[:, None, :] & (YI == TOP) & (np.abs(X - KX) < 2.6)
    s.fill(path, Noise([(0, "polished_blackstone_bricks"), (1, "polished_deepslate")], scale=3, seed=SEED + 12))
    s.fill(area[:, None, :] & (YI == TOP) & (np.abs(np.abs(X - KX) - 2.5) < 0.5), "chiseled_polished_blackstone")
    # clear anything above the court
    s.fill(area[:, None, :] & (Y > TOP + 0.5) & (Y < TOP + 14) & (Z > KZ + T1["R"] + 3.5), "air")
    # obelisks (spike + soul lantern) lining the path
    for z in (45, 51, 57):
        for sx in (-6, 6):
            x = CXI + sx
            if not inside[x, z]:
                continue
            h = 5 if z != 57 else 4
            s.box((x, TOP + 1, z), (x, TOP + h, z), "polished_blackstone_bricks")
            s.set(x, TOP + h + 1, z, "polished_blackstone_wall")
            s.set(x, TOP + h + 2, z, "polished_blackstone_wall")
            s.set(x, TOP + 1, z + 1, "soul_lantern")
    # broken curtain wall stubs at the court edge (silhouette + cover)
    for (x0, x1, z, h) in [(19, 22, 55, 3), (43, 46, 56, 4), (20, 21, 47, 5), (44, 45, 46, 2)]:
        for x in range(x0, x1 + 1):
            if inside[x, z]:
                hh = h - (x - x0) % 2
                s.box((x, TOP + 1, z), (x, TOP + hh, z), WALL)


def bridge(s):
    """Broken bridge from the court's west edge to a floating shard; the span snapped in the middle."""
    shard(s, 6.0, 50.0, TOP - 2, 5.5, 9, SEED + 20)
    for x in range(3, 22):
        if 11 <= x <= 13:
            continue     # the break
        for z in (49, 50, 51):
            if s.get(x, TOP, z) == "minecraft:air":
                s.set(x, TOP, z, "polished_blackstone_bricks" if z == 50 else "polished_blackstone_brick_slab[type=top]")
        if x % 3 == 0 and x not in (12,):
            for z in (48, 52):
                if s.get(x, TOP + 1, z) == "minecraft:air":
                    s.set(x, TOP + 1, z, "polished_blackstone_brick_wall")
    # ragged break ends + a dangling chain
    s.set(14, TOP - 1, 50, "cracked_polished_blackstone_bricks")
    s.set(10, TOP - 1, 50, "cracked_polished_blackstone_bricks")
    for y in range(TOP - 6, TOP):
        s.set(10, y, 49, "iron_chain[axis=y]")
    # arch supports under the bridge
    for x in (17, 20):
        for y in range(TOP - 5, TOP):
            for z in (49, 51):
                if s.get(x, y, z) == "minecraft:air":
                    s.set(x, y, z, "polished_blackstone_brick_wall")


def underside(s):
    """Chains + lanterns hanging from the fangs."""
    rng = np.random.default_rng(SEED + 30)
    for _ in range(14):
        x = int(rng.integers(12, 54)); z = int(rng.integers(14, 56))
        col = s.idx[x, :TOP, z]
        nz = np.nonzero(col)[0]
        if not len(nz):
            continue
        yb = int(nz.min())
        if yb < 6:
            continue
        n = int(rng.integers(3, 7))
        for y in range(yb - n, yb):
            s.set(x, y, z, "iron_chain[axis=y]")
        s.set(x, yb - n - 1, z, "soul_lantern[hanging=true]")


def guards(s):
    a1 = T1["a0"]; a2 = T2["a0"]; a3 = T3["a0"]
    # arena 1: 4 vindicators mid-room, 3 evokers at the back (north)
    for (x, z) in [(29, 31), (36, 31), (28, 27), (37, 27)]:
        guard(s, x, a1, z, "vindicator")
    for (x, z) in [(31, 25), (28, 24), (34, 25)]:
        guard(s, x, a1, z, "evoker")
    # arena 2: 3 wither skeletons, 3 breezes, 1 ravager in the middle
    for (x, z) in [(26, 26), (39, 26), (32, 35)]:
        guard(s, x, a2, z, "wither_skeleton")
    for (x, z) in [(27, 33), (38, 33), (32, 20)]:
        guard(s, x, a2, z, "breeze")
    guard(s, 32, a2, 28, "ravager")
    # arena 3: two wardens flanking the dais
    guard(s, 23, a3, 28, "warden")
    guard(s, 42, a3, 28, "warden")


def deposits(s):
    """Ore seams (tuff host) where a fighter can reach them: the first wall/rock cell hit walking outward from a floor,
    at shoulder height; arena walls (away from ramps and the gate), the court's rock teeth and the bridge shard."""
    def cast(x0, z0, y, ang, r0=0.5, rmax=40, natural=False):
        for r in np.arange(r0, rmax, 0.5):
            x = int(math.floor(x0 + r * math.cos(math.radians(ang))))
            z = int(math.floor(z0 + r * math.sin(math.radians(ang))))
            if not (0 <= x < W and 0 <= z < D):
                return None
            if s.get(x, y, z) not in ("minecraft:cave_air", "minecraft:air"):
                n = s.get(x, y, z)
                ok = any(k in n for k in ("deepslate", "blackstone", "tuff", "basalt", "sculk"))
                if natural and ("polished" in n or "brick" in n or "tiles" in n):
                    ok = False
                return (x, y, z) if ok else None
        return None
    plan = [(KX, KZ, T1["a0"] + 1, 120, 3), (KX, KZ, T1["a0"] + 1, 240, 3),                  # arena 1
            (KX, KZ, T2["a0"] + 1, 300, 4), (KX, KZ, T2["a0"] + 1, 12, 4),                    # arena 2
            (KX, KZ, T3["a0"] + 1, 160, 7), (KX, KZ, T3["a0"] + 1, 340, 7), (KX, KZ, T3["a0"] + 1, 250, 7)]   # arena 3
    n = 0
    for (x0, z0, y, a, r0) in plan:
        c = cast(x0, z0, y, a, r0)
        if c:
            deposit(s, *c, host="tuff")
            n += 1
    got = 0
    for (z0, a) in [(50.0, 0), (56.0, 160), (46.0, 200), (54.0, 30), (52.0, 150), (47.0, 340)]:   # court rock teeth
        c = cast(KX, z0, TOP + 1, a, 3, natural=True)
        if c and got < 3:
            deposit(s, *c, host="tuff")
            got += 1
    n += got
    deposit(s, 6, TOP - 1, 50, host="tuff")       # bridge shard (top)
    s.meta["deposits"] = n + 1


def build():
    s = Scene((W, H, D), name="nightmare_spire", seed=SEED)
    inside, top = island(s)
    court(s, inside, top)
    solid = keep(s)
    cornices(s)
    turrets(s)
    facade_craft(s)
    interiors(s)
    ramp(s, T1, T2, th_start=10.0, sweep=115.0, r_in=5.4, r_out=9.4)
    ramp(s, T2, T3, th_start=200.0, sweep=115.0, r_in=8.0, r_out=12.4)
    gate(s)
    windows(s, solid)
    crown(s)
    pillars(s)
    oculus_and_dais(s)
    props(s)
    hang_lanterns(s)
    banners(s)
    bridge(s)
    underside(s)
    sculk_rot(s)
    guards(s)
    deposits(s)
    s.mark("cam_approach", (CXI, TOP + 1, 60), look_at=(KX, 45, KZ))
    s.mark("cam_arena3", (CXI + 1, T3["a0"], CZI + 12), look_at=(KX, 57, KZ))
    s.mark("cam_arena1", (CXI, T1["a0"], CZI + 8), look_at=(KX, 34, KZ - 6))
    return finish(s, tier="nightmare", kind="sky", anchor=(CXI, TOP + 1, CZI + 12))
