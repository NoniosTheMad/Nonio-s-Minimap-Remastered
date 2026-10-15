"""VHARZUL, THE EMBER THRONE: the architectural shell (concept A of castle v2, picked by the user).

Statement
  A three-horned claw of black stone rises out of a burning caldera and grips a twisted needle tower with a lava heart.

Art direction: docs/concepts/castle-v2-infernal.md (concept sheet) + docs/builds/vharzul-zones.md (interior programme).
Massing came from scenes/concepts/infernal.py; this file is the refined shell. Notes per pass: scenes/vharzul.notes.md.

Identity (and what keeps it away from the EliteCraft nether cathedral): a VOLCANO, not a cathedral.
  basalt organ pipes and grey ash, an obsidian needle and obsidian horns, star-fort geometry, and the volcanic minerals
  of 26.3: sulfur (yellow trim), cinnabar (red roofs and stains), bone (tusks, horn tips, spikes), magma and lava.
  No nether bricks, no soul fire, no red/grey cathedral grammar.

Daylight read: light ash ring -> dark basalt rim -> orange lava ring -> mid-grey fort with sulfur and bone trims ->
  black obsidian Fang. Value contrast carries the day; lava, magma and lanterns carry dusk and night.

Passes are cumulative; VHARZUL_PASS=<n> (env) stops after pass n so every pass can be rendered on its own:
  1 blockout (whole composition, landscape, approach, rooms as boxes)
  2 facades and the Maw (depth layers, gate as densest element)
  3 rooflines, spikes, tower collars, skyline
  4 palette gradients and texture mixing, light trims
  5 bridges, stairs and approaches
  6 terrain and landscape transitions
  7 fixtures, joinery, rigging (light and night read), zone shells finished
  8+ critique fixes

Run:  python -m tools.voxel render scenes/vharzul.py [--mood ember]
      python -m tools.voxel place  scenes/vharzul.py --server vharzul --pristine
"""
import math
import os

import numpy as np

from scenes.vharzul_kit import (basalt_cells, bezier, cols2d, cone, fbm2, heightmask, pointed_arch_2d, polar, star_prism,
                                tube, wrap_deg)
from tools.voxel import noise, shapes
from tools.voxel.palette import Gradient, Mix, Noise
from tools.voxel.scene import Scene

PASS = int(os.environ.get("VHARZUL_PASS", "99"))

W, H, D = 208, 214, 238
C = (104.0, 100.0)          # crater / plug / Fang axis (x, z)
CX, CZ = 104, 100
SEED = 666

PLAIN = 18          # ash plain
LAKE_Y = 34         # lava surface
LAKE_R = 50         # foot of the inner crater wall
RIM_R = 61          # rim crest
PLUG_R = 31
DECK = 58           # plug top (bailey paving); standing level DECK+1
FANG_TOP = 200
GATE_F = 38         # Maw threshold (outer) floor level; passage floor blocks at GATE_F-1
GATE_I = 46         # Maw inner end = bridge head floor
GX0, GX1 = 99, 109  # gate passage (11 wide, axis x=104)
ZF = CZ + RIM_R + 8          # Maw front face (z)
ZB = CZ + LAKE_R + 1         # Maw back (bridge head)
ZP = CZ + PLUG_R             # plug edge on the axis

STAR_PTS = (0, 60, 120, 180, 240, 300)       # star-wall points (deg; 0 = east, 90 = south)
HORNS = (0, 120, 240)
SPIRES = (60, 180, 300)
FALLS = (30, 150, 210, 330)
BREACH = 12
RIM_FANGS = [(-90, 9, 42), (-62, 7, 36), (-118, 7, 34), (-30, 6, 28), (-150, 6, 30), (45, 5, 22), (66, 6, 28),
             (114, 6, 28), (140, 5, 22), (178, 7, 32), (215, 6, 26)]   # angle, radius, height over the rim crest

# ------------------------------------------------------------------ palette (roles)
# base: basalt / deepslate masonry (mid greys)    dark focal: obsidian (Fang, horns)
# trim: sulfur bricks / polished sulfur (yellow) + bone (tusks, tips, spikes)    roof/feature: cinnabar (red mineral)
# glow: lava, magma, shroomlight, ochre froglight, lanterns    ground: tuff/andesite ash, basalt flows, mineral crusts
ASH = Noise([(-0.35, Mix({"tuff": 3, "andesite": 2, "gravel": 1})),
             (0.15, Mix({"tuff": 4, "smooth_basalt": 1, "andesite": 1})),
             (1, Mix({"andesite": 2, "tuff": 2, "dead_tube_coral_block": 1}))], scale=11, seed=SEED)
FLOW = Mix({"basalt": 3, "smooth_basalt": 2, "blackstone": 1}, seed=SEED + 40)
CRATER = Gradient("y", [(LAKE_Y + 2, Mix({"magma_block": 2, "blackstone": 2, "basalt": 1})),
                        (LAKE_Y + 7, Mix({"blackstone": 3, "magma_block": 1, "cinnabar": 1})),
                        (999, Noise([(-0.45, Mix({"sulfur": 2, "calcite": 1})), (-0.2, Mix({"cinnabar": 2, "basalt": 1})),
                                     (1, Mix({"basalt": 3, "smooth_basalt": 2, "blackstone": 1}))], scale=7, seed=SEED + 41))],
                  jitter=2.5, jitter_scale=5, seed=SEED)
UNDER = Gradient("y", [(PLAIN - 52, "obsidian"), (PLAIN - 30, Mix({"blackstone": 3, "obsidian": 1})),
                       (PLAIN - 8, Mix({"blackstone": 2, "basalt": 2})), (999, Mix({"basalt": 2, "smooth_basalt": 2}))],
                 jitter=6, jitter_scale=9, seed=SEED + 1)
WALL = Gradient("y", [(DECK - 6, Mix({"blackstone": 2, "polished_blackstone_bricks": 2, "basalt": 1})),
                      (DECK + 4, Mix({"deepslate_bricks": 3, "polished_blackstone_bricks": 1, "cracked_deepslate_bricks": 1})),
                      (999, Mix({"deepslate_bricks": 3, "tuff_bricks": 2, "polished_basalt": 1, "deepslate_tiles": 1, "cracked_deepslate_bricks": 1}))],
                jitter=2, jitter_scale=5, seed=SEED + 2)
PILASTER = Mix({"polished_basalt": 4, "basalt": 1})
TRIM = Mix({"sulfur_bricks": 3, "polished_sulfur": 1})
BONE = "bone_block"
OBSIDIAN = Noise([(-0.66, "crying_obsidian"), (1, "obsidian")], scale=4, seed=SEED + 3)
HORN = Gradient("height", [(0.30, Mix({"obsidian": 4, "crying_obsidian": 0.3})), (0.55, Mix({"obsidian": 2, "blackstone": 2})),
                           (0.74, Mix({"blackstone": 2, "basalt": 2})), (0.86, Mix({"basalt": 1, "smooth_basalt": 1, "calcite": 1})),
                           (999, BONE)], jitter=0.04, jitter_scale=5, seed=SEED + 4)
ROOF = Mix({"cinnabar_bricks": 3, "polished_cinnabar": 1})
PAVE = Mix({"polished_blackstone": 2, "polished_basalt": 1, "deepslate_tiles": 1}, seed=SEED + 5)


def pol(a, r, c=C):
    return c[0] + math.cos(math.radians(a)) * r, c[1] + math.sin(math.radians(a)) * r


def ground_y(s, x, z):
    """First air y above the topmost solid block in the column."""
    col = s.idx[int(x), :, int(z)]
    nz = np.nonzero(col)[0]
    return int(nz.max()) + 1 if len(nz) else 0


YY = np.arange(H)[None, :, None]


# ================================================================== terrain
def rim_height(theta):
    a = np.radians(theta)
    h = 44 + 5 * noise.fbm(np.cos(a) * 2.2, np.sin(a) * 2.2, 3.0, scale=1.0, octaves=3, seed=SEED)
    h += 16 * np.exp(-(wrap_deg(theta + 90) / 28) ** 2)        # the north crown
    h -= 5 * np.exp(-(wrap_deg(theta - 90) / 16) ** 2)         # gate saddle
    return h


def edge_radius(theta):
    a = np.radians(theta)
    return 95.5 + 31 * np.exp(-(wrap_deg(theta - 90) / 15) ** 2) + 6 * np.exp(-(wrap_deg(theta - 90) / 40) ** 2) \
        + 2.5 * noise.fbm(np.cos(a) * 3, np.sin(a) * 3, 7.0, scale=1.0, octaves=3, seed=SEED + 8)


FLOWS = [(150, 9.0), (228, 7.5), (-28, 8.0)]       # cooled lava tongues on the outer flank: angle, half width at the foot


def terrain(s):
    gx, gz = cols2d(s.shape)
    r, th = polar(s.shape, C)
    rim = rim_height(th)
    edge = edge_radius(th)
    foot = edge - 10
    t_in = np.clip((r - LAKE_R) / (RIM_R - LAKE_R), 0, 1)
    inner = 22 + (rim - 22) * t_in ** 0.35
    t_out = np.clip((r - RIM_R) / (foot - RIM_R), 0, 1)
    gully = noise.ridged(th / 9.0, r / 14.0, 1.0, scale=1.0, octaves=2, seed=SEED + 5)
    outer = PLAIN + (rim - PLAIN) * (1 - t_out) ** 1.7 - 3.0 * gully * (1 - t_out) * t_out * 4
    plain = PLAIN + 1.3 * fbm2(gx, gz, 13, SEED + 6) + 0.8 * fbm2(gx, gz, 5, SEED + 16)
    h = np.where(r < RIM_R, inner, np.where(r < foot, outer, plain))
    h += 1.3 * fbm2(gx, gz, 5, SEED + 7) * (r > LAKE_R - 2)
    # cooled lava tongues: lobes raised 1-3 over the flank, widening downhill, rounded fronts on the plain
    flow2d = np.zeros(h.shape, bool)
    for a0, wfoot in FLOWS:
        wig = 4 * fbm2(gx, gz, 17, SEED + int(a0) + 100)
        across = np.radians(np.abs(wrap_deg(th - a0))) * r + wig
        wdt = 3 + (wfoot - 3) * np.clip((r - RIM_R) / (foot - RIM_R), 0, 1.3)
        front = foot + 6 + 2 * fbm2(gx, gz, 6, SEED + int(a0))
        lobe = np.clip(1 - (across / wdt) ** 2, 0, 1) * (r > RIM_R + 1) * (r < front)
        th_ = 2.6 * np.sqrt(lobe) * np.clip((front - r) / 4, 0, 1)
        h = h + np.where(th_ > 0.4, np.maximum(th_, 1), 0)
        flow2d |= th_ > 0.4
    # the Breach: a V-gorge through the east rim down to the lake, then a lava channel to the edge
    dth = np.abs(wrap_deg(th - BREACH))
    width = 2.5 + 0.06 * np.clip(r - LAKE_R, 0, None)
    across = np.radians(dth) * r
    breach_floor = LAKE_Y - 1 - np.clip(r - RIM_R, 0, None) * 0.14
    v = breach_floor + np.clip(across - width, 0, None) * 2.0
    h = np.where((r > LAKE_R - 3) & (across < 30), np.minimum(h, v), h)
    # the processional corridor: cut through the south flank to the Maw threshold, then a level road to the edge
    road = (np.abs(gx - 104) < 9.5) & (gz > ZF - 2)
    road_h = np.maximum(PLAIN, GATE_F - 1 - np.clip(gz - (ZF + 1), 0, None) * 0.75)
    h = np.where(road, np.minimum(h, road_h + 1.5 * (np.abs(gx - 104) > 7)), h)
    h = np.round(h).astype(int)
    # island edge + underbelly (a floating shard of the underworld)
    t = np.clip(1 - r / edge, 0, 1)
    bot = PLAIN - 4 - 64 * t ** 0.85 * (0.6 + 0.4 * (fbm2(gx, gz, 11, SEED + 9) * 0.5 + 0.5))
    bot = np.maximum(bot, 1)
    inside = r < edge
    land = heightmask(s.shape, np.where(inside, h, -1), np.where(inside, bot, 999))
    s.fill(land & (YY < PLAIN - 3), UNDER)
    s.fill(land & (YY >= PLAIN - 3) & (r[:, None, :] >= RIM_R + 3), ASH)
    s.fill(land & (YY >= PLAIN - 3) & (r[:, None, :] < RIM_R + 3), CRATER)
    s.fill(land & (YY >= h[:, None, :] - 3) & flow2d[:, None, :], FLOW)
    # lava lake (and the breach channel)
    lake = (YY <= LAKE_Y) & (YY > np.minimum(h, 99)[:, None, :]) & (r[:, None, :] < RIM_R) & inside[:, None, :]
    s.fill(lake, "lava")
    chan = (YY == np.minimum(h, 99)[:, None, :]) & ((dth < 8)[:, None, :]) & ((r > RIM_R - 4) & (r < edge))[:, None, :] \
        & (np.radians(dth) * r < width - 0.5)[:, None, :]
    s.fill(chan, "lava")
    s.meta["_edge"] = edge
    s.meta["_flow"] = flow2d
    return h, r, th


def breach_fall(s):
    a = math.radians(BREACH)
    for k in range(-1, 2):
        for rr in np.arange(90, 112, 0.5):
            x = int(C[0] + math.cos(a) * rr - math.sin(a) * k)
            z = int(C[1] + math.sin(a) * rr + math.cos(a) * k)
            if not (0 <= x < W and 0 <= z < D):
                continue
            if not s.idx[x, :, z].any():
                for y in range(2, PLAIN - 1):
                    s.set(x, y, z, "lava")
                break


# ================================================================== the outer ring (sub-places on the ash)
def spikes_field(s, h):
    """The Field of Spears: dense in the south-east, sparse elsewhere."""
    rng = np.random.default_rng(SEED + 11)
    for i in range(130):
        dense = i < 60
        a = rng.uniform(25, 78) if dense else rng.uniform(-180, 180)
        rr = rng.uniform(RIM_R + 8, 96)
        if abs(wrap_deg(a - 90)) < 16 or abs(wrap_deg(a - BREACH)) < 9 or abs(wrap_deg(a - 180)) < 30 \
                or abs(wrap_deg(a - 235)) < 18 or abs(wrap_deg(a + 45)) < 14:
            continue
        x, z = pol(a, rr)
        if not (2 <= x < W - 2 and 2 <= z < D - 2) or rr > edge_radius(np.array(a)) - 4:
            continue
        g = h[int(x), int(z)]
        ht = rng.uniform(5, 18) * (1.3 if dense else 1)
        rad = rng.uniform(0.9, 2.3)
        lean = rng.uniform(-0.25, 0.25, 2)
        top = (x + lean[0] * ht, g + ht, z + lean[1] * ht)
        s.fill(shapes.capsule((x, g - 2, z), top, 0.4) | cone((x, 0, z), rad, g - 2, g + ht * 0.45, 0.6),
               Mix({"basalt": 3, "blackstone": 1}))


def obelisks(s, h):
    """The Teeth: a ring of obsidian obelisks under the north crown."""
    for k, a in enumerate(np.linspace(-90 - 48, -90 + 48, 7)):
        x, z = pol(a, 86)
        g = h[int(x), int(z)]
        ht = 15 + 6 * math.cos(math.radians((a + 90) * 1.8))
        s.fill(star_prism((x, 0, z), g - 3, g + ht, 4, 2.6, 1.9, 0.9, 0.6, phase_deg=a + 45), "obsidian")
        s.box((int(x) - 2, g - 1, int(z) - 2), (int(x) + 2, g, int(z) + 2), Mix({"polished_basalt": 2, "basalt": 1}))


def ribcage(s, h):
    """The Wyrm: a colossal skeleton half-buried in the west ash; the road of the north-west passes under its ribs."""
    spine = []
    for a in np.linspace(158, 214, 40):
        rr = 81 + 3 * math.sin(math.radians((a - 158) * 4))
        x, z = pol(a, rr)
        spine.append((x, h[int(x), int(z)] - 1.5, z, a))
    for i, (x, y, z, a) in enumerate(spine):
        rad = 2.1 - 1.3 * (i / len(spine))
        s.fill(shapes.sphere((x, y + 1, z), rad), BONE)
        if i % 3 == 1 and 4 <= i <= 30:
            ht = 21 - abs(i - 13) * 0.55
            span = 10 - abs(i - 13) * 0.25
            for sgn in (-1, 1):
                ox, oz = pol(a, rr_ := math.hypot(x - C[0], z - C[1]) + sgn * span)
                ex, ez = ox, oz
                mx, mz = pol(a, rr_ + sgn * 3)
                path = bezier([(x, y + 1, z), (x + (mx - x) * 0.6, y + ht, z + (mz - z) * 0.6),
                               (ex, y + ht * 0.8, ez), (ex + (ex - x) * 0.15, h[int(np.clip(ex, 0, W - 1)), int(np.clip(ez, 0, D - 1))] - 1, ez + (ez - z) * 0.15)], 22)
                for sdf in tube(path, 1.3, 0.7):
                    s.fill(sdf, BONE)
    # the skull, facing south-east toward the approach
    x, y, z, a = spine[0]
    sx, sz = pol(152, 84)
    g = h[int(sx), int(sz)]
    skull = shapes.ellipsoid((sx, g + 4, sz), (7, 6, 6)).smooth_union(shapes.ellipsoid((sx + 4, g + 1, sz + 6), (5, 3.5, 6)), 2.5)
    s.fill(skull, BONE)
    for dx in (-3, 3):
        s.fill(shapes.sphere((sx + dx, g + 6, sz + 4.5), 2.2), "air")
    s.fill(shapes.box((sx - 1, g - 1, sz + 6), (sx + 9, g + 2, sz + 13)), "air")
    for k in range(-1, 2):   # horns of the skull
        path = bezier([(sx + k * 3, g + 8, sz - 2), (sx + k * 6, g + 15, sz - 5), (sx + k * 9, g + 18, sz - 3)], 10)
        for sdf in tube(path, 1.2, 0.4):
            s.fill(sdf, BONE)


def slag_works(s, h):
    """North-west: the slag works. Three chimneys, slag heaps and a walled yard on the flank."""
    yard_c = pol(236, 80)
    x0, z0 = int(yard_c[0]) - 9, int(yard_c[1]) - 7
    g = int(np.median(h[x0:x0 + 18, z0:z0 + 14]))
    s.box((x0, g - 3, z0), (x0 + 18, g - 1, z0 + 14), PAVE)
    s.box((x0, g, z0), (x0 + 18, g + 4, z0 + 14), WALL, hollow=True)
    s.box((x0 + 1, g, z0 + 1), (x0 + 17, g + 8, z0 + 13), "air")
    for i, (dx, dz, ht) in enumerate(((3, 3, 30), (14, 4, 24), (8, 11, 34))):
        cx, cz = x0 + dx, z0 + dz
        s.fill(shapes.cylinder((cx + 0.5, 0, cz + 0.5), 2.6, g - 2, g + ht, 1.9), WALL)
        s.fill(shapes.cylinder((cx + 0.5, 0, cz + 0.5), 1.2, g + 2, g + ht + 1), "air")
    rng = np.random.default_rng(SEED + 21)
    for k in range(5):
        a, rr = rng.uniform(222, 252), rng.uniform(70, 92)
        x, z = pol(a, rr)
        gg = h[int(x), int(z)]
        s.fill(shapes.ellipsoid((x, gg - 1, z), (rng.uniform(4, 7), rng.uniform(3, 5), rng.uniform(4, 7))).displace(1.2, 3, seed=k),
               Mix({"blackstone": 3, "magma_block": 1, "basalt": 1}))


def fumaroles(s, h):
    """North-east: the sulfur vents. Crusted cones with yellow and white rings."""
    rng = np.random.default_rng(SEED + 31)
    for k in range(9):
        a, rr = rng.uniform(-62, -22), rng.uniform(68, 92)
        x, z = pol(a, rr)
        g = h[int(x), int(z)]
        ra = rng.uniform(2.5, 5)
        ht = rng.uniform(2, 6)
        s.fill(cone((x, 0, z), ra + 2.5, g - 2, g + ht, ra * 0.5), Gradient("y", [(g + ht - 1.5, Mix({"sulfur": 2, "calcite": 1, "tuff": 2})),
                                                                                (999, Mix({"sulfur": 3, "polished_sulfur": 1}))], seed=k))
        s.fill(shapes.cylinder((x, 0, z), max(0.8, ra * 0.35), g + ht - 2, g + ht + 1), "air")


# ================================================================== the plug, lake and falls
def plug(s):
    r, th = polar(s.shape, C)
    jag = PLUG_R + 2.5 * fbm2(*cols2d(s.shape), 7, SEED + 12)
    cid, n, pts = basalt_cells(s.shape, r < jag + 3, 3.1, SEED + 13)
    rng = np.random.default_rng(SEED + 14)
    pr = np.hypot(pts[:, 0] - C[0], pts[:, 1] - C[1])
    top = np.where(pr < PLUG_R - 5, DECK, DECK - (pr - (PLUG_R - 5)) * 2.6 + rng.uniform(-4, 5, len(pts)))
    top = np.where(rng.random(len(pts)) < 0.12, top + rng.uniform(3, 9, len(pts)), top)
    htop = np.where(cid >= 0, top[np.maximum(cid, 0)], -1)
    col = heightmask(s.shape, np.round(htop).astype(int), np.full(htop.shape, 8))
    s.fill(col, Gradient("y", [(LAKE_Y + 3, Mix({"magma_block": 1, "basalt": 3})), (999, Mix({"basalt": 5, "polished_basalt": 1}))],
                         jitter=2, jitter_scale=4, seed=SEED))
    for a, rr, ht in ((70, 42, 44), (200, 40, 38), (275, 44, 50), (115, 43, 34)):
        x, z = pol(a, rr)
        s.fill(cone((x, 0, z), 3.5, 12, ht, 1.2).displace(1.0, 4, seed=a), Mix({"basalt": 3, "blackstone": 1}))


def lava_falls(s):
    for a in FALLS:
        rad = math.radians(a)
        for k in (-1, 0, 1):
            for y in range(LAKE_Y, DECK - 1):
                for rr in np.arange(10, PLUG_R + 14, 0.5):
                    x = int(C[0] + math.cos(rad) * rr - math.sin(rad) * k)
                    z = int(C[1] + math.sin(rad) * rr + math.cos(rad) * k)
                    if s.idx[x, y, z] == 0:
                        s.set(x, y, z, "lava")
                        break


# ================================================================== the citadel
def star(ro, ri, y0, y1, ro1=None, ri1=None, phase=0.0, twist=0.0, power=1.0, n=6, c=C):
    return star_prism((c[0], 0, c[1]), y0, y1, n, ro, ri, ro if ro1 is None else ro1, ri if ri1 is None else ri1,
                      twist_deg=twist, phase_deg=phase, power=power)


def star_wall(s):
    outer = star(32, 22, DECK - 14, DECK + 14, 29.5, 20.5)
    inner = star(28.5, 18.5, DECK + 1, DECK + 30)
    s.fill(outer - inner, WALL)
    s.fill(star(29, 19, DECK - 3, DECK), PAVE)
    m = outer.mask(s.shape) & (YY == DECK + 14)
    s.fill(m, TRIM)


def keep(s):
    c = (C[0], 0, C[1])
    fang = star_prism(c, DECK - 6, FANG_TOP, 6, 13.5, 9.0, 1.6, 0.8, twist_deg=55, phase_deg=30, power=1.45)
    s.fill(fang, OBSIDIAN)
    # throne lantern: a star-shaped bulb at three-quarter height (the far-read glowing crown)
    s.fill(star(9.5, 6.5, 146, 166, 7.5, 5.0, phase=30 + 40, twist=10), OBSIDIAN)
    s.fill(shapes.cylinder(c, 6.0, DECK + 1, DECK + 10), "air")            # heart sanctum (base ring)
    s.fill(shapes.cylinder(c, 5.0, DECK + 1, 132), "air")                   # the hollow shaft
    s.fill(shapes.cylinder(c, 3.2, 132, 146), "air")                        # upper stair well
    s.fill(shapes.cylinder(c, 2.4, DECK - 6, 128), "lava")                  # the caged heart
    s.fill(shapes.cylinder(c, 6.2, 149, 162), "air")                        # throne room
    s.fill(shapes.cylinder(c, 6.5, 147, 148), Mix({"polished_blackstone_bricks": 2, "polished_basalt": 1}))
    for k in range(6):     # six tall arches open the throne lantern to the sky
        a = 70 + k * 60
        x, z = pol(a, 7.5)
        s.fill(shapes.capsule((x, 151.5, z), (x, 159, z), 1.7), "air")
    # slits in the valleys show the heart
    r, th = polar(s.shape, C)
    for k in range(6):
        a = 60 + k * 60
        for y0, y1 in ((DECK + 10, DECK + 30), (DECK + 36, DECK + 52), (DECK + 62, DECK + 74)):
            tw = 55 * ((np.arange(H) - (DECK - 6)) / (FANG_TOP - DECK + 6))
            band = np.abs(wrap_deg(th[:, None, :] - (a + tw[None, :, None]))) * np.pi / 180 * r[:, None, :] < 1.0
            m = band & (YY >= y0) & (YY <= y1) & (r[:, None, :] < 16)
            s.fill(m & s.match("solid") & ~s.match("lava"), "air")
    # gilded finial: three thorns at the tip
    for k in range(3):
        a = math.radians(k * 120 + 30)
        s.fill(shapes.capsule((C[0] + 0.5, FANG_TOP - 5, C[1] + 0.5), (C[0] + 0.5 + math.cos(a) * 3, FANG_TOP + 5, C[1] + 0.5 + math.sin(a) * 3), 0.6), "gold_block")


COLLARS = ((DECK + 32, 16.5, 11.5), (DECK + 58, 13.5, 9.5), (DECK + 80, 11.0, 7.5), (DECK + 110, 8.5, 6.0))


def collar_phase(yc):
    return 30 + 55 * (yc - (DECK - 6)) / (FANG_TOP - DECK + 6)


def keep_collars(s):
    for yc, ro, ri in COLLARS:
        ph = collar_phase(yc)
        s.fill(star(ro, ri, yc - 3, yc + 1, ro - 1.5, ri - 1, phase=ph), Mix({"polished_blackstone_bricks": 2, "deepslate_tiles": 1}))
        s.fill(star(ro - 0.5, ri - 0.5, yc + 2, yc + 2, phase=ph), TRIM)
        s.fill(star(ro - 2.5, ri - 2, yc - 5, yc - 4, ro - 1.5, ri - 1.5, phase=ph), "polished_blackstone_bricks")


def horn_path(a):
    u = (math.cos(math.radians(a)), math.sin(math.radians(a)))
    cp = lambda rr, y: (C[0] + u[0] * rr, y, C[1] + u[1] * rr)
    return bezier([cp(25, DECK - 4), cp(53, DECK + 18), cp(46, DECK + 56), cp(13, 116)], 46)


def horns(s):
    for a in HORNS:
        path = horn_path(a)
        tubes = tube(path, 9.0, 0.6, power=1.1)
        u = tubes[0]
        for t in tubes[1:]:
            u = u | t
        s.fill(u, Gradient("y", [(DECK + 10, Mix({"obsidian": 5, "crying_obsidian": 0.3})), (DECK + 34, Mix({"obsidian": 3, "blackstone": 1})),
                                  (DECK + 50, Mix({"blackstone": 2, "basalt": 2})), (108, Mix({"basalt": 1, "smooth_basalt": 1, "calcite": 1})),
                                  (999, BONE)], jitter=3, jitter_scale=6, seed=SEED + 4 + a))
        for i in (24,):    # one gold tribute band
            p0, p1 = path[i], path[i + 1]
            rr = 9.0 + (0.6 - 9.0) * ((i + 0.5) / 46) ** 1.1
            s.fill(shapes.capsule(p0, p1, rr + 0.7) - shapes.capsule(path[i - 1], path[i + 2], rr - 0.6), "gold_block")


def spires(s):
    for k, a in enumerate(SPIRES):
        x, z = pol(a, 26)
        top = DECK + (44, 38, 50)[k]
        s.fill(star_prism((x, 0, z), DECK - 2, top, 4, 7, 4.5, 1.5, 0.8, twist_deg=70, phase_deg=a), WALL)
        s.fill(shapes.cylinder((x, 0, z), 3.2, DECK + 1, DECK + 16), "air")


HALL = (97, 111, CZ + 12, CZ + 31)      # Forge Hall outer x0, x1, z0, z1


def hall(s):
    x0, x1, z0, z1 = HALL
    s.fill(((x0, DECK - 9, z0), (x1, DECK + 15, z1)), WALL)
    s.fill(((x0 + 2, DECK + 1, z0 + 1), (x1 - 2, DECK + 14, z1 - 2)), "air")
    gx, gz = cols2d(s.shape)
    roof = (np.abs(gx - 104.5)[:, None, :] * 1.7 + (YY - (DECK + 16)) <= 15) & (YY >= DECK + 16) \
        & ((gx >= x0 - 1) & (gx <= x1 + 2) & (gz >= z0) & (gz <= z1 + 1))[:, None, :]
    s.fill(roof, ROOF)
    s.fill(((103, DECK, z0 + 1), (105, DECK, z1 - 3)), "lava")              # lava channel down the hall floor
    s.fill(((101, DECK + 1, z1 - 1), (107, DECK + 9, z1)), "air")           # south door to the bridge
    s.fill(((101, DECK + 1, z0 - 2), (107, DECK + 9, z0 + 1)), "air")       # north door into the Fang


def bridge(s):
    """The Ember Bridge: from the Maw's inner end (GATE_I) over the lava to the Forge Hall (DECK)."""
    z_hi, z_lo = ZB, ZP
    for z in range(z_lo, z_hi + 1):
        t = (z - z_lo) / (z_hi - z_lo)
        yd = int(round(DECK - (DECK - GATE_I) * t))
        s.box((99, yd - 3, z), (109, yd, z), WALL)
        s.box((99, yd + 1, z), (99, yd + 1, z), "polished_blackstone_brick_wall")
        s.box((109, yd + 1, z), (109, yd + 1, z), "polished_blackstone_brick_wall")
        s.box((100, yd + 1, z), (108, yd + 6, z), "air")
    for zp in (z_lo + 6, z_lo + 13):
        s.fill(shapes.box((98, 12, zp - 1), (111, GATE_I + 4, zp + 2)), WALL)


def gate(s):
    """The Maw (blockout): a battered gatehouse in the rim notch, split above the arch into two jaws; bone tusks rise
    from its flanks and cross over the gap, framing the Fang."""
    if PASS >= 2:
        return maw(s)
    s.fill(((GX0, GATE_F, ZB), (GX1, GATE_I + 14, ZF + 2)), "air")
    gx, gz = cols2d(s.shape)
    batter = np.clip((GATE_F + 30 - YY) / 30, 0, 1) * 4
    ax = np.abs(gx - 104)[:, None, :]
    body = (ax < 14 + batter) & ((gz >= ZB + 2) & (gz <= ZF))[:, None, :] & (YY >= GATE_F - 12) & (YY <= GATE_F + 34)
    jaws = (ax >= 6) | (YY <= GATE_F + 18)                 # the gap between the jaws above the arch
    tops = YY <= GATE_F + 34 - (14 - ax) * 0.5             # jaw tops slope outward-down like an open mouth
    s.fill(body & jaws & tops, WALL)
    u = (gx - 104.0)[:, None, :] + 0 * YY
    v = (YY - GATE_F) + 0 * gx[:, None, :]
    mouth = pointed_arch_2d(u, v, 5.5, 8) & (YY >= GATE_F)
    s.fill(mouth & ((gz >= ZB) & (gz <= ZF + 2))[:, None, :], "air")
    # passage floor ramps up inside the throat
    for z in range(ZB, ZF + 3):
        t = (ZF - z) / (ZF - ZB)
        yf = int(round(GATE_F - 1 + (GATE_I - GATE_F) * max(0.0, min(1.0, t))))
        s.box((GX0, GATE_F - 6, z), (GX1, yf, z), PAVE)
        s.box((GX0, yf + 1, z), (GX1, yf + 10, z), "air")
    for side in (-1, 1):
        path = bezier([(104 + side * 15, GATE_F - 8, ZF - 4), (104 + side * 23, GATE_F + 26, ZF + 8),
                       (104 + side * 11, GATE_F + 48, ZF + 16), (104 - side * 6, GATE_F + 50, ZF + 10)], 36)
        for sdf in tube(path, 5.5, 0.5, power=1.1):
            s.fill(sdf, BONE)


def processional(s, h):
    """The stair from the plain to the Maw threshold: three flights with landings."""
    y = GATE_F - 1
    z = ZF + 3
    flights = 0
    while y > PLAIN and z < D - 1:
        s.box((GX0 - 1, PLAIN - 4, z), (GX1 + 1, y, z), Mix({"polished_blackstone": 3, "polished_basalt": 1}))
        s.box((GX0 - 1, y + 1, z), (GX1 + 1, y + 10, z), "air")
        z += 1
        flights += 1
        if flights % 7 == 0:
            for _ in range(2):
                s.box((GX0 - 1, PLAIN - 4, z), (GX1 + 1, y, z), Mix({"polished_blackstone": 3, "polished_basalt": 1}))
                s.box((GX0 - 1, y + 1, z), (GX1 + 1, y + 10, z), "air")
                z += 1
        y -= 1
    s.meta["_stair_foot"] = z


def barbican(s, h):
    """The hornwork across the road at the island's south tip (threshold 1): two half-bastions and a gate."""
    zf = s.meta["_stair_foot"] + 16
    g = PLAIN
    if PASS >= 2:
        return barbican2(s, zf, g)
    for side in (-1, 1):
        cx = 104 + side * 13
        s.fill(star_prism((cx, 0, zf + 3), g - 6, g + 9, 3, 9.5, 4.5, 8.5, 4.0, phase_deg=90 if side < 0 else 90), WALL)
    s.box((97, g - 4, zf), (111, g + 12, zf + 5), WALL)
    s.fill(pointed_arch_2d((np.arange(W)[:, None, None] - 104.0) + 0 * YY, (YY - g) + 0 * np.arange(D)[None, None, :], 3.5, 5)
           & (YY >= g) & ((np.arange(D) >= zf) & (np.arange(D) <= zf + 5))[None, None, :], "air")
    s.box((99, g - 3, zf), (109, g - 1, zf + 5), PAVE)
    s.meta["_barb"] = zf + 5


def road(s, h):
    zs = s.meta["_stair_foot"]
    for z in range(zs, D):
        if not s.idx[104, :, z].any():
            break
        if s.meta["_barb"] - 5 <= z <= s.meta["_barb"]:
            continue
        s.box((99, PLAIN - 3, z), (109, PLAIN - 1, z), PAVE)
        s.box((99, PLAIN, z), (109, PLAIN + 12, z), "air")


def rim_wall(s, h, r, th):
    crest = np.round(rim_height(th)).astype(int)
    near = (np.abs(r - RIM_R) < 2.2) & (np.abs(wrap_deg(th + 90)) > 26) & (np.abs(wrap_deg(th - BREACH)) > 12) \
        & (np.abs(wrap_deg(th - 90)) > 13)
    merlon = ((np.round(np.radians(th) * RIM_R)).astype(int) % 4 < 2)
    top = crest + 7 + merlon * 2
    m = near[:, None, :] & (YY >= crest[:, None, :] - 8) & (YY <= top[:, None, :])
    s.fill(m, WALL)
    for a, rad, ht in RIM_FANGS:
        rr = RIM_R + (2 if a != -90 else -1)
        x, z = pol(a, rr)
        base = rim_height(np.array(a, float))
        s.fill(star_prism((x, 0, z), float(base) - 14, float(base) + ht, 5, rad, rad * 0.62, 1.2, 0.6,
                          twist_deg=40, phase_deg=a, power=1.3), WALL)


# ================================================================== interiors (named empty rooms; decorators furnish)
ZONES = []


def zone(name, kind, box, mood, doors=(), windows=(), must=(), wall=WALL, floor=None, ceil=None, carve=True, s=None):
    """Register a room (box = interior air, inclusive, like rooms.furnish) and build its shell: walls/floor/ceiling
    are closed with `wall` wherever the surrounding mass left air, then the interior is carved."""
    x0, y0, z0, x1, y1, z1 = box
    if s is not None and carve:
        shell = np.zeros(s.shape, bool)
        shell[x0 - 1:x1 + 2, y0 - 1:y1 + 2, z0 - 1:z1 + 2] = True
        inner = np.zeros(s.shape, bool)
        inner[x0:x1 + 1, y0:y1 + 1, z0:z1 + 1] = True
        s.fill(shell & ~inner & ~s.solid(), wall)
        if floor is not None:
            s.fill(((x0, y0 - 1, z0), (x1, y0 - 1, z1)), floor)
        if ceil is not None:
            s.fill(((x0, y1 + 1, z0), (x1, y1 + 1, z1)), ceil)
        s.fill(inner, "air")
        for d in doors:
            s.fill(((d[0], d[1], d[2]), (d[0], d[1] + 2, d[2])), "air")
    ZONES.append({"name": name, "kind": kind, "box": [int(v) for v in box], "mood": mood, "doors": [list(d) for d in doors],
                  "windows": [list(w) for w in windows], "must": list(must)})


def interiors(s):
    ZONES.clear()
    x0, x1, z0, z1 = HALL
    zone("forge_hall", "hall", (x0 + 2, DECK + 1, z0 + 1, x1 - 2, DECK + 14, z1 - 2), "forge glow", s=s, carve=False,
         doors=[(104, DECK + 1, z1 - 1), (104, DECK + 1, z0)],
         must=["anvils and smithing tables in the bays", "the lava channel is the runner", "war table at the north end"])
    zone("heart_sanctum", "chapel", (int(C[0]) - 5, DECK + 1, int(C[1]) - 5, int(C[0]) + 5, DECK + 9, int(C[1]) + 5), "lava heart",
         s=s, carve=False, doors=[(104, DECK + 1, int(C[1]) + 6)], must=["caged lava column as the altar", "spiral stair start"])
    zone("throne_lantern", "hall", (int(C[0]) - 5, 149, int(C[1]) - 5, int(C[0]) + 5, 161, int(C[1]) + 5), "open crown",
         s=s, carve=False, must=["the Ember Throne facing south", "six open arches", "crucible brazier"])
    # Maw guard rooms, either side of the throat
    gy = GATE_F + 4      # the throat floor at z = ZF-8 stands at GATE_F+4
    zone("maw_guard_w", "armoury", (91, gy, ZF - 13, 96, gy + 4, ZF - 3), "guard post", s=s,
         doors=[(97, gy, ZF - 8), (98, gy, ZF - 8)], must=["weapon racks", "arrow slits to the stair"])
    zone("maw_guard_e", "bedroom", (112, gy, ZF - 13, 117, gy + 4, ZF - 3), "barracks", s=s,
         doors=[(111, gy, ZF - 8), (110, gy, ZF - 8)], must=["bunks", "chests", "slits to the stair"])
    # spire rooms
    names = (("spire_se", "lab", "alchemy"), ("spire_w", "armoury", "arsenal"), ("spire_ne", "library", "archive"))
    for (nm, kind, mood), a in zip(names, SPIRES):
        x, z = pol(a, 26)
        x, z = int(x), int(z)
        zone(nm, kind, (x - 2, DECK + 1, z - 2, x + 2, DECK + 6, z + 2), mood, s=s, doors=[], must=[mood])
    # forge undercroft under the hall
    zone("undercroft", "cellar", (99, DECK - 8, CZ + 14, 109, DECK - 3, CZ + 28), "storage and gaol", s=s,
         must=["barrels and chests in bays", "two cells with bars"])



# ================================================================== P2: facades, depth layers, the Maw
GX = np.arange(W)[:, None, None]
GZ = np.arange(D)[None, None, :]


def zr(z0, z1):
    return (GZ >= z0) & (GZ <= z1)


def arch(half, spring, y0, cx=104.0):
    """(W,H,1) pointed-arch mask in an x-y plane, floor at y0."""
    U = ((GX - cx) + 0 * YY).astype(float)
    V = ((YY - y0) + 0 * GX).astype(float)
    return pointed_arch_2d(U, V, half, spring) & (YY >= y0)


MASONRY = lambda n: any(k in n for k in ("deepslate", "tuff", "basalt", "blackstone"))


def maw(s):
    """The Maw: a demon face cut into the rim notch. Mouth = the gate arch with three stepped archivolts and bone teeth,
    brow = a machicolated gallery, eyes = two slanted lava slits behind bars, jaws = two towers split above the brow with
    the Fang between them, cheeks = battered piers, tusks = bone horns curling up from the cheeks."""
    AX = np.abs(GX - 104)
    F = GATE_F
    s.fill(((GX0, F, ZB), (GX1, GATE_I + 14, ZF + 4)), "air")
    batter = np.clip((F + 12 - YY) / 24, 0, 1) * 4
    body = (AX <= 17 + batter) & zr(ZB + 2, ZF) & (YY >= F - 14) & (YY <= F + 22)
    s.fill(body, WALL)
    # the jaws: two diamond-section towers twisting outward like the Fang, prows to the front, needle tips
    for side in (-1, 1):
        jc = (104 + side * 11.5, 0, ZF - 8)
        s.fill(star_prism(jc, F + 18, F + 60, 4, 9.5, 6.0, 1.2, 0.6, twist_deg=-side * 25, phase_deg=90, power=1.25), WALL)
        for yc, off in ((F + 34, 0.9), (F + 46, 0.7)):
            tt = ((yc - (F + 18)) / 42) ** 1.25
            ro, ri = 9.5 + (1.2 - 9.5) * tt, 6.0 + (0.6 - 6.0) * tt
            ph = 90 - side * 25 * (yc - (F + 18)) / 42
            s.fill(star_prism(jc, yc - 1, yc, 4, ro + off + 0.6, ri + off, ro + off, ri + off, phase_deg=ph),
                   Mix({"polished_blackstone_bricks": 2, "deepslate_tiles": 1}))
            s.fill(star_prism(jc, yc + 1, yc + 1, 4, ro + off * 0.6, ri + off * 0.6, ro + off * 0.6, ri + off * 0.6, phase_deg=ph), TRIM)
    # cheeks: battered piers on the face
    cheek = (AX >= 12) & (AX <= 17) & zr(ZF + 1, ZF + 3) & (YY >= F - 14) & (YY <= F + 24 - (GZ - ZF) * 2)
    s.fill(cheek, PILASTER)
    s.fill(cheek & (YY == F + 24 - (GZ - ZF) * 2), TRIM)
    # brow: machicolated gallery across the face above the mouth, corbels under it
    s.fill((AX <= 12) & zr(ZF + 1, ZF + 2) & (YY >= F + 19) & (YY <= F + 22), WALL)
    s.fill((AX <= 12) & zr(ZF + 1, ZF + 2) & (YY == F + 22), TRIM)
    s.fill((AX <= 11) & (GX % 2 == 0) & zr(ZF + 1, ZF + 1) & (YY == F + 18), "polished_blackstone_bricks")
    # the archivolts: three nested rings stepping back toward the mouth (light, mid, dark)
    s.fill((arch(10, 9.5, F) & ~arch(8.4, 9, F)) & zr(ZF + 1, ZF + 2) & (YY <= F + 19), TRIM)
    s.fill((arch(8.4, 9, F) & ~arch(7, 8.5, F)) & zr(ZF + 1, ZF + 1), PILASTER)
    s.fill((arch(7, 8.5, F) & ~arch(5.5, 8, F)) & zr(ZF, ZF), "polished_blackstone_bricks")
    mouth = arch(5.5, 8, F)
    s.fill(mouth & zr(ZB, ZF + 3), "air")
    # bone teeth hanging from the mouth's intrados, alternate lengths
    for x in range(99, 110):
        col = np.nonzero(mouth[x, :, 0])[0]
        if not len(col):
            continue
        top = int(col.max())
        ln = (3, 1, 2, 1, 4, 2, 4, 1, 2, 1, 3)[x - 99]
        for z in (ZF - 1, ZF):
            for y in range(top - ln + 1, top + 1):
                s.set(x, y, z, BONE)
    # portcullis, raised
    s.fill(mouth & zr(ZF - 3, ZF - 3) & (YY >= F + 9), "iron_bars")
    # the eyes: slanted slits, lava behind iron bars
    for side in (-1, 1):
        for k in range(6):
            x = 104 + side * (7 + k)
            y = F + 25 + k // 2
            for dy in ((0, 1) if k < 4 else (0,)):
                s.set(x, y + dy, ZF, "iron_bars")
                s.set(x, y + dy, ZF - 1, "lava")
    # passage floor ramps up inside the throat
    for z in range(ZB, ZF + 4):
        tt = (ZF - z) / (ZF - ZB)
        yf = int(round(F - 1 + (GATE_I - F) * max(0.0, min(1.0, tt))))
        s.box((GX0, F - 6, z), (GX1, yf, z), PAVE)
        s.box((GX0, yf + 1, z), (GX1, yf + 8, z), "air", replace="solid")
    # tusks: bone horns curling up and inward from the cheeks (they flank, they no longer meet)
    for side in (-1, 1):
        path = bezier([(104 + side * 15, F - 6, ZF + 2), (104 + side * 24, F + 14, ZF + 9),
                       (104 + side * 19, F + 38, ZF + 11), (104 + side * 9, F + 46, ZF + 6)], 34)
        for sdf in tube(path, 3.8, 0.5, power=1.0):
            s.fill(sdf, BONE)


def barbican2(s, zf, g):
    """Threshold 1: the Pylons. Two horned bastions flank the road, joined only by a low breastwork with a gap, so the
    Maw stays in view from the spawn; their inner faces carry the same sulfur archivolt language as the Maw."""
    AX = np.abs(GX - 104)
    zb = zf + 5
    for side in (-1, 1):
        cx = 104 + side * 13
        s.fill(star_prism((cx, 0, zf + 3), g - 7, g + 8, 3, 9.0, 4.5, 8.4, 4.2, phase_deg=90), WALL)
        s.fill(star_prism((cx, 0, zf + 3), g - 7, g - 1, 3, 10.4, 5.6, 9.6, 4.9, phase_deg=90), FLOW, replace="air")
        s.fill(star_prism((cx, 0, zf + 3), g + 8, g + 8, 3, 8.4, 4.2, 8.4, 4.2, phase_deg=90), TRIM)
        # the pylon: a twisted horn-tower on each bastion, leaning out
        s.fill(star_prism((cx + side * 1.5, 0, zf + 3), g + 8, g + 30, 4, 4.2, 2.6, 0.8, 0.4, twist_deg=side * 40, phase_deg=45,
                          power=1.2), WALL)
        s.fill(star_prism((cx + side * 1.5, 0, zf + 3), g + 9, g + 10, 4, 4.8, 3.2, 4.6, 3.0, phase_deg=45), TRIM)
    s.fill((AX >= 6) & (AX <= 8) & zr(zf + 1, zb - 1) & (YY >= g - 4) & (YY <= g + 3), WALL)
    s.fill((AX >= 6) & (AX <= 8) & zr(zf + 1, zb - 1) & (YY == g + 4), TRIM)
    s.box((99, g - 3, zf - 2), (109, g - 1, zb + 2), PAVE)
    s.meta["_barb"] = zb


def star_r(y):
    tt = np.clip((y - (DECK - 14)) / 28, 0, 1)
    return 32 - 2.5 * tt, 22 - 1.5 * tt


def star_facade(s):
    """Star wall depth stack: battered basalt plinth, buttresses on every face, a sulfur string course, machicolation
    gallery on corbels, merlons with gaps, arrow slits through to the bailey."""
    r, th = polar(s.shape, C)
    R = r[:, None, :]

    def ring(y, off, spec, cond=None):
        ro, ri = star_r(y)
        m = star(ro + off, ri + off, y, y).mask(s.shape)
        if cond is not None:
            m &= cond
        s.fill(m, spec, replace="air")
    for y in range(DECK - 20, DECK - 9):
        ring(y, 1.6 + (DECK - 9 - y) * 0.18, Mix({"basalt": 2, "polished_blackstone": 1, "blackstone": 1}))
    ring(DECK + 1, 1.0, TRIM)
    arc = np.round(np.radians(th) * 26).astype(int)
    ring(DECK + 10, 1.0, "polished_blackstone_bricks", (arc % 2 == 0)[:, None, :])
    for y in range(DECK + 11, DECK + 14):
        ring(y, 1.4, WALL)
    ring(DECK + 13, 1.4, TRIM)
    ro, ri = star_r(DECK + 14)
    merl = (star(ro + 1.4, ri + 1.4, DECK + 14, DECK + 16) - star(ro - 1.2, ri - 1.2, DECK + 14, DECK + 16)).mask(s.shape)
    pick = ((arc % 3) != 0)[:, None, :]
    s.fill(merl & pick & (YY < DECK + 16), WALL)
    s.fill(merl & pick & (YY == DECK + 16), "polished_basalt")
    # buttresses mid-face, stepping back with height
    u = np.abs(((np.radians(th) % (np.pi / 3)) / (np.pi / 3)) * 2 - 1)
    for k in range(6):
        for off in (-15, 15):
            a = k * 60 + 30 + off
            across = np.radians(np.abs(wrap_deg(th - a))) * r
            for y in range(DECK - 18, DECK + 9):
                ro_, ri_ = star_r(y)
                redge = ri_ + (ro_ - ri_) * u
                out = 3.2 - max(0, y - (DECK - 4)) * 0.35
                m = (across < 1.2) & (r < redge + out) & (r > redge - 3)
                s.fill(m[:, None, :] & (YY == y), PILASTER if y > DECK - 12 else WALL, replace="air")
    # arrow slits
    for k in range(6):
        for off in (-7, 7, -23, 23):
            a = k * 60 + 30 + off
            across = np.radians(np.abs(wrap_deg(th - a))) * r
            m = (across < 0.5)[:, None, :] & (YY >= DECK + 4) & (YY <= DECK + 7) & (R > 17) & (R < 34)
            s.fill(m & s.match(MASONRY), "air")


def fang_ribs(s):
    """Light arrises: the Fang's six twisting edges are picked out in polished basalt so the twist reads by day."""
    x0, x1, z0, z1 = 88, 121, 84, 117
    y0, y1 = DECK - 6, FANG_TOP
    xs, ys, zs = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1), np.arange(z0, z1), indexing="ij")
    tt = np.clip((ys - y0) / (y1 - y0), 0, 1)
    tp = tt ** 1.45
    ro = 13.5 + (1.6 - 13.5) * tp
    ri = 9.0 + (0.8 - 9.0) * tp
    dx, dz = xs + 0.5 - C[0], zs + 0.5 - C[1]
    rho = np.hypot(dx, dz)
    ang = np.arctan2(dz, dx) - math.radians(30) - math.radians(55) * tt
    seg = 2 * math.pi / 6
    u = np.abs(((ang % seg) / seg) * 2 - 1)
    redge = ri + (ro - ri) * u
    sub = s.idx[x0:x1, y0:y1, z0:z1]
    obs = np.isin(sub, [s.id("obsidian"), s.id("crying_obsidian")])
    rib = obs & (u > 0.84) & (rho > redge - 1.6) & (ys < 182)
    full = np.zeros(s.shape, bool)
    full[x0:x1, y0:y1, z0:z1] = rib
    s.fill(full, Mix({"polished_basalt": 3, "smooth_basalt": 1}))


def hall_facade(s):
    """Forge Hall: stepped buttress piers, an arched south door with archivolts, a gable window."""
    x0, x1, z0, z1 = HALL
    for z in range(z0 + 2, z1 - 1, 4):
        for xa, xb, outer in ((x0 - 2, x0 - 1, x0 - 2), (x1 + 1, x1 + 2, x1 + 2)):
            for y in range(DECK - 9, DECK + 14):
                s.box((xa, y, z), (xb, y, z + 1), PILASTER, replace="air")
                if y >= DECK + 8:
                    s.box((outer, y, z), (outer, y, z + 1), "air", replace=lambda n: "basalt" in n)
            s.box((xa, DECK + 13, z), (xb, DECK + 13, z + 1), TRIM)
            s.box((outer, DECK + 7, z), (outer, DECK + 7, z + 1), TRIM)
    s.fill(((x0 + 1, DECK + 1, z1 - 1), (x1 - 1, DECK + 10, z1)), WALL)
    s.fill((arch(6.2, 6.6, DECK + 1) & ~arch(5, 6.2, DECK + 1)) & zr(z1 + 1, z1 + 1), PILASTER, replace="air")
    s.fill((arch(5, 6.2, DECK + 1) & ~arch(3.8, 5.8, DECK + 1)) & zr(z1, z1 + 1), TRIM)
    s.fill(arch(3.8, 5.8, DECK + 1) & zr(z1 - 1, z1 + 1), "air")
    s.fill(arch(2.4, 2.6, DECK + 17) & zr(z1, z1 + 1), "iron_bars")
    s.fill((arch(3.4, 2.8, DECK + 17) & ~arch(2.4, 2.6, DECK + 17)) & zr(z1 + 1, z1 + 1), TRIM)


def rim_facade(s, r, th):
    """Rim wall: battered outer skirt, buttresses every 11 blocks, a sulfur string course under the merlons, caps."""
    crest = np.round(rim_height(th)).astype(int)[:, None, :]
    R = r[:, None, :]
    ok = ((np.abs(wrap_deg(th + 90)) > 26) & (np.abs(wrap_deg(th - BREACH)) > 12) & (np.abs(wrap_deg(th - 90)) > 20))[:, None, :]
    skirt = ok & (R >= RIM_R + 2.2) & (R < RIM_R + 4.6 - (YY - (crest - 10)) * 0.22) & (YY >= crest - 10) & (YY <= crest + 1)
    s.fill(skirt, Mix({"basalt": 2, "polished_blackstone": 1, "blackstone": 1}), replace="air")
    arc = (np.radians(th) * (RIM_R + 3)) % 11
    but = ok & (arc < 2.2)[:, None, :] & (R >= RIM_R + 2) & (R < RIM_R + 6 - np.clip(YY - crest, 0, None) * 0.5) \
        & (YY >= crest - 9) & (YY <= crest + 6)
    s.fill(but, PILASTER, replace="air")
    s.fill(ok & (R >= RIM_R + 2.2) & (R < RIM_R + 3.2) & (YY == crest + 6), TRIM, replace="air")
    wall = s.match(lambda n: "deepslate" in n or "tuff_bricks" in n or "polished_basalt" in n or "polished_blackstone_bricks" in n)
    near = ok & (np.abs(R - RIM_R) < 2.3)
    above = np.zeros_like(wall)
    above[:, :-1, :] = wall[:, 1:, :]
    s.fill(near & wall & ~above & (YY >= crest + 7), "polished_basalt")


# ================================================================== build
def build():
    s = Scene((W, H, D), "vharzul", seed=SEED)
    h, r, th = terrain(s)
    spikes_field(s, h)
    obelisks(s, h)
    ribcage(s, h)
    slag_works(s, h)
    fumaroles(s, h)
    plug(s)
    lava_falls(s)
    star_wall(s)
    if PASS >= 2:
        star_facade(s)
    horns(s)
    spires(s)
    keep(s)
    keep_collars(s)
    if PASS >= 2:
        fang_ribs(s)
    hall(s)
    if PASS >= 2:
        hall_facade(s)
    bridge(s)
    rim_wall(s, h, r, th)
    if PASS >= 2:
        rim_facade(s, r, th)
    gate(s)
    processional(s, h)
    barbican(s, h)
    road(s, h)
    breach_fall(s)
    interiors(s)
    cameras(s)
    s.meta.pop("_edge", None)
    s.meta.pop("_flow", None)
    s.meta["zones"] = ZONES
    s.meta["mood"] = "day"
    s.meta["origin"] = [-104, 30, -100]
    return s


def cameras(s):
    zs = s.meta.get("_stair_foot", 196)
    zsp = min(s.meta["_barb"] + 14, D - 6)
    s.mark("spawn_approach", (104, ground_y(s, 104, zsp), zsp), look_at=(104, 112, 100))
    s.markers["spawn_approach"]["fov"] = 70
    s.mark("cam_stairfoot", (104, ground_y(s, 104, zs + 1), zs + 1), look_at=(104, 70, 140))
    s.mark("cam_gate", (104, GATE_I, ZB + 1), look_at=(104, 110, 100))
    bx, bz = pol(40, 17)
    s.mark("cam_bailey", (int(bx), DECK + 1, int(bz)), look_at=(104, 150, 100))
    s.mark("cam_maw", (104, ground_y(s, 104, ZF + 16), ZF + 16), look_at=(104, GATE_F + 20, ZF))
    s.mark("cam_heart", (104, DECK + 1, CZ + 5), look_at=(104, 100, 100.5))
    s.mark("cam_hall", (104, DECK + 1, HALL[3] - 3), look_at=(104, DECK + 6, HALL[2]))
    s.mark("cam_ash_west", (14, ground_y(s, 14, 112), 112), look_at=(60, 40, 96))
    s.mark("cam_ash_ne", (166, ground_y(s, 166, 40), 40), look_at=(104, 90, 100))
    bx, bz = int(C[0] + 88 * math.cos(math.radians(40))), int(C[1] + 88 * math.sin(math.radians(40)))
    s.mark("cam_breach", (bx, ground_y(s, bx, bz), bz), look_at=(C[0] + 75, 30, C[1] + 14))
    s.mark("cam_hero", (200, 112, 206), look_at=(104, 84, 100))
    s.markers["cam_hero"]["fov"] = 55
    s.mark("cam_far", (-60, 70, 260), look_at=(104, 100, 100))
    s.markers["cam_far"]["fov"] = 45
