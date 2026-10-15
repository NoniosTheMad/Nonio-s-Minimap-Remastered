"""The armillary: three graduated copper rings on axles around the Spire (the signature).

Each ring is an instrument band, not a tube. Ring-local coordinates: theta (deg, along the ring, 0 = the +axle pin),
q = radial offset from the band's mid-radius (+ out), w = offset along the ring's axis (its normal).
Cross-section (a channel / I-beam):
  rims   |w| > hw-1, solid cut copper, proud of both faces by 1      -> two bright rails that draw the circle
  web    |q| <= .75 between the rims, copper GRATE (lattice)         -> light passes, the band reads thin
  ribs   transverse every 5 deg, chiseled copper, full depth          -> rhythm
  ticks  outer rim face: chiseled every 2 deg; teeth every 10 deg (+1 out and +1 sideways) -> graduated scale
  plates every 30 deg (ring 1: the 12 signs; ring 2: the 12 hours; ring 3: the 7 wanderers): a solid plate with a
         5x5 glyph in relief, calcite on the outer face, amethyst inlay on the inner face; lit bulbs on both rims.
Ages: ring 1 oxidized, ring 2 weathered, ring 3 exposed (the Spire ribs are fresh copper): one sky, three ages.
Gimbal logic: every ring pivots on a horizontal axle along its tilt axis at the hub (y=HUB_Y): the axle runs from
the Spire's toothed hub collar to a bearing that pins the ring (boss through the band + an outer cap); collars on
the axle every 7 blocks. Axle directions 0/60/120 deg, so six spokes radiate from the hub like a compass rose."""
import math

import numpy as np

from tools.voxel import shapes

from .common import C, HUB_Y, SEED, Box, cu, rot, to_local

RING_C = (C[0], HUB_Y + 0.5, C[1])
#        R    hw   ht   tilt  yaw  age          glyph set
# tilt/yaw chosen by a clearance search against the castle + Spire (no voxel within 1 block of a tower crown, the
# turret or the gallery decks); hinge (axle) directions 0/180, 240/60, 330/150 deg: three distinct gimbal axes
RINGS = [(61, 3.0, 1.2, 16, 0, "oxidized", "signs"),
         (47, 2.6, 1.1, 30, 120, "weathered", "hours"),
         (28, 2.6, 1.0, 48, 30, "exposed", "planets")]
# per ring: accent age (rungs + teeth) and degree tick (rung spacing)
RING_STYLE = [("", 5.0), ("exposed", 5.0), ("oxidized", 10.0)]

# 5x5 glyphs, rows top (w>0) to bottom; '#' = relief pixel
_G = {
    "aries": ["#...#", "#.#.#", ".###.", "..#..", "..#.."],
    "taurus": ["#...#", ".###.", "#...#", "#...#", ".###."],
    "gemini": ["#####", ".#.#.", ".#.#.", ".#.#.", "#####"],
    "cancer": [".###.", "#...#", "..#..", "#...#", ".###."],
    "leo": [".##..", "#..#.", ".#.#.", "...#.", "...##"],
    "virgo": ["#.#.#", "#.#.#", "#.#.#", "#.###", "....#"],
    "libra": ["..#..", ".#.#.", "#####", ".....", "#####"],
    "scorpio": ["#.#..", "#.#..", "#.#..", "#.#.#", "...##"],
    "sagittarius": ["..###", "...##", "..#.#", ".#...", "#...."],
    "capricorn": ["#.#..", ".#.#.", ".#.##", ".#.##", "..#.."],
    "aquarius": [".#.#.", "#.#.#", ".....", ".#.#.", "#.#.#"],
    "pisces": ["#...#", ".#.#.", "#####", ".#.#.", "#...#"],
    "sun": [".###.", "#...#", "#.#.#", "#...#", ".###."],
    "moon": [".##..", "#....", "#....", "#....", ".##.."],
    "mercury": ["#...#", ".###.", ".#.#.", ".###.", "..#.."],
    "venus": [".###.", "#...#", ".###.", "..#..", ".###."],
    "mars": ["..###", "...##", ".###.", "#..#.", ".##.."],
    "jupiter": [".#...", "#.#..", "..#..", ".####", "...#."],
    "saturn": ["###..", ".#...", ".###.", ".#..#", ".#.#."],
}
SIGNS = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn",
         "aquarius", "pisces"]
PLANETS = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"]


def _hours(n):
    """Dot glyph for hour n (1..12): dots on a 5x5 dial."""
    pts = [(0, 0), (0, 2), (0, 4), (2, 4), (4, 4), (4, 2), (4, 0), (2, 0), (1, 1), (1, 3), (3, 3), (3, 1)]
    g = [["."] * 5 for _ in range(5)]
    for k in range(n):
        r, c = pts[k]
        g[r][c] = "#"
    g[2][2] = "#"
    return ["".join(r) for r in g]


def glyph_set(kind):
    if kind == "signs":
        return [(i * 30.0 + 15.0, _G[n]) for i, n in enumerate(SIGNS)]
    if kind == "hours":
        return [(i * 30.0 + 15.0, _hours(i + 1)) for i in range(12)]
    return [(i * 360.0 / 7 + 25.7, _G[n]) for i, n in enumerate(PLANETS)]


def ring_frame(R, tilt, yaw):
    M = rot(tilt_x=tilt, yaw=yaw)
    return M


def band(s, R, hw, ht, tilt, yaw, age, glyphs, k, accent, tick_deg, rc=None, keep=None, replace=None):
    """Voxelise one ring as an open truss: two rails, rungs at every degree tick, proud teeth on the outer face every
    major tick, glyph plates at the plate angles. Sky shows between the rungs, so the ring reads as fine metalwork."""
    RC = RING_C if rc is None else rc
    M = ring_frame(R, tilt, yaw)
    ext = R + ht + 3
    yext = ext * math.sin(math.radians(tilt)) + hw + 3
    b = Box(s, (RC[0] - ext, RC[1] - yext, RC[2] - ext), (RC[0] + ext + 1, RC[1] + yext + 1, RC[2] + ext + 1))
    lx, ly, lz = to_local(M, RC, b.x, b.y, b.z)
    rho = np.sqrt(lx ** 2 + lz ** 2)
    q = rho - R
    w = ly
    th = (np.degrees(np.arctan2(lz, lx)) + 360) % 360
    centres = np.array([g[0] for g in glyphs])
    dth = (th[..., None] - centres + 180) % 360 - 180
    gi = np.argmin(np.abs(dth), axis=-1)
    du = np.take_along_axis(dth, gi[..., None], -1)[..., 0] * math.pi / 180 * R
    aw, aq = np.abs(w), np.abs(q)
    deg2u = math.pi / 180 * R
    inband = (aw <= hw) & (aq <= ht)
    plate = (np.abs(du) <= 3.5) & inband
    rail_t = 1.3
    rail = inband & (aw > hw - rail_t)
    # rungs at every tick (in degrees), offset half a tick from the plates so they frame them
    tk = np.abs(((th + tick_deg / 2) % tick_deg) - tick_deg / 2) * deg2u
    rung = inband & (tk <= 0.55) & (np.abs(du) > 4.2)
    # major ticks every 3 ticks: a proud tooth across the outer face
    maj = np.abs(((th + tick_deg * 1.5) % (tick_deg * 3)) - tick_deg * 1.5) * deg2u
    tooth = (maj <= 0.55) & (aw <= hw - 0.3) & (q > ht - 0.5) & (q <= ht + 1.25) & (np.abs(du) > 4.2)
    # glyph pixels: rows across w (top row = +w), columns along u
    col = np.round(du + 2).astype(int)
    row = np.round(2 - w).astype(int)
    inside_g = (np.abs(du) <= 3.5) & (col >= 0) & (col < 5) & (row >= 0) & (row < 5)
    pix = np.zeros(q.shape, bool)
    for i, (_, g) in enumerate(glyphs):
        bm = np.array([[c == "#" for c in r] for r in g])
        sel = inside_g & (gi == i)
        pix[sel] = bm[row[sel], col[sel]]
    relief_out = pix & (q > ht - 0.5) & (q <= ht + 1.0)
    solid = rail | rung | plate | tooth | relief_out
    if keep is not None:                         # a sector only (the Fallen Arc): keep(th_deg) -> bool
        solid &= keep(th)
    if not solid.any():
        return None
    names = np.empty(q.shape, object)
    names[...] = None
    names[rail] = cu(age, "cut")
    # outer face of the rails: a calcite tick at every degree tick (the graduated scale)
    names[rail & (tk <= 0.55) & (q > ht - 1.0)] = "calcite"
    names[rung] = cu(accent, "chiseled")
    names[rail & rung & (q > ht - 1.0)] = "calcite"
    names[plate] = cu(age, "block")
    names[plate & (aw > hw - rail_t)] = cu(age, "cut")
    names[tooth] = cu(accent, "cut")
    names[relief_out] = "calcite"
    names[plate & pix & (q < -ht + 1.0)] = "amethyst_block"
    m = b.full(solid)
    vals = names[solid]
    xs, ys, zs = np.nonzero(m)
    for state in set(vals.tolist()):
        if state is None:
            continue
        sel = vals == state
        mm = np.zeros(s.shape, bool)
        mm[xs[sel], ys[sel], zs[sel]] = True
        s.fill(mm, state, replace=replace)
    # lit bulbs on both rails at each plate centre
    for ang, _ in glyphs:
        if keep is not None and not keep(np.array(ang)):
            continue
        for side in (-1, 1):
            for du_ in (-3.0, 3.0):
                a2 = math.radians(ang) + du_ / R
                p = np.array([math.cos(a2) * R, side * (hw - 0.6), math.sin(a2) * R])
                wp = M @ p + np.array(RC)
                s.set(int(math.floor(wp[0])), int(math.floor(wp[1])), int(math.floor(wp[2])), cu(age, "bulb", lit="true", powered="false"))
    return M


def axle(s, R, ht, tilt, yaw, age, hub_r):
    """Axle along the tilt axis from the hub collar to the bearing on the ring, both ends."""
    M = ring_frame(R, tilt, yaw)
    ax = M @ np.array([1.0, 0, 0])
    c = np.array(RING_C)
    for sgn in (1, -1):
        d = ax * sgn
        a = c + d * hub_r
        bpt = c + d * (R - ht - 0.5)
        s.fill(shapes.capsule(a, bpt, 1.15), cu(age, "cut"))
        # collars every 7 blocks
        L = R - ht - hub_r
        for t in np.arange(5, L - 3, 7):
            p = a + d * t
            col = shapes.SDF(lambda X, Y, Z, p=p, d=d: np.maximum(
                np.abs((X - p[0]) * d[0] + (Y - p[1]) * d[1] + (Z - p[2]) * d[2]) - 0.5,
                np.sqrt(np.maximum(0, (X - p[0]) ** 2 + (Y - p[1]) ** 2 + (Z - p[2]) ** 2 -
                                   ((X - p[0]) * d[0] + (Y - p[1]) * d[1] + (Z - p[2]) * d[2]) ** 2)) - 2.2),
                ((p[0] - 3, p[1] - 3, p[2] - 3), (p[0] + 3, p[1] + 3, p[2] + 3)))
            s.fill(col, cu("oxidized" if age != "oxidized" else "", "chiseled"))
        # bearing: a pin through the band with a boss inside and a cap outside
        pin_a, pin_b = c + d * (R - ht - 3.0), c + d * (R + ht + 2.5)
        s.fill(shapes.capsule(pin_a, pin_b, 1.6), cu("", "chiseled"))
        s.fill(shapes.sphere(tuple(c + d * (R - ht - 2.6)), 2.6), cu(age, "block"))
        s.fill(shapes.sphere(tuple(c + d * (R + ht + 2.8)), 2.0), cu("", "cut"))
        tip = c + d * (R + ht + 5.0)
        s.set(int(math.floor(tip[0])), int(math.floor(tip[1])), int(math.floor(tip[2])), cu("", "bulb", lit="true", powered="false"))


def hub_collar(s, r=12.5):
    """Toothed gear collar around the Spire at the hub height: the axles start here."""
    b = Box(s, (C[0] - r - 3, HUB_Y - 3, C[1] - r - 3), (C[0] + r + 4, HUB_Y + 4, C[1] + r + 4))
    rr = np.hypot(b.x - C[0], b.z - C[1])
    th = np.degrees(np.arctan2(b.z - C[1], b.x - C[0]))
    teeth = np.abs(((th + 360) % 10) - 5) < 2.6
    body = (rr <= r) & (rr > r - 3) & (np.abs(b.y - RING_C[1]) <= 2.0)
    tooth = teeth & (rr <= r + 1.6) & (rr > r) & (np.abs(b.y - RING_C[1]) <= 1.0)
    b.fill(body & (np.abs(b.y - RING_C[1]) > 1.0), cu("", "cut"))
    b.fill(body & (np.abs(b.y - RING_C[1]) <= 1.0), cu("exposed", "chiseled"))
    b.fill(tooth, cu("", "block"))


def clearance(s, before):
    """Report ring voxels that landed on cells that were already solid (collisions with the castle/Spire)."""
    hit = before & (s.idx != 0)
    return int(hit.sum())


def inner_shafts(s):
    """The axles continue through the Spire wall into the Gear Room and meet a central gear drum (overhead: the
    shafts run at HUB_Y, two blocks above the gear-room floor)."""
    c = np.array(RING_C)
    for R, hw, ht, tilt, yaw, age, gl in RINGS:
        ax = ring_frame(R, tilt, yaw) @ np.array([1.0, 0, 0])
        s.fill(shapes.capsule(tuple(c - ax * 12.5), tuple(c + ax * 12.5), 0.6), cu(age, "cut"))
    s.fill(shapes.cylinder((C[0], 0, C[1]), 2.4, HUB_Y - 1, HUB_Y + 2), cu("", "chiseled"))
    b = Box(s, (C[0] - 4, HUB_Y - 1, C[1] - 4), (C[0] + 5, HUB_Y + 3, C[1] + 5))
    rr = np.hypot(b.x - C[0], b.z - C[1])
    th = np.degrees(np.arctan2(b.z - C[1], b.x - C[0]))
    b.fill((rr > 2.4) & (rr <= 3.4) & (np.abs(((th + 360) % 30) - 15) < 6) & (b.y > HUB_Y - 0.5) & (b.y < HUB_Y + 1.5), cu("", "cut"))


def build(s, ctx):
    hub_collar(s)
    inner_shafts(s)
    old = s.idx.copy()
    for k, (R, hw, ht, tilt, yaw, age, gl) in enumerate(RINGS):
        band(s, R, hw, ht, tilt, yaw, age, glyph_set(gl), k, *RING_STYLE[k])
    for k, (R, hw, ht, tilt, yaw, age, gl) in enumerate(RINGS):
        axle(s, R, ht, tilt, yaw, age, hub_r=12.0)
    # collisions: ring/axle voxels written over cells that were solid before the bands (castle, Spire, turret);
    # the spire wall where the axles enter it is expected (bearings), so only count cells beyond the spire radius + 1
    hit = (s.idx != old) & (old != 0)
    xs, ys, zs = np.nonzero(hit)
    from .spire import radius as spire_r
    far = np.hypot(xs + 0.5 - C[0], zs + 0.5 - C[1]) > spire_r(np.clip(ys, 0, 250)) + 1.0
    ctx["ring_hits"] = int(far.sum())
    ctx["ring_hit_cells"] = list(zip(xs[far].tolist(), ys[far].tolist(), zs[far].tolist()))[:2000]
    ctx["rings"] = RINGS
