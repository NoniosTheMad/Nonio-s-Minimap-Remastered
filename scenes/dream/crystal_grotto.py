"""MAJOR site: THE CRACKED EGG (crystal grotto).

Statement: a geode the size of a chapel hatched on the island. Its shell broke open like an egg: the north wall still
stands high and jagged, the south side split to the floor (the walk-in crack), and the broken crown hovers in pieces
above it, crystals still pointing inward, drifting away. Inside: a violet and emerald crystal garden, the beam rising
from a quartz dais in the middle, the loot in a crystal niche at the back.
Layers like a real geode: smooth basalt rind, calcite, amethyst lining.

Render: python -m tools.voxel render scenes/dream/crystal_grotto.py --mood dream
"""
import math

import numpy as np

from scenes.dream._dream import (GLOW_GREEN, GLOW_WARM, SOIL, TURF, beacon, deposit, finish, loot_chest, skirt)
from tools.voxel import noise
from tools.voxel.palette import Gradient, Mix, Noise
from tools.voxel.scene import Scene

W, H, D = 41, 66, 41
CX, CZ = 20, 20
AY = 10                 # anchor y: first air above terrain = interior floor level
CY = 18                 # egg centre
RXZ, RY_LO, RY_HI = 18.5, 14.0, 27.0
SEED = 717

# a speckled dream-egg: pale shell with verdigris freckles, a dark basalt band (reads at every break), amethyst lining
RIND = Noise([(-0.55, Mix({"calcite": 3, "waxed_oxidized_copper": 1}, seed=SEED)),
              (0.35, Mix({"calcite": 5, "diorite": 2, "smooth_quartz": 1, "waxed_oxidized_copper": 0.35}, seed=SEED + 4)),
              (1, Mix({"diorite": 3, "calcite": 2, "polished_diorite": 1}, seed=SEED + 5))], scale=5, seed=SEED)
MID = Mix({"smooth_basalt": 5, "tuff": 1}, seed=SEED + 1)
LINING = Mix({"amethyst_block": 6, "purple_stained_glass": 0.4}, seed=SEED + 2)
FLOOR = Noise([(-0.35, "moss_block"), (0.15, "calcite"), (0.5, "polished_diorite"), (1, "amethyst_block")], scale=4, seed=SEED)


def egg_field(gx, gy, gz):
    """< 1 inside the egg. Wider low, taller top (egg)."""
    ry = np.where(gy < CY, RY_LO, RY_HI)
    # slight egg taper: narrower near the top
    taper = 1 - 0.18 * np.clip((gy - CY) / RY_HI, 0, 1)
    return np.sqrt(((gx - CX) / (RXZ * taper)) ** 2 + ((gy - CY) / ry) ** 2 + ((gz - CZ) / (RXZ * taper)) ** 2)


def rim_height(theta):
    """Height of the broken edge by azimuth (theta: 0 = +x east, pi/2 = +z south). High north, low south, zigzag."""
    south = np.cos(theta - math.pi / 2)          # 1 at south, -1 at north
    zig = np.abs(((theta * 9 / math.pi) % 2) - 1) * 2 - 1   # triangle wave, 18 teeth
    zig2 = np.abs(((theta * 23 / math.pi) % 2) - 1) * 2 - 1
    return 29 - 10 * south + 3.2 * zig + 1.2 * zig2


def build():
    s = Scene((W, H, D), name="crystal_grotto", seed=SEED)
    gx, gy, gz = np.meshgrid(np.arange(W), np.arange(H), np.arange(D), indexing="ij")
    th = np.arctan2(gz - CZ, gx - CX)
    rim = rim_height(th)
    f = egg_field(gx + 0.0, gy + 0.0, gz + 0.0)
    # shell thickness in "field" units (approx 1 block = 1/R)
    t = 1.0 / RXZ
    rind = (f < 1) & (f >= 1 - 1.3 * t)
    mid = (f < 1 - 1.3 * t) & (f >= 1 - 2.5 * t)
    lining = (f < 1 - 2.5 * t) & (f >= 1 - 3.7 * t)
    inside = f < 1 - 3.7 * t

    # the walk-in crack: south, jagged slit from the floor to the rim
    dz_ang = np.angle(np.exp(1j * (th - math.pi / 2)))
    slit_half = 0.16 + 0.22 * np.clip((gy - AY - 4) / 16, 0, 1) ** 1.5 + 0.035 * np.sin(gy * 1.7)
    slit = (np.abs(dz_ang) < slit_half) & (gy >= AY) & (gy < AY + 30)

    keep = (gy < rim) & ~slit
    shell_kept = keep & (rind | mid | lining)
    s.fill(rind & keep, RIND)
    s.fill(mid & keep, MID)
    s.fill(lining & keep, LINING)

    # fresh break: rim top cells read lighter (calcite/quartz) on the rind
    edge = shell_kept & (gy >= rim - 1.2)
    s.fill(edge & rind, Mix({"smooth_quartz": 2, "calcite": 1}, seed=SEED + 9))

    # ---------------------------------------------------------------- floating crown fragments
    band = (rind | mid | lining) & (gy >= rim + 1.5)
    frags = [  # (centre azimuth, half width, y lo above rim, y hi above rim, lift, outward)
        (-math.pi / 2 - 0.35, 0.45, 1.5, 9, 7, 1.5),     # north-west
        (-math.pi / 2 + 0.55, 0.40, 1.5, 8, 11, 2.0),    # north-east
        (math.pi, 0.35, 1.5, 7, 5, 1.0),                  # west
        (0.15, 0.32, 1.5, 7, 9, 1.5),                    # east
        (math.pi / 2 + 0.75, 0.28, 1.5, 6, 13, 1.0),     # south-west, highest, smallest
    ]
    for k, (a, hw, ylo, yhi, lift, out) in enumerate(frags):
        da = np.abs(np.angle(np.exp(1j * (th - a))))
        m = band & (da < hw) & (gy >= rim + ylo) & (gy < rim + yhi)
        xs, ys, zs = np.nonzero(m)
        if not len(xs):
            continue
        ox = int(round(out * math.cos(a)))
        oz = int(round(out * math.sin(a)))
        nx, ny, nz = xs + ox, ys + lift, zs + oz
        ok = (nx >= 0) & (nx < W) & (ny < H) & (nz >= 0) & (nz < D)
        xs, ys, zs, nx, ny, nz = xs[ok], ys[ok], zs[ok], nx[ok], ny[ok], nz[ok]
        for src, spec in ((rind, RIND), (mid, MID), (lining, LINING)):
            sel = src[xs, ys, zs]
            mm = np.zeros(s.shape, bool)
            mm[nx[sel], ny[sel], nz[sel]] = True
            s.fill(mm, spec)
        # crystals still growing on the inside of each fragment (pointing in / down)
        lin = lining[xs, ys, zs]
        lx, ly, lz = nx[lin], ny[lin], nz[lin]
        r01 = noise.hash01(lx, ly, lz, seed=SEED + 40 + k)
        for x, y, z, r in zip(lx, ly, lz, r01):
            if r < 0.35:
                vx, vz = CX - x, CZ - z
                if abs(vx) > abs(vz):
                    p = (x + (1 if vx > 0 else -1), y, z); fc = "east" if vx > 0 else "west"
                else:
                    p = (x, y, z + (1 if vz > 0 else -1)); fc = "south" if vz > 0 else "north"
                if s.get(*p) == "minecraft:air":
                    s.set(*p, f"amethyst_cluster[facing={fc}]")
            elif r < 0.5 and s.get(x, y - 1, z) == "minecraft:air":
                s.set(x, y - 1, z, "amethyst_cluster[facing=down]")

    # ---------------------------------------------------------------- floor + base mound
    rr = np.hypot(gx - CX, gz - CZ)
    floor = inside & (gy < AY)
    s.fill(floor & (gy == AY - 1), FLOOR)
    s.fill(floor & (gy < AY - 1), Mix({"calcite": 2, "tuff": 1}, seed=SEED + 3))
    # the crack floor continues the interior floor out of the shell
    s.fill(slit & (gy == AY - 1) & (f < 1.05), FLOOR)
    # mound the island turf around the egg base (the egg sits IN the ground)
    wob = 1 + 0.10 * np.sin(3 * th + 1.3) + 0.06 * np.sin(7 * th)
    mound_r = 20.3 * wob
    for y in range(AY - 1, AY + 3):
        rise = y - (AY - 1)
        m = (gy == y) & (rr < mound_r - rise * 1.6) & (s.idx == 0) & (f >= 1)
        # keep the crack approach (south) open
        m &= ~((np.abs(dz_ang) < 0.32) & (gy >= AY))
        s.fill(m, TURF if y >= AY - 1 else SOIL)
    s.fill((gy == AY - 1) & (rr < 20.4) & (s.idx == 0) & (gx >= 0), TURF)
    under = (gy < AY - 1) & (gy >= AY - 2) & (rr < 20) & (s.idx == 0)
    s.fill(under, SOIL)
    fp = np.zeros((W, D), bool)
    fp[np.hypot(*np.meshgrid(np.arange(W) - CX, np.arange(D) - CZ, indexing="ij")) < 19.5] = True
    skirt(s, fp, AY - 1, depth=8, seed=SEED)

    # ---------------------------------------------------------------- crystal spires (feature)
    def spire(base, tip, r0, core, skin, seed):
        b = np.array(base, float); tp = np.array(tip, float)
        L = np.linalg.norm(tp - b)
        n = int(L * 2) + 1
        for i in range(n + 1):
            u = i / n
            p = b + (tp - b) * u
            r = r0 * (1 - u) ** 0.8 + 0.35
            ri = int(math.ceil(r))
            for dx in range(-ri, ri + 1):
                for dy in range(-ri, ri + 1):
                    for dz in range(-ri, ri + 1):
                        d = math.sqrt(dx * dx + dy * dy + dz * dz)
                        if d <= r:
                            q = (int(round(p[0] + dx)), int(round(p[1] + dy)), int(round(p[2] + dz)))
                            if not (0 <= q[0] < W and 0 <= q[1] < H and 0 <= q[2] < D):
                                continue
                            cur = s.get(*q)
                            if d <= r - 1.1 and u < 0.75:
                                s.set(*q, core)
                            elif cur in ("minecraft:air",) or u < 0.95:
                                s.set(*q, skin)

    G_CORE, G_SKIN = GLOW_GREEN, "lime_stained_glass"
    V_CORE, V_SKIN = "amethyst_block", "purple_stained_glass"
    # inside, leaning toward the centre (base on the floor / lower wall)
    inner = [
        ((CX - 9, AY - 1, CZ - 6), (CX - 4, AY + 13, CZ - 3), 2.6, G_CORE, G_SKIN),
        ((CX + 9, AY - 1, CZ - 5), (CX + 5, AY + 10, CZ - 2), 2.2, V_CORE, V_SKIN),
        ((CX - 8, AY - 1, CZ + 7), (CX - 4, AY + 8, CZ + 4), 1.8, V_CORE, V_SKIN),
        ((CX + 10, AY - 1, CZ + 5), (CX + 6, AY + 7, CZ + 3), 1.6, G_CORE, G_SKIN),
        ((CX + 2, AY - 1, CZ - 11), (CX + 1, AY + 15, CZ - 6), 2.4, V_CORE, V_SKIN),
        ((CX - 3, AY - 1, CZ - 11), (CX - 2, AY + 9, CZ - 7), 1.7, G_CORE, G_SKIN),
    ]
    for k, (b, tp, r0, c, sk) in enumerate(inner):
        spire(b, tp, r0, c, sk, SEED + k)
    # outside, bursting through the shell (silhouette)
    outer = [
        ((CX - 13, AY + 6, CZ - 9), (CX - 22, AY + 16, CZ - 14), 2.0, G_CORE, G_SKIN),
        ((CX + 14, AY + 4, CZ - 7), (CX + 22, AY + 10, CZ - 11), 1.7, V_CORE, V_SKIN),
        ((CX + 12, AY + 8, CZ + 10), (CX + 18, AY + 19, CZ + 17), 1.6, G_CORE, G_SKIN),
        ((CX - 12, AY + 2, CZ + 12), (CX - 18, AY + 7, CZ + 19), 1.4, V_CORE, V_SKIN),
    ]
    for k, (b, tp, r0, c, sk) in enumerate(outer):
        spire(b, tp, r0, c, sk, SEED + 20 + k)

    # amethyst clusters on the interior floor and lining (facing away from the wall)
    lin_now = s.match("amethyst_block") & lining
    xs, ys, zs = np.nonzero(lin_now)
    r01 = noise.hash01(xs, ys, zs, seed=SEED + 77)
    for x, y, z, r in zip(xs, ys, zs, r01):
        if r > 0.22:
            continue
        vx, vy, vz = CX - x, (CY + 4) - y, CZ - z
        ax = max((abs(vx), 0), (abs(vy), 1), (abs(vz), 2))[1]
        if ax == 0:
            p, fc = (x + (1 if vx > 0 else -1), y, z), ("east" if vx > 0 else "west")
        elif ax == 1:
            p, fc = (x, y + (1 if vy > 0 else -1), z), ("up" if vy > 0 else "down")
        else:
            p, fc = (x, y, z + (1 if vz > 0 else -1)), ("south" if vz > 0 else "north")
        if 0 <= p[1] < H and s.get(*p) == "minecraft:air" and p[1] >= AY:
            kind = "amethyst_cluster" if r < 0.12 else "large_amethyst_bud"
            s.set(*p, f"{kind}[facing={fc}]")
    s.decorate("amethyst_block", Mix({"amethyst_cluster[facing=up]": 2, "medium_amethyst_bud[facing=up]": 2}),
               chance=0.5, seed=SEED + 5, where=((0, AY - 1, 0), (W - 1, AY - 1, D - 1)))
    s.decorate("moss_block", Mix({"moss_carpet": 3, "pink_petals[flower_amount=3]": 1, "short_grass": 1}),
               chance=0.45, seed=SEED + 6, where=((0, AY - 1, 0), (W - 1, AY - 1, D - 1)))

    # ---------------------------------------------------------------- the dais and the beam (centre, open sky)
    bx, bz = CX, CZ + 1
    for (r, y, blk) in ((4.5, AY, "smooth_quartz"), (3.2, AY + 1, "quartz_bricks")):
        m = (gy == y) & (np.hypot(gx - bx, gz - bz) < r)
        s.fill(m, blk)
    # quartz steps ring around the lower tier
    ring = (gy == AY) & (np.abs(np.hypot(gx - bx, gz - bz) - 4.9) < 0.6) & (s.idx == 0)
    s.fill(ring, "smooth_quartz_slab[type=bottom]")
    # beacon: base at AY+2 (3x3 verdant froglight), beacon on AY+3, lime glass above; column above is the open egg
    beacon(s, bx, AY + 3, bz)
    for dx, dz in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
        s.set(bx + dx, AY + 2, bz + dz, "waxed_oxidized_cut_copper")
        s.set(bx + dx, AY + 3, bz + dz, "amethyst_cluster[facing=up]")
    for dx, dz in ((-2, 0), (2, 0), (0, -2), (0, 2)):
        s.set(bx + dx, AY + 2, bz + dz, "smooth_quartz_slab[type=bottom]")
    for dx, dz in ((-1, -2), (1, -2), (-1, 2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)):
        s.set(bx + dx, AY + 2, bz + dz, "smooth_quartz_stairs[facing=" +
              ("south" if dz == -2 else "north" if dz == 2 else "east" if dx == -2 else "west") + "]")

    # ---------------------------------------------------------------- the loot niche (back, north)
    nx_, nz_ = CX, CZ - 9
    # a carved alcove into the north wall: crystal arch around a calcite plinth
    for y in range(AY, AY + 6):
        for dx in range(-2, 3):
            for dz in range(-3, 1):
                q = (nx_ + dx, y, nz_ + dz)
                if abs(dx) == 2 or y == AY + 5 or dz == -3:
                    s.set(*q, "amethyst_block" if (dx + y) % 3 else "purple_stained_glass")
                else:
                    s.set(*q, "air")
    s.set(nx_, AY + 4, nz_ - 2, GLOW_WARM)
    for dx in (-1, 0, 1):
        s.set(nx_ + dx, AY, nz_ - 1, "polished_diorite")
        s.set(nx_ + dx, AY, nz_, "polished_diorite_slab[type=bottom]")
    s.set(nx_ - 1, AY + 1, nz_ - 1, "amethyst_cluster[facing=up]")
    s.set(nx_ + 1, AY + 1, nz_ - 1, "lantern[hanging=false]")
    loot_chest(s, nx_, AY + 1, nz_ - 1, "major", facing="south")
    s.set(nx_ - 2, AY + 5, nz_ + 1, "amethyst_cluster[facing=south]")
    s.set(nx_ + 2, AY + 5, nz_ + 1, "amethyst_cluster[facing=south]")

    # ---------------------------------------------------------------- the approach: crack portal frame + lantern path
    # threshold: the crack's floor is moss + calcite stepping stones down the mound, two copper lantern posts
    sx = CX
    for k, dz in enumerate(range(19, 24)):
        z = CZ + dz - 1
        if z >= D:
            break
        for dx in (-1, 0, 1):
            if (dx + k) % 2 == 0:
                q = (sx + dx, AY - 1, z)
                if s.get(*q) != "minecraft:air":
                    s.set(*q, "calcite")
    for dx in (-4, 4):
        x, z = sx + dx, CZ + 18
        top = AY - 1
        while top < AY + 4 and s.get(x, top + 1, z) != "minecraft:air":
            top += 1
        s.set(x, top + 1, z, "waxed_oxidized_copper")
        for y in range(top + 2, top + 5):
            s.set(x, y, z, "diorite_wall")
        s.set(x, top + 5, z, "waxed_oxidized_cut_copper_slab[type=bottom]")
        s.set(x, top + 5, z - 1, "waxed_oxidized_cut_copper_slab[type=bottom]")
        s.set(x, top + 4, z - 1, "waxed_oxidized_copper_chain[axis=y]")
        s.set(x, top + 3, z - 1, "lantern[hanging=true]")

    # lights inside: hanging lanterns from the high north wall and glow lichen-like froglights in the lining
    for (x, z, L) in ((CX - 6, CZ - 8, 6), (CX + 6, CZ - 7, 4), (CX - 9, CZ + 1, 3), (CX + 9, CZ + 2, 5)):
        # find the lining above
        yy = None
        for y in range(H - 1, AY + 4, -1):
            if s.get(x, y, z) != "minecraft:air" and s.get(x, y - 1, z) == "minecraft:air":
                yy = y
                break
        if yy is None:
            continue
        for k in range(1, L):
            s.set(x, yy - k, z, "waxed_oxidized_copper_chain[axis=y]")
        s.set(x, yy - L, z, "lantern[hanging=true]")

    # flowers and bushes around the base (warm contrast)
    s.decorate("grass_block", Mix({"short_grass": 4, "pink_petals[flower_amount=4]": 2, "torchflower": 1, "air": 6,
                                   "azalea": 1, "flowering_azalea": 1}), chance=0.6, seed=SEED + 11)
    s.decorate("moss_block", Mix({"moss_carpet": 4, "air": 4, "firefly_bush": 1}), chance=0.6, seed=SEED + 12,
               where=((0, AY, 0), (W - 1, H - 1, D - 1)))

    # ---------------------------------------------------------------- crystal-bed deposits (regrowing veins)
    # on the floor ring just inside the lining, and two in the high basalt seam of the north wall
    for k, a in enumerate((-2.6, -1.9, -0.6, 0.2, 2.3, 2.9)):
        r = 10.5 if k % 2 else 9.5
        x, z = int(round(CX + r * math.cos(a))), int(round(CZ + r * math.sin(a)))
        deposit(s, x, AY - 1, z, host="amethyst_block")
        s.set(x, AY, z, "cave_air")
    for (x, y, z) in ((CX - 5, AY + 3, CZ - 12), (CX + 5, AY + 4, CZ - 12)):
        # step into the wall until we hit the lining, then put the seed in it with headroom in front
        zz = z
        while zz > 0 and s.get(x, y, zz) in ("minecraft:air", "minecraft:cave_air"):
            zz -= 1
        if s.get(x, y, zz) != "minecraft:air":
            s.set(x, y, zz, "amethyst_block")
            s.set(x, y, zz + 1, "cave_air")
            # seed marker goes above: leave that open too
            deposit(s, x, y, zz, host="amethyst_block")
            s.set(x, y + 1, zz, "cave_air")

    # props: offerings around the dais and the niche (candles, pots)
    from tools.voxel import nbt as N
    for (x, z, sh) in ((CX - 4, CZ - 2, "minecraft:heart_pottery_sherd"), (CX + 4, CZ + 4, "minecraft:flow_pottery_sherd"),
                       (CX - 2, CZ - 7, None), (CX + 2, CZ - 7, None)):
        if s.get(x, AY, z) in ("minecraft:air", "minecraft:cave_air") and s.get(x, AY - 1, z) != "minecraft:air":
            s.set(x, AY, z, "decorated_pot[facing=south]", nbt=N.pot(front=sh, back=sh) if sh else N.pot())
    for (x, z, n) in ((CX - 3, CZ - 3, 3), (CX + 3, CZ - 2, 2), (CX + 3, CZ + 5, 4), (CX - 4, CZ + 4, 2)):
        if s.get(x, AY, z) in ("minecraft:air", "minecraft:cave_air") and s.get(x, AY - 1, z) != "minecraft:air":
            s.set(x, AY, z, f"lime_candle[candles={n},lit=true]")
    # keep the walk-in path clear (crack to dais)
    for z in range(CZ + 7, D):
        for x in range(CX - 1, CX + 2):
            for y in (AY, AY + 1, AY + 2):
                if s.get(x, y, z) not in ("minecraft:air", "minecraft:cave_air"):
                    s.set(x, y, z, "cave_air")
            if s.get(x, AY - 1, z) in ("minecraft:air", "minecraft:cave_air"):
                s.set(x, AY - 1, z, "calcite")
    from tools.voxel.stability import fix_soil
    fix_soil(s)

    s.mark("cam_front", (CX, AY, D - 3), look_at=(CX, AY + 5, CZ - 4))
    s.mark("cam_inside", (CX - 3, AY, CZ + 7), look_at=(CX, AY + 6, CZ - 9))
    return finish(s, tier="major", kind="ground", anchor=(CX, AY, CZ))
