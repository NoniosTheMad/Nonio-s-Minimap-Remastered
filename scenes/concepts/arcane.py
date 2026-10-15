"""Concept B: THE ORRERY OF AST (arcane spire-castle), massing + silhouette model.

Brief
  An astronomer-mage tore the summit off a mountain and hung it over the crater it left. On the floating summit stands a
  ring-walled castle of needle towers around the Spire, a twisted tower whose copper ribs coil up to an open lantern holding
  the Focus, a giant amethyst. Three armillary rings, 120 blocks across, turn around it. A chain of amethyst shards rises
  from the geode at the bottom of the crater to the island; a floating stair spirals up from the crater rim.
  Mood: violet twilight, cold moonlight, amethyst and lantern glow. References: Tatlin's Tower (the spiral), armillary
  spheres and Jantar Mantar, Laputa (Castle in the Sky), Neuschwanstein's needle towers, real geode cross-sections.

Scale: ground ~200 across, castle (rings) 128 across, Spire tip ~y222.
Render: python -m tools.voxel render scenes/concepts/arcane.py --mood dusk
"""
import math

import numpy as np

from scenes.concepts._kit import (pointed_arch_2d, bezier, cols2d, cone, fbm2, heightmask, helix_rib, polar, ring_band, star_prism, tube,
                                  wrap_deg)
from tools.voxel import noise, shapes
from tools.voxel.palette import Gradient, Mix, Noise
from tools.voxel.scene import Scene

W, H, D = 208, 250, 208
C = (104.0, 104.0)
SEED = 4242

GROUND = 30         # highland level
CRATER_R = 50
LAKE_Y = 14
ISLAND_TOP = 108    # deck of the floating summit
ISLAND_R = 36
ISLAND_TIP = 58
SPIRE_TOP = 240
RING_C = (C[0], 160.0, C[1])
RINGS = [  # R, half width, half thickness, tilt_x, tilt_z, yaw, material
    (61, 3.0, 1.3, 16, 0, 0, "oxidized"),
    (47, 2.5, 1.2, 0, 40, 30, "weathered"),
    (33, 2.0, 1.0, 66, 0, 70, "exposed"),
]
TOWERS = [(a, 31 + (k % 2) * 2, 14 + 6 * ((k * 5) % 3), 3.0 + (k % 2) * 0.6) for k, a in enumerate(range(30, 390, 40))]

# ------------------------------------------------------------------ materials
GRASSLAND = Noise([(-0.25, Mix({"moss_block": 2, "grass_block": 3})), (0.3, "grass_block"),
                   (1, Mix({"grass_block": 3, "coarse_dirt": 1}))], scale=10, seed=SEED)
ROCK = Gradient("y", [(GROUND - 22, Mix({"deepslate": 3, "cobbled_deepslate": 1})), (GROUND - 8, Mix({"tuff": 3, "deepslate": 1})),
                      (999, Mix({"tuff": 2, "calcite": 1, "andesite": 1}))], jitter=4, jitter_scale=7, seed=SEED)
UNDERSIDE = Gradient("y", [(ISLAND_TIP + 10, Mix({"deepslate": 2, "tuff": 1, "amethyst_block": 0.2})),
                           (ISLAND_TOP - 26, Mix({"tuff": 3, "deepslate": 1, "calcite": 0.5})),
                           (ISLAND_TOP - 6, Mix({"tuff": 3, "calcite": 1})), (999, Mix({"calcite": 2, "tuff": 1}))],
                     jitter=4, jitter_scale=6, seed=SEED + 1)
MASONRY = Gradient("y", [(ISLAND_TOP + 4, Mix({"deepslate_bricks": 3, "polished_deepslate": 1})),
                         (ISLAND_TOP + 16, Mix({"tuff_bricks": 3, "polished_tuff": 1, "deepslate_bricks": 1})),
                         (ISLAND_TOP + 40, Mix({"tuff_bricks": 2, "calcite": 1, "polished_tuff": 1})),
                         (999, Mix({"calcite": 3, "smooth_quartz": 1}))], jitter=3, jitter_scale=6, seed=SEED + 2)
SPIRE_BODY = Gradient("y", [(ISLAND_TOP + 10, Mix({"polished_deepslate": 2, "deepslate_tiles": 1})),
                            (140, Mix({"deepslate_bricks": 2, "tuff_bricks": 1})),
                            (168, Mix({"tuff_bricks": 2, "polished_tuff": 1, "calcite": 1})),
                            (999, Mix({"calcite": 2, "quartz_bricks": 1}))], jitter=4, jitter_scale=8, seed=SEED + 3)
COPPER = {"oxidized": Mix({"oxidized_cut_copper": 3, "oxidized_copper": 1}),
          "weathered": Mix({"weathered_cut_copper": 3, "weathered_copper": 1}),
          "exposed": Mix({"exposed_cut_copper": 3, "exposed_copper": 1})}
RIB = Gradient("y", [(150, COPPER["oxidized"]), (185, COPPER["weathered"]), (999, COPPER["exposed"])], jitter=4, jitter_scale=6, seed=SEED + 4)
CAP = Mix({"oxidized_cut_copper": 3, "weathered_cut_copper": 1})
AMETHYST = "amethyst_block"


def ground_y(s, x, z):
    nz = np.nonzero(s.idx[int(x), :, int(z)])[0]
    return int(nz.max()) + 1 if len(nz) else 0


# ------------------------------------------------------------------ ground: highland + the wound
def ground(s):
    gx, gz = cols2d(s.shape)
    r, th = polar(s.shape, C)
    hill = GROUND + 4 * fbm2(gx, gz, 26, SEED) + 2 * fbm2(gx, gz, 9, SEED + 1)
    # crater: raised torn lip, steep wall, bowl
    lip = 9 * np.exp(-((r - CRATER_R - 3) / 6) ** 2) * (0.7 + 0.5 * noise.ridged(gx, gz, 0.0, scale=14, octaves=2, seed=SEED + 2))
    bowl = LAKE_Y - 4 + (r / CRATER_R) ** 3 * (GROUND - LAKE_Y + 6)
    h = np.where(r < CRATER_R, np.minimum(hill + lip, bowl), hill + lip)
    # shattered ground: radial plates heaved up towards the wound, chasms between them
    ang = th + 9 * fbm2(gx, gz, 30, SEED + 11)
    nplate = 11
    pid = np.floor((ang + 180) / 360 * nplate).astype(int) % nplate
    frac = ((ang + 180) / 360 * nplate) % 1
    rng = np.random.default_rng(SEED + 12)
    lift = rng.uniform(6, 18, nplate)
    tilt = np.clip(1 - (r - CRATER_R) / 46, 0, 1) ** 1.4
    h = np.where(r >= CRATER_R - 1, h + lift[pid] * tilt, h)
    chasm = (np.minimum(frac, 1 - frac) * (2 * np.pi * r / nplate) < 1.6 + 0.04 * (r - CRATER_R)) & (r > CRATER_R - 2) & (r < 92)
    h = np.where(chasm, GROUND - 30, h)
    # the Landing: a flattened shelf on the south lip where the floating stair starts
    land = np.hypot(gx - C[0], gz - (C[1] + CRATER_R + 4)) < 9
    h = np.where(land, GROUND + 6, h)
    h = np.round(h).astype(int)
    edge = 100 + 4 * fbm2(np.cos(np.radians(th)) * 30, np.sin(np.radians(th)) * 30, 14, SEED + 3)
    t = np.clip(1 - r / edge, 0, 1)
    bot = GROUND - 8 - 26 * t ** 0.6
    inside = r < edge
    m = heightmask(s.shape, np.where(inside, h, -1), np.where(inside, np.maximum(bot, 0), 999))
    y = np.arange(H)[None, :, None]
    s.fill(m, ROCK)
    top = m & ~np.roll(m, -1, axis=1)
    scar = Noise([(-0.2, Mix({"tuff": 2, "calcite": 1})), (0.25, Mix({"tuff": 1, "andesite": 1, "coarse_dirt": 1})),
                  (1, Mix({"coarse_dirt": 2, "rooted_dirt": 1, "moss_block": 1}))], scale=7, seed=SEED + 13)
    torn = (r < CRATER_R + 14 + 6 * fbm2(gx, gz, 10, SEED + 14))[:, None, :]
    s.fill(top & (r[:, None, :] > CRATER_R - 6) & (y > GROUND - 6) & ~torn, GRASSLAND)
    s.fill(top & (r[:, None, :] > CRATER_R - 6) & (y > GROUND - 6) & torn, scar)
    lake = (y <= LAKE_Y) & (y > h[:, None, :]) & (r < CRATER_R)[:, None, :]
    s.fill(lake, "water")
    return h, r, th


def geodes(s, h):
    """Broken-open geodes in the crater: basalt crust, calcite mantle, amethyst core (hollow)."""
    for (x, z, yc, R) in ((104, 104, LAKE_Y - 2, 13), (70, 78, 24, 8), (140, 124, 22, 9), (82, 140, 26, 7), (136, 70, 27, 6.5)):
        sph = lambda rr: shapes.sphere((x, yc, z), rr).displace(1.0, 5, seed=int(x))
        s.fill(sph(R), "smooth_basalt")
        s.fill(sph(R - 1.5), "calcite")
        s.fill(sph(R - 2.6), AMETHYST)
        s.fill(sph(R - 3.6), "air")
        # sliced open towards the sky
        s.fill(shapes.box((x - R - 2, yc + R * 0.35, z - R - 2), (x + R + 2, yc + R + 3, z + R + 2)) & sph(R + 0.5), "air")


# ------------------------------------------------------------------ the floating summit
def island(s):
    gx, gz = cols2d(s.shape)
    r, th = polar(s.shape, C)
    edge = ISLAND_R + 3 * fbm2(np.cos(np.radians(th)) * 20, np.sin(np.radians(th)) * 20, 8, SEED + 5)
    t = np.clip(1 - r / edge, 0, 1)
    top = ISLAND_TOP + 2 * fbm2(gx, gz, 8, SEED + 6) * (r > 22) - 0 * t
    # inverted mountain: deep jagged underside, a few hanging spurs
    spur = noise.ridged(gx, gz, 0.0, scale=9, octaves=3, seed=SEED + 7)
    bot = ISLAND_TOP - 6 - (ISLAND_TOP - ISLAND_TIP - 6) * t ** 1.3 * (0.55 + 0.6 * spur)
    inside = r < edge
    m = heightmask(s.shape, np.where(inside, np.round(top).astype(int), -1), np.where(inside, bot, 999))
    s.fill(m, UNDERSIDE)
    deck = m & ~np.roll(m, -1, axis=1)
    s.fill(deck & (r < edge - 2)[:, None, :], Noise([(-0.1, Mix({"moss_block": 1, "grass_block": 2})), (1, "grass_block")], scale=6, seed=SEED))
    # hanging amethyst stalactites
    rng = np.random.default_rng(SEED + 8)
    for _ in range(14):
        a = rng.uniform(0, 2 * math.pi); rr = rng.uniform(4, ISLAND_R - 8)
        x, z = C[0] + math.cos(a) * rr, C[1] + math.sin(a) * rr
        b = ground_bottom(s, x, z)
        if b is None:
            continue
        L = rng.uniform(5, 14)
        s.fill(cone((x, 0, z), 1.8, b - L, b + 1, 0.4) - shapes.half_space("y", b - L + 0.5), AMETHYST)
    s.fill(shapes.cylinder((C[0], 0, C[1]), 2.2, ISLAND_TIP - 10, ISLAND_TIP + 8, 0.6), AMETHYST)


def ground_bottom(s, x, z):
    col = s.idx[int(x), :, int(z)]
    nz = np.nonzero(col[60:])[0]
    return int(nz.min()) + 60 if len(nz) else None


def conduit(s):
    """The amethyst chain: floating shards from the root geode to the island tip, tightening upwards."""
    y = LAKE_Y + 6
    k = 0
    while y < ISLAND_TIP - 12:
        R = 2.6 - 1.2 * (y - LAKE_Y) / (ISLAND_TIP - LAKE_Y)
        oct_ = shapes.SDF(lambda X, Y, Z, y=y, R=R: (np.abs(X - C[0] - 0.5) + np.abs(Y - y) * 0.6 + np.abs(Z - C[1] - 0.5)) - R * 1.4,
                          ((C[0] - 5, y - 6, C[1] - 5), (C[0] + 6, y + 6, C[1] + 6)))
        s.fill(oct_, AMETHYST)
        y += 6 + (k % 2)
        k += 1


def waterfalls(s):
    """Two streams spill off the island's west edge and fall into the crater lake."""
    for a in (168, 196):
        rad = math.radians(a)
        for rr in np.arange(ISLAND_R - 6, ISLAND_R + 8, 0.5):
            x, z = int(C[0] + math.cos(rad) * rr), int(C[1] + math.sin(rad) * rr)
            col = s.idx[x, :, z]
            if not col[ISLAND_TOP - 30:ISLAND_TOP + 3].any():
                for dx in (-1, 0, 1):
                    for yy in range(LAKE_Y, ISLAND_TOP + 1):
                        if s.idx[x + dx, yy, z] == 0:
                            s.set(x + dx, yy, z, "water")
                break
        # the stream bed on the deck
        for rr in np.arange(10, ISLAND_R + 2, 0.5):
            x, z = int(C[0] + math.cos(rad) * rr), int(C[1] + math.sin(rad) * rr)
            g = ground_y(s, x, z)
            if g < ISLAND_TOP - 4:
                break
            s.set(x, g - 1, z, "water")


# ------------------------------------------------------------------ castle on the summit
def ring_wall(s):
    r, th = polar(s.shape, C)
    y = np.arange(H)[None, :, None]
    near = np.abs(r - 30) < 1.6
    merlon = (np.round(np.radians(th) * 30).astype(int) % 3 == 0)
    top = ISLAND_TOP + 9 + merlon
    m = near[:, None, :] & (y >= ISLAND_TOP - 6) & (y <= top[:, None, :])
    gate = (np.abs(wrap_deg(th - 90)) < 6)[:, None, :] & (y <= ISLAND_TOP + 6)
    s.fill(m & ~gate, MASONRY)


def needle_towers(s):
    for a, rr, ht, rad in TOWERS:
        x, z = C[0] + math.cos(math.radians(a)) * rr, C[1] + math.sin(math.radians(a)) * rr
        base = ISLAND_TOP - 10
        s.fill(shapes.cylinder((x, 0, z), rad, base, ISLAND_TOP + ht), MASONRY)
        # corbelled bell + cone cap
        s.fill(shapes.cylinder((x, 0, z), rad + 1.2, ISLAND_TOP + ht - 3, ISLAND_TOP + ht + 1, rad + 1.6), MASONRY)
        s.fill(cone((x, 0, z), rad + 2.0, ISLAND_TOP + ht + 1, ISLAND_TOP + ht + 1 + rad * 4.2, 0.2), CAP)
        # a lower corbel under the deck edge (towers grip the island)
        s.fill(cone((x, 0, z), 0.5, base - 9, base + 1, rad), UNDERSIDE)


def palace(s):
    """Two hall wings on the deck, between the wall and the Spire (north-west and east)."""
    for a0, a1 in ((200, 290), (330, 40)):
        r, th = polar(s.shape, C)
        y = np.arange(H)[None, :, None]
        span = (wrap_deg(th - (a0 + ((a1 - a0) % 360) / 2)) )
        sel = (np.abs(span) < ((a1 - a0) % 360) / 2) & (r > 15) & (r < 26)
        body = sel[:, None, :] & (y >= ISLAND_TOP - 2) & (y <= ISLAND_TOP + 14)
        s.fill(body, MASONRY)
        # roof: ridge along the arc
        roof = sel[:, None, :] & (y > ISLAND_TOP + 14) & ((np.abs(r - 20.5)[:, None, :] * 1.3 + (y - ISLAND_TOP - 14)) <= 8)
        s.fill(roof, CAP)


def spire(s):
    c = (C[0], 0, C[1])
    y0 = ISLAND_TOP - 4
    # core: tapering round tower, ends below the lantern
    s.fill(shapes.cylinder(c, 14, y0, 128, 12.5), SPIRE_BODY)              # battered foot
    s.fill(shapes.cylinder(c, 12.5, 128, 192, 6), SPIRE_BODY)
    # observatory gallery (disc + parapet) and a second smaller one
    for yc, R in ((150, 18), (178, 12)):
        s.fill(shapes.cylinder(c, R, yc - 1, yc), SPIRE_BODY)
        s.fill(cone(c, R - 0.5, yc - 7, yc - 1, 6), SPIRE_BODY)
        s.fill(shapes.cylinder(c, R, yc + 1, yc + 2) - shapes.cylinder(c, R - 1.2, yc + 1, yc + 3), "calcite")
    # copper ribs: 4 helices, one full turn, wider than the core, they leave it at the lantern and close above
    for k in range(4):
        s.fill(helix_rib(c, y0, 194, 15.5, 8.0, 0.75, k * 90, 2.0, flat=1.7), RIB)
        s.fill(helix_rib(c, 194, 222, 8.0, 1.8, 0.35, k * 90 + 270, 1.6, flat=1.4), RIB)
    # the lantern: open cage, the Focus floats in it
    s.fill(shapes.cylinder(c, 7.5, 192, 193), Mix({"calcite": 2, "exposed_cut_copper": 1}))
    focus = shapes.SDF(lambda X, Y, Z: np.abs(X - C[0]) + np.abs(Y - 205) * 0.7 + np.abs(Z - C[1]) - 6.0,
                       ((C[0] - 7, 195, C[1] - 7), (C[0] + 7, 216, C[1] + 7)))
    s.fill(focus, AMETHYST)
    s.fill(shapes.cylinder(c, 1.2, 220, SPIRE_TOP, 0.3), CAP)


def rings(s):
    for R, hw, ht, tx, tz, yaw, mat in RINGS:
        gaps = (yaw + 40, yaw + 200) if R > 50 else (yaw + 120,)
        s.fill(ring_band(RING_C, R, hw, ht, tx, tz, yaw, gaps=gaps, gap_w=9), COPPER[mat])
        # inner calcite lining (two-tone band)
        s.fill(ring_band(RING_C, R - ht - 0.6, hw * 0.6, 0.45, tx, tz, yaw, gaps=gaps, gap_w=9), "calcite")


def drifting_rocks(s):
    rng = np.random.default_rng(SEED + 9)
    for k, (a, rr, yy, R) in enumerate(((30, 52, 96, 6), (120, 58, 120, 5), (250, 50, 88, 7), (300, 62, 130, 4),
                                        (190, 64, 112, 5), (75, 46, 70, 4.5))):
        x, z = C[0] + math.cos(math.radians(a)) * rr, C[1] + math.sin(math.radians(a)) * rr
        body = shapes.ellipsoid((x, yy, z), (R, R * 1.4, R)).displace(1.2, 4, seed=k) & shapes.half_space("y", yy + R * 0.3)
        s.fill(body, UNDERSIDE)
        if k in (0, 2):  # a lone observatory tower
            s.fill(shapes.cylinder((x, 0, z), 2.2, yy, yy + 9), MASONRY)
            s.fill(cone((x, 0, z), 3.2, yy + 9, yy + 16, 0.2), CAP)


def floating_stair(s):
    """A continuous ribbon of floating steps spiralling from the Landing (south lip) to the gate, with four landings
    (small platforms with a lantern post) where the climb pauses. Under every step hangs a short stone root."""
    y_start, y_end = GROUND + 7, ISLAND_TOP
    turns = 1.25
    a_start = 90 + 360 * turns    # ends at 90 (south gate)
    n = 260
    step = Mix({"calcite": 3, "polished_tuff": 1})
    for i in range(n):
        t = i / (n - 1)
        a = math.radians(a_start - 360 * turns * t)
        rr = CRATER_R + 4 - (CRATER_R + 4 - (ISLAND_R + 4)) * t ** 0.7
        y = round(y_start + (y_end - y_start) * t)
        x, z = C[0] + math.cos(a) * rr, C[1] + math.sin(a) * rr
        s.fill(shapes.box((x - 1.6, y - 1, z - 1.6), (x + 1.6, y, z + 1.6)), step)
        if i % 4 == 0:
            s.fill(cone((x, 0, z), 0.5, y - 5, y - 1, 1.6), Mix({"tuff": 1, "deepslate": 1}))
    for t in (0.2, 0.42, 0.62, 0.82):
        a = math.radians(a_start - 360 * turns * t)
        rr = CRATER_R + 4 - (CRATER_R + 4 - (ISLAND_R + 4)) * t ** 0.7 + 3
        y = round(y_start + (y_end - y_start) * t)
        x, z = C[0] + math.cos(a) * rr, C[1] + math.sin(a) * rr
        s.fill(shapes.cylinder((x, 0, z), 4.5, y - 1, y), step)
        s.fill(cone((x, 0, z), 0.6, y - 12, y - 1, 4.5).displace(0.8, 3, seed=int(x)), UNDERSIDE)
        s.fill(shapes.cylinder((x, 0, z), 0.6, y + 1, y + 5), "calcite")
        s.set(int(x), y + 5, int(z), "lantern")


def gatehouse(s):
    """South gate: a tall pointed portal between two needle towers, nested recesses, copper crown; stair lands here."""
    zf = C[1] + 31   # outer face
    xs = np.arange(W)[:, None, None] + 0.5; ys = np.arange(H)[None, :, None]; zs = np.arange(D)[None, None, :] + 0.5
    u = xs - C[0]
    body = (np.abs(u) <= 9) & (ys >= ISLAND_TOP - 6) & (ys <= ISLAND_TOP + 20) & (zs >= zf - 6) & (zs <= zf + 1)
    s.fill(body, MASONRY)
    # stepped gable crown with a spike on every step
    for k in range(6):
        hw = 9 - k * 1.5
        s.fill((np.abs(u) <= hw) & (ys == ISLAND_TOP + 21 + k) & (zs >= zf - 5) & (zs <= zf), MASONRY)
        for sx in (-hw, hw):
            s.fill(shapes.box((C[0] + sx - 0.5, ISLAND_TOP + 21 + k, zf - 0.5), (C[0] + sx + 0.5, ISLAND_TOP + 24 + k, zf + 1.5)), "calcite")
    # nested recesses (-1 each) around a 5-wide pointed opening
    for ring, mat in ((0, "air"), (1, "polished_tuff"), (2, "calcite"), (3, "tuff_bricks")):
        hs, sp = 2.5 + ring, 7 + ring
        arch = pointed_arch_2d(u, ys - ISLAND_TOP - 1, hs, sp) & (zs >= zf - (6 if ring == 0 else 0) - 0.5 + ring * 0) & (zs <= zf + 1)
        depth = (zs >= zf + 1 - (4 - ring)) if ring else (zs >= zf - 7)
        if ring:
            s.fill(arch & (ys >= ISLAND_TOP) & depth & (zs <= zf + 1) & ~pointed_arch_2d(u, ys - ISLAND_TOP - 1, hs - 1, sp - 1), mat)
    s.fill(pointed_arch_2d(u, ys - ISLAND_TOP - 1, 2.5, 7) & (zs >= zf - 8) & (zs <= zf + 2) & (ys > ISLAND_TOP), "air")
    s.fill(pointed_arch_2d(u, ys - ISLAND_TOP - 1, 2.5, 7) & (zs >= zf - 8) & (zs <= zf + 2) & (ys == ISLAND_TOP), "polished_tuff")
    # rose oculus above the door
    s.fill(shapes.cylinder((C[0], 0, zf + 1), 3.2, 0, 1) if False else
           (((u ** 2 + (ys - ISLAND_TOP - 16) ** 2) <= 3.2 ** 2) & (zs >= zf) & (zs <= zf + 1)), "purple_stained_glass")
    for sx in (-11.5, 11.5):
        x = C[0] + sx
        s.fill(shapes.cylinder((x, 0, zf - 2), 3.4, ISLAND_TOP - 12, ISLAND_TOP + 30), MASONRY)
        s.fill(shapes.cylinder((x, 0, zf - 2), 4.6, ISLAND_TOP + 27, ISLAND_TOP + 31, 5.0), MASONRY)
        s.fill(cone((x, 0, zf - 2), 5.2, ISLAND_TOP + 31, ISLAND_TOP + 48, 0.2), CAP)
        for k in range(6):   # attached trim shafts, proud of the drum, rising past the eave
            a = math.radians(k * 60 + 30)
            px, pz = x + math.cos(a) * 3.6, zf - 2 + math.sin(a) * 3.6
            s.fill(shapes.box((px - 0.5, ISLAND_TOP - 4, pz - 0.5), (px + 0.5, ISLAND_TOP + 34, pz + 0.5)), "calcite")


def ribbing(s):
    """Detail pass: vertical calcite pilasters on the Spire core (every ~3 blocks of circumference) and on the ring
    wall (every 5), standing 1 proud; the pilasters on the wall rise 2 above the parapet as spikes."""
    r, th = polar(s.shape, C)
    y = np.arange(H)[None, :, None]
    core = np.zeros_like(r)
    # spire core radius by height, same profile as spire()
    yy = np.arange(H)
    rad = np.where(yy < 128, 14 - 1.5 * (yy - (ISLAND_TOP - 4)) / (128 - ISLAND_TOP + 4), 12.5 - 6.5 * (yy - 128) / 64)
    rad = np.where((yy >= ISLAND_TOP - 4) & (yy < 192), rad, -99)[None, :, None]
    flute = (np.round(np.radians(th) * 13).astype(int) % 3 == 0)[:, None, :] & (np.round(np.radians(th) * 13 * 3) % 3 == 0)[:, None, :]
    ang = np.radians(th)[:, None, :]
    pil = (np.abs(((ang * 24 / (2 * np.pi)) % 1) - 0.5) > 0.38)
    s.fill(pil & (r[:, None, :] >= rad - 0.2) & (r[:, None, :] <= rad + 0.9) & (y >= ISLAND_TOP), Mix({"calcite": 3, "polished_tuff": 1}))
    wpil = (np.abs(((ang * 38 / (2 * np.pi)) % 1) - 0.5) > 0.40)
    gate = (np.abs(wrap_deg(th - 90)) < 22)[:, None, :]
    s.fill(wpil & ~gate & (np.abs(r - 31.6)[:, None, :] < 0.8) & (y >= ISLAND_TOP - 6) & (y <= ISLAND_TOP + 12), "calcite")


def build():
    s = Scene((W, H, D), "concept_arcane", seed=SEED)
    h, r, th = ground(s)
    geodes(s, h)
    island(s)
    conduit(s)
    ring_wall(s)
    needle_towers(s)
    palace(s)
    spire(s)
    rings(s)
    drifting_rocks(s)
    floating_stair(s)
    gatehouse(s)
    ribbing(s)
    waterfalls(s)
    zl = int(C[1] + CRATER_R + 4)
    s.mark("spawn_approach", (104, ground_y(s, 104, 196), 196), look_at=(104, 140, 104))
    s.markers["spawn_approach"]["fov"] = 80
    s.mark("cam_landing", (98, ground_y(s, 98, zl + 7), zl + 7), look_at=(104, 150, 104))
    s.mark("cam_crater", (70, ground_y(s, 70, 132), 132), look_at=(104, 140, 104))
    s.mark("cam_gate", (104, ISLAND_TOP + 1, 146), look_at=(104, 170, 104))
    s.mark("cam_bailey", (88, ISLAND_TOP + 1, 121), look_at=(104, 180, 104))
    s.mark("cam_gallery", (104, 150, 120), look_at=(150, 150, 40))
    s.mark("cam_hero", (196, 92, 198), look_at=(104, 136, 100))
    s.markers["cam_hero"]["fov"] = 62
    s.meta["mood"] = "dusk"
    s.meta["origin"] = [-104, 20, -104]
    return s
