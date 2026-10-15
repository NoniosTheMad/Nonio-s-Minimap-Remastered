"""Concept C: OUR LADY OF THE CHASM (gothic cathedral-fortress), massing + silhouette model.

Brief
  When the earthquake split the plateau, the bishops did not move the cathedral: they bridged the wound. The nave stands
  on the south lip, the fortified choir on the north lip, and the crossing and both transept arms hang over the chasm
  on arches whose piers stride down to the river like legs. A curtain wall with round towers rings the plateau.
  Mood: golden afternoon, warm limestone against slate roofs and green copper spires. References: Albi (fortified
  brick apse), Chartres / Reims (twin-tower front, rose, flyers), Mont-Saint-Michel (church as fortress), Ronda's
  Puente Nuevo (arches down into a gorge), Carcassonne (round towers, conical roofs).

Scale: plateau ~210 across, castle (curtain wall) ~136 x 168, crossing spire tip ~y200 (~156 over the plateau).
Render: python -m tools.voxel render scenes/concepts/gothic.py --mood golden
"""
import math

import numpy as np

from scenes.concepts._kit import bezier, cols2d, cone, fbm2, heightmask, pointed_arch_2d, star_prism, tube, union
from tools.voxel import noise, shapes
from tools.voxel.palette import Gradient, Mix, Noise
from tools.voxel.scene import Scene

W, H, D = 208, 218, 240
SEED = 1163
G = 44                  # plateau / cathedral floor level
RIVER = 12              # river surface in the chasm
CH_Z = 106              # chasm centre line (runs east-west)
CH_HALF = 23            # chasm half width at the top
XC = 104                # cathedral axis (x)

# cathedral plan (z grows to the south; the front faces south)
NAVE = (93, 115)        # x of the nave outer walls
AISLE = 8               # aisle width each side
EAVE, AISLE_EAVE = 82, 62
CROSS = (90, 118, 93, 121)          # crossing tower x0, x1, z0, z1
NAVE_Z = (121, 160)
CHOIR_Z = (54, 93)
APSE_C = (XC, 54)
FRONT_Z = (160, 176)                # front block / towers
TOWER_X = ((75, 93), (115, 133))
TRANSEPT = (66, 142, 98, 116)       # x0, x1, z0, z1

# ------------------------------------------------------------------ materials
LIME = Gradient("y", [(G - 10, Mix({"stone_bricks": 2, "andesite": 2, "mossy_stone_bricks": 1})),
                      (G + 4, Mix({"stone_bricks": 2, "polished_andesite": 2, "smooth_stone": 1})),
                      (G + 24, Mix({"smooth_stone": 2, "polished_diorite": 2, "calcite": 1, "end_stone_bricks": 0.6})),
                      (G + 50, Mix({"calcite": 3, "polished_diorite": 1, "end_stone_bricks": 1})),
                      (999, Mix({"calcite": 3, "smooth_quartz": 1, "end_stone_bricks": 1}))], jitter=3, jitter_scale=6, seed=SEED)
TRIM = Mix({"calcite": 2, "smooth_quartz": 1, "quartz_bricks": 1})
RIB = Mix({"deepslate_bricks": 3, "polished_deepslate": 1})
ROOF = Mix({"deepslate_tiles": 4, "polished_deepslate": 1, "cracked_deepslate_tiles": 0.5})
COPPER = Gradient("y", [(140, Mix({"weathered_cut_copper": 2, "oxidized_cut_copper": 1})),
                        (999, Mix({"oxidized_cut_copper": 3, "oxidized_copper": 1}))], jitter=4, jitter_scale=5, seed=SEED + 1)
GLASS = Mix({"blue_stained_glass": 3, "red_stained_glass": 2, "purple_stained_glass": 1, "yellow_stained_glass": 1})
FLOOR = Mix({"polished_andesite": 2, "calcite": 1})
ROCK = Gradient("y", [(RIVER + 4, Mix({"mossy_cobblestone": 1, "andesite": 2, "stone": 2})),
                      (G - 14, Mix({"stone": 3, "andesite": 2, "tuff": 1})),
                      (999, Mix({"stone": 2, "andesite": 2, "calcite": 1, "diorite": 1}))], jitter=4, jitter_scale=8, seed=SEED + 2)
TURF = Noise([(-0.3, Mix({"grass_block": 3, "moss_block": 1})), (0.25, "grass_block"),
              (1, Mix({"grass_block": 2, "coarse_dirt": 1, "rooted_dirt": 1}))], scale=9, seed=SEED)
PAVING = Noise([(-0.2, Mix({"stone_bricks": 2, "polished_andesite": 1})), (0.3, Mix({"andesite": 1, "stone_bricks": 1, "gravel": 0.4})),
                (1, Mix({"polished_andesite": 2, "calcite": 1}))], scale=5, seed=SEED + 3)

X = np.arange(W)[:, None, None]
Y = np.arange(H)[None, :, None]
Z = np.arange(D)[None, None, :]


def B(x0, x1, y0, y1, z0, z1):
    """Full-grid bool for an inclusive box (clipped)."""
    m = np.zeros((W, H, D), bool)
    m[max(0, int(x0)):max(0, int(x1) + 1), max(0, int(y0)):max(0, int(y1) + 1), max(0, int(z0)):max(0, int(z1) + 1)] = True
    return m


def ground_y(s, x, z):
    nz = np.nonzero(s.idx[int(x), :, int(z)])[0]
    return int(nz.max()) + 1 if len(nz) else 0


def chasm_z(x):
    """Meandering centre line of the chasm."""
    return CH_Z + 3.0 * np.sin((np.asarray(x) - 20) / 26.0)


# ------------------------------------------------------------------ terrain: the split plateau
def terrain(s):
    gx, gz = cols2d(s.shape)
    h = G - 1 + 1.5 * fbm2(gx, gz, 20, SEED) + 0.8 * fbm2(gx, gz, 6, SEED + 1)
    # plateau edge: falls away in cliffs at the scene border
    rr = np.hypot((gx - XC) / 106, (gz - 108) / 104) ** 1.0 + 0.05 * fbm2(gx, gz, 14, SEED + 2)
    spur = (gz > 160) & (np.abs(gx - XC) < 15 + 3 * fbm2(gx, gz, 9, SEED + 5))
    h = np.where(spur & (gz > 200), np.minimum(h, G - 1 - (gz - 200) * 0.3), h)
    h = np.where((rr > 0.93) & ~spur, h - (rr - 0.93) * 600, h)
    h = np.where(spur & (rr > 0.93), h - 2 * np.clip(np.abs(gx - XC) - 11, 0, None), h)
    # the chasm: steep walls, narrowing downwards, a ledge or two
    dzc = np.abs(gz - chasm_z(gx))
    wall = CH_HALF + 2.2 * fbm2(gx, gz, 7, SEED + 3)
    depth = np.clip((wall - dzc) / 1.0, 0, None)
    floor = RIVER - 4 + 0.5 * dzc
    chasm_h = np.maximum(floor, G - 1 - depth * 4.0 - np.clip(depth - 4, 0, None) * 2)
    h = np.where(dzc < wall + 1, np.minimum(h, chasm_h), h)
    # east: the river drops off the plateau edge (waterfall), so the floor steps down past x=176
    h = np.where((gx > 176) & (dzc < wall), np.minimum(h, 2), h)
    h = np.round(np.clip(h, 1, None)).astype(int)
    h = np.where((h <= 2) & (dzc > 9), -1, h)          # beyond the plateau cliffs: void (diorama)
    m = heightmask(s.shape, h)
    s.fill(m, ROCK)
    top = m & ~np.roll(m, -1, axis=1)
    s.fill(top & (Y > G - 4), TURF)
    water = (Y <= RIVER) & (Y > h[:, None, :]) & (np.abs(gz - chasm_z(gx)) < CH_HALF + 2)[:, None, :] & (X <= 176)
    s.fill(water, "water")
    # the fall
    fall = (X >= 177) & (X <= 178) & (Y <= RIVER) & (Y > 2) & (np.abs(gz - chasm_z(gx)) < 5)[:, None, :]
    s.fill(fall, "water")
    s.fill((Y <= 3) & (Y > h[:, None, :]) & (X > 176) & (np.abs(gz - chasm_z(gx)) < 8)[:, None, :], "water")
    return h


# ------------------------------------------------------------------ gothic hall kit
def hall(s, t0, t1, l0, l1, y0, eave, axis="z", bay=7, pil_from=None, pitch=1.4, ends=(True, True), clerestory_from=None,
         lanterns=True):
    """A gothic hall: thick shell, pointed barrel vault with dark transverse ribs and wall shafts, lancet windows (glass
    one block behind the outer face) between buttress pilasters that rise into pinnacles, merlon parapet, steep slate
    roof with a spiked crest. axis = direction of the ridge ('z' or 'x'); t = across, l = along."""
    T, L = (X, Z) if axis == "z" else (Z, X)
    tc, half = (t0 + t1) / 2, (t1 - t0) / 2
    inT = (T >= t0) & (T <= t1)
    inL = (L >= l0) & (L <= l1)
    s.fill(inT & inL & (Y >= y0 - 4) & (Y <= eave), LIME)
    # interior + vault
    it = (T >= t0 + 2) & (T <= t1 - 2) & (L >= l0 + (2 if ends[0] else 0)) & (L <= l1 - (2 if ends[1] else 0))
    hs, sp = half - 2 + 0.5, (eave - y0) * 0.5
    arch = pointed_arch_2d(T + 0.5 - tc - 0.5 * 0, Y - y0, hs, sp) & (Y > y0)
    s.fill(it & arch & (Y < eave), "air")
    s.fill(it & (Y == y0), FLOOR)
    s.fill(it & (Y == y0) & (((T - int(tc)) % 6 == 0) | ((L - l0) % bay == 0)), "polished_deepslate")
    rib_ring = it & arch & ~pointed_arch_2d(T + 0.5 - tc, Y - y0, hs - 1, sp) & (Y > y0)
    bays = (L - l0) % bay == 0
    s.fill(rib_ring & bays, RIB)
    s.fill(it & bays & ((T == t0 + 2) | (T == t1 - 2)) & (Y > y0) & (Y < y0 + sp), RIB)
    # ridge rib along the apex
    apex = int(y0 + sp + hs * 1.6)
    s.fill(it & (np.abs(T + 0.5 - tc) < 1) & (Y >= apex - 1) & (Y <= apex) & ~arch.__invert__(), RIB)
    # outer buttress pilasters (+2, stepped +3 low) rising 4 above the eave into pinnacles
    pf = y0 if pil_from is None else pil_from
    ks = range(l0 + bay, l1 - 1, bay)
    for k in ks:
        for side in (-1, 1):
            tt = t0 if side < 0 else t1
            if side < 0:
                s.fill((T >= tt - 2) & (T <= tt - 1) & (L >= k - 1) & (L <= k) & (Y >= pf - 4) & (Y <= eave + 4), LIME)
                s.fill((T == tt - 3) & (L >= k - 1) & (L <= k) & (Y >= pf - 4) & (Y <= (pf + eave) // 2), LIME)
                s.fill((T >= tt - 2) & (T <= tt - 1) & (L >= k - 1) & (L <= k) & (Y >= eave + 5) & (Y <= eave + 8), TRIM)
            else:
                s.fill((T >= tt + 1) & (T <= tt + 2) & (L >= k - 1) & (L <= k) & (Y >= pf - 4) & (Y <= eave + 4), LIME)
                s.fill((T == tt + 3) & (L >= k - 1) & (L <= k) & (Y >= pf - 4) & (Y <= (pf + eave) // 2), LIME)
                s.fill((T >= tt + 1) & (T <= tt + 2) & (L >= k - 1) & (L <= k) & (Y >= eave + 5) & (Y <= eave + 8), TRIM)
    # lancet windows, one per bay, recessed: outer course air, inner course glass
    wy0 = (pf if clerestory_from is None else clerestory_from) + 4
    wsp = max(3, eave - 5 - wy0 - 4)
    for k in range(l0 + bay // 2 + (1 if bay % 2 else 0), l1 - 1, bay):
        win = pointed_arch_2d(L - k, Y - wy0, 1.5, wsp) & (Y >= wy0)
        twin = pointed_arch_2d(L - k, Y - wy0, 2.5, wsp) & (Y >= wy0 - 1)
        for tt, sgn in ((t0, 1), (t1, -1)):
            s.fill(twin & (T == tt) & ~win, TRIM)
            s.fill(win & (T == tt), "air")
            s.fill(win & (T == tt + sgn), GLASS)
    # parapet: merlons on the outer edge
    s.fill(inT & inL & ((T == t0) | (T == t1)) & (Y == eave + 1) & ((L % 2) == 0), TRIM)
    # roof
    rise = (half + 1 - np.abs(T + 0.5 - tc)) * pitch
    roofm = (Y > eave) & (Y - eave <= rise) & (T >= t0 - 0) & (T <= t1 + 0) & (L >= l0 + 1) & (L <= l1 - 1)
    roofm &= ~(((T == t0) | (T == t1)) & (Y == eave + 1))
    s.fill(roofm & (Y > eave + 1) | ((Y == eave + 1) & (T > t0) & (T < t1) & inL), ROOF)
    ridge = int(eave + (half + 0.5) * pitch)
    s.fill((np.abs(T + 0.5 - tc) < 1.1) & (L >= l0 + 1) & (L <= l1 - 1) & (Y == ridge + 1) & ((L % 2) == 0), TRIM)
    # gable walls (LIME) at the ends
    for e, lv in zip(ends, (l0, l1)):
        if e:
            g = (Y > eave) & (Y - eave <= rise) & (L >= lv - (0 if lv == l0 else 1)) & (L <= lv + (1 if lv == l0 else 0)) & inT
            s.fill(g, LIME)
    # hanging lanterns at bay centres
    if lanterns:
        for k in range(l0 + bay // 2, l1 - 1, bay):
            low = max(y0 + 12, apex - 22)
            for yy in range(low + 1, apex):
                if axis == "z":
                    s.set(int(tc), yy, k, "iron_chain[axis=y]")
                else:
                    s.set(k, yy, int(tc), "iron_chain[axis=y]")
            if axis == "z":
                s.set(int(tc), low, k, "lantern[hanging=true]")
            else:
                s.set(k, low, int(tc), "lantern[hanging=true]")
    return ridge


def lancet_band(s, axis, plane, c, y0, n, gap, hs=1.5, spring=6, depth_sign=1):
    """A row of n lancets in a wall plane (axis='z' -> wall at X=plane, lancets spaced along Z)."""
    U, P = (Z, X) if axis == "z" else (X, Z)
    for i in range(n):
        u = c + (i - (n - 1) / 2) * gap
        win = pointed_arch_2d(U - u, Y - y0, hs, spring) & (Y >= y0)
        s.fill(win & (P == plane), "air")
        s.fill(win & (P == plane - depth_sign), GLASS)


def rose(s, xc, yc, zface, R, normal=1, axis="z"):
    """Rose window in a wall facing +z (normal=1) / -z, or along x if axis='x': recessed glass disc with a trim frame,
    12 spokes, an inner ring and a hub; set in a pointed recess with 3 nested rings."""
    U, P = (X, Z) if axis == "z" else (Z, X)
    u0 = xc if axis == "z" else zc_dummy(xc)
    du, dv = U + 0.5 - u0, Y + 0.5 - yc
    rr = np.sqrt(du ** 2 + dv ** 2)
    ang = np.degrees(np.arctan2(dv, du))
    for i in range(3):     # nested recess rings around the rose (pointed)
        hs = R + 3 - i
        rec = pointed_arch_2d(du, Y - (yc - R - 2), hs, R + 2) & (Y >= yc - R - 2)
        mat = TRIM if i % 2 == 0 else LIME
        s.fill(rec & (P == zface - normal * i) & ~pointed_arch_2d(du, Y - (yc - R - 2), hs - 1, R + 2), mat)
        s.fill(pointed_arch_2d(du, Y - (yc - R - 2), hs - 1, R + 2) & (Y >= yc - R - 2) & (P == zface - normal * i), "air")
    pz = zface - normal * 3
    disc = rr <= R + 0.5
    s.fill(disc & (P == pz), GLASS)
    frame = (rr > R - 0.6) & (rr <= R + 0.6)
    spokes = (np.abs(((ang + 360) % 30) - 15) > 13.2) & (rr > 2.5) & (rr < R)
    inner = (rr > R * 0.48 - 0.5) & (rr <= R * 0.48 + 0.5)
    hub = rr <= 1.8
    s.fill((frame | spokes | inner | hub) & (P == pz), TRIM)
    s.fill((frame | hub) & (P == pz + normal), TRIM)


def zc_dummy(v):
    return v


def portal(s, xc, zface, y0, hs0, rings, normal=1, gable=True):
    """Nested recessed pointed portal: a porch block projecting `rings` in front of zface, carved in steps (-1 each),
    rings alternate trim / masonry; a crocketed gable (wimperg) above; steps and paired lanterns in front."""
    u = X + 0.5 - xc
    hs_out = hs0 + rings
    sp0 = int(hs0 * 2.4)
    front = zface + normal * rings
    zlo, zhi = sorted((zface - normal * 2, front))
    porch = pointed_arch_2d(u, Y - y0, hs_out + 1, sp0 + rings) & (Y >= y0) & (Z >= zlo) & (Z <= zhi)
    s.fill(porch, LIME)
    for i in range(rings, -1, -1):
        hs = hs0 + i
        a = pointed_arch_2d(u, Y - y0, hs, sp0 + i) & (Y > y0)
        ring = a & ~pointed_arch_2d(u, Y - y0, hs - 1, sp0 + i - 1)
        d = rings - i + 1       # carve depth from the front
        z_a, z_b = sorted((front, front - normal * (d - 1)))
        s.fill(ring & (Z >= zlo) & (Z <= zhi) & ~((Z >= z_a) & (Z <= z_b)), TRIM if i % 2 else RIB)
        s.fill(a & (Z >= z_a) & (Z <= z_b), "air")
    # door leaves deep inside, open passage through the wall
    s.fill(pointed_arch_2d(u, Y - y0, hs0 - 1, sp0 - 1) & (Y > y0) & (Z >= min(zlo, zface - normal * 4)) & (Z <= max(zlo, zface - normal * 4)), "air")
    if gable:
        top = y0 + sp0 + rings + int((hs_out + 1) * 1.7)
        g = (Y >= top - 2) & (Y - (top - 2) <= (hs_out + 2 - np.abs(u)) * 1.6) & (np.abs(u) <= hs_out + 2) & (Z == front)
        s.fill(g, TRIM)
        apex = int(top - 2 + (hs_out + 2) * 1.6)
        for k in range(0, int(hs_out) + 2, 2):         # crockets on both slopes
            yy = int(top - 2 + (hs_out + 2 - k) * 1.6)
            for sx in (-k, k):
                s.set(int(xc + sx), yy + 1, int(front), "calcite")
        s.fill(shapes.box((xc - 0.5, apex, front - 0.5), (xc + 0.5, apex + 3, front + 0.5)), "calcite")
    # steps + lanterns
    for k in range(4):
        zz = front + normal * (k + 1)
        s.fill(B(xc - hs_out - k, xc + hs_out + k, y0 - k, y0 - k, min(zz, zz), max(zz, zz)), "polished_andesite")
    for sx in (-hs_out - 1, hs_out + 1):
        s.set(int(xc + sx), y0 + 1, int(front + normal), "lantern")


# ------------------------------------------------------------------ the cathedral
def nave_and_choir(s):
    x0, x1 = NAVE
    for (l0, l1) in (NAVE_Z, CHOIR_Z):
        # aisles first (lower halls), then the nave on top of their inner walls
        hall(s, x0 - AISLE, x0, l0, l1, G, AISLE_EAVE, bay=7, pitch=0.9, ends=(True, True), lanterns=False)
        hall(s, x1, x1 + AISLE, l0, l1, G, AISLE_EAVE, bay=7, pitch=0.9, ends=(True, True), lanterns=False)
        hall(s, x0, x1, l0, l1, G, EAVE, bay=7, pil_from=AISLE_EAVE + 4, clerestory_from=AISLE_EAVE + 2,
             ends=(l0 != NAVE_Z[0], l1 != CHOIR_Z[1]))
        # arcade: open the nave walls to the aisles between the piers
        for k in range(l0 + 3, l1 - 2, 7):
            arc = pointed_arch_2d(Z - (k + 0.5), Y - G, 2.5, 9) & (Y > G)
            s.fill(arc & ((X == x0) | (X == x0 + 1) | (X == x1) | (X == x1 - 1)), "air")
        flyers(s, l0, l1)


def flyers(s, l0, l1):
    """Two-tier flying buttresses: free-standing piers outside the aisles, arched struts to the clerestory."""
    x0, x1 = NAVE
    for k in range(l0 + 7, l1 - 1, 7):
        for side in (-1, 1):
            xp = (x0 - AISLE - 6) if side < 0 else (x1 + AISLE + 6)
            xw = x0 - 1 if side < 0 else x1 + 1
            s.fill(B(xp - 1, xp + 1, G - 4, EAVE + 6, k - 1, k), LIME)
            s.fill(B(xp - 2 if side < 0 else xp - 1, xp + 1 if side < 0 else xp + 2, G - 4, G + 12, k - 1, k), LIME)
            s.fill(shapes.cylinder((xp + 0.5, 0, k + 0.5), 1.3, EAVE + 7, EAVE + 10), TRIM)
            s.fill(cone((xp + 0.5, 0, k + 0.5), 1.6, EAVE + 10, EAVE + 17, 0.2), COPPER)
            for (yp, yw) in ((EAVE - 2, EAVE - 6), (AISLE_EAVE + 10, AISLE_EAVE + 6)):
                path = bezier([(xp + 0.5, yp, k + 0.5), ((xp + xw) / 2 + 0.5, yp + 1, k + 0.5), (xw + 0.5, yw, k + 0.5)], 14)
                s.fill(union(tube(path, 0.9, 0.8)), TRIM if yp > EAVE - 5 else LIME)


def crossing(s):
    x0, x1, z0, z1 = CROSS
    top = 132
    s.fill(B(x0, x1, G - 4, top, z0, z1), LIME)
    s.fill(B(x0 + 3, x1 - 3, G + 1, top - 4, z0 + 3, z1 - 3), "air")
    s.fill(B(x0 + 3, x1 - 3, G, G, z0 + 3, z1 - 3), FLOOR)
    # great arches into the nave, choir and both transept arms
    w = pointed_arch_2d(X + 0.5 - (XC + 0.5), Y - G, 8.5, 18) & (Y > G)
    s.fill(w & ((Z <= z0 + 3) | (Z >= z1 - 3)) & (Z >= z0) & (Z <= z1), "air")
    w = pointed_arch_2d(Z + 0.5 - 107.5, Y - G, 7.5, 18) & (Y > G)
    s.fill(w & ((X <= x0 + 3) | (X >= x1 - 3)) & (X >= x0) & (X <= x1), "air")
    for yb in (G + 40, G + 62):
        for k in range(-2, 3):
            u = k * 5
            for (P, plane, n, U0) in ((Z, z0, -1, XC + 0.5), (Z, z1, 1, XC + 0.5), (X, x0, -1, 107.5), (X, x1, 1, 107.5)):
                Uc = X if P is Z else Z
                pan = pointed_arch_2d(Uc + 0.5 - (U0 + u), Y - yb, 1.5, 12) & (Y >= yb)
                frame = pointed_arch_2d(Uc + 0.5 - (U0 + u), Y - yb + 1, 2.5, 13) & (Y >= yb - 1) & ~pan
                s.fill(frame & (P == plane + n), TRIM)
                s.fill(pan & (P == plane), "air" if yb > G + 50 and abs(k) < 2 else RIB)
    # string courses every 16, protruding 1, trim
    for yy in range(G + 16, top, 16):
        s.fill(B(x0 - 1, x1 + 1, yy, yy, z0 - 1, z1 + 1) & ~B(x0, x1, yy, yy, z0, z1), TRIM)
    # belfry: tall twin lancets on each face above the roofs, outer recess + louvres (air)
    for c in (XC - 5, XC + 5):
        for zf, nrm in ((z0, -1), (z1, 1)):
            w = pointed_arch_2d(X + 0.5 - c, Y - 98, 2, 18) & (Y >= 98)
            s.fill(w & (Z == zf), "air"); s.fill(w & (Z == zf - nrm), "air")
    for c in (106 - 5 + 1, 106 + 5 + 1):
        for xf, nrm in ((x0, -1), (x1, 1)):
            w = pointed_arch_2d(Z + 0.5 - c, Y - 98, 2, 18) & (Y >= 98)
            s.fill(w & (X == xf), "air"); s.fill(w & (X == xf - nrm), "air")
    # corner turrets: buttress clusters rising 14 above the crown, octagonal caps
    for cx in (x0, x1):
        for cz in (z0, z1):
            s.fill(shapes.cylinder((cx + 0.5, 0, cz + 0.5), 3.0, G - 4, top + 10), LIME)
            s.fill(shapes.cylinder((cx + 0.5, 0, cz + 0.5), 3.8, top + 8, top + 11), TRIM)
            s.fill(star_prism((cx + 0.5, 0, cz + 0.5), top + 11, top + 26, 8, 3.6, 3.3, 0.4, 0.3), COPPER)
            for k in range(3):   # attached shafts
                a = math.radians(45 + 90 * k)
    # crown: merlon parapet
    s.fill((((X == x0) | (X == x1)) & (Z >= z0) & (Z <= z1) | ((Z == z0) | (Z == z1)) & (X >= x0) & (X <= x1))
           & (Y == top + 1) & (((X + Z) % 2) == 0), TRIM)
    # octagonal lantern + spire (the tallest point)
    c = (XC + 0.5, 0, 107.0)
    s.fill(star_prism(c, top, 152, 8, 11.5, 10.6, 11.5, 10.6), LIME)
    s.fill(star_prism(c, top + 1, 151, 8, 9.5, 8.8, 9.5, 8.8), "air")
    for k in range(8):   # lantern lancets on the 8 faces
        a = math.radians(22.5 + 45 * k)
        px, pz = c[0] + math.cos(a) * 10.6, c[2] + math.sin(a) * 10.6
        s.fill(shapes.capsule((px, top + 5, pz), (px, 146, pz), 1.6), "air")
        s.fill(shapes.capsule((px, 146, pz), (px, 149, pz), 0.9), "air")
        # buttress fins at the 8 corners rising into pinnacles
        b = math.radians(45 * k)
        qx, qz = c[0] + math.cos(b) * 12.2, c[2] + math.sin(b) * 12.2
        s.fill(shapes.cylinder((qx, 0, qz), 1.3, top, 156), TRIM)
        s.fill(cone((qx, 0, qz), 1.6, 156, 163, 0.2), COPPER)
    s.fill(star_prism(c, 151, 153, 8, 12.5, 11.6, 12.5, 11.6), TRIM)
    s.fill(star_prism(c, 153, 209, 8, 10.5, 9.7, 0.6, 0.5, power=0.9), COPPER)
    # crockets on the 8 arrises every 4
    cro = star_prism(c, 155, 204, 8, 11.6, 4.0, 1.4, 0.8, power=0.9)
    s.fill(cro.mask(s.shape) & (Y % 4 == 0), "weathered_cut_copper")
    s.fill(shapes.box((c[0] - 0.5, 209, c[2] - 0.5), (c[0] + 0.5, 215, c[2] + 0.5)), "gold_block")
    s.fill(shapes.box((c[0] - 2.5, 212, c[2] - 0.5), (c[0] + 2.5, 213, c[2] + 0.5)), "gold_block")


def transepts(s):
    x0, x1, z0, z1 = TRANSEPT
    for (a, b) in ((x0, CROSS[0]), (CROSS[1], x1)):
        hall(s, z0, z1, a, b, G, EAVE - 4, axis="x", bay=7, pil_from=G, ends=(a == x0, b == x1))
    # gable roses
    rose(s, 107.0, EAVE + 6, x0, 6, normal=-1, axis="x")
    rose(s, 107.0, EAVE + 6, x1, 6, normal=1, axis="x")
    # floor slab over the void + bridge legs: walls across the chasm with tall pointed arches down to the river
    s.fill(B(x0, x1, G - 3, G, z0 - 2, z1 + 2) & ~B(CROSS[0] + 3, CROSS[1] - 3, G, G, CROSS[2] + 3, CROSS[3] - 3), LIME)
    for xl in (x0 + 1, x0 + 12, CROSS[0] + 1, CROSS[1] - 3, x1 - 14, x1 - 3):
        leg = B(xl, xl + 2, 0, G - 1, 84, 128)
        cz = chasm_z(xl + 1)
        open_ = pointed_arch_2d(Z + 0.5 - cz, Y - (RIVER - 2), 8.5, 14)
        s.fill(leg & ~open_, LIME, replace="air")
        # a second, smaller arch higher up (two tiers of arches, Ronda-style)
        s.fill(leg & pointed_arch_2d(Z + 0.5 - cz, Y - (G - 13), 3, 4) & (Y >= G - 13), "air")


def front(s):
    z0, z1 = FRONT_Z
    x0, x1 = NAVE
    # central block between the towers: to the nave eave, gable to the ridge
    s.fill(B(x0, x1, G - 4, EAVE + 2, z0, z1), LIME)
    s.fill(B(x0 + 2, x1 - 2, G + 1, EAVE - 6, z0, z1 - 3), "air")
    half = (x1 - x0) / 2
    g = (Y > EAVE + 2) & (Y - EAVE - 2 <= (half + 1 - np.abs(X + 0.5 - XC - 0.5)) * 1.5) & (X >= x0) & (X <= x1) & (Z >= z1 - 2) & (Z <= z1)
    s.fill(g, LIME)
    # gallery of kings: a row of niches across the front at G+30, trim band above and below
    s.fill(B(x0 - 20, x1 + 20, G + 28, G + 28, z1 + 1, z1 + 1), TRIM)
    s.fill(B(x0 - 20, x1 + 20, G + 36, G + 36, z1 + 1, z1 + 1), TRIM)
    for k in range(x0 - 18, x1 + 19, 3):
        s.fill(B(k, k, G + 29, G + 35, z1 + 1, z1 + 1), TRIM)
    rose(s, XC + 0.5, G + 50, z1, 9.5, normal=1)
    # gable crockets + apex cross
    for k in range(0, 12, 2):
        yy = int(EAVE + 2 + (half + 1 - k) * 1.5)
        for sx in (-k, k):
            s.set(int(XC + sx), yy + 1, z1, "calcite")
    s.fill(B(XC, XC, EAVE + 20, EAVE + 26, z1, z1), "calcite")
    s.fill(B(XC - 2, XC + 2, EAVE + 24, EAVE + 24, z1, z1), "calcite")
    portal(s, XC + 0.5, z1, G, 3.5, 6)
    for (tx0, tx1) in TOWER_X:
        tower(s, tx0, tx1, z0 - 2, z1)
        portal(s, (tx0 + tx1) / 2 + 0.5, z1, G, 2.5, 4, gable=True)


def tower(s, x0, x1, z0, z1, top=124, tip=None):
    xc, zc = (x0 + x1) / 2 + 0.5, (z0 + z1) / 2 + 0.5
    s.fill(B(x0, x1, G - 4, top, z0, z1), LIME)
    s.fill(B(x0 + 2, x1 - 2, G + 1, top - 2, z0 + 2, z1 - 2), "air")
    # corner buttresses, stepped (+3 low, +2 mid, +1 high), all four corners, both faces
    for cx, sx in ((x0, -1), (x1, 1)):
        for cz, sz in ((z0, -1), (z1, 1)):
            for (y_a, y_b, p) in ((G - 4, G + 30, 3), (G + 30, G + 62, 2), (G + 62, top + 6, 1)):
                s.fill(B(min(cx, cx + sx * p), max(cx, cx + sx * p), y_a, y_b, min(cz, cz - sz * 2), max(cz, cz - sz * 2)), LIME)
                s.fill(B(min(cx, cx - sx * 2), max(cx, cx - sx * 2), y_a, y_b, min(cz, cz + sz * p), max(cz, cz + sz * p)), LIME)
            # corner pinnacle
            s.fill(shapes.cylinder((cx + 0.5 + sx, 0, cz + 0.5 + sz), 1.6, top + 6, top + 10), TRIM)
            s.fill(cone((cx + 0.5 + sx, 0, cz + 0.5 + sz), 2.0, top + 10, top + 20, 0.2), COPPER)
    # string courses
    for yy in (G + 28, G + 36, G + 62, top - 2):
        s.fill(B(x0 - 1, x1 + 1, yy, yy, z0 - 1, z1 + 1) & ~B(x0, x1, yy, yy, z0, z1), TRIM)
    # belfry lancets on all four faces (two tall, recessed)
    for c in (xc - 4, xc + 4):
        w = pointed_arch_2d(X + 0.5 - c, Y - (G + 66), 1.5, 20) & (Y >= G + 66)
        for zf, n in ((z0, 1), (z1, -1)):
            s.fill(w & (Z == zf), "air"); s.fill(w & (Z == zf + n), "air")
    for c in (zc - 4, zc + 4):
        w = pointed_arch_2d(Z + 0.5 - c, Y - (G + 66), 1.5, 20) & (Y >= G + 66)
        for xf, n in ((x0, 1), (x1, -1)):
            s.fill(w & (X == xf), "air"); s.fill(w & (X == xf + n), "air")
    # mid-level twin lancets on the front
    lancet_band(s, "x", z1, xc, G + 40, 2, 6, hs=1.5, spring=12, depth_sign=1)
    # parapet
    s.fill((((X == x0) | (X == x1)) & (Z >= z0) & (Z <= z1) | ((Z == z0) | (Z == z1)) & (X >= x0) & (X <= x1))
           & (Y == top + 1) & (((X + Z) % 2) == 0), TRIM)
    # flat crown: a pierced balustrade, mid-face pinnacles, a small copper belfry lantern off-centre
    for a in (0, 90, 180, 270):
        px, pz = xc + math.cos(math.radians(a)) * 9.5, zc + math.sin(math.radians(a)) * 9.5
        s.fill(shapes.box((px - 0.5, top + 1, pz - 0.5), (px + 0.5, top + 5, pz + 0.5)), TRIM)
    s.fill(B(x0 + 2, x1 - 2, top, top, z0 + 2, z1 - 2), "polished_andesite")


def apse(s):
    """Albi-style fortified apse: half-round, with round tower-buttresses, machicolations and a merlon crown."""
    cx, cz = APSE_C
    R = (NAVE[1] - NAVE[0]) / 2 + AISLE
    north = Z <= cz
    s.fill(shapes.cylinder((cx + 0.5, 0, cz + 0.5), R, G - 4, EAVE).mask(s.shape) & north, LIME)
    s.fill(shapes.cylinder((cx + 0.5, 0, cz + 0.5), R - 3, G + 1, EAVE - 6).mask(s.shape) & north, "air")
    # half cone roof
    s.fill(cone((cx + 0.5, 0, cz + 0.5), R - 2, EAVE, EAVE + int(R * 1.2), 0.5).mask(s.shape) & north, ROOF)
    for k, a in enumerate(range(195, 350, 22)):
        rad = math.radians(a)
        px, pz = cx + 0.5 + math.cos(rad) * (R + 1), cz + 0.5 + math.sin(rad) * (R + 1)
        ht = EAVE + 10
        s.fill(shapes.cylinder((px, 0, pz), 3.2, G - 4, ht), LIME)
        s.fill(shapes.cylinder((px, 0, pz), 4.2, ht - 3, ht), TRIM)          # machicolation course
        ring = shapes.cylinder((px, 0, pz), 4.2, ht + 1, ht + 2).mask(s.shape)
        s.fill(ring & ~shapes.cylinder((px, 0, pz), 3.0, ht, ht + 3).mask(s.shape) & (((X + Z) % 2) == 0), TRIM)
        # windows between the drums: tall lancets
        b = math.radians(a + 11)
        wx, wz = cx + 0.5 + math.cos(b) * R, cz + 0.5 + math.sin(b) * R
        s.fill(shapes.capsule((wx, G + 10, wz), (wx, EAVE - 10, wz), 1.4), "air")
        s.fill(shapes.capsule((wx - math.cos(b) * 2, G + 10, wz - math.sin(b) * 2), (wx - math.cos(b) * 2, EAVE - 10, wz - math.sin(b) * 2), 1.4), GLASS)


def donjon(s):
    """The bishop's keep: square, sheer, machicolated, corner bartizans, a slim watch turret."""
    x0, x1, z0, z1 = 40, 60, 134, 154
    top = G + 66
    s.fill(B(x0, x1, G - 6, top, z0, z1), LIME)
    s.fill(B(x0 + 3, x1 - 3, G + 1, top - 3, z0 + 3, z1 - 3), "air")
    for yy in range(G + 14, top - 6, 14):
        s.fill(B(x0, x1, yy, yy, z0 + 3, z1 - 3) & ~B(x0 + 1, x1 - 1, yy, yy, z0 + 1, z1 - 1), LIME)
        s.fill(B(x0 + 3, x1 - 3, yy, yy, z0 + 3, z1 - 3), "spruce_planks")
    # pilasters every 5 on all faces, +1
    for k in range(x0 + 5, x1 - 1, 5):
        for zf, d in ((z0, -1), (z1, 1)):
            s.fill(B(k, k, G - 6, top - 4, zf + d, zf + d), LIME)
    for k in range(z0 + 5, z1 - 1, 5):
        for xf, d in ((x0, -1), (x1, 1)):
            s.fill(B(xf + d, xf + d, G - 6, top - 4, k, k), LIME)
    # slit windows
    for yy in range(G + 6, top - 8, 7):
        for k in range(x0 + 3, x1 - 2, 5):
            s.fill(B(k, k, yy, yy + 3, z1, z1), "air"); s.fill(B(k, k, yy, yy + 3, z0, z0), "air")
    # machicolated crown (+1 corbel band, merlons)
    s.fill(B(x0 - 2, x1 + 2, top - 3, top, z0 - 2, z1 + 2) & ~B(x0 - 1, x1 + 1, top - 3, top, z0 - 1, z1 + 1).__invert__().__invert__(), TRIM)
    s.fill(B(x0 - 1, x1 + 1, top - 3, top, z0 - 1, z1 + 1), LIME)
    s.fill(B(x0 - 2, x1 + 2, top + 1, top + 1, z0 - 2, z1 + 2) & ~B(x0 - 1, x1 + 1, top + 1, top + 1, z0 - 1, z1 + 1) & (((X + Z) % 2) == 0), TRIM)
    for cx in (x0 - 1, x1 + 1):
        for cz in (z0 - 1, z1 + 1):
            s.fill(shapes.cylinder((cx + 0.5, 0, cz + 0.5), 2.6, top - 10, top + 6), LIME)
            s.fill(cone((cx + 0.5, 0, cz + 0.5), 0.6, top - 16, top - 10, 2.6), LIME)
            s.fill(cone((cx + 0.5, 0, cz + 0.5), 3.4, top + 6, top + 15, 0.2), ROOF)
    s.fill(shapes.cylinder((x0 + 6.5, 0, z0 + 6.5), 2.8, top, top + 18), LIME)
    s.fill(cone((x0 + 6.5, 0, z0 + 6.5), 3.6, top + 18, top + 30, 0.2), ROOF)


def cloister(s):
    x0, x1, z0, z1 = 136, 166, 126, 156
    y0, eave = G, G + 9
    s.fill(B(x0, x1, G - 3, G, z0, z1), PAVING)
    outer = B(x0, x1, y0, eave, z0, z1) & ~B(x0 + 1, x1 - 1, y0, eave, z0 + 1, z1 - 1)
    s.fill(outer, LIME)
    inner = B(x0 + 6, x1 - 6, y0, eave, z0 + 6, z1 - 6) & ~B(x0 + 7, x1 - 7, y0, eave, z0 + 7, z1 - 7)
    s.fill(inner, LIME)
    # arcade openings every 4 in the inner wall
    for k in range(x0 + 8, x1 - 6, 4):
        a = pointed_arch_2d(X + 0.5 - (k + 0.5), Y - y0, 1.5, 4) & (Y > y0)
        s.fill(a & ((Z == z0 + 6) | (Z == z1 - 6)), "air")
    for k in range(z0 + 8, z1 - 6, 4):
        a = pointed_arch_2d(Z + 0.5 - (k + 0.5), Y - y0, 1.5, 4) & (Y > y0)
        s.fill(a & ((X == x0 + 6) | (X == x1 - 6)), "air")
    # lean-to roof over the galleries
    gal = B(x0, x1, eave + 1, eave + 4, z0, z1) & ~B(x0 + 6, x1 - 6, eave + 1, eave + 4, z0 + 6, z1 - 6)
    dist = np.minimum(np.minimum(X - x0, x1 - X), np.minimum(Z - z0, z1 - Z))
    s.fill(gal & (Y - eave <= 4 - np.abs(dist - 3)), ROOF)
    # garth + fountain
    s.fill(B(x0 + 7, x1 - 7, G, G, z0 + 7, z1 - 7), TURF)
    xc, zc = (x0 + x1) / 2 + 0.5, (z0 + z1) / 2 + 0.5
    s.fill(shapes.cylinder((xc, 0, zc), 3.5, G + 1, G + 2), "calcite")
    s.fill(shapes.cylinder((xc, 0, zc), 2.5, G + 2, G + 3), "water")
    s.fill(shapes.cylinder((xc, 0, zc), 0.8, G + 2, G + 6), "calcite")


def chapter_house(s):
    c = (146.5, 0, 66.5)
    s.fill(star_prism(c, G - 4, G + 20, 8, 10.5, 9.7, 10.5, 9.7), LIME)
    s.fill(star_prism(c, G + 1, G + 18, 8, 8.5, 7.8, 8.5, 7.8), "air")
    s.fill(star_prism(c, G + 20, G + 38, 8, 11, 10.2, 0.6, 0.5), ROOF)
    for k in range(8):
        a = math.radians(45 * k)
        px, pz = c[0] + math.cos(a) * 11.5, c[2] + math.sin(a) * 11.5
        s.fill(shapes.box((px - 1, G - 4, pz - 1), (px + 1, G + 22, pz + 1)), LIME)
        s.fill(cone((px, 0, pz), 1.4, G + 22, G + 27, 0.2), COPPER)
    s.fill(B(122, 136, G - 3, G + 12, 62, 70), LIME)            # passage to the choir


# ------------------------------------------------------------------ curtain wall
WALL_PTS = [(36, 190), (88, 196), (120, 196), (172, 190), (180, 140), (182, 74), (162, 26), (104, 18), (46, 26), (26, 74),
            (28, 140)]


def curtain(s, h):
    pts = WALL_PTS
    gx, gz = cols2d(s.shape)
    dmin = np.full(gx.shape, 1e9)
    for i in range(len(pts)):
        (ax, az), (bx, bz) = pts[i], pts[(i + 1) % len(pts)]
        vx, vz = bx - ax, bz - az
        t = np.clip(((gx - ax) * vx + (gz - az) * vz) / (vx * vx + vz * vz), 0, 1)
        d = np.hypot(gx - ax - t * vx, gz - az - t * vz)
        dmin = np.minimum(dmin, d)
    top = G + 15
    near = dmin < 1.6
    wall = near[:, None, :] & (Y <= top) & (Y >= 0)
    deep = (h < G - 10)[:, None, :]
    pier = ((Z % 13) < 3)
    s.fill(wall & (Y > h[:, None, :] - 6) & ~deep, LIME)
    s.fill(wall & deep & (pier & (Y <= G - 2) | (Y >= G - 8) & (Y <= G - 2)), LIME)
    s.fill(near[:, None, :] & deep & (Y == G - 1) & (((X + Z) % 2) == 0), TRIM)
    # arch soffits between the piers over the chasm
    s.fill(wall & deep & ~pier & (Y >= G - 12) & (Y < G - 8) & ((Z % 13 == 3) | (Z % 13 == 12) | (Y >= G - 10) & ((Z % 13 == 4) | (Z % 13 == 11))), LIME)
    # merlons on the outer half (every other block) + a walkway
    s.fill(near[:, None, :] & ~(h < G - 10)[:, None, :] & (Y == top + 1) & (((X + Z) % 2) == 0), TRIM)
    # where the wall crosses the chasm: two tiers of arches (water gates)
    # round towers at the vertices, conical slate roofs
    for k, (px, pz) in enumerate(pts):
        if (px, pz) in ((88, 196), (120, 196)):
            continue
        r = 5.5
        base = int(h[int(np.clip(px, 0, W - 1)), int(np.clip(pz, 0, D - 1))]) - 8
        s.fill(shapes.cylinder((px + 0.5, 0, pz + 0.5), r, max(0, base), G + 24), LIME)
        s.fill(shapes.cylinder((px + 0.5, 0, pz + 0.5), r + 1, G + 22, G + 25), TRIM)
        s.fill(cone((px + 0.5, 0, pz + 0.5), r + 1.6, G + 25, G + 25 + int(r * 2.6), 0.2), ROOF)
        for a in (0, 90, 180, 270):
            sx, sz = px + 0.5 + math.cos(math.radians(a + 45 * k)) * r, pz + 0.5 + math.sin(math.radians(a + 45 * k)) * r
            s.fill(B(sx, sx, G + 8, G + 11, sz, sz), "air")


def barbican(s):
    """South gate: twin round towers, a deep pointed passage, a drawbridge pit; the road climbs to it."""
    x0, x1 = 88, 120
    zf = 196
    s.fill(B(x0 + 6, x1 - 6, G - 6, G + 22, zf - 6, zf + 4), LIME)
    for px in (x0 + 4.5, x1 - 3.5):
        s.fill(shapes.cylinder((px, 0, zf + 2.5), 7, G - 10, G + 30), LIME)
        s.fill(shapes.cylinder((px, 0, zf + 2.5), 8, G + 27, G + 31), TRIM)
        s.fill(cone((px, 0, zf + 2.5), 8.6, G + 31, G + 52, 0.2), ROOF)
        s.fill(shapes.box((px - 0.5, G + 52, zf + 2), (px + 0.5, G + 56, zf + 3)), "gold_block")
    u = X + 0.5 - (XC + 0.5)
    for i in range(3, -1, -1):
        a = pointed_arch_2d(u, Y - G, 3 + i, 8 + i) & (Y > G)
        s.fill(a & ~pointed_arch_2d(u, Y - G, 2 + i, 7 + i) & (Z == zf + 4 + 0), TRIM if i % 2 else LIME)
        s.fill(a & (Z >= zf + 4 - i) & (Z <= zf + 4) & (i > 0), "air")
    s.fill(pointed_arch_2d(u, Y - G, 3, 8) & (Y > G) & (Z >= zf - 8) & (Z <= zf + 6), "air")
    s.fill(pointed_arch_2d(u, Y - G, 3, 8) & (Y == G) & (Z >= zf - 8) & (Z <= zf + 6), PAVING)
    # the road: a ramp down to the south edge
    for zz in range(zf + 5, D):
        yy = G - (zz - zf - 5) // 3
        s.fill(B(XC - 3, XC + 4, yy - 4, yy, zz, zz), PAVING)
        s.fill(B(XC - 3, XC + 4, yy + 1, G + 6, zz, zz), "air")
        for xx in (XC - 4, XC + 5):
            s.fill(B(xx, xx, yy - 4, yy + 1, zz, zz), LIME)


def parvis(s):
    # paved square from the front to the barbican, medallions every 7, two lantern rows
    s.fill(B(66, 142, G - 3, G, 176, 192), PAVING)
    s.fill(B(66, 142, G + 1, G + 20, 177, 192) , "air")
    for xx in range(70, 140, 7):
        for zz in (180, 187):
            s.fill(B(xx - 1, xx + 1, G, G, zz - 1, zz + 1), "polished_diorite")
            s.set(xx, G, zz, "chiseled_stone_bricks")
    for xx in (80, 90, 118, 128):
        s.fill(B(xx, xx, G + 1, G + 3, 190, 190), "andesite_wall")
        s.set(xx, G + 4, 190, "lantern")


def foundations(s, h):
    """Everything the cathedral stands on goes down to rock: battered footings into the chasm walls."""
    x0, x1 = NAVE
    for (a, b, c0, c1) in ((x0 - AISLE - 1, x1 + AISLE + 1, NAVE_Z[0] - 1, FRONT_Z[1]),
                           (x0 - AISLE - 1, x1 + AISLE + 1, CHOIR_Z[0] - 12, CHOIR_Z[1] + 1)):
        cols = np.zeros((W, D), bool); cols[a:b + 1, c0:c1 + 1] = True
        s.fill(cols[:, None, :] & (Y <= G - 4) & (Y > h[:, None, :] - 2), Gradient("y", [(RIVER + 8, Mix({"mossy_stone_bricks": 1, "stone_bricks": 2})), (999, LIME)], jitter=3, jitter_scale=5, seed=SEED + 7), replace="air")
        s.fill(cols[:, None, :] & (Y <= G - 4) & (Y > h[:, None, :] - 2), "water", replace=None) if False else None


def build():
    s = Scene((W, H, D), "concept_gothic", seed=SEED)
    h = terrain(s)
    foundations(s, h)
    curtain(s, h)
    parvis(s)
    transepts(s)
    nave_and_choir(s)
    apse(s)
    crossing(s)
    front(s)
    donjon(s)
    cloister(s)
    chapter_house(s)
    barbican(s)
    s.mark("spawn_approach", (XC, ground_y(s, XC, 236), 236), look_at=(XC, 120, 120))
    s.markers["spawn_approach"]["fov"] = 80
    s.mark("cam_portal", (XC, G + 1, 193), look_at=(XC, G + 16, 176))
    s.markers["cam_portal"]["fov"] = 75
    s.mark("cam_nave", (XC, G + 1, 156), look_at=(XC, 70, 60))
    zc = int(chasm_z(46)) + 9
    s.mark("cam_chasm", (46, ground_y(s, 46, zc), zc), look_at=(XC, 56, 104))
    s.mark("cam_rampart", (178, G + 16, 153), look_at=(XC, 110, 106))
    s.mark("cam_cloister", (157, G + 1, 147), look_at=(XC, 150, 106))
    zc = int(chasm_z(160)) + 12
    s.mark("cam_gorge", (160, ground_y(s, 160, zc), zc), look_at=(XC, 64, 104))
    s.markers["cam_gorge"]["fov"] = 80
    s.mark("cam_hero_chasm", (206, 76, int(chasm_z(206)) + 4), look_at=(XC, 40, 106))
    s.markers["cam_hero_chasm"]["fov"] = 60
    s.mark("cam_hero", (206, 140, 236), look_at=(XC, 100, 106))
    s.markers["cam_hero"]["fov"] = 55
    s.meta["mood"] = "golden"
    s.meta["origin"] = [-104, 20, -108]
    return s
