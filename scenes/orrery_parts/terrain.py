"""The Shattered Highland and the Wound (crater): heightfield, gullies, crater walls with a ledge, lake, geodes.

Gameplay rules baked in here:
- every gully (the chasms between heaved plates) is a walkable ravine whose floor descends gently into the crater:
  they are the paths down; nothing is a pit you can't climb out of (slopes <= 1 block per block at the mouths);
- the lake is shallow (2-4) with gentle shores; a stepping-stone causeway reaches the central geode island;
- geode grottos have a flat floor at the level of their mouth."""
import math

import numpy as np

from tools.voxel import noise, shapes
from tools.voxel.palette import Gradient, Mix, Noise

from .common import (C, CRATER_R, D, GROUND, GRASS, H, LAKE_Y, ROCK, SEED, SOIL, W, Box, cols2d, fbm2, heightmask,
                     wrap_deg)

NPLATE = 11
CRATER_FLOOR = 18          # shore / crater floor level (top block)
LAKE_IN, LAKE_OUT = 15, 31  # lake ring radii (noisy)
GEODE_C = (104.0, 104.0)
LANDING = (104.0, 104.0 + CRATER_R + 5)   # south lip shelf where the floating stair starts
LANDING_Y = GROUND + 7     # its top block


def _plates(gx, gz, r, th):
    """Plate id, fractional position across the plate and the per-plate lift."""
    ang = th + 9 * fbm2(gx, gz, 30, SEED + 11)
    u = (ang + 180) / 360 * NPLATE
    pid = np.floor(u).astype(int) % NPLATE
    frac = u % 1
    rng = np.random.default_rng(SEED + 12)
    lift = rng.uniform(5, 17, NPLATE)
    side = rng.uniform(-0.12, 0.12, NPLATE)            # each plate also rolls a little sideways
    return pid, frac, lift, side


def heights(shape=(W, H, D)):
    """2D maps: h (top block y), bot (lowest solid y), and helper fields."""
    gx, gz = cols2d(shape)
    r = np.hypot(gx - C[0], gz - C[1])
    th = np.degrees(np.arctan2(gz - C[1], gx - C[0]))
    hill = GROUND + 3.5 * fbm2(gx, gz, 26, SEED) + 1.5 * fbm2(gx, gz, 9, SEED + 1)
    pid, frac, lift, side = _plates(gx, gz, r, th)
    rr = np.maximum(r, CRATER_R)
    tilt = np.clip(1 - (rr - CRATER_R) / 46, 0, 1) ** 1.4
    lipbump = 6 * np.exp(-((rr - CRATER_R - 2) / 5) ** 2) * (0.6 + 0.5 * noise.ridged(gx, gz, 0.0, scale=14, octaves=2, seed=SEED + 2))
    plate_h = hill + lift[pid] * tilt + side[pid] * (frac - 0.5) * 2 * np.pi * rr / NPLATE * tilt + lipbump
    # gullies between plates: width grows outwards; floor descends gently into the crater
    dist_b = np.minimum(frac, 1 - frac) * (2 * np.pi * rr / NPLATE)
    halfw = 1.8 + 0.035 * (rr - CRATER_R) + 0.9 * fbm2(gx, gz, 6, SEED + 21)
    gfloor = CRATER_FLOOR + 1 + (GROUND - 5 - CRATER_FLOOR) * np.clip((r - 40) / 52, 0, 1) + 0.8 * fbm2(gx, gz, 5, SEED + 22)
    in_gully_r = (r > 36) & (r < 93)
    gully_wall = gfloor + np.maximum(dist_b - halfw, 0) * np.where(r < 47, 1.0, 3.5)   # talus at the mouth, cliffs outside
    h = np.where(in_gully_r, np.minimum(plate_h, gully_wall), plate_h)
    # crater: shore, lake bed, wall with a ledge
    lip = h.copy()
    rn = r + 3.5 * fbm2(gx, gz, 11, SEED + 30)
    t = np.clip((rn - 39) / 11, 0, 1)
    shape_t = np.where(t < 0.3, t / 0.3 * 0.42, np.where(t < 0.5, 0.42 + (t - 0.3) * 0.15, 0.45 + (t - 0.5) / 0.5 * 0.55))
    wall = CRATER_FLOOR + (lip - CRATER_FLOOR) * shape_t ** 1.0
    shore = CRATER_FLOOR - 4 + 4 * np.clip((rn - LAKE_OUT) / 7, 0, 1) + 0.7 * fbm2(gx, gz, 4, SEED + 31)
    bed = LAKE_Y - 3 - 1.2 * (0.5 + 0.5 * fbm2(gx, gz, 7, SEED + 32))
    inner_shore = LAKE_Y + 1 + (CRATER_FLOOR + 2 - LAKE_Y) * np.clip((LAKE_IN - rn) / 5, 0, 1)
    crater = np.where(rn < LAKE_IN, inner_shore, np.where(rn < LAKE_OUT, bed, np.where(rn < 39, shore, wall)))
    crater = np.where(in_gully_r & (r < CRATER_R + 2), np.minimum(crater, np.maximum(gully_wall, crater - 99)), crater)
    h = np.where(r < CRATER_R + 1, np.minimum(np.where(r < CRATER_R - 1, crater, h), np.where(r < 39, crater, wall)), h)
    # the Landing shelf on the south lip + the approach road along the axis
    dl = np.hypot(gx - LANDING[0], gz - LANDING[1])
    h = np.where(dl < 8.5, LANDING_Y, np.where(dl < 12, np.maximum(np.minimum(h, LANDING_Y + (dl - 8.5) * 0.9), LANDING_Y - (dl - 8.5) * 1.2), h))
    road = (np.abs(gx - C[0] - 1.5 * np.sin(gz / 9)) < 3.2) & (gz > LANDING[1] + 6) & (gz < 201)
    hs = h.copy()
    # smooth the road: blend towards a straight grade from the Landing to the south edge
    zz = np.clip((gz - LANDING[1] - 6) / (200 - LANDING[1] - 6), 0, 1)
    grade = LANDING_Y - 1 + (GROUND + 1 - LANDING_Y + 1) * zz
    h = np.where(road, grade + 0.4 * (hs - grade).clip(-1, 1), h)
    h = np.round(h).astype(int)
    # canvas edge: a floating fragment whose underside tapers
    edge = 100 + 4 * fbm2(np.cos(np.radians(th)) * 30, np.sin(np.radians(th)) * 30, 14, SEED + 3)
    te = np.clip(1 - r / edge, 0, 1)
    bot = (GROUND - 9 - 30 * te ** 0.55 + 4 * fbm2(gx, gz, 6, SEED + 4)).clip(0, None)
    inside = r < edge
    return dict(h=np.where(inside, h, -1), bot=np.where(inside, bot, 999), r=r, th=th, gx=gx, gz=gz,
                gully=in_gully_r & (dist_b < halfw + 0.5) & (r > 44), road=road, edge=edge, rn=rn)


def ground(s):
    f = heights(s.shape)
    h, bot, r = f["h"], f["bot"], f["r"]
    m = heightmask(s.shape, h, bot)
    s.fill(m, ROCK)
    y = np.arange(H)[None, :, None]
    # strata seams: thin calcite / dripstone bands warped by noise, visible on every cliff and gully wall
    gx, gz = f["gx"], f["gz"]
    warp = 2.5 * fbm2(gx, gz, 17, SEED + 40)
    band = ((y + warp[:, None, :]) % 9)
    s.fill(m & (band < 1.0) & (y > 10), Mix({"calcite": 3, "dripstone_block": 1, "tuff": 1}))
    s.fill(m & (band >= 4.5) & (band < 5.2) & (y > 4) & (y < GROUND - 4), Mix({"deepslate": 2, "smooth_basalt": 1}))
    # soil caps on walkable slopes; scars (gravel/coarse) on steep ones; the crater lip is torn rock
    hp = np.pad(h, 1, mode="edge")
    slope = np.max(np.stack([np.abs(h - hp[2:, 1:-1]), np.abs(h - hp[:-2, 1:-1]), np.abs(h - hp[1:-1, 2:]),
                             np.abs(h - hp[1:-1, :-2])]), 0)
    top = (y == h[:, None, :])
    torn = (r < CRATER_R + 9 + 5 * fbm2(gx, gz, 10, SEED + 14))
    gentle = (slope <= 1) & (h > LAKE_Y + 1)
    soil_ok = gentle & ~torn & (r > CRATER_R - 1)
    s.fill(top & soil_ok[:, None, :], GRASS)
    for d in (1, 2):
        s.fill((y == h[:, None, :] - d) & soil_ok[:, None, :], SOIL)
    scar = Noise([(-0.2, Mix({"tuff": 2, "calcite": 1})), (0.25, Mix({"tuff": 1, "andesite": 1, "coarse_dirt": 1, "gravel": 0.6})),
                  (1, Mix({"coarse_dirt": 2, "rooted_dirt": 1, "moss_block": 1}))], scale=7, seed=SEED + 13)
    s.fill(top & (gentle & torn & (r > 38))[:, None, :], scar)
    # crater floor: shores of gravel / calcite sand with moss patches; lake bed of clay and gravel
    shore = (r < 39) & (h >= LAKE_Y)
    s.fill(top & shore[:, None, :], Noise([(-0.25, Mix({"gravel": 2, "calcite": 1})), (0.3, Mix({"moss_block": 2, "gravel": 1})),
                                           (1, Mix({"coarse_dirt": 2, "moss_block": 1}))], scale=5, seed=SEED + 33))
    lakebed = (h < LAKE_Y) & (r < 40)
    s.fill(top & lakebed[:, None, :], Mix({"clay": 2, "gravel": 2, "mud": 1}))
    s.fill(lakebed[:, None, :] & (y > h[:, None, :]) & (y <= LAKE_Y), "water")
    # gully floors: coarse dirt + moss + gravel runs
    s.fill(top & f["gully"][:, None, :] & gentle[:, None, :], Noise([(-0.2, "moss_block"), (0.3, Mix({"coarse_dirt": 2, "gravel": 1})),
                                                                       (1, Mix({"rooted_dirt": 1, "moss_block": 1}))], scale=4, seed=SEED + 34))
    # the road: packed gravel-and-paver path, the Landing: paved
    s.fill(top & f["road"][:, None, :], Mix({"dirt_path": 3, "gravel": 1, "packed_mud": 0.5}))
    dl = np.hypot(gx - 104, gz - (104 + CRATER_R + 5))
    s.fill(top & (dl < 8.5)[:, None, :], Mix({"polished_tuff": 3, "tuff_bricks": 2, "calcite": 1}))
    return f


def geode(s, c, R, open_dir=None, open_y=None, floor_y=None, crust="smooth_basalt", core=True, seed=0):
    """A geode: basalt crust, calcite mantle, amethyst lining, hollow core. open_dir (unit x, z) cuts a mouth on that side
    down to open_y; floor_y fills the cavity bottom flat (walkable, no pit)."""
    x, y, z = c
    sph = lambda rr: shapes.sphere((x, y, z), rr).displace(0.9, 5, seed=seed)
    s.fill(sph(R), crust)
    s.fill(sph(R - 1.3), "calcite")
    s.fill(sph(R - 2.3), "amethyst_block")
    if core:
        s.fill(sph(R - 3.2), "air")
    b = Box(s, (x - R - 2, y - R - 2, z - R - 2), (x + R + 3, y + R + 3, z + R + 3))
    if open_dir is not None:
        dx, dz = open_dir
        # mouth: a wedge on the open side above open_y
        proj = (b.x - x) * dx + (b.z - z) * dz
        lat = np.abs(-(b.x - x) * dz + (b.z - z) * dx)
        mouth = (proj > R * 0.25) & (lat < R * 0.55 + (b.y - open_y) * 0.25) & (b.y >= open_y) & (b.y < y + R * 0.7)
        b.fill(mouth, "air")
    if floor_y is not None:
        inner = ((b.x - x) ** 2 + (b.y - y) ** 2 + (b.z - z) ** 2) < (R - 2.0) ** 2
        b.fill(inner & (b.y < floor_y + 1), Mix({"calcite": 2, "amethyst_block": 1, "smooth_basalt": 0.5}))
    return b


def crater_features(s, f):
    """Root geode (central island, broken open, the Geode Grotto inside), lesser geode grottos in the crater wall,
    the stepping-stone causeway."""
    gx, gy = GEODE_C
    # central island: a mound of torn rock with the root geode breaking out of it
    mound = shapes.ellipsoid((gx, LAKE_Y - 2, gy), (15, 9, 15)).displace(1.6, 6, seed=SEED + 50)
    s.fill(mound, Gradient("y", [(LAKE_Y + 1, Mix({"tuff": 2, "smooth_basalt": 1})), (99, Mix({"calcite": 1, "tuff": 2, "moss_block": 1}))],
                           jitter=1.5, jitter_scale=4, seed=SEED + 51))
    g = geode(s, (gx, LAKE_Y + 6, gy), 11.5, open_dir=(0.0, 1.0), open_y=LAKE_Y + 2, floor_y=LAKE_Y + 1, seed=SEED + 52)
    # lesser geodes in the crater wall, opening onto the shore/ledge (grottos)
    lesser = []
    # each sits so its hollow core bottoms out at the shore level: the floor inside is flush with the shore outside
    for k, (a, rad, R) in enumerate(((210, 44.5, 7.5), (330, 45, 7.0), (25, 44, 6.5), (140, 45.5, 6.0))):
        yc = CRATER_FLOOR + R - 3.4
        cx, cz = C[0] + math.cos(math.radians(a)) * rad, C[1] + math.sin(math.radians(a)) * rad
        d = (-math.cos(math.radians(a)), -math.sin(math.radians(a)))
        geode(s, (cx, yc, cz), R, open_dir=d, open_y=CRATER_FLOOR + 1, floor_y=CRATER_FLOOR, seed=SEED + 60 + k)
        lesser.append(((cx, yc, cz), R, a))
    # causeway: stepping stones from the south shore to the root geode's mouth
    for i, t in enumerate(np.linspace(0, 1, 13)):
        x = gx + 1.2 * math.sin(i * 1.3)
        z = gy + 34 - t * 22
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if abs(dx) + abs(dz) < 2 or (i % 2 == 0):
                    s.set(int(x + dx), LAKE_Y, int(z + dz), "polished_tuff")
                    s.set(int(x + dx), LAKE_Y - 1, int(z + dz), "tuff")
    return lesser


def build(s, ctx):
    f = ground(s)
    ctx["terrain"] = f
    ctx["lesser_geodes"] = crater_features(s, f)
