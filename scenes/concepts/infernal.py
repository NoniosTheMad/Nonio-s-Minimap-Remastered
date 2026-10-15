"""Concept A: VHARZUL, THE EMBER THRONE (infernal citadel), massing + silhouette model.

Brief
  A citadel grown on a basalt plug in the middle of a living caldera. A star-fort of blackstone rings the plug, three
  obsidian horns rise from its points and curl inward like a claw around the Fang (a twisted obsidian needle keep with a
  caged lava heart). The caldera rim is the outer wall; the east rim has burst (the Breach) and the lake bleeds out
  over the edge of the world.
  Mood: ember dusk, light from below. References: Le Puy-en-Velay (chapel on a volcanic plug), Giant's Causeway / Fingal's
  Cave (basalt organ pipes), Barad-dur and Dark Souls' Izalith (silhouette, scale), Bourtange / Palmanova (star forts).

Scale: island ~200 across, castle (rim wall) 128 across, Fang tip ~y165 (~145 over the ash plain).
Render: python -m tools.voxel render scenes/concepts/infernal.py --mood ember
"""
import math

import numpy as np

from scenes.concepts._kit import (basalt_cells, bezier, cols2d, cone, fbm2, heightmask, polar, ring_band, star_prism,
                                  tube, union, wrap_deg)
from tools.voxel import noise, shapes
from tools.voxel.palette import Gradient, Mix, Noise
from tools.voxel.scene import Scene

W, H, D = 208, 204, 208
FANG_TOP = 194
C = (104.0, 104.0)
SEED = 666

PLAIN = 16          # ash plain
LAKE_Y = 34         # lava surface
LAKE_R = 50         # foot of the inner crater wall
RIM_R = 61          # rim crest
OUT_R = 96          # foot of the outer slope
EDGE_R = 101        # island edge (void beyond)
PLUG_R = 30
DECK = 62           # plug top (paving); standing level DECK+1
GATE_Y = 47         # gate passage floor (south rim)

STAR_PTS = (0, 60, 120, 180, 240, 300)       # star-wall points (deg; 0 = east, 90 = south)
HORNS = (0, 120, 240)                        # horn bases on those points
SPIRES = (60, 180, 300)
FALLS = (30, 150, 210, 330)                  # lava falls from the plug (valleys)
BREACH = 12                                  # the burst rim (deg)
RIM_FANGS = [(-90, 10, 70), (-62, 7, 44), (-118, 7, 40), (-30, 6, 30), (-150, 6, 34), (45, 5, 26), (66, 6, 36),
             (114, 6, 36), (140, 5, 26), (178, 7, 38), (215, 6, 30)]   # angle, radius, height over the rim crest

# ------------------------------------------------------------------ materials (massing level: families + gradients)
ASH = Noise([(-0.3, Mix({"smooth_basalt": 3, "basalt": 1})), (0.2, Mix({"blackstone": 2, "smooth_basalt": 2})),
             (1, Mix({"basalt": 2, "tuff": 1, "smooth_basalt": 1}))], scale=9, seed=SEED)
CRATER = Gradient("y", [(LAKE_Y + 2, Mix({"magma_block": 2, "blackstone": 2, "netherrack": 1})),
                        (LAKE_Y + 8, Mix({"blackstone": 3, "magma_block": 1})),
                        (999, Mix({"blackstone": 3, "basalt": 2, "smooth_basalt": 1}))], jitter=2.5, jitter_scale=5, seed=SEED)
UNDER = Gradient("y", [(-60, "obsidian"), (PLAIN - 30, Mix({"blackstone": 3, "obsidian": 1})),
                       (PLAIN - 8, Mix({"blackstone": 2, "basalt": 2})), (999, Mix({"basalt": 2, "smooth_basalt": 2}))],
                 jitter=6, jitter_scale=9, seed=SEED + 1)
WALL = Gradient("y", [(DECK - 4, Mix({"blackstone": 3, "basalt": 1})),
                      (DECK + 6, Mix({"polished_blackstone_bricks": 3, "blackstone": 1, "cracked_polished_blackstone_bricks": 1})),
                      (999, Mix({"polished_blackstone_bricks": 4, "cracked_polished_blackstone_bricks": 1, "polished_blackstone": 1}))],
                jitter=2, jitter_scale=5, seed=SEED + 2)
TRIM = "gilded_blackstone"
OBSIDIAN = Noise([(-0.62, "crying_obsidian"), (1, "obsidian")], scale=4, seed=SEED + 3)
HORN = Gradient("y", [(85, Mix({"blackstone": 3, "polished_blackstone": 1})), (110, Mix({"polished_blackstone": 2, "nether_bricks": 1})),
                      (128, Mix({"nether_bricks": 3, "red_nether_bricks": 1})), (999, "red_nether_bricks")],
                jitter=3, jitter_scale=6, seed=SEED + 4)
ROOF = Mix({"red_nether_bricks": 3, "nether_bricks": 1})


def ground_y(s, x, z):
    col = s.idx[int(x), :, int(z)]
    nz = np.nonzero(col)[0]
    return int(nz.max()) + 1 if len(nz) else 0


# ------------------------------------------------------------------ terrain
def rim_height(theta):
    a = np.radians(theta)
    h = 47 + 6 * noise.fbm(np.cos(a) * 2.2, np.sin(a) * 2.2, 3.0, scale=1.0, octaves=3, seed=SEED)
    h += 18 * np.exp(-(wrap_deg(theta + 90) / 30) ** 2)        # the north crown (highest rim)
    h -= 4 * np.exp(-(wrap_deg(theta - 90) / 18) ** 2)         # gate saddle
    return h


def terrain(s):
    gx, gz = cols2d(s.shape)
    r, th = polar(s.shape, C)
    rim = rim_height(th)
    # crater interior: lake floor -> steep inner wall
    t_in = np.clip((r - LAKE_R) / (RIM_R - LAKE_R), 0, 1)
    inner = 22 + (rim - 22) * t_in ** 0.35
    # outer slope: concave volcano flank with radial gullies
    t_out = np.clip((r - RIM_R) / (OUT_R - RIM_R), 0, 1)
    gully = noise.ridged(th / 9.0, r / 14.0, 1.0, scale=1.0, octaves=2, seed=SEED + 5)
    outer = PLAIN + (rim - PLAIN) * (1 - t_out) ** 1.8 - 3.5 * gully * (1 - t_out) * t_out * 4
    plain = PLAIN + 1.5 * fbm2(gx, gz, 14, SEED + 6)
    h = np.where(r < RIM_R, inner, np.where(r < OUT_R, outer, plain))
    h += 1.5 * fbm2(gx, gz, 5, SEED + 7) * (r > LAKE_R - 2)
    # the Breach: a V-gorge through the east rim down to the lake, then a lava channel to the edge
    dth = np.abs(wrap_deg(th - BREACH))
    width = 2.5 + 0.06 * np.clip(r - LAKE_R, 0, None)
    across = np.radians(dth) * r
    breach_floor = LAKE_Y - 1 - np.clip(r - RIM_R, 0, None) * 0.18
    v = breach_floor + np.clip(across - width, 0, None) * 2.2
    h = np.where((r > LAKE_R - 3) & (across < 30), np.minimum(h, v), h)
    # processional stair corridor on the south flank (x 100..108)
    stair = (np.abs(gx - 104) < 5.5) & (gz > 104 + RIM_R - 2)
    stair_h = GATE_Y - 1 - np.clip(gz - (104 + RIM_R + 2), 0, None) * 1.0
    h = np.where(stair, np.maximum(np.minimum(h, stair_h + 6), stair_h), h)
    h = np.round(h).astype(int)
    # island edge + underbelly (a floating shard of the underworld)
    edge = EDGE_R + 5 * fbm2(np.cos(np.radians(th)) * 40, np.sin(np.radians(th)) * 40, 18, SEED + 8)
    t = np.clip(1 - r / edge, 0, 1)
    bot = PLAIN - 4 - 70 * t ** 0.85 * (0.6 + 0.4 * (fbm2(gx, gz, 11, SEED + 9) * 0.5 + 0.5))
    bot = np.maximum(bot, 0)
    inside = r < edge
    land = heightmask(s.shape, np.where(inside, h, -1), np.where(inside, bot, 999))
    y = np.arange(s.shape[1])[None, :, None]
    s.fill(land & (y < PLAIN - 3), UNDER)
    s.fill(land & (y >= PLAIN - 3) & (r[:, None, :] >= RIM_R + 3), ASH)
    s.fill(land & (y >= PLAIN - 3) & (r[:, None, :] < RIM_R + 3), CRATER)
    # lava lake (and the breach channel)
    lake = (y <= LAKE_Y) & (y > np.minimum(h, 99)[:, None, :]) & (r[:, None, :] < RIM_R) & inside[:, None, :]
    s.fill(lake, "lava")
    chan = (y == np.minimum(h, 99)[:, None, :] ) & ((dth < 8)[:, None, :]) & ((r > RIM_R - 4) & (r < edge))[:, None, :] \
        & (np.radians(dth) * r < width - 0.5)[:, None, :]
    s.fill(chan, "lava")
    s.meta["edge"] = edge
    return h, r, th


def breach_fall(s, edge):
    """Lava pours off the island edge at the end of the breach channel."""
    a = math.radians(BREACH)
    for k in range(-1, 2):
        for rr in np.arange(EDGE_R - 6, EDGE_R + 8, 0.5):
            x = int(C[0] + math.cos(a) * rr - math.sin(a) * k)
            z = int(C[1] + math.sin(a) * rr + math.cos(a) * k)
            if not (0 <= x < W and 0 <= z < D):
                continue
            col = s.idx[x, :, z]
            if not col.any():
                for y in range(0, PLAIN - 1):
                    s.set(x, y, z, "lava")
                break


def spikes_field(s, h, r, th):
    """The Field of Spears: basalt spikes on the ash plain and the outer flank."""
    rng = np.random.default_rng(SEED + 11)
    for _ in range(90):
        rr = rng.uniform(RIM_R + 6, EDGE_R - 4)
        a = rng.uniform(-180, 180)
        if abs(wrap_deg(a - 90)) < 9 or abs(wrap_deg(a - BREACH)) < 8:
            continue
        x, z = C[0] + math.cos(math.radians(a)) * rr, C[1] + math.sin(math.radians(a)) * rr
        g = h[int(x), int(z)]
        ht = rng.uniform(4, 16) * (1.4 if rr > OUT_R - 6 else 1)
        rad = rng.uniform(0.9, 2.2)
        s.fill(cone((x, 0, z), rad, g - 2, g + ht, 0.3), Mix({"basalt": 3, "blackstone": 1}))


# ------------------------------------------------------------------ the plug
def plug(s):
    r, th = polar(s.shape, C)
    jag = PLUG_R + 2.5 * fbm2(*cols2d(s.shape), 7, SEED + 12)
    cid, n, pts = basalt_cells(s.shape, r < jag + 3, 3.1, SEED + 13)
    rng = np.random.default_rng(SEED + 14)
    pr = np.hypot(pts[:, 0] - C[0], pts[:, 1] - C[1])
    top = np.where(pr < PLUG_R - 5, DECK, DECK - (pr - (PLUG_R - 5)) * 2.6 + rng.uniform(-4, 5, len(pts)))
    top = np.where(rng.random(len(pts)) < 0.12, top + rng.uniform(3, 9, len(pts)), top)   # stray tall pipes
    htop = np.where(cid >= 0, top[np.maximum(cid, 0)], -1)
    col = heightmask(s.shape, np.round(htop).astype(int), np.full(htop.shape, 8))
    s.fill(col, Gradient("y", [(LAKE_Y + 3, Mix({"magma_block": 1, "basalt": 3})), (999, Mix({"basalt": 5, "polished_basalt": 1}))],
                         jitter=2, jitter_scale=4, seed=SEED))
    # sea stacks in the lake
    for a, rr, ht in ((70, 42, 44), (200, 40, 38), (275, 44, 50), (115, 43, 34)):
        x, z = C[0] + math.cos(math.radians(a)) * rr, C[1] + math.sin(math.radians(a)) * rr
        s.fill(cone((x, 0, z), 3.5, 12, ht, 1.2).displace(1.0, 4, seed=a), Mix({"basalt": 3, "blackstone": 1}))


def lava_falls(s):
    for a in FALLS:
        rad = math.radians(a)
        for k in (-1, 0, 1):
            for y in range(LAKE_Y, DECK - 1):
                # walk outwards to the first air cell at this height
                for rr in np.arange(10, PLUG_R + 14, 0.5):
                    x = int(C[0] + math.cos(rad) * rr - math.sin(rad) * k)
                    z = int(C[1] + math.sin(rad) * rr + math.cos(rad) * k)
                    if s.idx[x, y, z] == 0:
                        s.set(x, y, z, "lava")
                        break


# ------------------------------------------------------------------ citadel
def star_wall(s):
    outer = star_prism((C[0], 0, C[1]), DECK - 14, DECK + 14, 6, 31, 21, 28.5, 19.5, phase_deg=0)
    inner = star_prism((C[0], 0, C[1]), DECK + 1, DECK + 30, 6, 27.5, 17.5, 27.5, 17.5, phase_deg=0)
    s.fill(outer - inner, WALL)
    # paving of the bailey
    s.fill(star_prism((C[0], 0, C[1]), DECK - 3, DECK, 6, 28, 18, 28, 18), Mix({"polished_blackstone": 2, "blackstone": 1, "basalt": 1}))
    # gold crown course + spike merlons
    gx, gz = cols2d(s.shape)
    s.fill(shapes.from_mask(s.match("polished_blackstone_bricks") & (np.arange(H)[None, :, None] == DECK + 14)), TRIM)
    # ribbing: pilasters every 3 blocks of perimeter, 1 proud, rising 2 over the crown as spikes; lava-lit slits between
    r, th = polar(s.shape, C)
    y = np.arange(H)[None, :, None]
    shell = (star_prism((C[0], 0, C[1]), DECK - 14, DECK + 16, 6, 32.2, 22.2, 29.7, 20.7).mask(s.shape)
             & ~(outer.mask(s.shape)))
    arc = (np.radians(th) * 30.0) % 3.0
    pil = (arc < 1.0)[:, None, :]
    s.fill(shell & pil & (y <= DECK + 16), "polished_blackstone")
    s.fill(shell & pil & (y >= DECK + 15), TRIM)
    slit = (np.abs(arc - 2.0) < 0.5)[:, None, :] & (y >= DECK + 2) & (y <= DECK + 8)
    s.fill(outer.mask(s.shape) & ~inner.mask(s.shape) & slit & ~star_prism((C[0], 0, C[1]), DECK - 14, DECK + 14, 6, 30.0, 20.0, 27.5, 18.5).mask(s.shape), "magma_block")
    # gate in the south valley
    s.fill(shapes.box((100, DECK + 1, 120), (109, DECK + 10, 128)), "air")


def keep(s):
    c = (C[0], 0, C[1])
    fang = star_prism(c, DECK - 6, FANG_TOP, 6, 13.0, 8.6, 2.0, 1.0, twist_deg=55, phase_deg=30, power=1.5)
    s.fill(fang, OBSIDIAN)
    s.fill(shapes.cylinder(c, 5.5, DECK + 1, 146), "air")                     # the hollow shaft
    s.fill(shapes.cylinder(c, 2.6, DECK + 1, 145), "lava")                    # the caged heart
    # slits in the valleys show the heart
    gx, gz = cols2d(s.shape)
    r, th = polar(s.shape, C)
    y = np.arange(H)[None, :, None]
    for k in range(6):
        a = 30 + 30 + k * 60 + 55 * 0.0
        for y0, y1 in ((DECK + 8, DECK + 40), (DECK + 46, DECK + 60)):
            tw = 55 * ((np.arange(H) - (DECK - 6)) / (FANG_TOP - DECK + 6))
            band = np.abs(wrap_deg(th[:, None, :] - (a + tw[None, :, None]))) * np.pi / 180 * r[:, None, :] < 1.1
            m = band & (y >= y0) & (y <= y1) & (r[:, None, :] < 16)
            s.fill(m & s.match("solid") & ~s.match("lava"), "air")
    # crown chamber: open arcade ring
    for k in range(6):
        a = math.radians(k * 60 + 30 + 40)
        x, z = C[0] + math.cos(a) * 5, C[1] + math.sin(a) * 5
        s.fill(shapes.capsule((x, 152, z), (x, 160, z), 1.6), "air")
    s.fill(shapes.cylinder(c, 4.5, 147, 148), Mix({"polished_blackstone": 1, TRIM: 1}))
    s.fill(shapes.cylinder(c, 3.6, 149, 161), "air")
    # gilded finial: three thorns at the tip
    for k in range(3):
        a = math.radians(k * 120 + 30)
        s.fill(shapes.capsule((C[0] + 0.5, FANG_TOP - 4, C[1] + 0.5), (C[0] + 0.5 + math.cos(a) * 3, FANG_TOP + 4, C[1] + 0.5 + math.sin(a) * 3), 0.6), TRIM)


def horns(s):
    for a in HORNS:
        u = np.array([math.cos(math.radians(a)), 0, math.sin(math.radians(a))])
        cp = lambda rr, y: (C[0] + u[0] * rr, y, C[1] + u[2] * rr)
        path = bezier([cp(25, DECK - 4), cp(52, DECK + 16), cp(46, DECK + 52), cp(14, 118)], 44)
        for sdf in tube(path, 9.0, 0.6, power=1.1):
            s.fill(sdf, HORN)
        # ribs: red rings every few segments
        for i in range(4, 34, 5):
            p0, p1 = path[i], path[i + 1]
            rr = 9.0 + (0.6 - 9.0) * ((i + 0.5) / 44) ** 1.1
            s.fill(shapes.capsule(p0, p1, rr + 0.8) - shapes.capsule(path[i - 1], path[i + 2], rr - 0.5), "red_nether_bricks")


def spires(s):
    for a in SPIRES:
        rr = 26
        x, z = C[0] + math.cos(math.radians(a)) * rr, C[1] + math.sin(math.radians(a)) * rr
        s.fill(star_prism((x, 0, z), DECK - 2, DECK + 44, 4, 7, 4.5, 1.5, 0.8, twist_deg=70, phase_deg=a), WALL)
        s.fill(shapes.cylinder((x, 0, z), 3, DECK + 1, DECK + 20), "air")


def hall(s):
    """The Forge Hall: long hall from the gate to the keep, steep spiked roof."""
    x0, x1, z0, z1 = 96, 112, 108, 126
    s.fill(shapes.box((x0, DECK + 1, z0), (x1 + 1, DECK + 16, z1 + 1)), WALL)
    s.fill(shapes.box((x0 + 2, DECK + 1, z0), (x1 - 1, DECK + 15, z1 - 1)), "air")
    gx, gz = cols2d(s.shape)
    y = np.arange(H)[None, :, None]
    roof = (np.abs(gx - 104.5)[:, None, :] * 1.6 + (y - (DECK + 16)) <= 15) & (y >= DECK + 16) \
        & ((gx >= x0 - 1) & (gx <= x1 + 2) & (gz >= z0) & (gz <= z1 + 1))[:, None, :]
    s.fill(roof, ROOF)
    # roof spikes along the ridge
    for z in range(z0 + 2, z1, 4):
        s.fill(cone((104.5, 0, z + 0.5), 1.2, DECK + 28, DECK + 36, 0.2), "nether_bricks")
    # buttress ribs every 3 blocks on both flanks, spiked
    for z in range(z0 + 1, z1, 3):
        for xb in (x0 - 1, x1 + 2):
            s.fill(shapes.box((xb, DECK - 2, z), (xb + 1, DECK + 17, z + 1)), "polished_blackstone")
            s.fill(cone((xb + 0.5, 0, z + 0.5), 0.9, DECK + 17, DECK + 22, 0.1), TRIM)
    # lava channel down the hall floor
    s.fill(shapes.box((103, DECK, z0), (106, DECK + 1, z1)), "lava")
    s.fill(shapes.box((100, DECK + 1, z1 + 1), (109, DECK + 12, z1 + 3)), "air")    # hall door to the gate court


def bridge(s):
    z0, z1 = 104 + PLUG_R - 2, 104 + RIM_R - 8
    for z in range(int(z0), int(z1) + 1):
        t = (z1 - z) / (z1 - z0)
        yd = int(round(GATE_Y + (DECK - GATE_Y) * t))
        s.box((100, yd - 3, z), (108, yd, z), WALL)
        s.box((100, yd + 1, z), (100, yd + 2, z), "polished_blackstone_wall")
        s.box((108, yd + 1, z), (108, yd + 2, z), "polished_blackstone_wall")
    # piers standing in the lava, pointed arches between
    for zp in (z0 + 7, z0 + 15):
        s.fill(shapes.box((99, 10, zp - 1), (110, GATE_Y + 2, zp + 2)), WALL)
        s.fill(cone((99.5, 0, zp + 0.5), 1.6, GATE_Y + 4, GATE_Y + 16, 0.2), WALL)
        s.fill(cone((109.5, 0, zp + 0.5), 1.6, GATE_Y + 4, GATE_Y + 16, 0.2), WALL)


def gate(s):
    """The Maw: a battered gate tower with a pointed-arch mouth; two tusks rise from its flanks, lean out over the stair
    and cross above it."""
    from scenes.concepts._kit import pointed_arch_2d
    zc = 104 + RIM_R
    s.fill(shapes.box((99, GATE_Y, zc - 14), (110, GATE_Y + 12, zc + 9)), "air")
    s.fill(shapes.box((99, GATE_Y - 1, zc - 14), (110, GATE_Y, zc + 9)), Mix({"polished_blackstone": 2, "blackstone": 1}))
    # battered tower mass (wider at the foot), front face at zc+8
    y = np.arange(H)[None, :, None]
    gx, gz = cols2d(s.shape)
    batter = np.clip((GATE_Y + 30 - y) / 30, 0, 1) * 4
    tower = (np.abs(gx - 104.5)[:, None, :] < 13 + batter) & ((gz > zc - 6) & (gz < zc + 8))[:, None, :]         & (y >= GATE_Y - 10) & (y <= GATE_Y + 30) & ((np.abs(gx - 104.5)[:, None, :] * 0.9 + (y - (GATE_Y + 30))) < 6)
    u = (gx - 104.5)[:, None, :] + 0 * y
    mouth = pointed_arch_2d(u, (y - GATE_Y) + 0 * gx[:, None, :], 5.5, 9) & (y >= GATE_Y) & ((gz > zc - 7) & (gz < zc + 9))[:, None, :]
    s.fill(tower & ~mouth, WALL)
    s.fill(mouth & ((gz > zc - 7) & (gz < zc + 9))[:, None, :], "air")
    # recessed second arch (depth)
    rim = pointed_arch_2d(u, (y - GATE_Y) + 0 * gx[:, None, :], 7.5, 10) & ~mouth & (y >= GATE_Y) & ((gz >= zc + 7) & (gz < zc + 8))[:, None, :]
    s.fill(rim, "air")
    s.fill(pointed_arch_2d(u, (y - GATE_Y) + 0 * gx[:, None, :], 8.5, 10.5) & ~pointed_arch_2d(u, (y - GATE_Y) + 0 * gx[:, None, :], 7.5, 10)
           & (y >= GATE_Y) & ((gz >= zc + 7) & (gz < zc + 10))[:, None, :], TRIM)
    for side in (-1, 1):
        path = bezier([(104.5 + side * 15, GATE_Y - 8, zc + 2), (104.5 + side * 22, GATE_Y + 26, zc + 12),
                       (104.5 + side * 10, GATE_Y + 50, zc + 22), (104.5 - side * 7, GATE_Y + 50, zc + 16)], 36)
        for sdf in tube(path, 6.5, 0.6, power=1.1):
            s.fill(sdf, HORN)


def keep_collars(s):
    """Star-shaped ledges that break the Fang's taper (gallery rings), with gilded lips."""
    c = (C[0], 0, C[1])
    for yc, ro, ri in ((DECK + 30, 15.5, 10), (DECK + 56, 13, 8.5), (DECK + 80, 10.5, 7), (DECK + 102, 8, 5.5)):
        tw = 55 * (yc - (DECK - 6)) / (FANG_TOP - DECK + 6)
        s.fill(star_prism(c, yc - 2, yc + 1, 6, ro, ri, ro - 1.5, ri - 1, phase_deg=30 + tw), Mix({"polished_blackstone_bricks": 2, "blackstone": 1}))
        s.fill(star_prism(c, yc + 2, yc + 2, 6, ro - 0.5, ri - 0.5, ro - 0.5, ri - 0.5, phase_deg=30 + tw), TRIM)
        s.fill(star_prism(c, yc - 4, yc - 3, 6, ro - 2.5, ri - 2, ro - 1.5, ri - 1.5, phase_deg=30 + tw), "polished_blackstone_bricks")


def stair(s):
    zc = 104 + RIM_R + 6
    for z in range(zc, D):
        y = GATE_Y - 1 - (z - zc)
        if y < PLAIN - 2:
            break
        s.box((99, y - 4, z), (109, y, z), Mix({"polished_blackstone": 3, "blackstone": 1}))
        s.box((99, y + 1, z), (109, y + 8, z), "air")
        if z % 6 == 0:
            for x in (98.5, 110.5):
                s.fill(cone((x, 0, z + 0.5), 1.4, y - 3, y + 9, 0.2), Mix({"basalt": 2, "blackstone": 1}))


def rim_wall(s, h, r, th):
    y = np.arange(H)[None, :, None]
    crest = np.round(rim_height(th)).astype(int)
    near = (np.abs(r - RIM_R) < 2.2) & (np.abs(wrap_deg(th + 90)) > 26) & (np.abs(wrap_deg(th - BREACH)) > 12)
    gx, gz = cols2d(s.shape)
    merlon = ((np.round(np.radians(th) * RIM_R)).astype(int) % 4 < 2)
    top = crest + 8 + merlon * 2
    m = near[:, None, :] & (y >= crest[:, None, :] - 8) & (y <= top[:, None, :])
    s.fill(m, WALL)
    for a, rad, ht in RIM_FANGS:
        rr = RIM_R + (2 if a != -90 else -1)
        x, z = C[0] + math.cos(math.radians(a)) * rr, C[1] + math.sin(math.radians(a)) * rr
        base = rim_height(np.array(a, float))
        s.fill(star_prism((x, 0, z), float(base) - 14, float(base) + ht, 5, rad, rad * 0.62, 1.2, 0.6,
                          twist_deg=40, phase_deg=a, power=1.3), WALL)


def build():
    s = Scene((W, H, D), "concept_infernal", seed=SEED)
    h, r, th = terrain(s)
    spikes_field(s, h, r, th)
    plug(s)
    lava_falls(s)
    star_wall(s)
    horns(s)
    spires(s)
    keep(s)
    keep_collars(s)
    hall(s)
    bridge(s)
    rim_wall(s, h, r, th)
    gate(s)
    stair(s)
    breach_fall(s, s.meta.pop("edge"))
    # cameras
    zc = 104 + RIM_R
    s.mark("spawn_approach", (84, ground_y(s, 84, 198), 198), look_at=(104, 118, 104))
    s.markers["spawn_approach"]["fov"] = 80
    s.mark("cam_stairfoot", (104, ground_y(s, 104, 196), 196), look_at=(104, 80, 120))
    s.mark("cam_gate", (104, GATE_Y, zc - 10), look_at=(104, 105, 104))
    s.mark("cam_bailey", (120, DECK + 1, 110), look_at=(104, 170, 104))
    s.mark("cam_heart", (104, DECK + 1, 99), look_at=(104, 122, 104.5))
    xr = int(C[0] - RIM_R + 5)
    s.mark("cam_rimwest", (xr, ground_y(s, xr, 104), 104), look_at=(104, 90, 104))
    bx, bz = int(C[0] + 86 * math.cos(math.radians(40))), int(C[1] + 86 * math.sin(math.radians(40)))
    s.mark("cam_breach", (bx, ground_y(s, bx, bz), bz), look_at=(C[0] + 75, 30, C[1] + 14))
    s.mark("cam_hero", (198, 118, 200), look_at=(104, 84, 102))
    s.markers["cam_hero"]["fov"] = 55
    s.meta["mood"] = "ember"
    s.meta["origin"] = [-104, 30, -104]
    return s
