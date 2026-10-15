"""The Shattered Highland's landmarks: what the far ring of the map is about, and what a player sees from the rim.

- The Fallen Arc (NW): a sector of an older, larger ring that fell when the summit was torn off; it stands out of the
  heath as a broken copper arch, its glyph plates and rubble strewn below. The first armillary, before the Orrery.
- The Old Observatory (NE): the astronomer's first tower, a roofless ruin on a plinth, its copper dome lying cracked
  in the grass and the telescope fallen across the wall. A ramp climbs to a half floor (a sniper perch).
- Two oak groves (SW, SE) on the plates, with an understorey: soft cover between the spawns and the crater.
- The pilgrims' road from the white spawn to the Landing: lantern pylons every 8 blocks.
- Spawn plazas at both ends (paved, four pylons and a lodestone), and amethyst shards thrown out over the heath."""
import math

import numpy as np

from tools.voxel import noise, shapes
from tools.voxel.palette import Gradient, Mix

from .common import C, FLOOR, GROUND, SEED, Box, at_polar, cu, helix_path, ramp, slab_states, wrap_deg

ARC = (225.0, 80.0)
OBSERVATORY = (335.0, 83.0)
GROVES = [(150.0, 80.0, 9), (40.0, 84.0, 7)]
SPAWNS = {"spawn_white": (104, 196), "spawn_black": (104, 12)}


def top(s, x, z, below=100):
    col = s.idx[int(x), :below, int(z)]
    nz = np.nonzero(col)[0]
    return int(nz.max()) if len(nz) else 0


def disc_top(s, x, z, r, below=100, f=max):
    hs = [top(s, x + dx, z + dz, below) for dx in range(-int(r), int(r) + 1) for dz in range(-int(r), int(r) + 1)
          if dx * dx + dz * dz <= r * r]
    return f(hs)


# ------------------------------------------------------------------ the Fallen Arc
def fallen_arc(s, ctx):
    from .rings import band, glyph_set
    a, rr = ARC
    x, z = at_polar(a, rr)
    g = top(s, x, z)
    R = 24.0
    yaw = a - 180            # the arc faces the crater: seen whole from the island rim (its crown is local theta 270)
    rc = (x, g - 5.0, z)
    gap = lambda th: ~((th > 262) & (th < 292))      # broken at the crown: two horns
    band(s, R, 2.6, 1.1, 74, yaw, "oxidized", glyph_set("signs"), 0, "weathered", 6.0, rc=rc, keep=gap, replace="air")
    # rubble under the break: copper fragments, a fallen plate, calcite chips
    rng = np.random.default_rng(SEED + 400)
    from .common import rot
    M = rot(tilt_x=74, yaw=yaw)
    for th in (262.0, 292.0):
        p = M @ np.array([math.cos(math.radians(th)) * R, 0, math.sin(math.radians(th)) * R]) + np.array(rc)
        for k in range(14):
            px, pz = p[0] + rng.normal(0, 4), p[2] + rng.normal(0, 4)
            gy = top(s, px, pz)
            st = rng.choice([cu("oxidized", "cut"), cu("weathered", "chiseled"), "calcite", cu("oxidized", "block"),
                             cu("oxidized", "slab", type="bottom")])
            s.set(int(px), gy + 1, int(pz), str(st))
    # a fallen glyph plate half sunk in the turf, tilted
    px, pz = at_polar(a + 6, rr - 9)
    gy = top(s, px, pz)
    plate = shapes.box((px - 3, gy - 1, pz - 0.5), (px + 4, gy + 4, pz + 1.5))
    s.fill(plate, cu("oxidized", "block"))
    for (dx, dy) in ((0, 1), (1, 2), (2, 1), (1, 0), (1, 3)):
        s.set(int(px - 1 + dx), gy + dy, int(pz + 1.5), "calcite")
    ctx["fallen_arc"] = dict(c=(round(x, 1), g, round(z, 1)), R=R)


# ------------------------------------------------------------------ the Old Observatory
def observatory(s, ctx):
    a, rr = OBSERVATORY
    x, z = at_polar(a, rr)
    c = (x, 0, z)
    fy = disc_top(s, x, z, 11) + 1                   # plinth top (paving)
    # plinth: a battered drum of masonry down into the slope, paved on top
    s.fill(shapes.cylinder(c, 11.5, fy - 12, fy - 0.5, 12.5), Mix({"deepslate_bricks": 2, "tuff_bricks": 2, "cracked_deepslate_bricks": 1}))
    s.fill(shapes.cylinder(c, 11.0, fy - 0.5, fy + 0.5), Mix({"polished_tuff": 3, "tuff_bricks": 1, "mossy_stone_bricks": 1}))
    s.fill(shapes.cylinder(c, 11.0, fy + 0.5, fy + 42), "air")
    # broken parapet round the plinth
    b = Box(s, (x - 12, fy + 1, z - 12), (x + 13, fy + 2, z + 13))
    r = np.hypot(b.x - x, b.z - z)
    th = np.degrees(np.arctan2(b.z - z, b.x - x))
    keep = noise.hash01(np.floor(th / 12).astype(int), 0, 0, seed=SEED + 410) > 0.35
    b.fill((r > 10.0) & (r <= 11.0) & keep, Mix({"tuff_brick_wall": 2, "mossy_stone_brick_wall": 1}))
    # steps down the slope towards the crater (inward)
    ia = math.radians(a + 180)
    for k in range(10):
        sx, sz = x + math.cos(ia) * (11 + k), z + math.sin(ia) * (11 + k)
        gy = top(s, sx, sz)
        if gy >= fy - k:
            break
        s.fill(shapes.cylinder((sx, 0, sz), 2.2, fy - k - 1, fy - k + 0.5), Mix({"polished_tuff": 2, "tuff_bricks": 1}))
        s.fill(shapes.cylinder((sx, 0, sz), 2.2, fy - k + 0.5, fy - k + 4), "air")
    # the tower: r 6, wall 1.5, torn on a slant: chest-high over the perch on the crater side, 34 tall on the far side
    # (a vertical answer to the Spire across the crater; the slant reads in profile from the island), with the iron frame of its dome still clinging to the top
    R = 6.0
    ia_deg = a + 180
    tall = ia_deg + 110                 # seen from the crater the break is a slant, low left to high right
    hfun = lambda th_: 10 + 24 * np.maximum(0.0, np.cos(np.radians(th_ - tall)))
    b = Box(s, (x - R - 1, fy, z - R - 1), (x + R + 2, fy + 40, z + R + 2))
    r = np.hypot(b.x - x, b.z - z)
    th = np.degrees(np.arctan2(b.z - z, b.x - x))
    h = hfun(th) + 3.0 * noise.hash01(np.floor(th / 9).astype(int), 0, 0, seed=SEED + 411)
    wall = (r <= R) & (r > R - 1.6) & (b.y - fy < h)
    b.fill(wall, Gradient("y", [(fy + 3, Mix({"deepslate_bricks": 2, "cracked_deepslate_bricks": 1, "mossy_stone_bricks": 0.6})),
                                (fy + 16, Mix({"tuff_bricks": 3, "cracked_stone_bricks": 1, "polished_tuff": 1})),
                                (999, Mix({"tuff_bricks": 2, "polished_tuff": 2, "calcite": 0.4}))], jitter=1.5))
    # calcite bands (the floors that are gone) and a buttress pair on the tall side
    b.fill(wall & (r > R - 0.8) & np.isin(np.floor(b.y - fy).astype(int), (9, 18, 27)), "calcite")
    for sg in (-1, 1):
        ba = math.radians(tall + sg * 35)
        bx, bz = x + math.cos(ba) * (R + 0.8), z + math.sin(ba) * (R + 0.8)
        for k, (hh, rr_) in enumerate(((22, 1.6), (14, 2.2))):
            s.fill(shapes.cylinder((bx + math.cos(ba) * k, 0, bz + math.sin(ba) * k), rr_, fy - 2, fy + hh),
                   Mix({"deepslate_bricks": 2, "tuff_bricks": 1}), replace="air")
    # upper lancets on the tall side
    for k in (-1, 0, 1):
        wa = tall + k * 30
        db = np.radians(wrap_deg(th - wa))
        b.fill((np.abs(db * r) < 0.6) & (r > R - 2) & (b.y > fy + 20.5) & (b.y < fy + 26.5), "air")
    # the dome frame: copper ribs springing from the broken top, bent in, snapped off
    for k, off in enumerate((-40, -20, 0, 20, 40)):
        ph = math.radians(tall + off)
        base = fy + float(hfun(tall + off)) - 1.5
        span = (75, 52, 95, 60, 40)[k]
        pts = []
        for t_ in np.arange(0, span, 2.5):
            tt = math.radians(t_)
            pts.append((x + math.cos(ph) * (R - 0.8) * math.cos(tt), base + (R + 1) * math.sin(tt), z + math.sin(ph) * (R - 0.8) * math.cos(tt)))
        for q in pts:
            s.fill(shapes.sphere(q, 0.75), cu("weathered", "cut"), replace="air")
        s.fill(shapes.sphere(pts[-1], 0.9), cu("oxidized", "chiseled"))
    # door (towards the crater) and lancets
    da = np.radians(wrap_deg(th - math.degrees(ia)))
    b.fill((np.abs(da * r) < 1.6) & (r > R - 2) & (b.y > fy + 0.5) & (b.y < fy + 4.5), "air")
    for k in range(6):
        wa = math.degrees(ia) + 30 + k * 60
        db = np.radians(wrap_deg(th - wa))
        b.fill((np.abs(db * r) < 0.6) & (r > R - 2) & (b.y > fy + 3.5) & (b.y < fy + 8.5), "air")
    # inner ramp to a half floor (feet fy + 8), the perch: the broken wall is chest-high there on the crater side
    full, slab = slab_states("polished_tuff")
    path = helix_path((x, z), 3.4, math.degrees(ia) + 40, fy + 1, fy + 8, rise_per_block=0.5, direction=1, step=0.5)
    ramp(s, path, 2.2, full, slab, thick=1, carve=3, chunk=12)
    xe, ze, _ = path[-1]
    ae = math.atan2(ze - z, xe - x)
    hb = Box(s, (x - R, fy + 7, z - R), (x + R + 1, fy + 8, z + R + 1))
    rt = np.hypot(hb.x - x, hb.z - z)
    rel = (np.degrees(np.arctan2(hb.z - z, hb.x - x)) - math.degrees(ae) + 400) % 360 - 40
    hb.fill((rt <= R - 1.4) & (rel >= -20) & (rel <= 160), Mix({"spruce_planks": 2, "stripped_spruce_wood": 1}), replace="air")
    # the dome, fallen beside the tower: a cracked copper half shell resting on its rim, ribs every 45
    da_ = math.radians(a + 70)
    dx, dz = x + math.cos(da_) * 13, z + math.sin(da_) * 13
    gy = top(s, dx, dz)
    Rd = 6.5
    dome = (shapes.sphere((dx, gy - 1, dz), Rd) - shapes.sphere((dx, gy - 1, dz), Rd - 1.1)) & shapes.half_space("y", gy - 0.5, below=False)
    crack = shapes.SDF(lambda X, Y, Z: np.abs((X - dx) * 0.8 + (Z - dz) * 0.6 + 0.6 * np.sin(Y * 1.3)) - 0.8)
    s.fill(dome - crack, cu("weathered", "cut"))
    # it lies half sunk in the slope, full of earth (an air pocket under a shell on a slope is a trap)
    s.fill(shapes.sphere((dx, gy - 1, dz), Rd - 1.0) & shapes.half_space("y", gy - 0.5, below=False),
           Mix({"rooted_dirt": 2, "coarse_dirt": 2, "moss_block": 1}), replace="air")
    db = Box(s, (dx - Rd - 1, gy - 1, dz - Rd - 1), (dx + Rd + 2, gy + Rd + 1, dz + Rd + 2))
    dd = np.sqrt((db.x - dx) ** 2 + (db.y - gy + 1) ** 2 + (db.z - dz) ** 2)
    tht = np.degrees(np.arctan2(db.z - dz, db.x - dx))
    db.fill((dd <= Rd) & (dd > Rd - 1.2) & (np.abs(((tht + 360) % 45) - 22.5) > 20) & (db.y > gy - 0.5),
            cu("oxidized", "chiseled"), replace="solid")
    # the telescope, fallen across the wall: from the half floor out over the parapet to the turf
    ta = math.radians(a - 60)
    p0 = (x + math.cos(ta) * 2, fy + 9.5, z + math.sin(ta) * 2)
    tx, tz = x + math.cos(ta) * 17, z + math.sin(ta) * 17
    p1 = (tx, top(s, tx, tz) + 1.5, tz)
    s.fill(shapes.capsule(p0, p1, 1.1), cu("", "block"))
    for t in (0.25, 0.5, 0.75):
        q = tuple(p0[i] + (p1[i] - p0[i]) * t for i in range(3))
        s.fill(shapes.sphere(q, 1.6) - shapes.sphere(q, 1.0), cu("exposed", "chiseled"))
    s.fill(shapes.sphere(p1, 1.9), cu("", "chiseled"))
    # lights: lanterns on the plinth parapet stubs, one in the door
    for k in range(4):
        la = math.radians(a + 45 + 90 * k)
        lx, lz = x + math.cos(la) * 10.5, z + math.sin(la) * 10.5
        s.set(int(lx), fy + 1, int(lz), "polished_tuff_wall")
        s.set(int(lx), fy + 2, int(lz), cu("weathered", "lantern"))
    ctx["observatory"] = dict(c=(round(x, 1), round(z, 1)), floor=fy, r=R, perch=fy + 7)


# ------------------------------------------------------------------ groves
def tree(s, x, z, rng, kind):
    gy = top(s, x, z)
    ground = s.get(int(x), gy, int(z))
    if not any(k in ground for k in ("grass", "moss", "dirt", "podzol")):
        return False
    hgt = int(rng.integers(6, 10))
    log, leaves = {"oak": ("oak_log", "oak_leaves"), "dark": ("dark_oak_log", "dark_oak_leaves"),
                   "birch": ("birch_log", "birch_leaves")}[kind]
    for y in range(gy + 1, gy + 1 + hgt):
        s.set(int(x), y, int(z), f"{log}[axis=y]")
    s.set(int(x), gy, int(z), "dirt")
    # two branches
    for k in range(2):
        ba = rng.uniform(0, 2 * math.pi)
        by = gy + hgt - 2 - k
        for t in (1, 2):
            s.set(int(x + math.cos(ba) * t), by + (t == 2), int(z + math.sin(ba) * t), f"{log}[axis={'x' if abs(math.cos(ba)) > abs(math.sin(ba)) else 'z'}]")
    crown = shapes.ellipsoid((x + 0.5, gy + hgt + 0.5, z + 0.5), (3.6, 2.8, 3.6)).displace(0.9, 2.5, seed=int(x * 7 + z))
    s.fill(crown, Mix({f"{leaves}[persistent=true]": 5, "azalea_leaves[persistent=true]": 1}), replace="air")
    return True


def groves(s, ctx):
    rng = np.random.default_rng(SEED + 420)
    out = []
    for a, rr, n in GROVES:
        planted = 0
        for k in range(n * 3):
            if planted >= n:
                break
            ta = a + rng.normal(0, 7)
            tr = rr + rng.normal(0, 5)
            x, z = at_polar(ta, tr)
            kind = rng.choice(["oak", "oak", "dark", "birch"])
            if tree(s, x, z, rng, kind):
                planted += 1
        # understorey: ferns, bushes, flowers on the grass under the crowns
        cx, cz = at_polar(a, rr)
        for k in range(70):
            x, z = cx + rng.normal(0, 7), cz + rng.normal(0, 7)
            gy = top(s, x, z)
            if "grass_block" in s.get(int(x), gy, int(z)) and s.idx[int(x), gy + 1, int(z)] == 0:
                s.set(int(x), gy + 1, int(z), str(rng.choice(["fern", "short_grass", "short_grass", "bush", "lily_of_the_valley", "azalea"])))
        out.append(dict(c=(round(cx, 1), round(cz, 1)), trees=planted))
    ctx["groves"] = out


# ------------------------------------------------------------------ road, spawns, shards
def pylon(s, x, z, age="weathered", h=3):
    gy = top(s, x, z)
    s.set(int(x), gy, int(z), "polished_tuff")
    for dy in range(1, h + 1):
        s.set(int(x), gy + dy, int(z), "polished_tuff_wall" if dy < h else "chiseled_tuff")
    s.set(int(x), gy + h + 1, int(z), cu(age, "lantern"))


def road(s, ctx):
    from .terrain import LANDING
    for z in range(int(LANDING[1]) + 10, 200, 8):
        xr = C[0] + 1.5 * math.sin(z / 9)
        for sx in (-4.6, 4.6):
            pylon(s, xr + sx, z, "weathered" if (z // 8) % 2 else "oxidized")


def spawn_plaza(s, name, x, z):
    gy = disc_top(s, x, z, 5, f=lambda v: int(np.median(v)))
    s.fill(shapes.cylinder((x + 0.5, 0, z + 0.5), 5.5, gy - 3, gy + 0.5), Mix({"polished_tuff": 3, "tuff_bricks": 2, "calcite": 0.5}))
    s.fill(shapes.cylinder((x + 0.5, 0, z + 0.5), 5.5, gy + 0.5, gy + 8), "air")
    s.fill(shapes.cylinder((x + 0.5, 0, z + 0.5), 1.5, gy - 0.5, gy + 0.5), "white_concrete" if "white" in name else "black_concrete")
    s.set(x, gy, z, "lodestone")
    for k in range(4):
        a = math.radians(45 + 90 * k)
        pylon(s, x + 0.5 + math.cos(a) * 5.0, z + 0.5 + math.sin(a) * 5.0, "oxidized" if "black" in name else "", 4)
    # soften the plaza edge into the slope: a ring of coarse dirt / moss one below
    return gy + 1


def shards(s, ctx):
    rng = np.random.default_rng(SEED + 430)
    for k in range(10):
        a = rng.uniform(0, 360)
        rr = rng.uniform(62, 95)
        x, z = at_polar(a, rr)
        if any(abs(wrap_deg(a - m)) < 14 for m in (ARC[0], OBSERVATORY[0], 90, 300, 15, 105)):
            continue
        gy = top(s, x, z)
        L = rng.uniform(4, 8)
        tip = (x + rng.uniform(-2, 2), gy + L, z + rng.uniform(-2, 2))
        s.fill(shapes.capsule((x, gy - 1, z), tip, 0.9 + L * 0.06), Gradient("y", [(gy + 1, "calcite"), (999, "amethyst_block")]))
        s.set(int(tip[0]), int(tip[1]) + 1, int(tip[2]), "amethyst_cluster[facing=up]") if s.idx[int(tip[0]), int(tip[1]) + 1, int(tip[2])] == 0 else None


def build(s, ctx):
    fallen_arc(s, ctx)
    observatory(s, ctx)
    groves(s, ctx)
    road(s, ctx)
    shards(s, ctx)
    ctx["spawn_y"] = {n: spawn_plaza(s, n, x, z) for n, (x, z) in SPAWNS.items()}
