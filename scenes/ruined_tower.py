"""Voxel studio demo: a ruined watchtower on a rocky sky-island crag.

Brief (playbook pass 1): "weathered border watchtower on a tuff and deepslate crag, half collapsed, reclaimed by moss".
Families: cool stone ramp (blackstone -> cobbled_deepslate -> tuff -> stone_bricks/mossy -> andesite -> smooth_stone trim),
ground (rooted_dirt / coarse_dirt / moss / grass), dark wood accents (spruce, dark oak). Mood: late afternoon, quiet.

Run:  python -m tools.voxel render scenes/ruined_tower.py      (views in .mcdev/voxel/out/ruined_tower/)
      python -m tools.voxel place  scenes/ruined_tower.py --server voxel
Every element is one function; parameters at the top."""
import math

import numpy as np

from tools.voxel import noise, shapes
from tools.voxel.palette import Gradient, Mix, Noise
from tools.voxel.scene import Scene

W, H, D = 80, 70, 80
SEED = 11
ORIGIN = (-40, 40, -40)          # world position of scene (0,0,0) when placed

TX, TZ = 48.5, 44.5              # tower axis (x.5 -> odd width)
TB = 27                          # tower floor level (top of the crag)
R_OUT, R_IN = 6.6, 4.4           # tower radii (13 wide, 2-thick wall)
T_TOP = TB + 32                  # intact rim height (west side); the east side is broken down
FLOORS = (TB + 9, TB + 19)

ROCK = Gradient("y", [(4, "blackstone"),
                      (8, Mix({"cobbled_deepslate": 3, "blackstone": 1})),
                      (12, Mix({"deepslate": 2, "tuff": 2})),
                      (17, Mix({"tuff": 4, "andesite": 1})),
                      (23, Mix({"tuff": 3, "andesite": 2, "stone": 1})),
                      (99, Mix({"andesite": 3, "tuff": 1, "stone": 2}))],
                jitter=3.5, jitter_scale=7, seed=SEED)


def walls_palette(seed):
    """Value ramp for masonry: dark heavy base -> tuff -> stone bricks (mossy clusters) -> lighter andesite top."""
    bricks = Noise([(-0.25, Mix({"mossy_stone_bricks": 4, "stone_bricks": 1})),
                    (0.35, Mix({"stone_bricks": 6, "cracked_stone_bricks": 2, "mossy_stone_bricks": 1})),
                    (1, Mix({"stone_bricks": 3, "andesite": 1, "cracked_stone_bricks": 1}))], scale=6, seed=seed)
    return Gradient("y", [(TB + 2, Mix({"cobbled_deepslate": 3, "blackstone": 1})),
                          (TB + 6, Mix({"tuff_bricks": 3, "tuff": 1, "cobbled_deepslate": 1})),
                          (TB + 24, bricks),
                          (99, Mix({"stone_bricks": 3, "andesite": 2, "polished_andesite": 1}))],
                    jitter=2.0, jitter_scale=5, seed=seed + 1)


def grid():
    x, y, z = np.meshgrid(np.arange(W) + 0.5, np.arange(H) + 0.5, np.arange(D) + 0.5, indexing="ij")
    return x, y, z


# ------------------------------------------------------------------ terrain
def island(s):
    """Sky island: irregular coastline, gentle top, tapering rocky underside."""
    x, z = np.meshgrid(np.arange(W) + 0.5, np.arange(D) + 0.5, indexing="ij")
    cx, cz = W / 2 - 1, D / 2 + 1
    ang = np.arctan2(z - cz, x - cx)
    r = np.hypot(x - cx, z - cz)
    R = 31 + 6 * noise.fbm(np.cos(ang) * 3, np.sin(ang) * 3, 0.0, scale=1.6, octaves=3, seed=SEED)
    t = np.clip(1 - r / R, 0, 1)
    top = 11 + 4 * t ** 0.5 + 2.4 * noise.fbm(x, z, 3.0, scale=13, seed=SEED + 1)
    under = 2 + 24 * t ** 0.9 * (0.75 + 0.5 * (noise.fbm(x, z, 9.0, scale=7, seed=SEED + 3) * 0.5 + 0.5))
    bottom = top - under
    yy = np.arange(H)[None, :, None] + 0.5
    m = (r < R)[:, None, :] & (yy < top[:, None, :]) & (yy >= bottom[:, None, :])
    s.fill(m, ROCK)
    return top


def crag(s):
    """The outcrop the tower stands on: smooth-unioned displaced lumps, steep faces with overhangs, flat-ish top at TB."""
    c = (TX, 0, TZ)
    body = shapes.cylinder(c, 10.5, 6, TB, r_top=8.5)
    lumps = [shapes.ellipsoid((TX - 9, 16, TZ + 6), (9, 10, 8)),
             shapes.ellipsoid((TX + 7, 13, TZ - 8), (8, 9, 7)),
             shapes.ellipsoid((TX + 9, 18, TZ + 7), (6, 8, 6)),
             shapes.ellipsoid((TX - 4, 21, TZ - 7), (7, 6, 6))]
    rock = body
    for L in lumps:
        rock = rock.smooth_union(L, 3.5)
    rock = rock.displace(amp=2.6, scale=6.5, octaves=3, seed=SEED + 5)
    cap = shapes.half_space("y", TB, below=True)
    s.fill(rock & cap, ROCK)
    # make sure the tower footprint is solid right up to TB (no gaps under the plinth)
    s.fill(shapes.cylinder(c, R_OUT + 1.6, TB - 6, TB), ROCK, replace="air")


def soil(s):
    """Topsoil on gentle slopes only (steep faces stay rock): grass over 1-3 dirt, moss patches, path wear."""
    solid = s.solid()
    hm = s.surface("solid")
    pad = np.pad(hm, 1, mode="edge")
    slope = np.max([np.abs(hm - pad[1:-1, :-2]), np.abs(hm - pad[1:-1, 2:]), np.abs(hm - pad[:-2, 1:-1]), np.abs(hm - pad[2:, 1:-1])], 0)
    gentle = (slope <= 1) & (hm >= 0)
    xs, zs = np.nonzero(gentle)
    top = np.zeros(s.shape, bool)
    sub = np.zeros(s.shape, bool)
    depth = 1 + (noise.hash01(xs, 0, zs, seed=SEED + 9) * 3).astype(int)
    for x, z, d in zip(xs, zs, depth):
        y = hm[x, z]
        if y >= TB - 1 and math.hypot(x + 0.5 - TX, z + 0.5 - TZ) < R_OUT + 2.5:
            continue  # tower plinth
        top[x, y, z] = True
        sub[x, max(0, y - d):y, z] = True
    sub &= solid
    s.fill(sub, Noise([(-0.3, "rooted_dirt"), (0.4, "dirt"), (1, "coarse_dirt")], scale=5, seed=SEED + 10))
    s.fill(top, Noise([(-0.45, "moss_block"), (0.62, "grass_block"), (0.7, "coarse_dirt"), (1, "grass_block")], scale=7, seed=SEED + 11))
    return hm


# ------------------------------------------------------------------ tower
def tower(s):
    x, y, z = grid()
    dx, dz = x - TX, z - TZ
    r = np.hypot(dx, dz)
    ang = np.arctan2(dz, dx)
    h = y - TB
    flare = np.clip(1 - h / 5, 0, 1) * 1.3                       # battered plinth
    outer = r <= R_OUT + flare
    inner = r <= R_IN
    # ruined top: high on the west, broken down to the east, noisy edge
    ca, sa = np.cos(ang), np.sin(ang)
    cut = (T_TOP - 11 * np.clip((dx + 1) / 8, 0, 1) - 2.2 * noise.fbm(ca * 2, sa * 2, 0.0, scale=0.8, octaves=2, seed=SEED + 20)
           - 1.0 * (noise.hash01(np.floor(x), 0, np.floor(z), seed=SEED + 21) > 0.7))
    shaft = (y >= TB - 4) & (y < cut)
    wall = outer & ~inner & shaft
    # breach on the east face, rubble spills from it
    breach = shapes.sphere((TX + 6.5, TB + 15, TZ + 1.5), 5.2).displace(1.6, 3, 2, seed=SEED + 22).mask(s.shape)
    wall &= ~breach
    s.fill(wall, walls_palette(SEED + 30))
    # interior: hollow, floor at TB
    s.fill(inner & (y >= TB) & (y < T_TOP + 2), "air")
    s.fill(inner & (y >= TB - 1) & (y < TB), Mix({"cobbled_deepslate": 2, "tuff": 2, "mossy_cobblestone": 1}))
    return wall, r, ang


def buttresses(s):
    """Four stepped buttresses on the diagonals (depth layer 1), each stopping at a different height."""
    tops = [TB + 13, TB + 9, TB + 16, TB + 7]
    for k, (a, top) in enumerate(zip((45, 135, 225, 315), tops)):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        for step, (reach, y1) in enumerate([(R_OUT + 2.6, top - 5), (R_OUT + 1.6, top)]):
            cxp, czp = TX + ca * reach, TZ + sa * reach
            b = shapes.box((cxp - 1.0, TB - 3, czp - 1.0), (cxp + 1.0, y1, czp + 1.0))
            s.fill(b, Gradient("y", [(TB + 3, "cobbled_deepslate"), (99, Mix({"deepslate_bricks": 2, "stone_bricks": 3, "mossy_stone_bricks": 1}, seed=k))],
                                jitter=1.5, seed=k), replace="air")
            # sloped cap: stairs facing the tower
            ix, iz = int(math.floor(cxp)), int(math.floor(czp))
            face = "west" if abs(ca) > abs(sa) and ca > 0 else "east" if abs(ca) > abs(sa) else "north" if sa > 0 else "south"
            for ddx in (-1, 0):
                for ddz in (-1, 0):
                    xx, zz = ix + ddx + (1 if cxp - ix >= 0.5 else 0), iz + ddz + (1 if czp - iz >= 0.5 else 0)
                    if s.idx[xx, y1, zz] == 0:
                        s.set(xx, y1, zz, f"stone_brick_stairs[facing={face}]")


def openings(s, r, ang):
    x, y, z = grid()
    # door: south, 3 wide x 4 high, round-ish head
    door = (np.abs(x - TX) <= 1.5) & (z > TZ) & (y >= TB) & (y < TB + 4) & (r > R_IN - 0.5)
    door |= (np.abs(x - TX) <= 0.5) & (z > TZ) & (y >= TB + 4) & (y < TB + 5) & (r > R_IN - 0.5)
    s.fill(door, "air")
    # arrow slits: 1 wide x 3 high, staggered around the tower per storey
    for lvl, y0 in enumerate((TB + 5, TB + 12, TB + 22)):
        for a in range(0, 360, 90):
            a2 = math.radians(a + 45 * (lvl % 2) + 20)
            sx, sz = TX + math.cos(a2) * (R_OUT - 0.5), TZ + math.sin(a2) * (R_OUT - 0.5)
            ix, iz = int(sx), int(sz)
            for yy in range(y0, y0 + 3):
                for t in np.linspace(R_IN - 0.3, R_OUT + 0.8, 8):
                    px, pz = int(TX + math.cos(a2) * t), int(TZ + math.sin(a2) * t)
                    if 0 <= px < W and 0 <= pz < D:
                        s.idx[px, yy, pz] = 0
    # door frame: deepslate jambs + lintel stairs (sub-block layer)
    zf = int(TZ + R_OUT + 0.6)
    for yy in range(TB, TB + 4):
        for xx in (int(TX - 2.5), int(TX + 2.5)):
            s.set(xx, yy, zf, "polished_deepslate")
    s.set(int(TX - 1.5), TB + 4, zf, "polished_deepslate_stairs[facing=east,half=top]")
    s.set(int(TX + 1.5), TB + 4, zf, "polished_deepslate_stairs[facing=west,half=top]")
    s.set(int(TX - 0.5), TB + 5, zf, "chiseled_stone_bricks")
    s.set(int(TX - 0.5), TB - 1, zf + 1, "polished_deepslate_slab[type=top]")


def floors(s):
    """Two timber floors, partly collapsed, on dark oak beams."""
    x, y, z = grid()
    for k, fy in enumerate(FLOORS):
        r = np.hypot(x - TX, z - TZ)
        disc = (r <= R_IN + 0.3) & (y >= fy) & (y < fy + 1)
        holes = noise.fbm(x, fy, z, scale=4, octaves=2, seed=SEED + 40 + k) > (0.05 if k else 0.3)
        holes |= (x - TX) > (1.5 if k else 2.5)   # the breach side fell in
        s.fill(disc & ~holes, Mix({"spruce_planks": 5, "dark_oak_planks": 1}, seed=k), replace="air")
        for bz in (-2, 2):
            beam = (np.abs(z - (TZ + bz)) < 0.5) & (y >= fy - 1) & (y < fy) & (r <= R_IN + 1.2) & ((x - TX) < (3 if k else 4))
            s.fill(beam, "stripped_dark_oak_log[axis=x]", replace="air")
    # a ladder up the inside north wall
    lx, lz = int(TX), int(TZ - R_IN + 0.5)
    for yy in range(TB, FLOORS[1] + 1):
        if s.idx[lx, yy, lz] == 0 or "planks" in s.palette[s.idx[lx, yy, lz]]:
            s.set(lx, yy, lz, "ladder[facing=south]")


def trim(s, wall):
    """String course + corbel ring (depth layer 2): smooth stone ring at the first floor, upside-down stairs under the rim."""
    x, y, z = grid()
    dx, dz = x - TX, z - TZ
    r = np.hypot(dx, dz)
    ring_r = (r > R_OUT - 0.2) & (r <= R_OUT + 0.9)
    for fy, st in ((FLOORS[0] - 1, "smooth_stone_slab[type=bottom]"), (FLOORS[1] + 3, "polished_andesite_slab[type=top]")):
        band = ring_r & (y >= fy) & (y < fy + 1)
        below_wall = np.zeros_like(band)
        below_wall[:, :, :] = wall[:, :, :]
        support = np.roll(wall, 1, axis=1) | np.roll(wall, -1, axis=1)
        s.fill(band & support, st, replace="air")
    # merlons on what survives of the rim (west half): every other 2-block arc
    surf = s.surface("solid")
    ang = np.degrees(np.arctan2(dz[:, 0, :], dx[:, 0, :])) % 360
    rr = r[:, 0, :]
    rim = (rr > R_IN + 0.2) & (rr <= R_OUT + 0.2) & ((ang // 22) % 2 == 0)
    for px, pz in zip(*np.nonzero(rim)):
        top = surf[px, pz]
        if top >= T_TOP - 4:
            s.set(px, top + 1, pz, "stone_bricks" if (px + pz) % 3 else "mossy_stone_bricks")
            if (px * 7 + pz) % 5 == 0:
                s.set(px, top + 2, pz, "stone_brick_slab")


def curtain_wall(s, hm):
    """A broken curtain wall running down the crag to the north-west, 3 thick, with a walkway and a gap."""
    a = np.array([TX - 6, TZ - 4.0]); b = np.array([TX - 30, TZ - 20.0])
    n = int(np.linalg.norm(b - a))
    d = (b - a) / n
    perp = np.array([-d[1], d[0]])
    for i in range(n + 1):
        p = a + d * i
        if 13 <= i <= 16:  # the gap
            continue
        height = 7 - 3.5 * max(0, (i - 17) / 12) + 1.5 * noise.fbm(i, 0, 0, scale=4, octaves=1, seed=SEED + 50)
        for w in (-1, 0, 1):
            q = p + perp * w
            px, pz = int(q[0]), int(q[1])
            if not (0 <= px < W and 0 <= pz < D):
                continue
            g = int(hm[px, pz])
            if w == -1:
                gc = int(hm[int(p[0]), int(p[1])])  # ground on the centre line keeps the top continuous
            if g < 0:
                continue
            top = max(g + 2, gc + int(round(height)))
            col = range(max(0, g - 2), top + 1)
            for yy in col:
                if s.idx[px, yy, pz] == 0 or yy <= g:
                    s.set(px, yy, pz, "minecraft:stone")  # placeholder, painted below
            s.idx[px, max(0, g - 2):top + 1, pz] = s.id("minecraft:cobblestone")
            if w == -1 and i % 2 == 0 and height > 4:
                s.set(px, top + 1, pz, "stone_bricks")
    # paint: wall masonry gradient over everything placed as cobblestone
    m = s.match("minecraft:cobblestone")
    s.fill(m, Gradient("depth", [(1, Mix({"stone_bricks": 3, "mossy_stone_bricks": 2, "cracked_stone_bricks": 1})),
                                 (99, Noise([(-0.2, "mossy_cobblestone"), (0.3, "cobblestone"), (1, "tuff")], scale=4, seed=SEED + 51))],
                                 seed=SEED + 52))


def hm_local(s, x, z):
    col = s.idx[x, :, z]
    nz = np.nonzero(col)[0]
    return int(nz.max()) if len(nz) else -1


def rubble(s):
    """Ground the ruin: heaps below the breach and at wall feet, scattered fragments (stairs/slabs/walls)."""
    rng = np.random.default_rng(SEED)
    heaps = [(TX + 11, TZ + 3, 3.2), (TX + 9, TZ - 3, 2.4), (TX + 14, TZ + 7, 2.0), (TX - 15, TZ - 13, 2.2), (TX + 3, TZ + 10, 1.8)]
    mix = Mix({"cobblestone": 3, "mossy_cobblestone": 3, "stone_bricks": 2, "cracked_stone_bricks": 2, "tuff": 1, "andesite": 1}, seed=3)
    for hx, hz, hr in heaps:
        gx, gz = int(hx), int(hz)
        if not (0 <= gx < W and 0 <= gz < D):
            continue
        g = hm_local(s, gx, gz)
        heap = shapes.ellipsoid((hx, g + 0.6, hz), (hr * 1.3, hr * 0.8, hr)).displace(0.9, 2.5, 2, seed=int(hx * 7 + hz))
        m = heap.mask(s.shape) & s.match("air")
        # only cells resting on something (no floating rubble)
        below = np.zeros_like(m); below[:, 1:] = s.solid()[:, :-1] | m[:, :-1]
        s.fill(m & below, mix)
    # loose fragments around the tower base
    frags = ["stone_brick_slab", "mossy_stone_brick_slab", "cobblestone_wall", "stone_brick_stairs[facing=north]",
             "stone_brick_stairs[facing=east]", "mossy_cobblestone_slab", "cobblestone"]
    for _ in range(70):
        a = rng.uniform(0, 2 * math.pi); d = rng.uniform(R_OUT + 1.5, R_OUT + 16) * (1.4 if math.cos(a) > 0.3 else 1.0)
        px, pz = int(TX + math.cos(a) * d), int(TZ + math.sin(a) * d)
        if not (0 <= px < W and 0 <= pz < D):
            continue
        g = hm_local(s, px, pz)
        if g < 0 or g + 1 >= H:
            continue
        if s.palette[s.idx[px, g, pz]].split("[")[0].endswith(("slab", "stairs", "wall", "carpet", "grass", "fern", "lantern", "iron_chain")):
            continue
        s.set(px, g + 1, pz, frags[rng.integers(len(frags))])


def vines(s):
    """Vines hanging down steep rock and tower faces, from ledges and under overhangs."""
    from tools.voxel.connect import sturdy
    rng = np.random.default_rng(SEED + 1)
    solid = sturdy(s)  # vines only survive on full faces
    air = s.match("air")
    X, Y, Z = s.shape
    dirs = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
    cand = []
    for name, (ddx, ddz) in dirs.items():
        nb = np.zeros_like(solid)
        xs = slice(max(0, ddx), X + min(0, ddx)); xd = slice(max(0, -ddx), X + min(0, -ddx))
        zs = slice(max(0, ddz), Z + min(0, ddz)); zd = slice(max(0, -ddz), Z + min(0, -ddz))
        nb[xd, :, zd] = solid[xs, :, zs]
        c = air & nb
        c[:, :8] = False
        pts = np.argwhere(c)
        keep = noise.fbm(pts[:, 0], pts[:, 1], pts[:, 2], scale=6, octaves=1, seed=SEED + 60 + len(name)) > 0.45
        pts = pts[keep]
        for p in pts[rng.random(len(pts)) < 0.12]:
            cand.append((p, name, ddx, ddz))
    vine_ids = {}
    for (x, y, z), name, ddx, ddz in cand:
        L = int(rng.integers(2, 7))
        for k in range(L):
            yy = y - k
            if yy < 0 or s.idx[x, yy, z] != 0 or not solid[x + ddx, yy, z + ddz]:
                break
            st = f"minecraft:vine[{name}=true]"
            s.idx[x, yy, z] = vine_ids.setdefault(st, s.id(st))


def moss_on_rock(s):
    """Moss sheets on upward-facing rock where it is flattish (clusters, not speckle)."""
    rock = s.match(["minecraft:tuff", "minecraft:andesite", "minecraft:stone", "minecraft:deepslate"])
    s.fill(rock, Gradient("up", [(0.5, None), (2, Noise([(-0.15, "moss_block"), (1, None)], scale=5, seed=SEED + 73))]))


def greenery(s):
    s.decorate("grass_block", Mix({"short_grass": 6, "fern": 2, "tall_grass[half=lower]": 0, "poppy": 0.2, "cornflower": 0.2}), chance=0.32, seed=SEED + 70)
    s.decorate("moss_block", Mix({"moss_carpet": 3, "short_grass": 1}), chance=0.35, seed=SEED + 71)
    # moss carpets creeping onto rock tops next to soil
    s.decorate(["minecraft:tuff", "minecraft:andesite", "minecraft:cobbled_deepslate"], "moss_carpet", chance=0.12, seed=SEED + 72)
    # a few azalea bushes (persistent leaves never decay)
    for i, (bx, bz) in enumerate([(TX - 20, TZ + 14), (TX + 16, TZ + 15), (TX - 26, TZ - 2), (TX + 4, TZ - 16)]):
        bx, bz = int(bx), int(bz)
        if not (2 <= bx < W - 2 and 2 <= bz < D - 2):
            continue
        g = hm_local(s, bx, bz)
        bush = shapes.ellipsoid((bx + 0.5, g + 1.6, bz + 0.5), (2.2, 1.6, 1.9)).displace(0.6, 2, 1, seed=i)
        s.fill(bush, Mix({"azalea_leaves[persistent=true]": 3, "flowering_azalea_leaves[persistent=true]": 1}, seed=i), replace="air")


PATH_END = int(TZ + R_OUT + 1) + (TB - 13) + 2


def path(s):
    """A stair path cut into the crag from the south meadow up to the door: 3 wide, headroom, wall rail on the east."""
    zf = int(TZ + R_OUT + 1)
    x0 = int(TX) - 1
    y = TB - 1
    z = zf
    body = np.zeros(s.shape, bool)
    while y > 0 and z < D - 1:
        landing = z <= zf + 1
        g = max(hm_local(s, xx, z) for xx in range(x0, x0 + 4))
        for xx in range(x0, x0 + 4):
            body[xx, max(0, y - 4):y + 1, z] = True
            s.idx[xx, max(0, y - 4):y + 1, z] = s.id("stone_bricks")
            s.idx[xx, y + 1:min(H, y + 5), z] = 0
        for xx in range(x0, x0 + 3):
            s.set(xx, y + 1, z, "polished_andesite_slab" if landing else "stone_brick_stairs[facing=north]")
        s.set(x0 + 3, y + 1, z, "mossy_stone_brick_wall" if z % 3 else "stone_brick_wall")
        if g <= y - 1 and not landing:
            pass
        if g >= y and not landing:
            break
        z += 1
        if not landing:
            y -= 1
    s.fill(body & s.match("minecraft:stone_bricks"),
           Gradient("depth", [(1, Mix({"stone_bricks": 3, "mossy_stone_bricks": 2})), (99, Mix({"cobbled_deepslate": 2, "tuff": 1}))]))


def lights(s):
    """Hanging lantern at the door on a dark oak bracket; a soul lantern glow inside; lanterns on the curtain wall."""
    zf = int(TZ + R_OUT + 0.6)
    bx = int(TX + 2.5)
    s.set(bx, TB + 5, zf + 1, "dark_oak_fence")
    s.set(bx, TB + 4, zf + 1, "iron_chain[axis=y]")
    s.set(bx, TB + 3, zf + 1, "lantern[hanging=true]")
    s.set(int(TX) - 2, TB, int(TZ) + 1, "campfire[lit=false]")
    s.set(int(TX) + 1, FLOORS[0] + 1, int(TZ) - 2, "lantern")


def markers(s, hm):
    def ground(x, z):
        """Nearest column with ground (spiral search), standing on top of it."""
        for rad in range(0, 20):
            for ddx in range(-rad, rad + 1):
                for ddz in range(-rad, rad + 1):
                    xx, zz = x + ddx, z + ddz
                    if max(abs(ddx), abs(ddz)) == rad and 0 <= xx < W and 0 <= zz < D and hm[xx, zz] > 0:
                        return [xx, hm_local(s, xx, zz) + 1, zz]
        raise ValueError("no ground near", x, z)
    s.mark("spawn_white", ground(12, 46), look_at=[TX, TB + 10, TZ])
    s.mark("spawn_black", ground(62, 22), look_at=[TX, TB + 10, TZ])
    s.mark("cam_path", ground(int(TX) + 11, PATH_END + 7), look_at=[TX, TB + 3, TZ + R_OUT])
    s.meta["origin"] = list(ORIGIN)


def build():
    s = Scene((W, H, D), "ruined_tower", seed=SEED)
    island(s)
    crag(s)
    hm = soil(s)
    wall, r, ang = tower(s)
    buttresses(s)
    openings(s, r[..., ], ang)
    floors(s)
    trim(s, wall)
    curtain_wall(s, hm)
    rubble(s)
    moss_on_rock(s)
    greenery(s)
    vines(s)
    path(s)
    lights(s)
    markers(s, hm)
    return s
