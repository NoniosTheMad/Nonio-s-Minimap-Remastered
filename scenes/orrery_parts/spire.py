"""The Spire: a battered, tapering tower whose fresh-copper ribs coil up to an open lantern holding the Focus.

Floors (feet levels): Orrery Hall 109-124 (oculus over the Root Shaft) -> stair turret (NNE) -> Gallery Room 151 with
the outer gallery deck (r18) -> Gear Room 158 (the axles end here) -> Lens Room 179 with the upper deck (r12) ->
Lantern 193 (open cage, the Focus floats at ~205) -> crown needle to SPIRE_TOP."""
import math

import numpy as np

from tools.voxel import shapes
from tools.voxel.palette import Gradient, Mix

from .common import (C, FLOOR, GLASS_V, GLASS_V_PANE, HUB_Y, SEED, SPIRE_BODY, SPIRE_TOP, TRIM, Box, at_polar,
                     box_around, cu, helix_path, ramp, skin, slab_states)

Y0 = FLOOR - 4
HALL = (FLOOR + 1, FLOOR + 20)          # feet .. last air row (20 tall)
ARCHIVE = (FLOOR + 23, 148)             # the Star Archive: air rows between the hall ceiling and the gallery floor
GALLERY_Y = 150                         # gallery deck top cell (feet 151)
GEAR_Y = 162                            # gear room floor top cell (feet 163): a copper grate over the shaft deck
SHAFT_DECK = (159, 161)                 # between the gallery-room ceiling (158) and the gear floor: the axles + drum
LENS_Y = 178                            # upper deck top cell (feet 179)
LANTERN_Y = 192                         # lantern floor top cell (feet 193)
TURRET = (300.0, 15.5, 4.6)             # angle, centre radius, radius
WALL_T = 2.0


def radius(y):
    y = np.asarray(y, float)
    return np.where(y < 128, 14 - 1.5 * (y - Y0) / (128 - Y0), 12.5 - 6.5 * (y - 128) / 64)


def body(s):
    c = (C[0], 0, C[1])
    s.fill(shapes.cylinder(c, 14, Y0, 128, 12.5), SPIRE_BODY)
    s.fill(shapes.cylinder(c, 12.5, 128, LANTERN_Y + 0.5, 6), SPIRE_BODY)
    # hollow interior: walls WALL_T thick
    b = box_around(s, C, 14, Y0, LANTERN_Y)
    rr = np.hypot(b.x - C[0], b.z - C[1])
    inner = rr <= radius(b.y) - WALL_T
    b.fill(inner & (b.y > FLOOR + 0.5) & (b.y < LANTERN_Y - 0.5), "air")
    # floors / ceilings
    floor_mat = Mix({"polished_deepslate": 2, "deepslate_tiles": 1})
    for yf in (HALL[1] + 1, HALL[1] + 2, GALLERY_Y - 1, GALLERY_Y, SHAFT_DECK[0] - 1, LENS_Y - 1, LENS_Y, LANTERN_Y - 1, LANTERN_Y):
        b.fill(inner & (b.y > yf - 0.5) & (b.y < yf + 0.5), floor_mat)
    b.fill(inner & (b.y > GEAR_Y - 0.5) & (b.y < GEAR_Y + 0.5), cu("", "grate"))
    # the Orrery Hall floor: inlaid star map, oculus over the Root Shaft
    from .island import SHAFT_R
    hf = inner & (b.y > FLOOR - 0.5) & (b.y < FLOOR + 0.5)
    b.fill(hf, Mix({"polished_deepslate": 3, "deepslate_tiles": 1}))
    th = np.degrees(np.arctan2(b.z - C[1], b.x - C[0]))
    b.fill(hf & (np.abs(((th + 360) % 30) - 15) > 14.2) & (rr > SHAFT_R + 1), "calcite")
    b.fill(hf & (rr > SHAFT_R + 0.5) & (rr <= SHAFT_R + 1.5), cu("", "cut"))
    b.fill((rr <= SHAFT_R) & (b.y > FLOOR - 2.5) & (b.y < FLOOR + 0.5), "air")
    return b


def hall_openings(s):
    """South door (3x5 pointed) from the court; tall lancets every 30 deg; the turret door (NNE)."""
    from scenes.concepts._kit import pointed_arch_2d
    b = box_around(s, C, 15, FLOOR, HALL[1] + 2)
    rr = np.hypot(b.x - C[0], b.z - C[1])
    th = np.degrees(np.arctan2(b.z - C[1], b.x - C[0]))
    wall = (rr > radius(b.y) - WALL_T - 0.5) & (rr <= radius(b.y) + 1.5)
    # door: axis south
    u = b.x - C[0]
    door = pointed_arch_2d(u, b.y - FLOOR - 0.5, 1.5, 3.5) & (b.z > C[1]) & wall & (b.y > FLOOR + 0.5)
    b.fill(door, "air")
    # lancets
    for a in range(0, 360, 30):
        if a in (90,):
            continue
        da = ((th - a + 180) % 360) - 180
        uu = np.radians(da) * rr
        lan = pointed_arch_2d(uu, b.y - FLOOR - 4, 0.6, 7) & (b.y > FLOOR + 3.5) & wall & (np.abs(da) < 20)
        b.fill(lan & (rr > radius(b.y) - WALL_T + 0.5), GLASS_V)


def galleries(s):
    c = (C[0], 0, C[1])
    for yc, R in ((GALLERY_Y, 21.5), (LENS_Y, 12.5)):     # the gallery deck wraps right round the stair turret
        s.fill(shapes.cylinder(c, R, yc - 1.5, yc + 0.5), Mix({"polished_tuff": 2, "calcite": 1}))
        s.fill(shapes.cylinder(c, R - 0.5, yc - 8, yc - 1.5, radius(yc - 8) + 0.5), SPIRE_BODY)
        # parapet: calcite posts + copper bars
        # (2 high: nobody hops over it onto the rings, which pass 2-4 blocks beyond)
        b = box_around(s, C, R + 1, yc + 1, yc + 3)
        rr = np.hypot(b.x - C[0], b.z - C[1])
        th = np.degrees(np.arctan2(b.z - C[1], b.x - C[0]))
        ring = (rr > R - 1) & (rr <= R)
        post = np.abs(((np.radians(th) * R) % 4) - 2) > 1.5
        b.fill(ring & post, TRIM)
        b.fill(ring & ~post & (b.y < yc + 2.5), cu("weathered", "bars"))
        b.fill(ring & ~post & (b.y > yc + 2.5), "air")
        # lit bulbs on the posts every ~8 blocks
        lamp = np.abs(((np.radians(th) * R) % 8) - 4) > 3.5
        b.fill(ring & post & lamp & (b.y > yc + 2.5), cu("", "bulb", lit="true", powered="false"))
    # doors from the rooms onto the decks (4 each)
    for yc in (GALLERY_Y, LENS_Y):
        b = box_around(s, C, 14, yc + 1, yc + 3)
        rr = np.hypot(b.x - C[0], b.z - C[1])
        th = np.degrees(np.arctan2(b.z - C[1], b.x - C[0]))
        for a in (0, 90, 180, 270):      # axis-aligned: an oblique 2-wide door is a diagonal gap nobody can pass
            da = ((th - a + 180) % 360) - 180
            b.fill((np.abs(np.radians(da) * rr) < 1.1) & (rr > radius(b.y) - WALL_T - 0.6) & (rr < radius(b.y) + 0.6), "air")


def windows_upper(s):
    """Lancets on the gallery, gear and lens rooms."""
    from scenes.concepts._kit import pointed_arch_2d
    for y0, h, n in ((GALLERY_Y + 1, 5, 8), (GEAR_Y + 1, 9, 6), (LENS_Y + 1, 9, 6)):
        b = box_around(s, C, 14, y0, y0 + h)
        rr = np.hypot(b.x - C[0], b.z - C[1])
        th = np.degrees(np.arctan2(b.z - C[1], b.x - C[0]))
        wall = (rr > radius(b.y) - WALL_T - 0.5) & (rr <= radius(b.y) + 0.6)
        for k in range(n):
            a = k * 360 / n + 22.5
            if y0 in (GALLERY_Y + 1, LENS_Y + 1) and any(abs(((a - d + 180) % 360) - 180) < 15 for d in (0, 90, 180, 270)):
                continue
            da = ((th - a + 180) % 360) - 180
            uu = np.radians(da) * rr
            lan = pointed_arch_2d(uu, b.y - y0 - 1, 0.6, h - 4) & (b.y > y0 + 0.5) & wall & (np.abs(da) < 25)
            b.fill(lan, GLASS_V_PANE)


def turret(s):
    """Stair turret (NNE) from the Orrery Hall up to the gallery deck: helix ramp around a newel."""
    a, rc, R = TURRET
    x, z = at_polar(a, rc)
    c = (x, 0, z)
    s.fill(shapes.cylinder(c, R, Y0, GALLERY_Y + 6), SPIRE_BODY)
    s.fill(shapes.cylinder(c, R + 1.2, GALLERY_Y + 6, GALLERY_Y + 8, R + 0.4), TRIM)
    s.fill(shapes.cylinder(c, R + 0.8, GALLERY_Y + 8, GALLERY_Y + 22, 0.2), Gradient("y", [(GALLERY_Y + 12, cu("weathered", "cut")), (GALLERY_Y + 16, cu("oxidized", "cut")), (999, cu("exposed", "cut"))]))
    s.set(int(math.floor(x)), GALLERY_Y + 22, int(math.floor(z)), cu("", "rod"))
    s.fill(shapes.cylinder(c, R - 1.0, FLOOR + 1, GALLERY_Y + 5.5), "air")
    s.fill(shapes.cylinder(c, 0.9, FLOOR, GALLERY_Y + 5), Mix({"polished_deepslate": 1, "deepslate_tiles": 1}))
    # the door from the Orrery Hall, cut after the turret body (which overlaps the spire wall); wide enough to pass at
    # an oblique angle (a 2-wide oblique cut is a diagonal gap)
    hb = box_around(s, C, 15, FLOOR + 1, FLOOR + 3)
    rr = np.hypot(hb.x - C[0], hb.z - C[1])
    da = ((np.degrees(np.arctan2(hb.z - C[1], hb.x - C[0])) - a + 180) % 360) - 180
    hb.fill((rr > float(radius(FLOOR + 1)) - WALL_T - 0.8) & (rr < rc - 1.6) & (np.abs(np.radians(da) * rr) < 1.7), "air")
    full, slab = slab_states("polished_deepslate")
    # start facing the spire door (angle from turret centre to the spire centre)
    a_in = math.degrees(math.atan2(C[1] - z, C[0] - x))
    path = helix_path((x, z), 2.35, a_in, FLOOR + 1, GALLERY_Y + 1, rise_per_block=0.5, direction=1, step=0.5)
    cells = ramp(s, path, 2.6, full, slab, thick=1, carve=3, chunk=14)
    # a door into the Star Archive (the tall room between the hall ceiling and the gallery floor)
    best = None
    for (cx_, top, cz_, dd, _) in cells:
        if ARCHIVE[0] - 0.6 <= top + 1 <= ARCHIVE[0] + 0.6:
            d = math.hypot(cx_ + 0.5 - C[0], cz_ + 0.5 - C[1])
            if best is None or d < best[0]:
                best = (d, cx_, top + 1, cz_)
    if best:
        _, bx, by, bz = best
        ux, uz = C[0] - (bx + 0.5), C[1] - (bz + 0.5)
        n = math.hypot(ux, uz)
        ux, uz = ux / n, uz / n
        for t in np.arange(0, 5.0, 0.4):
            for dy in (0, 1, 2):
                for side in (-0.5, 0.5):
                    s.set(int(math.floor(bx + 0.5 + ux * t - uz * side)), by + dy, int(math.floor(bz + 0.5 + uz * t + ux * side)), "air")
        # a landing inside the archive door
    # a landing at the top of the ramp (half disc ahead of the ramp end: the ramp below it is >= 3.5 blocks lower)
    xe, ze, _ = path[-1]
    a_end = math.degrees(math.atan2(ze - z, xe - x))
    lb = Box(s, (x - R, GALLERY_Y, z - R), (x + R + 1, GALLERY_Y + 1, z + R + 1))
    rt = np.hypot(lb.x - x, lb.z - z)
    rel = (np.degrees(np.arctan2(lb.z - z, lb.x - x)) - a_end + 400) % 360 - 40
    lb.fill((rt <= R - 1.0) & (rt > 0.9) & (rel <= 185) & (rel >= -30), Mix({"polished_deepslate": 2, "deepslate_tiles": 1}), replace="air")
    # turret exit onto the gallery deck
    ae = math.radians(a + 90)          # tangential (clockwise), onto the deck beside the turret
    for t in np.arange(R - 1.5, R + 1.0, 0.4):
        for side in (-0.9, 0.0, 0.9):
            px = x + math.cos(ae) * t - math.sin(ae) * side
            pz = z + math.sin(ae) * t + math.cos(ae) * side
            for dy in (1, 2, 3):
                s.set(int(math.floor(px)), GALLERY_Y + dy, int(math.floor(pz)), "air")
    # slit windows
    for k in range(6):
        ang = math.radians(k * 60)
        for yy in range(FLOOR + 6, GALLERY_Y, 9):
            wx, wz = x + math.cos(ang) * (R - 0.5), z + math.sin(ang) * (R - 0.5)
            for dy in range(2):
                if np.hypot(wx - C[0], wz - C[1]) > radius(yy) + 0.5:
                    s.set(int(math.floor(wx)), yy + dy, int(math.floor(wz)), GLASS_V_PANE)
    return dict(c=(x, z), r=R, top=GALLERY_Y + 1)


def inner_stairs(s):
    """Helix ramps against the inner wall: gallery room -> gear room -> lens room -> lantern."""
    full, slab = slab_states("polished_tuff")
    # leg 1 starts at 310 deg so the stretch where it climbs through the shaft deck (feet 157.5-161) lies between the
    # axles (no axle between 62 and 148 deg); legs 2-3 start where the previous one ends
    legs = [(GALLERY_Y + 1, GEAR_Y + 1, 310.0), (GEAR_Y + 1, LENS_Y + 1, 190.0), (LENS_Y + 1, LANTERN_Y + 1, 320.0)]
    out = []
    for y0, y1, a0 in legs:
        ri = float(radius(y1)) - WALL_T - 1.4
        path = helix_path(C, ri, a0, y0, y1, rise_per_block=0.5, direction=1, step=0.5)
        # cut the stair hole through the floor above (ramp carve does it) and build the ramp
        ramp(s, path, 2.4, full, slab, thick=1, carve=3, chunk=int(max(10, ri * 2 * math.pi * 2 * 0.7)))
        out.append(path)
    return out


def ribs(s):
    """Four fresh-copper helical ribs (one turn), ribbed: cut copper with chiseled bands every 4 blocks."""
    from scenes.concepts._kit import helix_rib
    c = (C[0], 0, C[1])
    mat = lambda ctx: np.where(((ctx.ys // 2) % 3) == 0, cu("", "chiseled"), cu("", "cut")).astype(str)
    for k in range(4):
        s.fill(helix_rib(c, Y0, LANTERN_Y + 2, 15.6, 8.2, 0.75, k * 90 + 45, 1.5, flat=1.6), mat)
        s.fill(helix_rib(c, LANTERN_Y + 2, 224, 8.2, 1.6, 0.35, k * 90 + 45 + 270, 1.3, flat=1.4), mat)


def lantern(s):
    c = (C[0], 0, C[1])
    s.fill(shapes.cylinder(c, 8.0, LANTERN_Y - 1.5, LANTERN_Y + 0.5), Mix({"calcite": 2, cu("exposed", "cut"): 1}))
    # cage posts with lit bulbs
    for k in range(8):
        ang = math.radians(k * 45 + 22.5)
        px, pz = C[0] + math.cos(ang) * 7.0, C[1] + math.sin(ang) * 7.0
        s.fill(shapes.box((px - 0.5, LANTERN_Y + 1, pz - 0.5), (px + 0.5, LANTERN_Y + 16, pz + 0.5)), cu("", "cut"))
        s.set(int(math.floor(px)), LANTERN_Y + 1, int(math.floor(pz)), cu("", "bulb", lit="true", powered="false"))
    # rail between the posts
    b = box_around(s, C, 8, LANTERN_Y + 1, LANTERN_Y + 1)
    rr = np.hypot(b.x - C[0], b.z - C[1])
    b.fill((rr > 6.4) & (rr <= 7.4), cu("weathered", "bars"))
    # the Focus: a floating amethyst octahedron
    focus = shapes.SDF(lambda X, Y, Z: np.abs(X - C[0]) + np.abs(Y - 206) * 0.7 + np.abs(Z - C[1]) - 5.5,
                       ((C[0] - 7, 196, C[1] - 7), (C[0] + 7, 216, C[1] + 7)))
    s.fill(focus, "amethyst_block")
    s.fill(shapes.sphere((C[0], 206, C[1]), 1.5), "glowstone")
    # crown needle
    s.fill(shapes.cylinder(c, 1.4, 222, SPIRE_TOP - 4, 0.6), cu("", "cut"))
    for yy in range(SPIRE_TOP - 4, SPIRE_TOP + 1):
        s.set(int(C[0]), yy, int(C[1]), cu("", "rod"))


def build(s, ctx):
    body(s)
    ribs(s)
    skin(s, (C[0] - 17, FLOOR + 2, C[1] - 17), (C[0] + 18, LANTERN_Y - 1, C[1] + 18),       # shingle the taper + rib tops
         mask=lambda x, y, z: np.hypot(x - C[0], z - C[1]) > radius(y) - 0.8)
    hall_openings(s)
    galleries(s)
    windows_upper(s)
    ctx["turret"] = turret(s)
    lantern(s)                                   # before the stairs: the last leg cuts its hole through the lantern floor
    ctx["inner_stairs"] = inner_stairs(s)
