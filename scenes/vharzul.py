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
FANG_TOP = 207
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
if PASS >= 4:       # P4: walls are one masonry family; weather() grades them by height above their own foot
    WALL = Mix({"deepslate_bricks": 3, "tuff_bricks": 1, "deepslate_tiles": 1}, seed=SEED + 2)
PILASTER = Mix({"polished_basalt": 4, "basalt": 1})
TRIM = Mix({"sulfur_bricks": 3, "polished_sulfur": 1})
BONE = "bone_block"
OBSIDIAN = Noise([(-0.66, "crying_obsidian"), (1, "obsidian")], scale=4, seed=SEED + 3)
HORN = Gradient("height", [(0.30, Mix({"obsidian": 4, "crying_obsidian": 0.3})), (0.55, Mix({"obsidian": 2, "blackstone": 2})),
                           (0.74, Mix({"blackstone": 2, "basalt": 2})), (0.86, Mix({"basalt": 1, "smooth_basalt": 1, "calcite": 1})),
                           (999, BONE)], jitter=0.04, jitter_scale=5, seed=SEED + 4)
ROOF = Mix({"cinnabar_bricks": 3, "polished_cinnabar": 1})
PAVE = Mix({"polished_blackstone": 1, "polished_basalt": 1, "deepslate_tiles": 1, "polished_deepslate": 1}, seed=SEED + 5)


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
    if PASS >= 7:       # P7: ash dunes, long and low, fading in below the flank and sloping down to the road
        fade = np.clip((r - (RIM_R + 8)) / 16, 0, 1) * np.where(gz > ZF - 4, np.clip((np.abs(gx - 104) - 9) / 7, 0, 1), 1)
        h = h + (2.4 * np.abs(fbm2(gx, gz, 21, SEED + 17)) + 1.4) * fade
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
    if PASS >= 8:     # yard gates toward the citadel (the yard was a closed pen)
        s.box((x0 + 18, g, z0 + 6), (x0 + 18, g + 3, z0 + 8), "air")
        s.box((x0 + 8, g, z0 + 14), (x0 + 10, g + 3, z0 + 14), "air")
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
    s.fill(col, Gradient("y", [(LAKE_Y + 3, Mix({"magma_block": 1, "basalt": 3})), (999, Mix({"basalt": 5, "smooth_basalt": 1}))],
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


def band_slab(path, i, half):
    """Slab of thickness 2*half across a path at segment i (for crisp rings on tubes)."""
    mid = (np.asarray(path[i]) + np.asarray(path[i + 1])) / 2
    tg = np.asarray(path[i + 1]) - np.asarray(path[i])
    tg = tg / np.linalg.norm(tg)
    R = 14
    return shapes.SDF(lambda x, y, z: np.abs((x - mid[0]) * tg[0] + (y - mid[1]) * tg[1] + (z - mid[2]) * tg[2]) - half,
                      ((mid[0] - R, mid[1] - R, mid[2] - R), (mid[0] + R, mid[1] + R, mid[2] + R)))


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
            s.fill(band_slab(path, i, 0.9) & (shapes.capsule(path[i - 1], path[i + 2], rr + 0.8)
                                              - shapes.capsule(path[i - 2], path[i + 3], rr - 0.8)), "gold_block")


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
    zf = s.meta["_stair_foot"] + (9 if PASS >= 5 else 16)
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
        jc = (104 + side * 11.5, 0, ZF - 4)
        s.fill(star_prism(jc, F + 20, F + 60, 4, 9.5, 6.0, 1.2, 0.6, twist_deg=-side * 25, phase_deg=90, power=1.25), WALL)
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


# ================================================================== P3: rooflines, spikes, collars, skyline
def thorn(s, p0, p1, p2, r0, r1, tip_frac=0.45, base=Mix({"basalt": 2, "smooth_basalt": 1}), tip=BONE, n=12):
    """A curved spike: bezier p0->p1->p2, radius r0->r1; the last tip_frac of it in `tip`."""
    path = bezier([p0, p1, p2], n)
    parts = tube(path, r0, r1)
    k = int(len(parts) * (1 - tip_frac))
    for i, sdf in enumerate(parts):
        s.fill(sdf, base if i < k else tip)


def spires3(s):
    """Three spires, three silhouettes: the Alembic (dome + flues), the Blade (pyramid + corner thorns),
    the Bell (open belfry + twisted cinnabar needle)."""
    tiles = Mix({"deepslate_tiles": 3, "cracked_deepslate_tiles": 1})
    for k, a in enumerate(SPIRES):
        x, z = pol(a, 26)
        c = (x, 0, z)
        if k == 0:      # Alembic (SE)
            s.fill(shapes.cylinder(c, 5.2, DECK - 2, DECK + 26), WALL)
            s.fill(shapes.cylinder(c, 6.2, DECK + 24, DECK + 26), "polished_blackstone_bricks")
            s.fill(shapes.cylinder(c, 6.0, DECK + 27, DECK + 27), TRIM)
            s.fill(shapes.ellipsoid((x, DECK + 28, z), (6.4, 9, 6.4)) & shapes.box((x - 8, DECK + 28, z - 8), (x + 9, DECK + 40, z + 9)), ROOF)
            for j in range(3):
                fx, fz = x + math.cos(math.radians(a + 90 + j * 120)) * 4.6, z + math.sin(math.radians(a + 90 + j * 120)) * 4.6
                s.fill(shapes.cylinder((fx, 0, fz), 1.1, DECK + 26, DECK + 38), "polished_blackstone_bricks")
                s.set(int(fx), DECK + 38, int(fz), "polished_blackstone_brick_wall")
            s.fill(shapes.capsule((x, DECK + 36, z), (x, DECK + 46, z), 0.7), TRIM)
            s.set(int(x), DECK + 47, int(z), "gold_block")
            for y in (DECK + 6, DECK + 14):
                s.fill(shapes.cylinder(c, 5.8, y, y), TRIM)
        elif k == 1:    # Blade (W)
            s.fill(star_prism(c, DECK - 2, DECK + 30, 4, 7.5, 5.0, 6.0, 4.0, twist_deg=20, phase_deg=a), WALL)
            s.fill(star_prism(c, DECK + 28, DECK + 30, 4, 7.4, 5.0, 7.0, 4.8, twist_deg=0, phase_deg=a + 20), "polished_blackstone_bricks")
            s.fill(star_prism(c, DECK + 31, DECK + 31, 4, 7.0, 4.8, 7.0, 4.8, phase_deg=a + 20), TRIM)
            s.fill(star_prism(c, DECK + 32, DECK + 50, 4, 6.4, 4.2, 0.6, 0.4, phase_deg=a + 20, power=0.9), tiles)
            for j in range(4):
                ang = math.radians(a + 20 + j * 90)
                p0 = (x + math.cos(ang) * 5.5, DECK + 30, z + math.sin(ang) * 5.5)
                p1 = (x + math.cos(ang) * 8, DECK + 33, z + math.sin(ang) * 8)
                p2 = (x + math.cos(ang) * 8.5, DECK + 38, z + math.sin(ang) * 8.5)
                thorn(s, p0, p1, p2, 1.2, 0.45)
            s.fill(shapes.capsule((x, DECK + 49, z), (x, DECK + 53, z), 0.5), BONE)
        else:           # Bell (NE)
            s.fill(star_prism(c, DECK - 2, DECK + 34, 6, 6.8, 4.8, 5.8, 4.1, twist_deg=-15, phase_deg=a), WALL)
            ph = a - 15
            s.fill(star_prism(c, DECK + 34, DECK + 34, 6, 6.6, 4.8, 6.6, 4.8, phase_deg=ph), TRIM)
            s.fill(star_prism(c, DECK + 35, DECK + 43, 6, 5.8, 4.1, 5.8, 4.1, phase_deg=ph), WALL)
            s.fill(shapes.cylinder(c, 3.2, DECK + 35, DECK + 43), "air")
            for j in range(6):    # belfry openings in the six faces
                ang = math.radians(ph + 30 + j * 60)
                px, pz = x + math.cos(ang) * 4.6, z + math.sin(ang) * 4.6
                s.fill(shapes.capsule((px, DECK + 36.5, pz), (px, DECK + 40.5, pz), 1.3), "air")
            s.fill(star_prism(c, DECK + 44, DECK + 44, 6, 6.8, 5.0, 6.8, 5.0, phase_deg=ph), TRIM)
            s.fill(star_prism(c, DECK + 45, DECK + 56, 6, 6.2, 4.4, 0.5, 0.3, twist_deg=40, phase_deg=ph, power=0.85), ROOF)
            s.set(int(x), DECK + 56, int(z), "gold_block")
            s.set(int(x), DECK + 57, int(z), "gold_block")
        s.fill(shapes.cylinder(c, 3.2, DECK + 1, DECK + 16), "air")


def horn_ridges(s):
    """Annular ridges along each horn (ram's-horn growth rings) so they read by shadow, plus bone thorns on the outer curve."""
    for a in HORNS:
        path = horn_path(a)
        for i in range(2, 40, 3):
            rr = 9.0 + (0.6 - 9.0) * ((i + 0.5) / 46) ** 1.1
            ring = shapes.capsule(path[i], path[i + 1], rr + 0.75)
            s.fill(ring, Gradient("y", [(DECK + 22, "obsidian"), (DECK + 44, Mix({"obsidian": 1, "polished_blackstone": 1})),
                                        (108, "smooth_basalt"), (999, BONE)], seed=SEED + a), replace="air")
        u = np.array([math.cos(math.radians(a)), 0, math.sin(math.radians(a))])
        for i in (9, 15, 21):
            p = path[i]
            rr = 9.0 + (0.6 - 9.0) * ((i + 0.5) / 46) ** 1.1
            p0 = p + u * (rr - 1)
            thorn(s, tuple(p0), tuple(p0 + u * 4 + np.array([0, 2, 0])), tuple(p0 + u * 6 + np.array([0, 6, 0])), 1.4, 0.4)


def fang_crowns(s):
    """Collar thorns at every star point of every collar, a thorn crown on the throne lantern, bone needles on the Maw jaws,
    ridge thorns and pinnacles on the Forge Hall."""
    for yc, ro, ri in COLLARS:
        ph = collar_phase(yc)
        ln = 5 + ro * 0.25
        for k in range(6):
            ang = math.radians(ph + k * 60)
            ux, uz = math.cos(ang), math.sin(ang)
            p0 = (C[0] + ux * (ro - 2), yc, C[1] + uz * (ro - 2))
            p1 = (C[0] + ux * (ro + ln * 0.6), yc + ln * 0.3, C[1] + uz * (ro + ln * 0.6))
            p2 = (C[0] + ux * (ro + ln * 0.8), yc + ln, C[1] + uz * (ro + ln * 0.8))
            thorn(s, p0, p1, p2, 1.3, 0.4)
    # throne lantern crown
    s.fill(star(7.8, 5.2, 166, 166, phase=80), TRIM)
    for k in range(6):
        ang = math.radians(80 + 10 + k * 60)
        ux, uz = math.cos(ang), math.sin(ang)
        thorn(s, (C[0] + ux * 6, 165, C[1] + uz * 6), (C[0] + ux * 8.5, 169, C[1] + uz * 8.5),
              (C[0] + ux * 8, 175, C[1] + uz * 8), 1.1, 0.35, base="obsidian", tip="gold_block", tip_frac=0.3)
    # Maw jaw needles in bone
    F = GATE_F
    for side in (-1, 1):
        jc = (104 + side * 11.5, 0, ZF - 4)
        m = star_prism(jc, F + 50, F + 62, 4, 9.5, 6.0, 1.2, 0.6, phase_deg=90).mask(s.shape) & s.match(MASONRY)
        s.fill(m & (YY >= F + 50), BONE)
    # Forge Hall: ridge thorns and buttress pinnacles
    x0, x1, z0, z1 = HALL
    for z in range(z0 + 1, z1 + 1, 3):
        top = ground_y(s, 104, z)
        if top <= DECK + 34:
            s.box((104, top, z), (105, top + 1, z), BONE)
    for z in range(z0 + 2, z1 - 1, 4):
        for x in (x0 - 2, x1 + 2):
            s.box((x, DECK + 14, z), (x, DECK + 15, z + 1), "polished_basalt")
            s.box((x, DECK + 16, z), (x, DECK + 16, z + 1), "cinnabar_brick_wall")


# ================================================================== P4: palette gradients, texture mixing, light copings
MASONRY_IDS = ("deepslate_bricks", "cracked_deepslate_bricks", "deepslate_tiles", "polished_deepslate", "tuff_bricks")


def weather(s):
    """Re-material all masonry by its height above its own foot (not by world y), so every outwork gets the same read:
    dark plinth (0-2) -> deepslate body -> lighter tuff-mixed upper body; every sky-facing top edge gets a pale coping
    (polished tuff) so silhouettes and steps read in daylight; cracked patches by noise."""
    m = np.isin(s.idx, [s.id(n) for n in MASONRY_IDS])
    run = np.zeros(s.shape, np.int16)
    acc = np.zeros((W, D), np.int16)
    for y in range(H):
        acc = np.where(m[:, y], acc + 1, 0)
        run[:, y] = acc
    above = np.zeros_like(m)
    above[:, :-1] = s.solid()[:, 1:]
    plinth = m & (run <= 3)
    s.fill(plinth, Mix({"blackstone": 2, "polished_blackstone_bricks": 3, "basalt": 1}, seed=SEED + 70))
    body = m & (run > 3)
    s.fill(body, Gradient(lambda c: run[c.xs, c.ys, c.zs], [
        (9, Mix({"deepslate_bricks": 2, "cracked_deepslate_bricks": 1, "polished_blackstone_bricks": 1, "polished_deepslate": 1,
                 "deepslate_tiles": 1})),
        (16, Mix({"deepslate_bricks": 2, "deepslate_tiles": 2, "tuff_bricks": 1, "cracked_deepslate_bricks": 1, "polished_deepslate": 1})),
        (999, Noise([(-0.25, Mix({"tuff_bricks": 3, "deepslate_bricks": 1, "polished_tuff": 1})),
                     (0.3, Mix({"deepslate_bricks": 2, "tuff_bricks": 2, "deepslate_tiles": 2})),
                     (1, Mix({"deepslate_tiles": 2, "cracked_deepslate_bricks": 1, "deepslate_bricks": 2}))], scale=9, seed=SEED + 71))],
        jitter=2.5, seed=SEED + 72))
    cope = m & ~above & (run > 1)
    s.fill(cope, Mix({"polished_tuff": 3, "tuff_bricks": 1}, seed=SEED + 73))


def horn_bands(s):
    """Cinnabar growth rings on the horns' dark lower half (the red of the roofs carried onto the horns)."""
    for a in HORNS:
        path = horn_path(a)
        for i in (5, 11, 17):
            rr = 9.0 + (0.6 - 9.0) * ((i + 0.5) / 46) ** 1.1
            mid = (np.asarray(path[i]) + np.asarray(path[i + 1])) / 2
            tg = np.asarray(path[i + 1]) - np.asarray(path[i])
            tg = tg / np.linalg.norm(tg)
            slab = shapes.SDF(lambda x, y, z, m=mid, g=tg: np.abs((x - m[0]) * g[0] + (y - m[1]) * g[1] + (z - m[2]) * g[2]) - 1.1,
                              ((mid[0] - rr - 2, mid[1] - rr - 2, mid[2] - rr - 2), (mid[0] + rr + 2, mid[1] + rr + 2, mid[2] + rr + 2)))
            ring = slab & (shapes.capsule(path[i - 1], path[i + 2], rr + 1.0)
                                                         - shapes.capsule(path[i - 2], path[i + 3], rr - 0.8))
            s.fill(ring, Mix({"cinnabar_bricks": 2, "polished_cinnabar": 1}, seed=SEED + a),
                   replace=lambda n: "obsidian" in n or "blackstone" in n or "basalt" in n)


# ================================================================== P5: bridges, stairs, approaches
def lay_steps(s, x0, x1, prof, full, stair, under=None, depth=4, facing="north"):
    """Walkable stepped surface along z. prof: {z: y_top}. Top block of column z is a stair (facing = the ascending
    direction) when the next column downhill (z+1 for facing north) is exactly one lower; else a full block."""
    dz = 1 if facing == "north" else -1
    for z, yt in prof.items():
        lower = prof.get(z + dz)
        top = f"{stair}[facing={facing},half=bottom]" if (lower is not None and lower == yt - 1) else full
        if under is not None:
            s.box((x0, yt - depth, z), (x1, yt - 1, z), under)
        s.box((x0, yt, z), (x1, yt, z), top)


TREAD = Mix({"polished_tuff": 3, "tuff_bricks": 1}, seed=SEED + 80)


def processional2(s, h):
    """The Tongue: the processional stair from the plain to the Maw, three flights and landings; a cinnabar runner
    pours out of the mouth down its centre; parapets with light copings; pedestals with bone spikes at each landing."""
    prof = {}
    z, y = ZF + 1, GATE_F - 1
    for _ in range(5):          # threshold landing under the archivolts
        prof[z] = y
        z += 1
    flights = (7, 7, 6)
    landings = []
    for fi, n in enumerate(flights):
        for _ in range(n):
            y -= 1
            prof[z] = y
            z += 1
        if fi < len(flights) - 1:
            landings.append(z)
            for _ in range(3):
                prof[z] = y
                z += 1
    foot = z
    for zz, yt in prof.items():
        s.box((97, PLAIN - 5, zz), (111, yt - 1, zz), WALL)
        s.box((97, yt + 1, zz), (111, yt + 12, zz), "air")
        s.box((97, yt, zz), (97, yt, zz), WALL)
        s.box((111, yt, zz), (111, yt, zz), WALL)
        s.box((97, yt + 1, zz), (97, yt + 1, zz), "polished_tuff_wall")
        s.box((111, yt + 1, zz), (111, yt + 1, zz), "polished_tuff_wall")
    lay_steps(s, 98, 101, prof, "polished_tuff", "polished_tuff_stairs")
    lay_steps(s, 107, 110, prof, "polished_tuff", "polished_tuff_stairs")
    lay_steps(s, 102, 106, prof, "polished_cinnabar", "polished_cinnabar_stairs")
    for zl in landings:
        yt = prof[zl]
        for x0 in (93, 113):
            s.box((x0, PLAIN - 4, zl), (x0 + 2, yt + 2, zl + 2), WALL)
            s.box((x0, yt + 3, zl), (x0 + 2, yt + 3, zl + 2), TRIM)
            cx = x0 + 1.5
            thorn(s, (cx, yt + 4, zl + 1.5), (cx, yt + 7, zl + 1.0), (cx, yt + 10, zl + 0.5), 0.9, 0.35, tip_frac=0.6)
        s.box((97, yt + 1, zl), (97, yt + 1, zl + 2), "air")      # gaps in the parapets toward the pedestals
        s.box((111, yt + 1, zl), (111, yt + 1, zl + 2), "air")
    s.meta["_stair_foot"] = foot
    s.meta["_landings"] = landings


def road2(s, h):
    """The pyre road from the stair foot to the Pylons and on to the island tip: light paving with a dark kerb, spear
    posts every 5 blocks."""
    zs = s.meta["_stair_foot"]
    zb = s.meta["_barb"]
    for z in range(zs, D):
        if not s.idx[104, :, z].any() and z > zb:
            break
        s.box((97, PLAIN - 3, z), (111, PLAIN - 1, z), WALL)
        s.box((99, PLAIN - 1, z), (109, PLAIN - 1, z), TREAD)
        s.box((97, PLAIN - 1, z), (98, PLAIN - 1, z), "polished_blackstone_bricks")
        s.box((110, PLAIN - 1, z), (111, PLAIN - 1, z), "polished_blackstone_bricks")
        if not (zb - 6 <= z <= zb + 1):
            s.box((97, PLAIN, z), (111, PLAIN + 12, z), "air")
        if (z - zs) % 5 == 2 and not (zb - 7 <= z <= zb + 2):
            for x in (96, 112):
                s.box((x, PLAIN - 3, z), (x, PLAIN + 2, z), Mix({"basalt": 2, "polished_basalt": 1}))
                thorn(s, (x + 0.5, PLAIN + 3, z + 0.5), (x + 0.5, PLAIN + 4.5, z + 0.5), (x + 0.5, PLAIN + 6, z + 0.5), 0.6, 0.3,
                      tip_frac=0.5)


def bridge2(s):
    """The Ember Bridge: two pointed spans on three piers over the lava, from the Maw's throat (GATE_I) up to the Forge
    Hall door (DECK); stepped deck with stairs, parapets with merlons and copings, sulfur string course on the faces."""
    z_hall, z_maw = ZP + 1, ZB
    prof = {}
    for z in range(z_hall, z_maw + 1):
        t = (z - (z_hall + 2)) / max(1, (z_maw - 2) - (z_hall + 2))
        prof[z] = int(round(DECK - (DECK - (GATE_I - 1)) * min(1.0, max(0.0, t))))
    zs = sorted(prof)
    for i in range(len(zs) - 2, -1, -1):          # keep every step <= 1 (walkable)
        prof[zs[i]] = min(prof[zs[i]], prof[zs[i + 1]] + 1)
    spans = ((z_hall + 3, z_hall + 9), (z_hall + 12, z_maw - 1))
    piers = ((z_hall, z_hall + 2), (z_hall + 10, z_hall + 11))
    for z, yt in prof.items():
        under = 14
        for a, b in spans:
            if a <= z <= b:
                half = (b - a + 1) / 2
                u = (z - (a + b) / 2) / (half + 0.5)
                crown = yt - 3
                spring = 37
                under = int(round(spring + (crown - spring) * math.sqrt(max(0.0, 1 - u * u))))
        s.box((99, under, z), (109, yt - 1, z), WALL)
        s.box((99, yt + 1, z), (109, yt + 8, z), "air")
        s.box((99, yt, z), (99, yt + 1, z), WALL)
        s.box((109, yt, z), (109, yt + 1, z), WALL)
        if z % 2 == 0:
            s.box((99, yt + 2, z), (99, yt + 2, z), WALL)
            s.box((109, yt + 2, z), (109, yt + 2, z), WALL)
        elif PASS >= 8:   # a coping wall between the merlons: the parapet can't be hopped
            s.box((99, yt + 2, z), (99, yt + 2, z), "polished_blackstone_brick_wall")
            s.box((109, yt + 2, z), (109, yt + 2, z), "polished_blackstone_brick_wall")
        s.box((98, yt - 3, z), (98, yt - 3, z), TRIM)
        s.box((110, yt - 3, z), (110, yt - 3, z), TRIM)
    for a, b in piers:
        s.box((97, 12, a), (111, prof[a] - 4, b), WALL)
        s.box((96, 12, a), (112, LAKE_Y + 2, b), Mix({"basalt": 2, "polished_blackstone": 1}))
    if PASS >= 8:   # rungs from the outer pier ledges back up over the parapet (no stranding on a pier top)
        a = piers[1][0]
        for x, xw, f in ((98, 99, "west"), (110, 109, "east")):
            top = max(y for y in range(H) if s.idx[xw, y, a] != 0 and y < prof[a] + 4)
            for y in range(prof[a] - 3, top + 1):
                if s.idx[x, y, a] == 0:
                    s.set(x, y, a, f"ladder[facing={f}]")
    lay_steps(s, 100, 102, prof, "polished_tuff", "polished_tuff_stairs", facing="north")
    lay_steps(s, 106, 108, prof, "polished_tuff", "polished_tuff_stairs", facing="north")
    lay_steps(s, 103, 105, prof, "polished_cinnabar", "polished_cinnabar_stairs", facing="north")
    s.meta["_bridge_prof"] = prof


def throat_steps(s):
    """Smooth the Maw's rising throat with stairs (the tongue's runner continues inside)."""
    prof = {}
    for z in range(ZB + 1, ZF + 1):
        tt = (ZF - z) / (ZF - ZB)
        prof[z] = int(round(GATE_F - 1 + (GATE_I - GATE_F) * max(0.0, min(1.0, tt))))
    lay_steps(s, 99, 101, prof, "polished_tuff", "polished_tuff_stairs")
    lay_steps(s, 107, 109, prof, "polished_tuff", "polished_tuff_stairs")
    lay_steps(s, 102, 106, prof, "polished_cinnabar", "polished_cinnabar_stairs")


# ================================================================== P6: terrain transitions, the outer ring
COLUMN = Mix({"basalt": 5, "smooth_basalt": 2}, seed=SEED + 90)


def causeway(s, h, r, th):
    """The island edge becomes a crown of hexagonal basalt columns (echoing the plug's organ pipes): column tops step up
    toward the brink (a palisade of shards along the edge) and hang below it as organ pipes of uneven length, so the
    cliff reads as a curtain of columns instead of an extruded wall. Dark blackstone joints between cells.
    Only raises the ground (never digs): no pits. Returns the updated heightmap."""
    edge = s.meta["_edge"]
    d = edge - r                                                    # depth inside the edge
    rng = np.random.default_rng(SEED + 91)
    region = (d > -2.5) & (d < 15)
    cid, n, pts = basalt_cells(s.shape, region, 3.0, SEED + 92)
    pr = np.hypot(pts[:, 0] - C[0], pts[:, 1] - C[1])
    pth = np.degrees(np.arctan2(pts[:, 1] - C[1], pts[:, 0] - C[0]))
    pd = edge_radius(pth) - pr                                      # cell-centre depth
    keep = (pd > -1.2) | (rng.random(n) < 0.35)                     # ragged outline
    road = (np.abs(cols2d(s.shape)[0] - 104) < 10) & (cols2d(s.shape)[1] > ZF)
    raise_ = np.where(pd < 3.0, rng.integers(2, 7, n), np.where(pd < 8, rng.integers(0, 2, n), (rng.random(n) < 0.25).astype(int)))
    hang = np.clip(1 - pd / 15, 0, 1) * (rng.uniform(4, 34, n) + 18 * (rng.random(n) < 0.15)) + rng.uniform(0, 4, n)
    m = cid >= 0
    ci = np.where(m, cid, 0)
    ok = m & keep[ci]
    # ground under each cell: the cell's median-ish ground (its centre column), so tops are flat per cell
    cx = np.clip(np.round(pts[:, 0]).astype(int), 0, W - 1)
    cz = np.clip(np.round(pts[:, 1]).astype(int), 0, D - 1)
    cg = np.maximum(h[cx, cz], PLAIN)
    top = np.where(ok, np.where(road, h, np.maximum(h, cg[ci] + raise_[ci])), -1)
    bot = np.where(ok, PLAIN - 6 - np.round(hang[ci]), 999)
    col = heightmask(s.shape, top, bot)
    s.fill(col, COLUMN)
    joint = np.zeros(m.shape, bool)
    joint[:-1] |= cid[:-1] != cid[1:]
    joint[:, :-1] |= cid[:, :-1] != cid[:, 1:]
    s.fill(col & joint[:, None, :] & (YY < top[:, None, :] - 1) & (YY > PLAIN - 5), Mix({"blackstone": 2, "polished_blackstone": 1}))
    glow = (rng.random(n) < 0.3) & (pd < 4)                       # some pipes drip with embers at their tips
    s.fill(col & (YY <= bot[:, None, :] + 1) & glow[ci][:, None, :] & ok[:, None, :], "magma_block")
    # the column caps fade into the ash: inner cells keep some ash on top
    ash_top = col & (YY == top[:, None, :]) & ((d > 9) & (fbm2(*cols2d(s.shape), 7, SEED + 93) > 0.0))[:, None, :]
    s.fill(ash_top, ASH)
    h2 = np.where(ok, np.maximum(h, top), h)
    return h2


def sulfur_terraces(s, h):
    """North-east: the Sulfur Terraces. Three travertine-like mounds of stepped pools (each step one block, walkable),
    sulfur rims, calcite floors, a lava eye and a venting potent-sulfur throat at the top, sulfur spikes around it."""
    rng = np.random.default_rng(SEED + 95)
    for k, (a, rr, R, steps) in enumerate(((-48, 80, 12.5, 6), (-30, 76, 8.5, 4), (-64, 86, 7.0, 3))):
        x, z = pol(a, rr)
        g = int(np.median(h[int(x) - 3:int(x) + 4, int(z) - 3:int(z) + 4]))
        for i in range(steps):
            Ri = R * (1 - i / (steps + 0.6))
            y = g + i
            wob = shapes.SDF(lambda X, Y, Z, Ri=Ri, i=i, x=x, z=z, k=k: np.hypot(X - x, Z - z) - Ri
                             - 1.4 * np.sin(np.arctan2(Z - z, X - x) * (3 + i) + k + i),
                             ((x - Ri - 3, g - 4, z - Ri - 3), (x + Ri + 3, y + 2, z + Ri + 3)))
            body = wob & shapes.box((x - Ri - 3, g - 4, z - Ri - 3), (x + Ri + 4, y + 1, z + Ri + 4))
            s.fill(body, Noise([(-0.2, Mix({"calcite": 3, "tuff": 1})), (1, Mix({"sulfur": 2, "calcite": 2, "tuff": 1}))],
                               scale=4, seed=SEED + 96 + i))
            m = body.mask(s.shape) & (YY == y)
            inner = np.zeros_like(m)
            inner[1:-1, :, 1:-1] = m[1:-1, :, 1:-1] & m[:-2, :, 1:-1] & m[2:, :, 1:-1] & m[1:-1, :, :-2] & m[1:-1, :, 2:]
            s.fill(m & ~inner, Mix({"polished_sulfur": 2, "sulfur": 2, "sulfur_bricks": 1}, seed=SEED + 97 + i))
        ytop = g + steps - 1
        s.fill(shapes.cylinder((x, 0, z), 1.6 + R * 0.08, ytop, ytop), "lava")
        s.set(int(x), ytop - 1, int(z), "potent_sulfur[potent_sulfur_state=continuous]")
        s.set(int(x), ytop, int(z), "air")
        for j in range(6 + k):
            ang = rng.uniform(0, 2 * math.pi)
            rad = rng.uniform(2.6, R * 0.55)
            px, pz = int(x + math.cos(ang) * rad), int(z + math.sin(ang) * rad)
            gy = ground_y(s, px, pz)
            if s.idx[px, gy - 1, pz] and gy < ytop + 2:
                ln = int(rng.integers(1, 4))
                for q in range(ln):
                    th_ = "tip" if q == ln - 1 else ("frustum" if q == ln - 2 else ("base" if q == 0 else "middle"))
                    s.set(px, gy + q, pz, f"sulfur_spike[thickness={th_},vertical_direction=up]")


def spear_clusters(s, h):
    """The Field of Spears, regrouped: splayed bundles of 3-6 basalt shards leaning out from a common root (one tall
    leader per bundle), some with polished tips or bone tips; scoria boulders between them."""
    rng = np.random.default_rng(SEED + 98)
    centres = []
    for i in range(60):
        dense = len(centres) < 11
        a = rng.uniform(22, 78) if dense else rng.uniform(-180, 180)
        rr = rng.uniform(RIM_R + 10, 90)
        if abs(wrap_deg(a - 90)) < 17 or abs(wrap_deg(a - BREACH)) < 10 or abs(wrap_deg(a - 180)) < 30 \
                or abs(wrap_deg(a - 235)) < 18 or abs(wrap_deg(a + 45)) < 26:
            continue
        x, z = pol(a, rr)
        if rr > edge_radius(np.array(a)) - 12 or any(math.hypot(x - cx, z - cz) < 9 for cx, cz, _ in centres):
            continue
        centres.append((x, z, dense))
        if len(centres) >= 22:
            break
    for ci, (x, z, dense) in enumerate(centres):
        g = h[int(x), int(z)]
        nsp = int(rng.integers(3, 7))
        tall = rng.uniform(14, 24) * (1.15 if dense else 0.85)
        s.fill(shapes.ellipsoid((x, g - 1, z), (3.2, 2.0, 3.2)).displace(0.8, 2.5, seed=ci), FLOW)
        for j in range(nsp):
            ang = rng.uniform(0, 2 * math.pi)
            lean = 0.12 + 0.3 * (j > 0) * rng.random()
            ht = tall if j == 0 else tall * rng.uniform(0.35, 0.75)
            off = 0 if j == 0 else rng.uniform(0.8, 2.2)
            bx, bz = x + math.cos(ang) * off, z + math.sin(ang) * off
            tip = (bx + math.cos(ang) * lean * ht, g + ht, bz + math.sin(ang) * lean * ht)
            rad = (2.1 if j == 0 else rng.uniform(0.9, 1.5))
            path = [(bx, g - 2, bz), ((bx + tip[0]) / 2, g + ht * 0.5, (bz + tip[2]) / 2), tip]
            tipm = BONE if (j == 0 and ci % 3 == 0) else ("polished_basalt" if j == 0 else Mix({"basalt": 3, "blackstone": 1}))
            thorn(s, path[0], path[1], path[2], rad, 0.35, tip_frac=0.25 if j == 0 else 0.0,
                  base=Mix({"basalt": 3, "blackstone": 1, "smooth_basalt": 1}, seed=ci * 7 + j), tip=tipm, n=10)
    for k in range(45):
        a, rr = rng.uniform(-180, 180), rng.uniform(RIM_R + 8, 92)
        if abs(wrap_deg(a - 90)) < 15:
            continue
        x, z = pol(a, rr)
        if rr > edge_radius(np.array(a)) - 6:
            continue
        g = h[int(x), int(z)]
        rad = rng.uniform(0.9, 2.2)
        s.fill(shapes.ellipsoid((x, g, z), (rad * 1.3, rad, rad)).displace(0.5, 2, seed=k + 300),
               Mix({"blackstone": 2, "basalt": 2, "magma_block": 0.4}))


# ================================================================== P7: relief, ember slits, fixtures, night read
STAIR_OF = {"deepslate_bricks": "deepslate_brick_stairs", "cracked_deepslate_bricks": "deepslate_brick_stairs",
            "deepslate_tiles": "deepslate_tile_stairs", "tuff_bricks": "tuff_brick_stairs",
            "polished_blackstone_bricks": "polished_blackstone_brick_stairs", "polished_tuff": "polished_tuff_stairs",
            "blackstone": "blackstone_stairs", "polished_deepslate": "polished_deepslate_stairs",
            "cinnabar_bricks": "cinnabar_brick_stairs", "polished_cinnabar": "polished_cinnabar_stairs",
            "sulfur_bricks": "sulfur_brick_stairs", "polished_sulfur": "polished_sulfur_stairs",
            "polished_blackstone": "polished_blackstone_stairs"}
WALL_OF = {"deepslate_brick_stairs": "deepslate_brick_wall", "deepslate_tile_stairs": "deepslate_tile_wall",
           "tuff_brick_stairs": "tuff_brick_wall", "polished_tuff_stairs": "polished_tuff_wall",
           "polished_deepslate_stairs": "polished_deepslate_wall", "blackstone_stairs": "blackstone_wall",
           "cinnabar_brick_stairs": "cinnabar_brick_wall", "polished_cinnabar_stairs": "polished_cinnabar_wall",
           "sulfur_brick_stairs": "sulfur_brick_wall", "polished_sulfur_stairs": "polished_sulfur_wall"}
DIRS = (((1, 0), "east", "west"), ((-1, 0), "west", "east"), ((0, 1), "south", "north"), ((0, -1), "north", "south"))


def _shift(a, dx, dy, dz):
    """b[x,y,z] = a[x+dx, y+dy, z+dz] (False outside)."""
    b = np.zeros_like(a)
    src = tuple(slice(max(d, 0), n + min(d, 0)) for d, n in zip((dx, dy, dz), a.shape))
    dst = tuple(slice(max(-d, 0), n - max(d, 0)) for d, n in zip((dx, dy, dz), a.shape))
    b[dst] = a[src]
    return b


def relief(s):
    """Masonry relief on every flat wall, by rule (so every outwork gets the same grammar):
    - copings: sky-facing wall edges become outward-sloping stairs;
    - drip courses: every 7th course is a groove of upside-down stairs (a shadow line);
    - ember slits: 3-high slits on an 8-block bay rhythm, iron bars in front of ochre froglights (the fortress glows from
      inside at night), each with an iron hood above and a sill below;
    - putlog holes: a sparse lattice of 1-deep holes (scale and shadow on the big plain faces)."""
    idx = s.idx
    air = idx == 0
    names = s.palette
    fam = {}
    for i, p in enumerate(names):
        nm = p.split(":")[-1].split("[")[0]
        if nm in STAIR_OF:
            fam[i] = STAIR_OF[nm]
    mas = np.isin(idx, list(fam))
    solid = s.solid()
    zone_air = np.zeros(s.shape, bool)
    for zn in ZONES:
        x0, y0, z0, x1, y1, z1 = zn["box"]
        zone_air[x0 - 1:x1 + 2, y0 - 1:y1 + 2, z0 - 1:z1 + 2] = True
    keep_out = np.zeros(s.shape, bool)
    keep_out[84:125, :GATE_F + 66, ZF - 26:ZF + 5] = True             # the Maw keeps its own composition
    keep_out[95:114, :, ZP:] |= True                                   # stair, road and bridge treads
    keep_out |= zone_air
    keep_out |= (polar(s.shape, C)[0] < 6.5)[:, None, :]              # the heart shaft and its helix
    keep_out[:, :PLAIN + 1, :] = True
    up_air = _shift(air, 0, 1, 0)
    up_m, dn_m = _shift(mas, 0, 1, 0), _shift(mas, 0, -1, 0)
    plans = []
    for (dx, dz), out_name, in_name in DIRS:
        front = _shift(air, dx, 0, dz)
        back = _shift(solid, -dx, 0, -dz)
        side = (0, 1) if dx else (1, 0)
        flat = _shift(mas, side[0], 0, side[1]) & _shift(mas, -side[0], 0, -side[1]) \
            & _shift(front, side[0], 0, side[1]) & _shift(front, -side[0], 0, -side[1])
        face = mas & front & back & ~keep_out
        n_air = sum(_shift(air, a, 0, b).astype(np.int8) for (a, b), _, _ in DIRS)
        single = n_air == 1
        plans.append(((dx, dz), out_name, in_name, face, flat, single, front, back))
    U = lambda dx: (np.arange(D)[None, None, :] if dx else np.arange(W)[:, None, None])
    yy = np.arange(H)[None, :, None]
    set_ops = []                                      # (mask, state or fn)
    slit_count = 0
    done = np.zeros(s.shape, bool)
    for (dx, dz), out_name, in_name, face, flat, single, front, back in plans:
        u = U(dx)
        face &= ~done
        cope = face & up_air & (_shift(solid, 0, -1, 0))
        drip = face & up_m & dn_m & ((yy % 7 == 3) | (yy % 7 == 0) | (yy % 7 == 5))
        back2 = _shift(solid, -2 * dx, 0, -2 * dz)
        slit_col = face & back2 & (u % 8 == 4)
        slit = np.zeros_like(face)
        cx, cz = np.nonzero(slit_col.any(1))
        for x, z in zip(cx, cz):          # a 3-high slit centred in every vertical face run of 5+, one per 10 blocks
            col = slit_col[x, :, z]
            y = 0
            while y < H:
                if not col[y]:
                    y += 1
                    continue
                y1 = y
                while y1 < H and col[y1]:
                    y1 += 1
                n_ = y1 - y
                if n_ >= 5:
                    for k0 in range(y + 1 + ((n_ - 2) % 10) // 2, y1 - 3, 10):
                        slit[x, k0:k0 + 3, z] = True
                y = y1
        slit_count += int(slit[:, ::1, :].sum()) // 3
        hole = face & back2 & (u % 5 == 1) & (yy % 6 == 1) & ~slit & ~_shift(slit, 0, 1, 0) & ~_shift(slit, 0, -1, 0)
        drip &= ~slit & ~hole
        done |= cope | drip | slit | hole
        set_ops.append(("cope", cope & ~slit, in_name, None))
        # corbel table: a bracket under every other coping block, in front of the wall
        below_front = _shift(_shift(air, dx, 0, dz), 0, -1, 0) & _shift(_shift(air, dx, 0, dz), 0, -2, 0)
        corb = _shift(cope & (u % 2 == 0), 0, 1, 0) & below_front & ~keep_out
        set_ops.append(("corbel", corb, in_name, (dx, dz)))
        set_ops.append(("drip", drip, in_name, None))
        set_ops.append(("slit", slit, (dx, dz), out_name))
        set_ops.append(("hole", hole, None, None))
        if PASS >= 9:     # lesenes: a slender wall-block rib up the face every 8 blocks (between the slit bays)
            rib = face & (u % 8 == 0) & ~slit & ~hole & ~cope & (yy > PLAIN + 2)                 & _shift(front, 0, -1, 0) & _shift(front, 0, -2, 0) & _shift(front, 0, -3, 0)   # never at head height
            set_ops.append(("rib", rib, (dx, dz), None))
    bars_side = {(1, 0): "north=true,south=true", (-1, 0): "north=true,south=true",
                 (0, 1): "east=true,west=true", (0, -1): "east=true,west=true"}
    for kind, m, a, b in set_ops:
        xs, ys, zs = np.nonzero(m)
        if kind in ("cope", "drip"):
            half = "bottom" if kind == "cope" else "top"
            for x, y, z in zip(xs, ys, zs):
                st = fam.get(int(idx[x, y, z]))
                if st:
                    s.set(int(x), int(y), int(z), f"{st}[facing={a},half={half}]")
        elif kind == "corbel":
            dx, dz = b
            for x, y, z in zip(xs, ys, zs):
                st = fam.get(int(idx[x, y + 1, z])) or "deepslate_brick_stairs"
                fx, fz = int(x + dx), int(z + dz)
                if 0 <= fx < W and 0 <= fz < D and s.idx[fx, y, fz] == 0:
                    s.set(fx, int(y), fz, f"{st}[facing={a},half=top]")
        elif kind == "rib":
            dx, dz = a
            for x, y, z in zip(xs, ys, zs):
                fx, fz = int(x + dx), int(z + dz)
                if 0 <= fx < W and 0 <= fz < D and s.idx[fx, y, fz] == 0:
                    st = fam.get(int(idx[x, y, z]), "")
                    s.set(fx, int(y), fz, WALL_OF.get(st, "polished_blackstone_brick_wall"))
        elif kind == "slit":
            dx, dz = a
            for x, y, z in zip(xs, ys, zs):
                s.set(int(x), int(y), int(z), f"iron_bars[{bars_side[(dx, dz)]}]")
                s.set(int(x - dx), int(y), int(z - dz), "ochre_froglight")
                fx, fz = int(x + dx), int(z + dz)
                if 0 <= fx < W and 0 <= fz < D:
                    for yy_, cond in ((int(y) + 1, not m[x, min(H - 1, y + 1), z]), (int(y) - 1, not m[x, max(0, y - 1), z])):
                        if cond and s.idx[fx, yy_, fz] == 0:
                            s.set(fx, yy_, fz, f"iron_trapdoor[facing={b},half=top,open=false]")
        else:
            for x, y, z in zip(xs, ys, zs):
                s.set(int(x), int(y), int(z), "air")
    s.meta["_slits"] = slit_count


def skull_rot(theta):
    return int(round(((theta - 90) % 360) / 22.5)) % 16


def night_fixtures(s):
    """Designed lights for the night read: lanterns on the Tongue and bridge parapets, the throne lantern's ember ring,
    wither skulls on the star merlons and the Pylons, lanterns hung in the Maw throat."""
    # Tongue parapet lanterns (every 4th post) and landing pedestal braziers
    for x in (97, 111):
        for z in range(ZF + 2, s.meta["_stair_foot"], 4):
            y = ground_y(s, x, z)
            if "wall" in s.palette[s.idx[x, y - 1, z]]:
                s.set(x, y, z, "lantern[hanging=false]")
    for zl in s.meta.get("_landings", []):
        for x0 in (93, 113):
            for dx, dz in ((0, 0), (2, 0), (0, 2), (2, 2)):
                y = ground_y(s, x0 + dx, zl + dz)
                s.set(x0 + dx, y, zl + dz, "lantern[hanging=false]")
    # Ember Bridge: lanterns on every 4th merlon
    for z in range(ZP + 2, ZB, 4):
        for x in (99, 109):
            y = ground_y(s, x, z)
            if y < DECK + 6:
                s.set(x, y, z, "lantern[hanging=false]")
    # Maw throat: lanterns hung from the vault on chains
    for z in range(ZB + 3, ZF - 2, 5):
        top = None
        for y in range(GATE_I + 2, GATE_F + 20):
            if s.idx[104, y, z] != 0:
                top = y
                break
        if top:
            s.set(104, top - 1, z, "iron_chain[axis=y]")
            s.set(104, top - 2, z, "lantern[hanging=true]")
    # throne lantern: an ember ring in the floor shows through the six arches
    r, th = polar(s.shape, C)
    ring = (r >= 4.5) & (r < 6.0)
    for y in (148,):
        m = np.zeros(s.shape, bool)
        m[:, y, :] = ring
        s.fill(m & s.match("solid"), "ochre_froglight")
    # skulls on the star wall copings: one per 7.5-degree bay (alternate bays), on the highest sky-facing coping in
    # the bay, facing out over the lava
    idx = s.idx
    air = idx == 0
    tops = (idx != 0) & np.concatenate([air[:, 1:], np.ones_like(air[:, :1])], 1)
    cope = s.match(lambda nm: "polished_tuff" in nm or "tuff_brick" in nm) & tops
    cope[:, :DECK + 10, :] = False
    cope[:, DECK + 20:, :] = False
    xs, ys, zs = np.nonzero(cope)
    best = {}
    for x, y, z in zip(xs, ys, zs):
        rr_ = math.hypot(x + 0.5 - C[0], z + 0.5 - C[1])
        if not 16 <= rr_ <= 38:
            continue
        th_ = math.degrees(math.atan2(z + 0.5 - C[1], x + 0.5 - C[0]))
        if abs(wrap_deg(th_ - 90)) < 8:            # keep the hall door axis clear
            continue
        b_ = int((th_ + 180) // 7.5)
        key = (y, rr_)
        if b_ not in best or key > best[b_][0]:
            best[b_] = (key, int(x), int(y), int(z), th_)
    n = 0
    for _, x, y, z, th_ in best.values():
        if s.idx[x, y + 1, z] == 0:
            s.set(x, y + 1, z, f"wither_skeleton_skull[rotation={skull_rot(th_)}]")
            n += 1
    # skulls on the Tongue landing pedestals and on the spear posts of the road (facing the approach)
    for z in range(s.meta["_stair_foot"] + 2, D, 5):
        for x in (96, 112):
            y = ground_y(s, x, z)
            if PLAIN + 3 <= y <= PLAIN + 12 and s.idx[x, y - 1, z] != 0:
                s.set(x, y, z, "skeleton_skull[rotation=0]")
                n += 1
    s.meta["_skulls"] = n


def light_interiors(s):
    """Interiors and the bailey canyon: the voxel auto-light (hanging lanterns on chains, wall lanterns) in the
    'noble' kit (polished blackstone, dark oak), so every walkable room cell reaches light 7 (no spawns)."""
    import tools.voxel.light as L
    added = L.autolight(s, "noble", minimum=8, max_new=420 if PASS >= 9 else 260, outdoor=False)
    # the citadel and its approach are lit for the night too (walls, bailey, Tongue, bridge, road): the garrison's
    # lanterns; the ash plain stays dark (the island glows only where it is held)
    r, _ = polar(s.shape, C)
    held = np.zeros(s.shape, bool)
    held[:, DECK - 2:, :] = (r < PLUG_R + 6)[:, None, :]
    held[93:116, PLAIN - 2:, ZB - 2:] = True
    held[98:111, :, ZB - 2:] = False          # never a lantern on the treads: the parapet lanterns light them
    walk0 = L.walkable
    L.walkable = lambda sc: walk0(sc) & held
    try:
        added += L.autolight(s, "noble", minimum=8, max_new=500, outdoor=True)
    finally:
        L.walkable = walk0
    s.meta["_autolights"] = len(added)


def _runs(m, axis):
    """Length of the contiguous run of m along `axis` through each cell."""
    a = np.moveaxis(m, axis, 0)
    fwd = np.zeros(a.shape, np.int16)
    bwd = np.zeros(a.shape, np.int16)
    acc = np.zeros(a.shape[1:], np.int16)
    for i in range(a.shape[0]):
        acc = np.where(a[i], acc + 1, 0)
        fwd[i] = acc
    acc[:] = 0
    for i in range(a.shape[0] - 1, -1, -1):
        acc = np.where(a[i], acc + 1, 0)
        bwd[i] = acc
    return np.moveaxis(fwd + bwd - 1, 0, axis)


def bone_grain(s):
    """Bone grows along its length: every bone block takes the axis of the longest bone run through it, so horns,
    ribs and thorn tips show their grain (side texture along, ring ends at the tips)."""
    m = s.match(lambda n: "bone_block" in n)
    rx, ry, rz = _runs(m, 0), _runs(m, 1), _runs(m, 2)
    ax = np.argmax(np.stack([rx, ry, rz]), 0)
    for k, name in enumerate("xyz"):
        s.fill(m & (ax == k), f"bone_block[axis={name}]")


def shards(s, h):
    """The Shattered Rim: basalt shards torn off the island drift around it (corners and flanks), each a column-capped
    raft with a tapering underside, a few carrying a spear bundle or a fallen obelisk. Unreachable scenery."""
    rng = np.random.default_rng(SEED + 120)
    edge = s.meta["_edge"]
    gx, gz = cols2d(s.shape)
    r, th = polar(s.shape, C)
    placed = []
    free = r > edge + 5
    tries = 0
    while len(placed) < 34 and tries < 6000:
        tries += 1
        x, z = rng.uniform(4, W - 4), rng.uniform(4, D - 4)
        if not free[int(x), int(z)]:
            continue
        rr_ = math.hypot(x - C[0], z - C[1])
        a = math.degrees(math.atan2(z - C[1], x - C[0]))
        room = rr_ - edge_radius(np.array(a)) - 3
        rad = min(rng.uniform(4, 15), room, x - 1, W - 2 - x, z - 1, D - 2 - z)
        if rad < 3 or any(math.hypot(x - px, z - pz) < rad + pr + 1.5 for px, pz, pr in placed):
            continue
        if abs(wrap_deg(a - 90)) < 22 and z > ZF:     # keep the approach axis clear
            continue
        placed.append((x, z, rad))
    for k, (x, z, rad) in enumerate(placed):
        top = PLAIN + (rng.uniform(4, 26) if k % 2 else rng.uniform(-16, -3))
        depth = rad * rng.uniform(1.6, 3.2)
        tilt = rng.uniform(-0.25, 0.25, 2)
        raft = shapes.SDF(lambda X, Y, Z, x=x, z=z, rad=rad, top=top, depth=depth, tilt=tilt, k=k:
                          np.maximum(np.hypot(X - x, Z - z) - rad * np.clip((Y - (top - depth)) / depth, 0, 1) ** 0.6
                                     - 0.9 * np.sin((X + 2 * Z) * 0.7 + k), Y - (top + tilt[0] * (X - x) + tilt[1] * (Z - z))),
                          ((x - rad - 2, top - depth - 1, z - rad - 2), (x + rad + 2, top + rad * 0.3 + 2, z + rad + 2)))
        s.fill(raft, UNDER)
        m = raft.mask(s.shape)
        topm = m & ~np.concatenate([m[:, 1:], np.zeros_like(m[:, :1])], 1)
        s.fill(topm, ASH)
        if k % 3 == 0:          # a spear bundle torn off with its shard
            g = int(top)
            for j in range(3):
                ang = rng.uniform(0, 2 * math.pi)
                ht = rng.uniform(6, 13)
                thorn(s, (x, g - 1, z), (x + math.cos(ang) * 1.5, g + ht * 0.5, z + math.sin(ang) * 1.5),
                      (x + math.cos(ang) * ht * 0.3, g + ht, z + math.sin(ang) * ht * 0.3), 1.3, 0.35, tip_frac=0.2,
                      base=Mix({"basalt": 3, "blackstone": 1}), n=8)
        elif k % 5 == 1 and rad > 5:   # a fallen obelisk lying across it
            ang = rng.uniform(0, math.pi)
            p0 = (x - math.cos(ang) * rad * 0.7, top + 1.2, z - math.sin(ang) * rad * 0.7)
            p1 = (x + math.cos(ang) * rad * 0.8, top + 1.0, z + math.sin(ang) * rad * 0.8)
            s.fill(shapes.capsule(p0, p1, 1.4), "obsidian")
    s.meta["_shards"] = len(placed)


# ================================================================== P8: access (every zone reachable), the helix
FACING_OF = {(1, 0): "east", (-1, 0): "west", (0, 1): "south", (0, -1): "north"}


def stairify(s, tread, full, stair):
    """Tread cells -> full blocks, or stairs facing the neighbour whose tread is one higher (walk up without jumping)."""
    xs, ys, zs = np.nonzero(tread)
    for x, y, z in zip(xs, ys, zs):
        st = full
        for (dx, dz), f in FACING_OF.items():
            nx, nz = x + dx, z + dz
            if 0 <= nx < W and 0 <= nz < D and y + 1 < H and tread[nx, y + 1, nz]:
                st = f"{stair}[facing={f},half=bottom]"
                break
        s.set(int(x), int(y), int(z), st)


def heart_helix(s):
    """The Ember Stair: a helix from the heart sanctum floor to the throne lantern, wound around the caged lava heart.
    Below the cage top it runs in the ring between the iron cage and the shaft wall; above it, round a newel in the
    upper well, and it surfaces through the throne-room floor. One block of rise per ~3 blocks of travel, 6 per turn."""
    r, th = polar(s.shape, C)
    P = 6
    y_lo, y_hi, y_cap = DECK, 148, 129
    tn = (((th - 100.0) % 360.0) / 360.0)
    tread = np.zeros(s.shape, bool)
    head = np.zeros(s.shape, bool)
    for t in range(0, (y_hi - y_lo) // P + 2):
        yt = np.floor(y_lo + P * (tn + t)).astype(int)
        band = np.where(yt < y_cap + 2, (r >= 2.9) & (r <= 5.0), (r >= 1.0) & (r <= 3.25))
        ok = band & (yt <= y_hi) & (yt >= y_lo)
        xs, zs = np.nonzero(ok)
        tread[xs, yt[xs, zs], zs] = True
        for k in (1, 2, 3):
            head[xs, np.minimum(yt[xs, zs] + k, H - 1), zs] = True
    cage = np.zeros(s.shape, bool)
    cage[:, DECK + 1:y_cap, :] = ((r >= 2.4) & (r < 2.9))[:, None, :]
    s.fill(cage & ~tread, "iron_bars")
    capm = np.zeros(s.shape, bool)
    capm[:, y_cap, :] = (r < 2.9)
    s.fill(capm, "polished_blackstone_bricks")
    newel = np.zeros(s.shape, bool)
    newel[:, y_cap + 1:y_hi + 1, :] = (r < 1.0)[:, None, :]
    s.fill(newel, Mix({"polished_blackstone_bricks": 2, "gilded_blackstone": 1}, seed=SEED + 130))
    s.fill(head & ~tread & ~newel, "air")
    # the valley slits are glazed with bars where they cut the shaft wall: the heart still shows from outside, but the
    # stair cannot be left onto the Fang's collars (no way back up from there)
    grille = np.zeros(s.shape, bool)
    tw = 55 * ((np.arange(H) - (DECK - 6)) / (FANG_TOP - DECK + 6))
    for k in range(6):                       # the same six twisted valley slits that keep() cut
        a_ = 60 + k * 60
        grille |= np.abs(wrap_deg(th[:, None, :] - (a_ + tw[None, :, None]))) * np.pi / 180 * r[:, None, :] < 1.6
    grille &= ((r >= 4.9) & (r < 7.5))[:, None, :]
    grille[:, :DECK + 6, :] = False
    grille[:, y_hi:, :] = False
    s.fill(grille & s.match("air") & ~head & ~tread, "iron_bars")
    stairify(s, tread, "polished_blackstone_bricks", "polished_blackstone_brick_stairs")
    # balustrades in the six throne-lantern arches (the crown is open to the sky, not to a 90-block fall)
    bal = np.zeros(s.shape, bool)
    gx, gz = cols2d(s.shape)
    for k in range(6):
        ax_, az_ = pol(70 + k * 60, 7.5)
        bal[:, 150, :] |= (np.hypot(gx - ax_, gz - az_) < 2.4) & (r >= 6.2)
    s.fill(bal & s.match("air"), "polished_blackstone_wall")
    if PASS >= 10:   # ember rings: froglight courses in the shaft wall every 12 blocks light the climb
        ring = np.zeros(s.shape, bool)
        for y in range(DECK + 8, y_cap, 12):
            ring[:, y, :] = (r >= 5.0) & (r < 5.9)
        s.fill(ring & s.match("solid") & ~s.match("iron_bars"), "ochre_froglight")
    s.meta["_helix_treads"] = int(tread.sum())


def access(s):
    """Every zone gets a way in: the hall's north door runs on to the heart sanctum; a stair drops from the hall floor to
    the undercroft; each spire room opens toward the bailey through a short pointed passage."""
    x0, x1, z0, z1 = HALL
    # hall north door -> sanctum: a 5-wide passage under a pointed vault
    s.fill(((102, DECK + 1, int(C[1]) + 5), (106, DECK + 5, z0 + 1)), "air")
    s.fill(((103, DECK + 6, int(C[1]) + 5), (105, DECK + 6, z0 + 1)), "air")
    s.fill(((102, DECK, int(C[1]) + 6), (106, DECK, z0 + 1)), PAVE)
    # undercroft stair: west aisle of the hall, descending south, one block per step
    zt = z0 + 4
    prof = {zt + i: DECK - 1 - i for i in range(9)}
    for z, yt in prof.items():
        s.fill(((99, yt + 1, z), (100, DECK + 4, z)), "air")
    lay_steps(s, 99, 100, prof, "polished_blackstone_bricks", "polished_blackstone_brick_stairs", under="polished_blackstone_bricks", depth=2)
    s.fill(((101, DECK + 1, zt), (101, DECK + 1, zt + 9)), "polished_blackstone_wall")
    s.fill(((99, DECK + 1, zt + 9), (100, DECK + 1, zt + 9)), "polished_blackstone_wall")
    for zn in ZONES:
        if zn["name"] == "undercroft":
            zn["doors"].append([99, DECK - 8, zt + 8])            # foot of the stair from the hall's west aisle
        elif zn["name"] == "throne_lantern":
            hx, hz = pol(100, 4.0)
            zn["doors"].append([int(hx), 149, int(hz)])           # the Ember Stair surfaces here
    # spire rooms: walk toward the Fang until the bailey floor is reached
    for zn in ZONES:
        if not zn["name"].startswith("spire_"):
            continue
        bx0, by0, bz0, bx1, by1, bz1 = zn["box"]
        cx, cz = (bx0 + bx1) / 2, (bz0 + bz1) / 2
        dx, dz = C[0] - cx, C[1] - cz
        if abs(dx) >= abs(dz):
            step = (int(np.sign(dx)), 0)
            x = bx1 + 1 if dx > 0 else bx0 - 1
            z = int(round(cz))
        else:
            step = (0, int(np.sign(dz)))
            z = bz1 + 1 if dz > 0 else bz0 - 1
            x = int(round(cx))
        door = None
        for i in range(14):
            px, pz = x + step[0] * i, z + step[1] * i
            open_ = all(s.idx[px + step[1] * j, by0, pz + step[0] * j] == 0 for j in (-1, 0, 1)) \
                and s.idx[px, by0 - 1, pz] != 0
            if i > 0 and open_:
                break
            a0 = (px - abs(step[1]), by0, pz - abs(step[0]))
            a1 = (px + abs(step[1]), by0 + 2, pz + abs(step[0]))
            s.fill((a0, a1), "air")
            s.fill(((px, by0 + 3, pz), (px, by0 + 3, pz)), "air")
            s.fill(((a0[0], by0 - 1, a0[2]), (a1[0], by0 - 1, a1[2])), PAVE)
            door = door or (px, by0, pz)
        zn["doors"].append([int(v) for v in door])


def reach(s, start):
    """Forward walk from start (4-neighbour, up 1, down up to 3), then which of those cells can walk back.
    Returns (walkable, forward, returnable)."""
    from collections import deque
    from tools.voxel.light import walkable
    Wk = walkable(s)
    X_, Y_, Z_ = Wk.shape

    def moves(x, y, z):
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, nz = x + dx, z + dz
            if 0 <= nx < X_ and 0 <= nz < Z_:
                for dy in (0, 1, -1, -2, -3):
                    ny = y + dy
                    if 0 <= ny < Y_ and Wk[nx, ny, nz]:
                        yield nx, ny, nz
                        break
    F = np.zeros(Wk.shape, bool)
    F[start] = True
    q = deque([start])
    rev = {}
    while q:
        c = q.popleft()
        for n in moves(*c):
            rev.setdefault(n, []).append(c)
            if not F[n]:
                F[n] = True
                q.append(n)
    B = np.zeros(Wk.shape, bool)
    B[start] = True
    q = deque([start])
    while q:
        c = q.popleft()
        for p_ in rev.get(c, ()):
            if not B[p_]:
                B[p_] = True
                q.append(p_)
    return Wk, F, B


def spawn_cell(s):
    zsp = min(s.meta["_barb"] + 14, D - 6)
    return (104, ground_y(s, 104, zsp), zsp)


def fill_pockets(s, rounds=5):
    """No inescapable pits: ash drifts into every hollow of the outer plain that a player could drop into but not climb
    out of (between causeway columns, behind boulders), one block per round until it is escapable."""
    r, _ = polar(s.shape, C)
    outer = (r > RIM_R + 4)[:, None, :]
    n = 0
    for _ in range(rounds):
        _, F, B = reach(s, spawn_cell(s))
        trap = F & ~B & outer
        if not trap.any():
            break
        n += int(trap.sum())
        s.fill(trap, ASH)
    s.meta["_pockets_filled"] = n


def hall_shell(s):
    """The Forge Hall as architecture (still unfurnished): wall pilasters on a 4-block bay rhythm carrying pointed
    transverse ribs, a clerestory of barred lancets between them, a cinnabar kerb along the lava channel."""
    x0, x1, z0, z1 = HALL
    xa, xb = x0 + 2, x1 - 2                     # interior x 99..109
    za, zb = z0 + 3, z1 - 4
    yt = DECK + 14
    for z in range(za, zb + 1, 4):
        for x in (xa, xb):
            s.box((x, DECK + 1, z), (x, yt, z), "polished_blackstone_bricks")
            s.set(x, DECK + 1, z, "chiseled_polished_blackstone")
        # pointed rib across the vault: springs at DECK+10 on each pilaster, apex at the ceiling
        half = (xb - xa) / 2
        for x in range(xa + 1, xb):
            u = abs(x - (xa + xb) / 2) / half
            yr = int(round(DECK + 10 + (yt - (DECK + 10)) * (1 - u ** 1.6) ** 0.5))
            s.box((x, yr, z), (x, yt, z), "polished_blackstone_bricks")
            if yr > DECK + 10 and s.idx[x, yr - 1, z] == 0:
                side = "east" if x < (xa + xb) / 2 else "west"
                s.set(x, yr - 1, z, f"polished_blackstone_brick_stairs[facing={side},half=top]")
    for z in range(za + 2, zb, 4):               # clerestory lancets between the pilasters
        for x, xo in ((xa - 1, xa - 2), (xb + 1, xb + 2)):
            s.box((x, DECK + 8, z), (x, DECK + 11, z), "air")
            s.box((xo, DECK + 8, z), (xo, DECK + 11, z), "iron_bars")
    s.fill(((102, DECK, z0 + 1), (102, DECK, z1 - 3)), "polished_cinnabar")
    s.fill(((106, DECK, z0 + 1), (106, DECK, z1 - 3)), "polished_cinnabar")


def bailey_path(s):
    """The ember path: a cinnabar inlay along the medial line of the bailey floor, so the ring route round the Fang
    reads at a glance (and at night under the garrison lanterns)."""
    from scipy import ndimage
    r, _ = polar(s.shape, C)
    y = DECK + 1
    floor = (s.idx[:, y, :] == 0) & (s.idx[:, y + 1, :] == 0) & (s.idx[:, y - 1, :] != 0) & (r < PLUG_R) & (r > 6.5)
    hx0, hx1, hz0, hz1 = HALL
    floor[hx0 - 1:hx1 + 2, hz0 - 3:hz1 + 2] = False          # not inside the hall or its north passage
    dist = ndimage.distance_transform_edt(floor)
    ridge = floor & (dist >= 2.0) & (dist >= ndimage.maximum_filter(dist, size=3) - 0.01)
    ridge = ndimage.binary_dilation(ridge, iterations=1) & floor & (dist >= 1.5)
    m = np.zeros(s.shape, bool)
    m[:, y - 1, :] = ridge
    s.fill(m, Mix({"polished_cinnabar": 3, "cinnabar_bricks": 2}, seed=SEED + 140))
    s.meta["_bailey_path"] = int(ridge.sum())
    # the widest bailey spot (for the bailey camera): look along the ring, counter-clockwise
    bx, bz = np.unravel_index(int(np.argmax(np.where(floor, dist, 0))), dist.shape)
    s.meta["_bailey_wide"] = [int(bx), int(bz)]


def throne_crown(s):
    """The throne lantern as a room (shell only): gilded surrounds on the six arches, a three-step half-round dais on
    the north side facing the Tongue, a cinnabar band where the arches spring."""
    r, th = polar(s.shape, C)
    gx, gz = cols2d(s.shape)
    YYf = YY.astype(float)
    sur = np.zeros(s.shape, bool)
    for k in range(6):
        ax_, az_ = pol(70 + k * 60, 7.5)
        d = np.hypot(gx - ax_, gz - az_)[:, None, :]
        # distance to the arch's vertical capsule axis (151.5..159)
        dy = np.maximum(np.maximum(151.5 - YYf, YYf - 159), 0)
        dist = np.sqrt(d ** 2 + dy ** 2)
        sur |= (dist >= 1.7) & (dist < 2.7)
    sur &= s.match("solid") & ~s.match("lava")
    sur[:, :149, :] = False
    s.fill(sur, Mix({"gilded_blackstone": 2, "polished_blackstone_bricks": 1}, seed=SEED + 150))
    band = s.match("solid") & ((r >= 6.0) & (r < 7.0))[:, None, :] & (YY == 162)
    s.fill(band, "polished_cinnabar")
    north = (gz < C[1] - 0.5) & (np.abs(wrap_deg(th + 90)) < 70)
    for i, rad in enumerate((5.6, 4.2, 2.8)):
        m = np.zeros(s.shape, bool)
        m[:, 149 + i, :] = north & (r < rad)
        s.fill(m & s.match("air"), "polished_blackstone_bricks" if i < 2 else "polished_cinnabar")


# ================================================================== build
def build():
    s = Scene((W, H, D), "vharzul", seed=SEED)
    h, r, th = terrain(s)
    if PASS >= 6:
        h = causeway(s, h, r, th)
        spear_clusters(s, h)
    if PASS >= 7:
        shards(s, h)
    else:
        spikes_field(s, h)
    obelisks(s, h)
    ribcage(s, h)
    slag_works(s, h)
    if PASS >= 6:
        sulfur_terraces(s, h)
    else:
        fumaroles(s, h)
    plug(s)
    lava_falls(s)
    star_wall(s)
    if PASS >= 2:
        star_facade(s)
    horns(s)
    if PASS >= 3:
        horn_ridges(s)
        spires3(s)
    else:
        spires(s)
    if PASS >= 4:
        horn_bands(s)
    keep(s)
    keep_collars(s)
    if PASS >= 2:
        fang_ribs(s)
    hall(s)
    if PASS >= 2:
        hall_facade(s)
    if PASS >= 5:
        bridge2(s)
    else:
        bridge(s)
    rim_wall(s, h, r, th)
    if PASS >= 2:
        rim_facade(s, r, th)
    gate(s)
    if PASS >= 3:
        fang_crowns(s)
    if PASS >= 5:
        throat_steps(s)
        processional2(s, h)
        barbican(s, h)
        road2(s, h)
    else:
        processional(s, h)
        barbican(s, h)
        road(s, h)
    breach_fall(s)
    interiors(s)
    if PASS >= 8:
        heart_helix(s)
        access(s)
        hall_shell(s)
        bailey_path(s)
    if PASS >= 9:
        throne_crown(s)
    if PASS >= 4:
        weather(s)
    if PASS >= 8:
        fill_pockets(s)
    if PASS >= 7:
        relief(s)
        bone_grain(s)
        night_fixtures(s)
        light_interiors(s)
    cameras(s)
    s.meta.pop("_bridge_prof", None)
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
    if PASS >= 10:   # defenders muster in the Forge Hall, facing the bridge door
        x0, x1, z0, z1 = HALL
        s.mark("spawn_defender", (101, DECK + 1, z0 + 3), look_at=(101, DECK + 4, z1))
        s.markers["spawn_defender"]["fov"] = 75
    s.mark("cam_stairfoot", (104, ground_y(s, 104, zs + 1), zs + 1), look_at=(104, 70, 140))
    s.mark("cam_gate", (104, GATE_I, ZB + 1), look_at=(104, 110, 100))
    if "_bailey_wide" in s.meta:
        bx, bz = s.meta.pop("_bailey_wide")
        a0 = math.degrees(math.atan2(bz + 0.5 - C[1], bx + 0.5 - C[0]))
        rr0 = math.hypot(bx + 0.5 - C[0], bz + 0.5 - C[1])
        lx, lz = pol(a0 + 50, rr0)
        s.mark("cam_bailey", (bx, DECK + 2, bz), look_at=(lx, DECK + 9, lz))
        s.markers["cam_bailey"]["fov"] = 80
        s.mark("cam_helix", (100, 91, 100), look_at=(104, 140, 100))
        s.markers["cam_helix"]["fov"] = 85
        s.mark("cam_throne", (104, 150, int(C[1]) + 4), look_at=(104, 152, int(C[1]) - 6))
        s.markers["cam_throne"]["fov"] = 85
    else:
        bx, bz = (int(v) for v in pol(152, 17.5))
        lx, lz = pol(95, 19)
        s.mark("cam_bailey", (bx, DECK + 1, bz), look_at=(lx, DECK + 16, lz))
    s.mark("cam_maw", (104, ground_y(s, 104, ZF + 16), ZF + 16), look_at=(104, GATE_F + 20, ZF))
    if PASS < 9:     # superseded by cam_helix
        s.mark("cam_heart", (104, DECK + 1, CZ + 5), look_at=(104, 100, 100.5))
    if "_bridge_prof" in s.meta:
        bz = ZB - 2
        s.mark("cam_bridge", (104, s.meta["_bridge_prof"][bz] + 1, bz), look_at=(104, DECK + 8, ZP - 4))
    s.mark("cam_hall", (104, DECK + 1, HALL[3] - 3), look_at=(104, DECK + 6, HALL[2]))
    s.mark("cam_ash_west", (14, ground_y(s, 14, 112), 112), look_at=(60, 40, 96))
    nx, nz = (int(v) for v in pol(-33 if PASS >= 8 else -40, 96))
    s.mark("cam_ash_ne", (nx, ground_y(s, nx, nz) + 2, nz), look_at=(104, 80, 100))
    bx, bz = (int(v) for v in pol(BREACH, 52))
    lx, lz = pol(BREACH, 110)
    s.mark("cam_breach", (bx, LAKE_Y + 6, bz), look_at=(lx, LAKE_Y - 6, lz))
    s.mark("cam_hero", (200, 112, 206), look_at=(104, 84, 100))
    s.markers["cam_hero"]["fov"] = 55
    s.mark("cam_far", (-60, 70, 260), look_at=(104, 100, 100))
    s.markers["cam_far"]["fov"] = 45
