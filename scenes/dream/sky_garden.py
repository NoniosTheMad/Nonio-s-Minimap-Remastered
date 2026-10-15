"""MAJOR site: THE TEA GARDEN IN THE SKY.

Statement: a floating meadow where the flowers grew taller than the trees: five giant blossoms on verdigris stems lean
over a little copper-domed tea pavilion, the table still laid, candles lit. A pond, a red toadstool the size of a
house, stepping stones to every edge. Underneath, the island's taproot trails roots, glow berries and spore blossoms.
The beam rises from a moss knoll on the west side.

Render: python -m tools.voxel render scenes/dream/sky_garden.py --mood dream
"""
import math

import numpy as np

from scenes.dream._dream import (GLOW_PEARL, GLOW_WARM, beacon, deposit, finish, island, loot_chest)
from tools.voxel import noise
from tools.voxel.palette import Gradient, Mix, Noise
from tools.voxel.scene import Scene

W, H, D = 41, 84, 41
CX, CZ = 20, 20
TOP = 42                # island turf level
SEED = 9091
AIR = ("minecraft:air", "minecraft:cave_air")


def is_air(s, x, y, z):
    return 0 <= x < W and 0 <= y < H and 0 <= z < D and s.get(x, y, z) in AIR


def bez(p0, p1, p2, n):
    p0, p1, p2 = (np.array(p, float) for p in (p0, p1, p2))
    return [(1 - u) ** 2 * p0 + 2 * (1 - u) * u * p1 + u * u * p2 for u in np.linspace(0, 1, n)]


def stem(s, base, ctrl, head, spec, r=0.5):
    pts = bez(base, ctrl, head, 40)
    for a, b in zip(pts, pts[1:]):
        s.line(tuple(a), tuple(b), spec, radius=r)
    return pts


def blossom(s, c, normal, R, petal_spec, heart_spec, k=5, cup=0.25, seed=0):
    """Flower head: a disc of k petals (cupped upward by `cup`), around a glowing heart."""
    c = np.array(c, float)
    n = np.array(normal, float); n /= np.linalg.norm(n)
    a = np.cross(n, [0, 0, 1.0]) if abs(n[2]) < 0.9 else np.cross(n, [1.0, 0, 0])
    a /= np.linalg.norm(a); b = np.cross(n, a)
    ri = int(R + 3)
    x0, y0, z0 = (int(v) - ri for v in c)
    xs, ys, zs = np.meshgrid(np.arange(x0, x0 + 2 * ri + 1), np.arange(y0, y0 + 2 * ri + 1),
                             np.arange(z0, z0 + 2 * ri + 1), indexing="ij")
    v = np.stack([xs - c[0], ys - c[1], zs - c[2]], -1)
    h = v @ n
    pa, pb = v @ a, v @ b
    rr = np.hypot(pa, pb)
    phi = np.arctan2(pb, pa) + seed
    shape = R * (0.55 + 0.45 * np.abs(np.cos(phi * k / 2)) ** 0.7)
    surf = cup * (rr ** 2) / R          # petals curl up toward the rim
    petal = (rr < shape) & (np.abs(h - surf) < 0.62)
    heart = (rr < max(1.2, R * 0.22)) & (h > -0.7) & (h < 1.3)
    ok = (xs >= 0) & (xs < W) & (ys >= 0) & (ys < H) & (zs >= 0) & (zs < D)
    m = np.zeros(s.shape, bool)
    sel = petal & ok
    m[xs[sel], ys[sel], zs[sel]] = True
    edge = np.zeros(s.shape, bool)
    se = petal & ok & (rr > shape - 1.2)
    edge[xs[se], ys[se], zs[se]] = True
    s.fill(m & ~edge, petal_spec[0])
    s.fill(edge, petal_spec[1])
    m2 = np.zeros(s.shape, bool)
    sel = heart & ok
    m2[xs[sel], ys[sel], zs[sel]] = True
    s.fill(m2, heart_spec)


def build():
    s = Scene((W, H, D), name="sky_garden", seed=SEED)
    gx, gy, gz = np.meshgrid(np.arange(W), np.arange(H), np.arange(D), indexing="ij")

    # ---------------------------------------------------------------- the island + a second, smaller lobe (figure-8)
    island(s, CX, TOP, CZ, 18.5, 30, seed=SEED)
    island(s, CX - 10, TOP - 1, CZ + 10, 8.5, 14, seed=SEED + 1)
    # a few satellite rocks drifting below the rim
    for (x, y, z, r, d) in ((5, TOP - 9, 6, 3.2, 5), (35, TOP - 14, 30, 2.6, 4), (34, TOP - 4, 5, 2.2, 3)):
        island(s, x, y, z, r, d, seed=SEED + x)

    # the taproot: a long tapering rock cone under the island, ending in a hanging crystal (far-read from below)
    for y in range(TOP - 6, TOP - 34, -1):
        u = (TOP - 6 - y) / 28
        r = 12.5 * (1 - u) ** 1.1 + 0.4
        ox = 2.0 * math.sin(u * 2.4)
        oz = 1.5 * math.cos(u * 1.7)
        rr_ = np.hypot(gx - CX - ox, gz - CZ - oz) / (1 + 0.15 * np.sin(5 * np.arctan2(gz - CZ, gx - CX) + y * 0.3))
        s.fill((gy == y) & (rr_ < r), Mix({"calcite": 4, "stone": 2, "amethyst_block": 1, "tuff": 1}, seed=y), replace="air")
    tip = (CX + 2, TOP - 34, CZ + 1)
    for k in range(7):
        rr = 1.6 * (1 - k / 7) + 0.3
        s.fill((gy == tip[1] - k) & (np.hypot(gx - tip[0], gz - tip[2]) < rr), "verdant_froglight" if k < 3 and rr > 1 else "lime_stained_glass")

    # moss knoll (west) for the beacon
    kx, kz = CX - 11, CZ - 3
    for y in range(TOP + 1, TOP + 5):
        rr = 5.5 - (y - TOP) * 1.2
        s.fill((gy == y) & (np.hypot(gx - kx, gz - kz) < rr), Mix({"moss_block": 3, "calcite": 1, "mossy_cobblestone": 1}, seed=y))
    beacon(s, kx, TOP + 5, kz)
    for dx, dz in ((-2, 0), (2, 0), (0, -2), (0, 2)):
        s.set(kx + dx, TOP + 4, kz + dz, "moss_block")
        s.set(kx + dx, TOP + 5, kz + dz, "moss_carpet")
    for dx, dz in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
        s.set(kx + dx, TOP + 4, kz + dz, "moss_block")
        s.set(kx + dx, TOP + 5, kz + dz, "waxed_oxidized_copper_lantern[hanging=false]")

    # ---------------------------------------------------------------- pond (south-east), organic edge
    px, pz = CX + 7, CZ + 9
    pr = np.hypot((gx - px) / 4.6, (gz - pz) / 3.4) + 0.18 * noise.fbm(gx, gy * 0, gz, 3, 2, seed=SEED)
    pond = pr < 1
    s.fill(pond & (gy == TOP), "water")
    s.fill(pond & (gy == TOP - 1), Mix({"clay": 2, "moss_block": 1}, seed=SEED))
    s.fill((pr >= 1) & (pr < 1.25) & (gy == TOP), Mix({"mud_bricks": 1, "calcite": 2, "moss_block": 2}, seed=SEED + 3))
    for (x, z) in ((px - 2, pz), (px + 1, pz - 1), (px + 2, pz + 1)):
        if s.get(x, TOP, z) == "minecraft:water":
            s.set(x, TOP + 1, z, "lily_pad")

    # ---------------------------------------------------------------- the tea pavilion (centre-east)
    tx, tz, TR = CX + 4, CZ - 4, 4.6
    trr = np.hypot(gx - tx, gz - tz)
    s.fill((gy == TOP) & (trr < TR + 0.5), "smooth_quartz")
    s.fill((gy == TOP + 1) & (trr < TR), Noise([(0, "polished_diorite"), (1, "calcite")], scale=2, seed=SEED))
    # floor pattern: a verdigris ring + quartz rosette
    s.fill((gy == TOP + 1) & (np.abs(trr - 2.6) < 0.5), "waxed_oxidized_cut_copper")
    s.fill((gy == TOP + 1) & (trr < 1.2), "chiseled_quartz_block")
    s.fill((gy == TOP + 1) & (np.abs(trr - TR - 0.2) < 0.55) & (s.idx == 0), "smooth_quartz_slab[type=bottom]")
    pillars = []
    for k in range(6):
        a = k * math.pi / 3 + math.pi / 6
        x, z = int(round(tx + 3.7 * math.cos(a))), int(round(tz + 3.7 * math.sin(a)))
        pillars.append((x, z))
        for y in range(TOP + 2, TOP + 7):
            s.set(x, y, z, "quartz_pillar[axis=y]")
        s.set(x, TOP + 2, z, "smooth_quartz")
        s.set(x, TOP + 7, z, "chiseled_quartz_block")
    # dome: verdigris onion dome
    ys0 = TOP + 7
    for y in range(ys0, ys0 + 9):
        u = (y - ys0) / 8.0
        r = 5.1 * math.sin(math.pi * (0.5 + 0.5 * u)) ** 0.8 + 0.4 * math.sin(math.pi * u * 1.6) if u < 1 else 0
        r = max(r, 0.0)
        shell = (gy == y) & (trr < r + 0.5) & (trr >= r - 0.7)
        if y == ys0:
            shell = (gy == y) & (trr < 5.4)
        s.fill(shell, Mix({"waxed_oxidized_cut_copper": 4, "waxed_oxidized_copper": 1}, seed=y))
        s.fill((gy == y) & (trr < r - 0.7) & (y > ys0), "cave_air")
    # eave: slabs around the dome base + hanging lanterns
    s.fill((gy == ys0) & (np.abs(trr - 5.9) < 0.55) & (s.idx == 0), "waxed_oxidized_cut_copper_slab[type=top]")
    for (x, z) in pillars:
        ox, oz = x + int(np.sign(x - tx)), z + int(np.sign(z - tz))
        if s.get(ox, ys0, oz) != "minecraft:air":
            s.set(ox, ys0 - 1, oz, "lantern[hanging=true]")
    # finial
    s.set(tx, ys0 + 9, tz, "waxed_oxidized_lightning_rod[facing=up]")
    s.set(tx, ys0 + 8, tz, "waxed_oxidized_cut_copper")
    # interior: carved air, ceiling lamp, the tea table and chairs
    s.fill((gy > TOP + 1) & (gy < ys0) & (trr < 3.4), "cave_air")
    s.fill((gy == ys0) & (trr < 3.8), "cave_air")
    s.set(tx, ys0 + 2, tz, GLOW_WARM)
    for y in range(ys0 - 1, ys0 + 2):
        s.set(tx, y, tz, "waxed_oxidized_copper_chain[axis=y]")
    s.set(tx, ys0 - 2, tz, "lantern[hanging=true]")
    s.set(tx, TOP + 2, tz, "dark_oak_fence")
    s.set(tx, TOP + 3, tz, "white_carpet")
    s.set(tx + 1, TOP + 2, tz, "dark_oak_trapdoor[facing=east,half=top,open=false]")
    s.set(tx - 1, TOP + 2, tz, "dark_oak_trapdoor[facing=west,half=top,open=false]")
    s.set(tx, TOP + 2, tz + 1, "dark_oak_trapdoor[facing=south,half=top,open=false]")
    s.set(tx, TOP + 2, tz - 1, "dark_oak_trapdoor[facing=north,half=top,open=false]")
    s.set(tx + 1, TOP + 3, tz, "white_candle[candles=3,lit=true]")
    s.set(tx - 1, TOP + 3, tz, "potted_torchflower")
    s.set(tx, TOP + 3, tz + 1, "pink_candle[candles=2,lit=true]")
    s.set(tx, TOP + 3, tz - 1, "decorated_pot[facing=south]")
    for (dx, dz, f) in ((2, 0, "west"), (-2, 0, "east"), (0, 2, "north"), (0, -2, "south")):
        s.set(tx + dx, TOP + 2, tz + dz, f"cherry_stairs[facing={f},half=bottom]")
    # the loot: a chest against the back (north-east) pillar, between two potted azaleas
    lx, lz = tx + 2, tz - 2
    loot_chest(s, lx, TOP + 2, lz, "major", facing="south")
    s.set(lx - 1, TOP + 2, lz, "potted_flowering_azalea_bush")
    if is_air(s, lx + 1, TOP + 2, lz + 1):
        s.set(lx + 1, TOP + 2, lz + 1, "potted_azalea_bush")

    # ---------------------------------------------------------------- giant flowers
    PETALS = [
        (("pink_wool", "magenta_wool"), GLOW_WARM),
        (("white_wool", "pink_wool"), GLOW_WARM),
        (("light_blue_wool", "white_wool"), GLOW_PEARL),
        (("yellow_terracotta", "orange_terracotta"), GLOW_WARM),
        (("magenta_wool", "purple_wool"), GLOW_PEARL),
    ]
    STEM = Mix({"waxed_oxidized_copper": 3, "waxed_weathered_copper": 1, "moss_block": 1}, seed=SEED)
    flowers = [  # base, ctrl, head, normal, R, petals, k
        ((CX - 3, TOP + 1, CZ + 2), (CX - 6, TOP + 18, CZ + 6), (CX - 2, TOP + 33, CZ + 3), (0.25, 1, -0.15), 7.5, 0, 5),
        ((CX + 10, TOP + 1, CZ + 3), (CX + 12, TOP + 10, CZ + 2), (CX + 13, TOP + 18, CZ + 7), (0.4, 1, 0.3), 5.0, 1, 6),
        ((CX - 7, TOP + 1, CZ - 10), (CX - 9, TOP + 9, CZ - 13), (CX - 5, TOP + 16, CZ - 14), (-0.1, 1, -0.45), 4.5, 2, 5),
        ((CX - 12, TOP, CZ + 11), (CX - 14, TOP + 6, CZ + 12), (CX - 13, TOP + 11, CZ + 15), (-0.4, 1, 0.4), 3.6, 3, 7),
        ((CX + 9, TOP + 1, CZ - 12), (CX + 12, TOP + 8, CZ - 13), (CX + 14, TOP + 13, CZ - 10), (0.5, 1, -0.2), 3.8, 4, 5),
    ]
    for i, (b, c, h, n, R, pi, k) in enumerate(flowers):
        pts = stem(s, b, c, h, STEM, r=0.75 if i == 0 else 0.5)
        blossom(s, h, n, R, PETALS[pi][0], PETALS[pi][1], k=k, seed=i * 0.7)
        # leaf blades: broad two-lobed leaves off the stem at 35% / 60%
        for j, u in enumerate((0.35, 0.62)):
            p = pts[int(u * (len(pts) - 1))]
            ang = i * 1.9 + j * 2.6
            off = np.array([math.cos(ang), 0.0, math.sin(ang)])
            cen = p + off * (2.2 + R * 0.25) + np.array([0, 0.6, 0])
            s.line(tuple(p), tuple(cen), STEM, radius=0.5)
            blossom(s, tuple(cen), tuple(off * 0.5 + np.array([0, 1, 0])), 2.2 + R * 0.18,
                    ("azalea_leaves", "moss_block"), "azalea_leaves", k=2, cup=0.35, seed=ang)
        # a few hanging copper lanterns under the biggest heads
        if R >= 4.5:
            hx, hy, hz = (int(round(v)) for v in h)
            for (dx, dz) in ((2, 1), (-2, -1)):
                x, z = hx + dx, hz + dz
                y = hy - 1
                while y > hy - 4 and not is_air(s, x, y, z):
                    y -= 1
                if is_air(s, x, y, z) and not is_air(s, x, y + 1, z):
                    s.set(x, y, z, "waxed_oxidized_copper_chain[axis=y]")
                    s.set(x, y - 1, z, "waxed_oxidized_copper_lantern[hanging=true]")

    # ---------------------------------------------------------------- the toadstool (north-west)
    mx, mz = CX - 4, CZ - 2
    for y in range(TOP + 1, TOP + 9):
        s.fill((gy == y) & (np.hypot(gx - mx, gz - mz) < 1.6 + 0.15 * (TOP + 9 - y) / 3), "mushroom_stem")
    for y in range(TOP + 8, TOP + 13):
        u = (y - TOP - 8) / 4
        r = 6.2 * math.sqrt(max(0.0, 1 - u * u)) + 0.3
        cap = (gy == y) & (np.hypot(gx - mx, gz - mz) < r)
        inner = (gy == y) & (np.hypot(gx - mx, gz - mz) < r - 1.2) & (y < TOP + 12)
        s.fill(cap & ~inner, "red_mushroom_block")
        s.fill(inner, "cave_air")
    spots = s.match("red_mushroom_block") & (noise.hash01(gx, gy, gz, seed=SEED + 8) < 0.13)
    s.fill(spots, "white_wool")
    s.fill((gy == TOP + 8) & (np.abs(np.hypot(gx - mx, gz - mz) - 4.0) < 0.5), "shroomlight")
    s.fill((gy == TOP + 8) & (np.hypot(gx - mx, gz - mz) < 5.8) & (np.hypot(gx - mx, gz - mz) > 1.9) & s.match("air"),
           "mushroom_stem")

    # ---------------------------------------------------------------- stepping-stone paths: edges -> pavilion
    rng = np.random.default_rng(SEED)
    for ang in (math.pi * 0.5, math.pi * 1.0, math.pi * 1.55, 0.05):
        for d in np.arange(4.5, 17.5, 1.6):
            x = int(round(tx + d * math.cos(ang) + rng.uniform(-0.6, 0.6)))
            z = int(round(tz + d * math.sin(ang) + rng.uniform(-0.6, 0.6)))
            if 0 <= x < W and 0 <= z < D and s.get(x, TOP, z) in ("minecraft:grass_block", "minecraft:moss_block"):
                s.set(x, TOP, z, "calcite" if (x + z) % 3 else "polished_diorite")

    # ---------------------------------------------------------------- rock edge + deposits (the garden's mining)
    dep_pts = []
    for k in range(7):
        a = k * 2 * math.pi / 7 + 0.4
        r = 16.5 if k % 2 else 15.5
        x, z = int(round(CX + r * math.cos(a))), int(round(CZ + r * math.sin(a)))
        # outcrop: a 3x3 calcite boulder rising 2 above the turf, deposit on top
        top = TOP
        while top > 0 and is_air(s, x, top, z):
            top -= 1
        if top < TOP - 6:
            continue
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                hgt = 2 if dx == 0 and dz == 0 else (1 if (dx == 0 or dz == 0) else 0)
                for y in range(top - 2, top + hgt + 1):
                    if 0 <= x + dx < W and 0 <= z + dz < D:
                        s.set(x + dx, y, z + dz, "calcite" if (dx + dz + y) % 2 else "diorite")
        deposit(s, x, top + 2, z, host="calcite")
        s.set(x, top + 3, z, "cave_air")
        dep_pts.append((x, z))

    # ---------------------------------------------------------------- underside: roots, glow berries, blossoms, glow
    under = s.match("calcite") | s.match("stone") | s.match("amethyst_block") | s.match("andesite")
    below_air = np.zeros(s.shape, bool)
    below_air[:, 1:, :] = s.match("air")[:, :-1, :]
    hang = under & below_air & (gy < TOP - 3)
    xs, ys, zs = np.nonzero(hang)
    r01 = noise.hash01(xs, ys, zs, seed=SEED + 50)
    for x, y, z, r in zip(xs, ys, zs, r01):
        if r < 0.10:
            L = 2 + int(r * 60) % 6
            for k in range(1, L):
                if not is_air(s, x, y - k, z):
                    break
                s.set(x, y - k, z, "cave_vines_plant[berries=true]" if k % 2 else "cave_vines_plant[berries=false]")
            if is_air(s, x, y - L, z):
                s.set(x, y - L, z, "cave_vines[berries=true,age=25]")
        elif r < 0.16:
            s.set(x, y - 1, z, "hanging_roots")
        elif r < 0.19:
            s.set(x, y - 1, z, "spore_blossom")
        elif r < 0.215:
            s.set(x, y, z, "verdant_froglight")
        elif r < 0.24:
            s.set(x, y, z, GLOW_PEARL)

    # ---------------------------------------------------------------- meadow dressing
    s.decorate("grass_block", Mix({"short_grass": 5, "air": 5, "wildflowers[flower_amount=3]": 2, "pink_petals[flower_amount=4]": 2,
                                   "torchflower": 1, "allium": 1, "azure_bluet": 1, "tall_grass[half=lower]": 0}),
               chance=0.75, seed=SEED + 21, where=((0, TOP, 0), (W - 1, TOP, D - 1)))
    s.decorate("moss_block", Mix({"moss_carpet": 4, "air": 3, "firefly_bush": 1, "flowering_azalea": 0.5}),
               chance=0.7, seed=SEED + 22, where=((0, TOP - 1, 0), (W - 1, TOP + 4, D - 1)))
    from tools.voxel.stability import fix_soil
    fix_soil(s)

    s.mark("cam_front", (CX + 3, TOP + 1, D - 3), look_at=(tx, TOP + 6, tz))
    s.mark("cam_pavilion", (tx - 3, TOP + 2, tz + 1), look_at=(lx, TOP + 2, lz))
    s.mark("cam_under", (CX + 8, TOP - 26, CZ + 18), look_at=(CX, TOP - 8, CZ))
    return finish(s, tier="major", kind="sky", anchor=(CX, TOP + 1, CZ))
