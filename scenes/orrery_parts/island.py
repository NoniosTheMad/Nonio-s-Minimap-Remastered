"""The floating summit: an inverted, torn mountain top under a flat deck.

Underside language (read from below, the view every crater player has):
  strata bands (calcite seams) -> a band of torn foundations just under the rim (cellars cut in half, arches, a stair
  shaft, a well) -> geode pockets breaking the rock -> stalactites (rock, dripstone, amethyst) with crystal tips ->
  mangrove-root ropes with hanging roots and pale moss -> the Root Crystal crown around the throat at the tip.
Route B lives inside: the Throat (tip) -> Root Grotto -> Root Shaft (spiral) -> Orrery Hall floor oculus."""
import math

import numpy as np

from tools.voxel import noise, shapes
from tools.voxel.palette import Gradient, Mix, Noise

from .common import (C, FLOOR, H, ISLAND_R, ISLAND_TIP, SEED, UNDERSIDE, Box, cols2d, fbm2, heightmask, wrap_deg,
                     at_polar, box_around)

TOWER_ANGLES = (30, 150, 190, 230, 270, 310, 350)      # needle towers (70/110 dropped: gate towers stand there)
BASTION_ANGLES = TOWER_ANGLES + (90,)

THROAT = (44, 64)            # carved tube at the tip (y range), r <= THROAT_R
THROAT_R = 10.0
GROTTO = (104.0, 71.0, 104.0)
GROTTO_R = (14.0, 8.0, 14.0)
GROTTO_FLOOR = 63            # top cell; feet at 64
SHAFT_R = 7.0                # Root Shaft radius (y GROTTO_FLOOR..FLOOR)
HEART_R = 2.2                # the amethyst heart column


def edge_r(th):
    """Island rim radius by angle (deg): noisy, with bastions under the towers and the gate."""
    e = ISLAND_R + 2.6 * fbm2(np.cos(np.radians(th)) * 20, np.sin(np.radians(th)) * 20, 8, SEED + 5)
    for a in BASTION_ANGLES:
        d = np.abs(wrap_deg(th - a))
        e = e + (4.5 if a == 90 else 3.0) * np.exp(-(d / (11 if a == 90 else 7)) ** 2)
    return e


def shape_fields(shape):
    gx, gz = cols2d(shape)
    r = np.hypot(gx - C[0], gz - C[1])
    th = np.degrees(np.arctan2(gz - C[1], gx - C[0]))
    edge = edge_r(th)
    t = np.clip(1 - r / edge, 0, 1)
    spur = noise.ridged(gx, gz, 0.0, scale=9, octaves=3, seed=SEED + 7)
    lobes = 0.5 + 0.5 * np.cos(np.radians(th) * 5 + 1.3 * fbm2(gx, gz, 14, SEED + 70))   # 5 hanging lobes
    # an inverted mountain: a steep cone (~50 deg) whose flanks carry five hanging ridges (lobes) and spurs;
    # the centre ends in the tip, a crown ring around the Throat
    depth = (FLOOR - 5 - ISLAND_TIP) * (t ** 1.05) * (0.52 + 0.22 * spur + 0.36 * lobes * np.clip(t * 2.2, 0, 1))
    bot = FLOOR - 5 - depth
    tip = ISLAND_TIP - 6 + np.maximum(r - 12, 0) * 2.2
    bot = np.minimum(bot, np.where(r < 22, tip, 999))
    # rim: a 2-block lip with a notched profile so the rim never reads as a ruler line
    bot = np.where(t < 0.06, FLOOR - 3 - 2 * (0.5 + 0.5 * fbm2(gx, gz, 3, SEED + 71)), bot)
    return dict(gx=gx, gz=gz, r=r, th=th, edge=edge, t=t, bot=bot, inside=r < edge)


def body(s, f):
    m = heightmask(s.shape, np.where(f["inside"], FLOOR, -1), np.where(f["inside"], np.round(f["bot"]), 999))
    s.fill(m, UNDERSIDE)
    y = np.arange(H)[None, :, None]
    # strata seams, bowed with the island (they were horizontal before the summit was torn off, now tilted ~6 deg)
    tilt = (f["gx"] - C[0]) * 0.1 + (f["gz"] - C[1]) * 0.04 + 2.0 * fbm2(f["gx"], f["gz"], 13, SEED + 72)
    band = (y + tilt[:, None, :]) % 7
    s.fill(m & (band < 1.0) & (y < FLOOR - 4), Mix({"calcite": 3, "dripstone_block": 1.5, "smooth_basalt": 0.5}))
    s.fill(m & (band >= 3.5) & (band < 4.2) & (y < FLOOR - 10), Mix({"deepslate": 1, "cobbled_deepslate": 1, "tuff": 1}))
    # the deck surface (castle paving and court come later; this is the outer lawn and rim)
    top = (y == FLOOR) & f["inside"][:, None, :]
    s.fill(top, Noise([(-0.15, Mix({"moss_block": 1, "grass_block": 2})), (1, "grass_block")], scale=6, seed=SEED))
    s.fill((y == FLOOR - 1) & f["inside"][:, None, :], Mix({"dirt": 2, "rooted_dirt": 1, "coarse_dirt": 1}))
    return m


def torn_foundations(s, f):
    """Cellars of the old summit village, cut in half when the summit tore off: brick rooms open to the air on the
    rim's underside, with arches, a half stair shaft and a well shaft."""
    rng = np.random.default_rng(SEED + 80)
    out = []
    for k, a in enumerate((205, 250, 330, 15, 125, 165)):
        e = float(edge_r(np.array([a]))[0])
        x, z = at_polar(a, e - 3.5)
        w, d, hh = rng.integers(7, 11), 5, rng.integers(6, 9)
        y1 = FLOOR - 3
        y0 = y1 - hh
        ux, uz = math.cos(math.radians(a)), math.sin(math.radians(a))
        b = Box(s, (x - 8, y0 - 2, z - 8), (x + 9, FLOOR + 1, z + 9))
        # local coordinates: along the rim (v) and outward (u)
        u = (b.x - x) * ux + (b.z - z) * uz
        v = -(b.x - x) * uz + (b.z - z) * ux
        shell = (np.abs(v) <= w / 2 + 1) & (u >= -d - 1) & (b.y >= y0 - 1) & (b.y <= y1 + 0.5)
        room = (np.abs(v) <= w / 2) & (u >= -d) & (b.y >= y0) & (b.y <= y1 - 1)
        brick = Mix({"stone_bricks": 3, "cracked_stone_bricks": 2, "mossy_stone_bricks": 1.5, "tuff_bricks": 1})
        b.fill(shell, brick)
        # the wall heads rise to the lawn (FLOOR - 1): the ledge they make under the rim is one step below the deck
        head = (np.abs(v) <= w / 2 + 1) & (u >= -d - 1) & (b.y > y1) & (b.y < FLOOR)
        b.fill(head, brick, replace="air")
        b.fill(room & (u < 6), "air")
        # vaulted ceiling: a barrel arch across the room
        arch = room & ((v / (w / 2)) ** 2 + ((b.y - (y1 - 1)) / 2.2) ** 2 > 1) & (b.y > y1 - 3)
        b.fill(arch, brick)
        # floor: old tiles; broken off at the outer edge
        b.fill((np.abs(v) <= w / 2) & (u >= -d) & (u < 1.5 + 2 * noise.hash01(b.xi, 0, b.zi, seed=k)) &
               (b.y >= y0 - 1) & (b.y < y0), Mix({"polished_andesite": 2, "andesite": 1, "cracked_stone_bricks": 1}))
        # the old well: a ladder shaft from the lawn down into the cellar (the only way in on foot)
        # (outer half of the room: the inner half lies under the ring wall), against a side wall
        ui, vi = max(0.8, 37.0 - e), w / 2 - 0.6        # outside the wall's plinth (r >= 33.5)
        lx, lz = x + ui * ux - vi * uz, z + ui * uz + vi * ux
        sx_, sz_ = -uz, ux                                                                # lateral (towards the side wall)
        ix, iz = (int(np.sign(sx_)), 0) if abs(sx_) >= abs(sz_) else (0, int(np.sign(sz_)))
        facing = {(1, 0): "west", (-1, 0): "east", (0, 1): "north", (0, -1): "south"}[(ix, iz)]
        cx, cz = int(math.floor(lx)), int(math.floor(lz))
        for yy in range(y0, FLOOR + 1):
            if s.get(cx + ix, yy, cz + iz) in ("minecraft:air", "air"):
                s.set(cx + ix, yy, cz + iz, "mossy_stone_bricks")
            s.set(cx, yy, cz, f"ladder[facing={facing}]")
        for yy in (FLOOR + 1, FLOOR + 2):
            s.set(cx, yy, cz, "air")
        s.set(cx, y0 - 1, cz, "polished_andesite")
        # a flush well rim in the lawn (nothing that blocks the narrow lawn between the wall and the edge)
        for ox in (-1, 0, 1):
            for oz in (-1, 0, 1):
                if (ox or oz) and s.get(cx + ox, FLOOR, cz + oz) not in ("minecraft:air", "air"):
                    s.set(cx + ox, FLOOR, cz + oz, "mossy_stone_bricks" if (ox + oz) % 2 else "cracked_stone_bricks")
        out.append(dict(c=(x, y0, z), a=a, w=int(w), h=int(hh), well=(cx, cz)))
    return out


def stalactites(s, f):
    """Rock and crystal stalactites under the island; the biggest ones hang from the lobes."""
    rng = np.random.default_rng(SEED + 8)
    tips = []
    bot = f["bot"]
    inside = f["inside"]
    for k in range(70):
        a = rng.uniform(0, 360)
        rr = rng.uniform(8, ISLAND_R - 3) if k % 3 else rng.uniform(12, 24)
        x, z = at_polar(a, rr)
        xi, zi = int(x), int(z)
        if not inside[xi, zi]:
            continue
        b0 = float(bot[xi, zi])
        L = rng.uniform(4, 9) if k % 4 else rng.uniform(10, 20)
        r0 = 1.2 + L * 0.12
        crystal = (k % 5 == 0)
        mat = (Gradient("y", [(b0 - L * 0.45, "amethyst_block"), (999, Mix({"calcite": 2, "amethyst_block": 1}))], jitter=1.0)
               if crystal else Gradient("y", [(b0 - L * 0.5, Mix({"dripstone_block": 3, "calcite": 1})),
                                             (999, Mix({"tuff": 2, "dripstone_block": 2, "deepslate": 1}))], jitter=1.5))
        cone = shapes.cylinder((x, 0, z), 0.45, b0 - L, b0 + 1.5, r0)
        bend = rng.uniform(-0.12, 0.12, 2)
        cone = cone.translate(0, 0, 0)
        s.fill(cone.displace(0.4, 3, seed=k), mat)
        tips.append((xi, int(round(b0 - L)), zi, crystal))
    # tips: a pointed dripstone (rock) or a downward amethyst cluster (crystal) under the lowest cell of each
    for xi, yt, zi, crystal in tips:
        col = s.idx[xi, 36:FLOOR, zi]
        nz = np.nonzero(col)[0]
        if not len(nz):
            continue
        lo = nz.min() + 36
        if s.idx[xi, lo - 1, zi] != 0:
            continue
        if crystal:
            s.set(xi, lo - 1, zi, "amethyst_cluster[facing=down]")
        else:
            s.set(xi, lo - 1, zi, "pointed_dripstone[thickness=frustum,vertical_direction=down]")
            s.set(xi, lo - 2, zi, "pointed_dripstone[thickness=tip,vertical_direction=down]")
    return tips


def root_ropes(s, f):
    """Mangrove-root ropes (the summit's old trees still hang on), ending in hanging roots / pale moss."""
    rng = np.random.default_rng(SEED + 90)
    for k in range(46):
        a = rng.uniform(0, 360)
        rr = rng.uniform(ISLAND_R - 9, ISLAND_R - 1)
        x, z = at_polar(a, rr)
        xi, zi = int(x), int(z)
        if not f["inside"][xi, zi]:
            continue
        col = s.idx[xi, 36:FLOOR, zi]
        nz = np.nonzero(col)[0]
        if not len(nz):
            continue
        y = int(nz.min()) + 36 - 1
        L = int(rng.integers(4, 13))
        dx = dz = 0
        for i in range(L):
            if s.idx[xi + dx, y - i, zi + dz] != 0:
                break
            s.set(xi + dx, y - i, zi + dz, "mangrove_roots")
            if i % 4 == 3:   # ropes wander
                dx += int(rng.integers(-1, 2)) if abs(dx) < 2 else 0
                if s.idx[xi + dx, y - i, zi + dz] == 0:
                    s.set(xi + dx, y - i, zi + dz, "mangrove_roots")
        else:
            i = L
        yb = y - i
        if s.idx[xi + dx, yb, zi + dz] == 0 and s.idx[xi + dx, yb + 1, zi + dz] != 0:
            if k % 3 == 0:
                s.set(xi + dx, yb, zi + dz, "pale_hanging_moss[tip=false]")
                if s.idx[xi + dx, yb - 1, zi + dz] == 0:
                    s.set(xi + dx, yb - 1, zi + dz, "pale_hanging_moss[tip=true]")
            else:
                s.set(xi + dx, yb, zi + dz, "hanging_roots")


def throat_grotto_shaft(s, f):
    """Route B inside the island: the Throat (open tip) -> Root Grotto -> Root Shaft -> Orrery Hall oculus.
    The amethyst heart column runs up the middle of all three."""
    cx, cz = C
    # throat: an open tube through the tip
    s.fill(shapes.cylinder((cx, 0, cz), THROAT_R, THROAT[0], THROAT[1] + 1), "air")
    # grotto: a wide lens-shaped cave, walls lined with calcite and amethyst
    g = shapes.ellipsoid(GROTTO, GROTTO_R).displace(1.2, 5, seed=SEED + 100)
    lining = shapes.ellipsoid(GROTTO, (GROTTO_R[0] + 2.2, GROTTO_R[1] + 2.2, GROTTO_R[2] + 2.2)).displace(1.2, 5, seed=SEED + 100)
    s.fill(lining & shapes.half_space("y", FLOOR - 6), Gradient("exposure", [(1.5, Mix({"amethyst_block": 2, "calcite": 2, "smooth_basalt": 1})),
                                                                          (99, "calcite")]), replace="solid")
    s.fill(g, "air")
    b = box_around(s, C, GROTTO_R[0] + 4, GROTTO_FLOOR - 4, GROTTO_FLOOR + 1)
    rr = np.hypot(b.x - cx, b.z - cz)
    ell = ((b.x - cx) / (GROTTO_R[0] + 1.5)) ** 2 + ((b.z - cz) / (GROTTO_R[2] + 1.5)) ** 2 <= 1
    b.fill(ell & (b.y < GROTTO_FLOOR + 1) & (b.y > GROTTO_FLOOR - 3) & (rr > THROAT_R),
           Mix({"calcite": 3, "smooth_basalt": 1, "amethyst_block": 1}))
    # root shaft
    s.fill(shapes.cylinder((cx, 0, cz), SHAFT_R, GROTTO_FLOOR, FLOOR + 1), "air")
    sh = box_around(s, C, SHAFT_R + 1.5, GROTTO_FLOOR + 6, FLOOR - 1)
    rr = np.hypot(sh.x - cx, sh.z - cz)
    ang = np.degrees(np.arctan2(sh.z - cz, sh.x - cx))
    rib = (np.abs(((ang + 360) % 30) - 15) > 12.5)
    sh.fill((rr > SHAFT_R) & (rr <= SHAFT_R + 1.2) & rib, Mix({"calcite": 2, "polished_tuff": 1}), replace="solid")
    sh.fill((rr > SHAFT_R) & (rr <= SHAFT_R + 1.2) & ~rib, Mix({"tuff_bricks": 3, "tuff": 1}), replace="solid")
    # the amethyst heart column
    s.fill(shapes.cylinder((cx, 0, cz), HEART_R, THROAT[0] - 4, FLOOR + 3), Mix({"amethyst_block": 5, "calcite": 0.0001}))
    # the Root Crystal crown: amethyst spikes hanging around the throat mouth
    rng = np.random.default_rng(SEED + 110)
    for k in range(12):
        a = k * 30 + rng.uniform(-8, 8)
        r0 = THROAT_R + 1.5 + rng.uniform(0, 2.5)
        x, z = at_polar(a, r0)
        L = rng.uniform(7, 15)
        y1 = ISLAND_TIP - 6
        tip = (x + (x - cx) * 0.25, y1 - L, z + (z - cz) * 0.25)
        s.fill(shapes.capsule((x, y1, z), tip, 1.3), Gradient("y", [(y1 - L * 0.6, "amethyst_block"), (999, Mix({"amethyst_block": 2, "calcite": 1}))], jitter=1))
        s.set(int(tip[0]), int(tip[1]) - 1, int(tip[2]), "amethyst_cluster[facing=down]")
    # the rim of the throat: a ring of calcite so the opening reads as made, not broken
    s.fill(shapes.cylinder((cx, 0, cz), THROAT_R + 1.6, ISLAND_TIP - 9, ISLAND_TIP - 6) - shapes.cylinder((cx, 0, cz), THROAT_R, 0, 999),
           Mix({"calcite": 2, "amethyst_block": 1}))


def build(s, ctx):
    f = shape_fields(s.shape)
    ctx["island"] = f
    body(s, f)
    ctx["foundations"] = torn_foundations(s, f)
    stalactites(s, f)
    root_ropes(s, f)
    throat_grotto_shaft(s, f)
