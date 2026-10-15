"""The castle on the summit: court, ring wall with wall-walk, needle towers (each crown different), the three wings
(west Library, east Chart Room with its instrument terrace, north Service house) and the Gatehouse (densest element).

Floor convention: FLOOR is the top solid block of the deck; feet at FLOOR + 1. Interiors are carved here and
registered as zones in rooms.py (empty: walls, floor, ceiling, openings, windows; no furniture)."""
import math

import numpy as np

from tools.voxel import shapes
from tools.voxel.palette import Gradient, Mix, Noise

from scenes.concepts._kit import pointed_arch_2d

from .common import (C, FLOOR, GLASS_V_PANE, MASONRY, PAVING, SEED, TRIM, Box, at_polar, box_around, cu, ramp,
                     skin, slab_states, wrap_deg)

WALL_IN, WALL_OUT = 28.5, 31.5
WALK = FLOOR + 8                    # wall-walk top cell (feet WALK + 1)
#          angle  r     radius top crown
TOWERS = [(30, 31.5, 5.0, 30, "dome"),
          (150, 31.5, 5.0, 26, "bell"),
          (190, 31.0, 3.2, 21, "banded"),
          (230, 31.0, 3.5, 25, "armillary"),
          (270, 31.0, 3.8, 37, "needle"),
          (310, 31.0, 3.5, 25, "banded"),
          (350, 31.0, 3.2, 19, "bell")]
GATE_X0, GATE_X1 = 95, 113          # gatehouse body x (inclusive)
GATE_Z0, GATE_Z1 = 130, 138         # gatehouse body z (inclusive), outer face z = 138
GATE_TOWERS = [(92.5, 135.5), (115.5, 135.5)]
WINGS = {   # name: (x0, x1, z0, z1, interior height, long axis)
    "library": (78, 87, 94, 114, 11, "z"),
    "chart_room": (121, 130, 94, 114, 9, "z"),
    "service": (96, 112, 77, 85, 13, "x"),
}
ROOF = Mix({"deepslate_tiles": 3, "cracked_deepslate_tiles": 0.6, "deepslate_bricks": 0.5})


def banded(y0, step=2, ages=("weathered", "oxidized", "weathered", "exposed"), kind="cut", ring_every=0, ribs=None,
           rib_state=None):
    """Banded copper shingles: horizontal bands of different ages; ribs=(cx, cz, n): n vertical ribs (rib_state)."""
    states = np.array([cu(a, kind) for a in ages] + [cu("", "chiseled"), rib_state or cu("", "cut")], object)

    def f(ctx):
        k = ((ctx.ys - y0) // step) % len(ages)
        if ring_every:
            k = np.where(((ctx.ys - y0) % ring_every) == 0, len(ages), k)
        if ribs:
            cx, cz, n = ribs
            th = np.degrees(np.arctan2(ctx.zs + 0.5 - cz, ctx.xs + 0.5 - cx)) + 360
            rr = np.hypot(ctx.xs + 0.5 - cx, ctx.zs + 0.5 - cz)
            per = 360.0 / n
            k = np.where(np.abs((th % per) - per / 2) * np.pi / 180 * np.maximum(rr, 0.5) > per / 2 * np.pi / 180 * np.maximum(rr, 0.5) - 0.6,
                         len(ages) + 1, k)
        return states[k].astype(str)
    return f


# ------------------------------------------------------------------ court
def court(s, ctx):
    b = box_around(s, C, WALL_IN + 1, FLOOR, FLOOR)
    rr = np.hypot(b.x - C[0], b.z - C[1])
    th = np.degrees(np.arctan2(b.z - C[1], b.x - C[0]))
    inner = rr < WALL_IN
    edge_blend = Noise([(-0.1, Mix({"moss_block": 1, "polished_tuff": 1, "tuff": 1})), (1, PAVING)], scale=4, seed=SEED + 200)
    b.fill(inner & (rr > WALL_IN - 3), edge_blend)
    b.fill(inner & (rr <= WALL_IN - 3), PAVING)
    # concentric paving rings every 4 (darker)
    b.fill(inner & (np.abs(((rr + 2) % 4) - 2) < 0.45) & (rr > 15), "polished_deepslate")
    # meridian line (N-S) with copper hour ticks
    mer = (np.abs(b.x - C[0]) < 1.01) & inner & (rr > 14)
    b.fill(mer, "calcite")
    b.fill(mer & (np.abs(((b.z + 2) % 4) - 2) < 0.6), cu("", "chiseled"))
    # compass rose ring around the Spire foot: 16 segments
    seg = (np.floor((th + 360 + 11.25) / 22.5) % 2 == 0)
    b.fill(inner & (rr > 15) & (rr <= 17) & seg, "amethyst_block")
    b.fill(inner & (rr > 15) & (rr <= 17) & ~seg, "calcite")
    b.fill(inner & (rr > 17) & (rr <= 18), cu("weathered", "cut"))


# ------------------------------------------------------------------ ring wall
def ring_wall(s, ctx):
    b = box_around(s, C, WALL_OUT + 1, FLOOR - 6, WALK + 3)
    rr = np.hypot(b.x - C[0], b.z - C[1])
    th = np.degrees(np.arctan2(b.z - C[1], b.x - C[0]))
    gate = np.abs(wrap_deg(th - 90)) < 19
    body = (rr >= WALL_IN) & (rr <= WALL_OUT) & (b.y <= WALK + 0.5) & ~gate
    b.fill(body, MASONRY)
    # outer parapet with crenels (merlon 2, crenel 1 along the arc)
    arc = np.radians(th) * WALL_OUT
    merlon = (np.floor(arc) % 3) != 0
    par = (rr > WALL_OUT - 1) & (rr <= WALL_OUT) & ~gate
    b.fill(par & (b.y > WALK + 0.5) & (b.y < WALK + 1.5), MASONRY)
    b.fill(par & merlon & (b.y > WALK + 1.5) & (b.y < WALK + 2.5), MASONRY)
    # wall-walk paving
    b.fill((rr >= WALL_IN) & (rr <= WALL_OUT - 1) & (b.y > WALK - 0.5) & (b.y < WALK + 0.5) & ~gate, Mix({"polished_tuff": 2, "tuff_bricks": 1}))
    # string course (trim) and base plinth on the outer face
    b.fill((rr > WALL_OUT) & (rr <= WALL_OUT + 1) & (np.abs(b.y - (WALK - 0.5)) < 0.6) & ~gate, TRIM)
    b.fill((rr > WALL_OUT) & (rr <= WALL_OUT + 1) & (b.y < FLOOR + 1.5) & (b.y > FLOOR - 5) & ~gate, Mix({"deepslate_bricks": 2, "polished_deepslate": 1}))
    # pilasters every ~5 blocks on the outer face (+1)
    pil = (np.abs(((arc + 2.5) % 5) - 2.5) < 0.55)
    b.fill(pil & (rr > WALL_OUT) & (rr <= WALL_OUT + 1) & (b.y > FLOOR + 1) & (b.y < WALK) & ~gate, TRIM)
    # stairs up to the wall-walk on both sides of the gate (court side), solid underneath
    full, slab = slab_states("polished_tuff")
    for a0, a1 in ((38, 70), (142, 110)):
        n = 80
        path = []
        for i in range(n + 1):
            t = i / n
            a = math.radians(a0 + (a1 - a0) * t)
            path.append((C[0] + math.cos(a) * 26.9, C[1] + math.sin(a) * 26.9, FLOOR + 1 + (WALK + 1 - FLOOR - 1) * t))
        ramp(s, path, 3.2, full, slab, thick=10, carve=4)


def court_lamps(s, ctx):
    """Eight lamp standards round the compass rose (a copper armillary cage over a lantern), and a lantern on every
    fourth merlon: the wall's crown sparkles from the highland at night."""
    for k in range(8):
        a = 22.5 + 45 * k
        x, z = at_polar(a, 19.6)
        xi, zi = int(x), int(z)
        s.set(xi, FLOOR + 1, zi, "polished_deepslate")
        for dy in (2, 3, 4):
            s.set(xi, FLOOR + dy, zi, "deepslate_brick_wall")
        s.set(xi, FLOOR + 5, zi, cu("", "chiseled"))
        s.set(xi, FLOOR + 6, zi, cu("", "lantern", hanging="false"))
        for dx, dz, f in ((1, 0, "east"), (-1, 0, "west"), (0, 1, "south"), (0, -1, "north")):
            s.set(xi + dx, FLOOR + 5, zi + dz, cu("weathered", "trapdoor", facing=f, half="top", open="true"))
    n = 0
    for k in range(int(2 * math.pi * WALL_OUT)):
        th = k / WALL_OUT
        if wrap_deg(math.degrees(th) - 90) ** 2 < 21 ** 2 or k % 12:
            continue
        x, z = C[0] + math.cos(th) * (WALL_OUT - 0.5), C[1] + math.sin(th) * (WALL_OUT - 0.5)
        xi, zi = int(x), int(z)
        if s.idx[xi, WALK + 2, zi] != 0 and s.idx[xi, WALK + 3, zi] == 0:
            s.set(xi, WALK + 3, zi, cu("exposed", "lantern", hanging="false"))
            n += 1
    ctx["merlon_lamps"] = n


# ------------------------------------------------------------------ towers
def tower(s, ctx, a, rc, rad, top, crown):
    x, z = at_polar(a, rc)
    y_top = FLOOR + top
    base = FLOOR - 10
    c = (x, 0, z)
    # under-deck corbel: the tower grips the island
    s.fill(shapes.cylinder(c, 0.6, base - 10, base + 1, rad + 0.5), Gradient("y", [(base - 4, "tuff"), (999, MASONRY)]))
    s.fill(shapes.cylinder(c, rad, base, y_top), MASONRY)
    # plinth
    s.fill(shapes.cylinder(c, rad + 0.9, FLOOR - 3, FLOOR + 2), Mix({"deepslate_bricks": 2, "polished_deepslate": 1}))
    # attached trim shafts, rising past the eave
    n = 6 if rad >= 4.5 else 4
    for k in range(n):
        ang = math.radians(a + 45 + k * 360 / n)
        px, pz = x + math.cos(ang) * (rad + 0.4), z + math.sin(ang) * (rad + 0.4)
        s.fill(shapes.box((px - 0.5, FLOOR + 2, pz - 0.5), (px + 0.5, y_top + 3, pz + 0.5)), TRIM)
    # interior: ground room + walk-level room, ladder between
    ri = rad - 1.25
    s.fill(shapes.cylinder(c, ri, FLOOR + 0.5, y_top - 1.5), "air")
    s.fill(shapes.cylinder(c, ri, WALK - 0.5, WALK + 0.5), Mix({"spruce_planks": 2, "stripped_spruce_wood": 1}))
    # door from the court (inward) and doors for the wall-walk (tangential)
    ux, uz = math.cos(math.radians(a)), math.sin(math.radians(a))
    b = Box(s, (x - rad - 2, FLOOR, z - rad - 2), (x + rad + 3, y_top + 1, z + rad + 3))
    u = (b.x - x) * ux + (b.z - z) * uz          # outward
    v = -(b.x - x) * uz + (b.z - z) * ux         # tangential
    door_court = (u < 0) & (np.abs(v) < 1.0) & (b.y > FLOOR + 0.5) & (b.y < FLOOR + 3.5)
    b.fill(door_court, "air")
    walk_door = (np.abs(u) < 1.6) & (b.y > WALK + 0.5) & (b.y < WALK + 3.5)
    b.fill(walk_door & (np.abs(v) <= rad + 0.6) & (np.abs(u - (-1.5)) < 1.2), "air")
    # ladder hole in the walk floor + ladder on the outer wall inside
    lx, lz = x + ux * (ri - 0.5), z + uz * (ri - 0.5)
    face = "west" if abs(ux) >= abs(uz) and ux > 0 else "east" if abs(ux) >= abs(uz) else "north" if uz > 0 else "south"
    for yy in range(FLOOR + 1, WALK + 1):
        s.set(int(math.floor(lx)), yy, int(math.floor(lz)), f"ladder[facing={face}]")
    # slit windows on 4 sides, two levels
    for k in range(4):
        ang = math.radians(a + 45 + 90 * k)
        for yy in (FLOOR + 4, WALK + 4):
            wx, wz = x + math.cos(ang) * (rad - 0.5), z + math.sin(ang) * (rad - 0.5)
            for dy in range(3):
                s.set(int(math.floor(wx)), yy + dy, int(math.floor(wz)), "air")
    # eave: corbel ring + light
    s.fill(shapes.cylinder(c, rad + 1.3, y_top - 2, y_top + 1) - shapes.cylinder(c, rad - 0.2, y_top - 2, y_top + 2), MASONRY)
    s.fill(shapes.cylinder(c, rad + 1.4, y_top - 2.5, y_top - 1.5, rad + 0.2) - shapes.cylinder(c, rad - 0.2, 0, 999), TRIM)
    s.fill(shapes.cylinder(c, rad + 1.3, y_top, y_top + 1), TRIM)
    crown_fn = CROWNS[crown]
    crown_fn(s, c, rad, y_top + 1, a)
    # shingle the eave and the crown (the armillary model on top stays crisp)
    R = rad + 4
    skin(s, (x - R, y_top - 2, z - R), (x + R + 1, y_top + (6 if crown == "armillary" else 60), z + R + 1),
         mask=lambda X, Y, Z: np.hypot(X - x, Z - z) > ri + 0.5)
    return dict(c=(x, z), rad=rad, top=y_top, crown=crown, room=ri)


def _finial(s, x, y, z, age=""):
    s.set(int(math.floor(x)), y, int(math.floor(z)), cu(age, "rod"))


def crown_needle(s, c, rad, y0, a):
    """Tallest: banded copper needle with four dormers and a lightning-rod finial."""
    h = rad * 6.0
    s.fill(shapes.cylinder(c, rad + 2.0, y0, y0 + h, 0.3),
           banded(y0, 3, ("oxidized", "oxidized", "exposed"), ribs=(c[0], c[2], 8), rib_state=cu("", "cut")))
    for k in range(4):
        ang = math.radians(a + 45 + 90 * k)
        dx, dz = c[0] + math.cos(ang) * (rad + 0.5), c[2] + math.sin(ang) * (rad + 0.5)
        s.fill(shapes.box((dx - 1, y0 + 1, dz - 1), (dx + 1, y0 + 4, dz + 1)), MASONRY)
        s.fill(shapes.cylinder((dx, 0, dz), 1.6, y0 + 4, y0 + 7, 0.2), cu("oxidized", "cut"))
    _finial(s, c[0], int(y0 + h), c[2])
    _finial(s, c[0], int(y0 + h) + 1, c[2])


def crown_banded(s, c, rad, y0, a):
    h = rad * 4.4
    s.fill(shapes.cylinder(c, rad + 1.7, y0, y0 + 2, rad + 1.4), cu("oxidized", "cut"))
    s.fill(shapes.cylinder(c, rad + 1.4, y0 + 2, y0 + h, 0.25), banded(y0, 2, ("oxidized", "oxidized", "exposed"), ribs=(c[0], c[2], 6),
                                                                        rib_state=cu("weathered", "cut")))
    _finial(s, c[0], int(y0 + h), c[2], "weathered")


def crown_bell(s, c, rad, y0, a):
    """Open belfry with a flared ogee roof and a hanging lantern."""
    ri = rad - 0.6
    for k in range(8):
        ang = math.radians(k * 45 + 22.5)
        px, pz = c[0] + math.cos(ang) * ri, c[2] + math.sin(ang) * ri
        s.fill(shapes.box((px - 0.5, y0, pz - 0.5), (px + 0.5, y0 + 5, pz + 0.5)), TRIM)
    s.fill(shapes.cylinder(c, rad + 0.6, y0 - 1, y0), MASONRY)
    yb = y0 + 5
    s.fill(shapes.cylinder(c, rad + 2.2, yb, yb + 1.5, rad + 0.6), cu("weathered", "cut"))
    s.fill(shapes.cylinder(c, rad + 0.6, yb + 1.5, yb + 4, rad - 0.6), cu("oxidized", "cut"))
    s.fill(shapes.cylinder(c, rad - 0.6, yb + 4, yb + 4 + rad * 2.6, 0.2), banded(yb + 4, 1, ("exposed", "weathered")))
    s.set(int(math.floor(c[0])), yb - 1, int(math.floor(c[2])), cu("", "chain"))
    s.set(int(math.floor(c[0])), yb - 2, int(math.floor(c[2])), cu("", "lantern", hanging="true"))
    _finial(s, c[0], int(yb + 4 + rad * 2.6), c[2], "exposed")


def crown_dome(s, c, rad, y0, a):
    """Telescope dome with an open slit and the telescope poking out (facing the Spire's lantern side)."""
    R = rad + 1.2
    dome = shapes.sphere((c[0], y0, c[2]), R) & shapes.half_space("y", y0, below=False)
    s.fill(dome, cu("weathered", "cut"))
    s.fill(shapes.sphere((c[0], y0, c[2]), R - 1.2) & shapes.half_space("y", y0, below=False), "air")
    # ribs every 45 deg in chiseled copper
    b = Box(s, (c[0] - R - 1, y0, c[2] - R - 1), (c[0] + R + 2, y0 + R + 2, c[2] + R + 2))
    th = np.degrees(np.arctan2(b.z - c[2], b.x - c[0]))
    d = np.sqrt((b.x - c[0]) ** 2 + (b.y - y0) ** 2 + (b.z - c[2]) ** 2)
    rib = np.abs(((th + 360) % 45) - 22.5) > 19.5
    b.fill(rib & (d <= R) & (d > R - 1.3), cu("oxidized", "chiseled"))
    # slit towards angle a+180 (towards the sky over the crater) and the telescope
    sa = math.radians(a + 160)
    sx, sz = math.cos(sa), math.sin(sa)
    slit = (np.abs(-(b.x - c[0]) * sz + (b.z - c[2]) * sx) < 1.1) & (((b.x - c[0]) * sx + (b.z - c[2]) * sz) > 0) & (d <= R + 0.5) & (d > R - 1.6) & (b.y > y0 + 1)
    b.fill(slit, "air")
    p0 = (c[0], y0 + 1.5, c[2])
    p1 = (c[0] + sx * (R + 3), y0 + R + 1.5, c[2] + sz * (R + 3))
    s.fill(shapes.capsule(p0, p1, 0.9), cu("", "block"))
    s.fill(shapes.sphere(p1, 1.2), cu("", "chiseled"))
    s.fill(shapes.cylinder(c, 1.0, y0 - 1, y0 + 1), cu("", "chiseled"))
    _finial(s, c[0], int(y0 + R), c[2], "weathered")


def crown_armillary(s, c, rad, y0, a):
    """Low cone carrying a small armillary sphere: the castle's model of the great rings."""
    s.fill(shapes.cylinder(c, rad + 1.7, y0, y0 + 4, 1.2), banded(y0, 1, ("oxidized", "weathered")))
    cy = y0 + 9
    s.fill(shapes.cylinder(c, 0.6, y0 + 4, cy), cu("", "chiseled"))
    from .common import rot, to_local
    b = Box(s, (c[0] - 6, cy - 6, c[2] - 6), (c[0] + 7, cy + 7, c[2] + 7))
    for k, (tx, yaw, age) in enumerate(((16, 0, "oxidized"), (38, 60, "weathered"), (52, 120, "exposed"))):
        M = rot(tilt_x=tx, yaw=yaw)
        lx, ly, lz = to_local(M, (c[0], cy + 0.5, c[2]), b.x, b.y, b.z)
        R = 4.6 - k * 1.1
        ring = (np.abs(np.sqrt(lx ** 2 + lz ** 2) - R) < 0.55) & (np.abs(ly) < 0.55)
        b.fill(ring, cu(age, "cut"))
    s.set(int(math.floor(c[0])), cy, int(math.floor(c[2])), "amethyst_block")


def crown_pagoda(s, c, rad, y0, a):
    """Gate towers: three flared tiers (a deliberate pair)."""
    y = y0
    for k, (r0, r1, hh) in enumerate(((rad + 3.0, rad + 1.0, 2), (rad + 2.2, rad + 0.4, 2), (rad + 1.4, 0.3, rad * 2.2))):
        s.fill(shapes.cylinder(c, r0, y, y + hh, r1), cu(("weathered", "oxidized", "weathered")[k], "cut"))
        if k < 2:
            s.fill(shapes.cylinder(c, rad - 0.3, y + hh, y + hh + 2), MASONRY)
            y += hh + 2
        else:
            y += hh
        # corner bells at the flare tips
    _finial(s, c[0], int(y), c[2])


CROWNS = {"needle": crown_needle, "banded": crown_banded, "bell": crown_bell, "dome": crown_dome,
          "armillary": crown_armillary, "pagoda": crown_pagoda}


# ------------------------------------------------------------------ wings
def wing(s, ctx, name, x0, x1, z0, z1, h, axis):
    """Shell of a rectangular hall: walls (1) + buttresses, floor, ceiling, roof, lancets, door to the court."""
    y0, y1 = FLOOR - 2, FLOOR + h + 1        # walls from under the deck to the ceiling slab
    s.box((x0, y0, z0), (x1, y1, z1), MASONRY)
    s.box((x0 + 1, FLOOR + 1, z0 + 1), (x1 - 1, FLOOR + h, z1 - 1), "air")
    s.box((x0 + 1, FLOOR, z0 + 1), (x1 - 1, FLOOR, z1 - 1), Mix({"polished_tuff": 2, "polished_deepslate": 1}))
    # plinth course + eave course
    b = Box(s, (x0 - 1, y0, z0 - 1), (x1 + 2, y1 + 2, z1 + 2))
    outside1 = ((b.x < x0) | (b.x > x1 + 1) | (b.z < z0) | (b.z > z1 + 1)) & (b.x > x0 - 1) & (b.x < x1 + 2) & (b.z > z0 - 1) & (b.z < z1 + 2)
    b.fill(outside1 & (b.y < FLOOR + 2) & (b.y > FLOOR - 3), Mix({"deepslate_bricks": 2, "polished_deepslate": 1}))
    b.fill(outside1 & (b.y > y1 - 0.5), TRIM)
    # buttress pilasters every 4 along the long sides (+1, trim), rising 2 above the eave as pinnacles
    long_lo, long_hi = (z0, z1) if axis == "z" else (x0, x1)
    for t in range(long_lo + 2, long_hi - 1, 4):
        for side in (0, 1):
            if axis == "z":
                px = x0 - 1 if side == 0 else x1 + 1
                s.box((px, FLOOR - 2, t), (px, y1 + 2, t), TRIM)
                s.set(px, y1 + 3, t, cu("", "rod"))
            else:
                pz = z0 - 1 if side == 0 else z1 + 1
                s.box((t, FLOOR - 2, pz), (t, y1 + 2, pz), TRIM)
                s.set(t, y1 + 3, pz, cu("", "rod"))
    # lancet windows between the buttresses, both long sides
    for t in range(long_lo + 4, long_hi - 1, 4):
        for side in (0, 1):
            for yy in range(FLOOR + 3, FLOOR + h - 1):
                if axis == "z":
                    s.set(x0 if side == 0 else x1, yy, t, GLASS_V_PANE)
                else:
                    s.set(t, yy, z0 if side == 0 else z1, GLASS_V_PANE)
    # door to the court: on the side facing the Spire
    cxm, czm = (x0 + x1) // 2, (z0 + z1) // 2
    if axis == "z":
        dx = x1 if cxm < C[0] else x0
        door = [(dx, yy, czm + dz) for yy in range(FLOOR + 1, FLOOR + 5) for dz in (-1, 0, 1)]
    else:
        dz = z1 if czm < C[1] else z0
        door = [(cxm + dx, yy, dz) for yy in range(FLOOR + 1, FLOOR + 5) for dx in (-1, 0, 1)]
    for p in door:
        s.set(*p, "air")
    # roof
    roof(s, x0 - 1, x1 + 1, z0 - 1, z1 + 1, y1 + 1, axis, name)
    return dict(box=(x0 + 1, FLOOR + 1, z0 + 1, x1 - 1, FLOOR + h, z1 - 1), door=door[len(door) // 2])


def roof(s, x0, x1, z0, z1, y0, axis, name):
    """Gable roof along the long axis; the chart room gets a flat instrument terrace instead."""
    if name == "chart_room":
        s.box((x0, y0, z0), (x1, y0, z1), Mix({"polished_tuff": 2, "calcite": 1}))
        for x in range(x0, x1 + 1):
            for z in (z0, z1):
                s.set(x, y0 + 1, z, "polished_tuff_wall" if (x % 2) else "calcite")
        for z in range(z0, z1 + 1):
            for x in (x0, x1):
                s.set(x, y0 + 1, z, "polished_tuff_wall" if (z % 2) else "calcite")
        return
    b = Box(s, (x0, y0, z0), (x1 + 1, y0 + 12, z1 + 1))
    if axis == "z":
        half = (x1 - x0) / 2
        d = np.abs(b.x - (x0 + x1 + 1) / 2)
    else:
        half = (z1 - z0) / 2
        d = np.abs(b.z - (z0 + z1 + 1) / 2)
    rise = b.y - y0
    body = (d + rise <= half + 0.5)
    b.fill(body, ROOF)
    b.fill(body & (d + rise > half - 0.5), ROOF)
    ridge = body & (d < 1.0) & (d + rise > half - 0.5)
    b.fill(ridge, cu("oxidized", "cut"))
    skin(s, (x0 - 1, y0, z0 - 1), (x1 + 2, y0 + 12, z1 + 2), corners=None,
         dirs=("west", "east") if axis == "z" else ("north", "south"))


# ------------------------------------------------------------------ gatehouse
def gatehouse(s, ctx):
    x0, x1, z0, z1 = GATE_X0, GATE_X1, GATE_Z0, GATE_Z1
    top = FLOOR + 26
    s.box((x0, FLOOR - 6, z0), (x1, top, z1), MASONRY)
    b = Box(s, (x0 - 4, FLOOR - 1, z0 - 1), (x1 + 5, top + 12, z1 + 5))
    u = b.x - C[0]
    v = b.y - FLOOR - 1 + 0.5
    # passage: 5 wide pointed arch through the body
    passage = pointed_arch_2d(u, v - 0.5, 2.5, 5) & (b.y > FLOOR + 0.5) & (b.z > z0 - 1) & (b.z < z1 + 1.5)
    b.fill(passage, "air")
    b.fill((np.abs(u) < 3) & (b.y > FLOOR - 0.5) & (b.y < FLOOR + 0.5) & (b.z > z0 - 1) & (b.z < z1 + 1), Mix({"polished_tuff": 2, "calcite": 1}))
    # nested recessed rings on the outer face (each ring -1 deeper, alternating materials)
    for ring, mat in ((3, "tuff_bricks"), (2, "calcite"), (1, "polished_tuff")):
        hs, sp = 2.5 + ring, 5 + ring
        arch = pointed_arch_2d(u, v - 0.5, hs, sp) & ~pointed_arch_2d(u, v - 0.5, hs - 1, sp - 1) & (b.y > FLOOR + 0.5)
        b.fill(arch & (b.z > z1 + 1 - (4 - ring)) & (b.z < z1 + 1), mat)
    # gate room above the passage (wall-walk level), tall: the astrolabe window fills its upper south wall
    s.box((x0 + 2, WALK + 1, z0 + 1), (x1 - 2, WALK + 16, z1 - 1), "air")
    s.box((x0 + 2, WALK, z0 + 1), (x1 - 2, WALK, z1 - 1), Mix({"spruce_planks": 2, "polished_tuff": 1}))
    for side in (x0, x1):      # wall-walk doors
        for yy in range(WALK + 1, WALK + 4):
            for zz in (z0 + 1, z0 + 2):
                s.set(side, yy, zz, "air")
        s.box((side, WALK + 1, z0 + 1), (side + (1 if side == x0 else -1), WALK + 3, z0 + 2), "air")
    # stepped gable crown with spikes
    for k in range(7):
        hw = 9 - k * 1.3
        s.box((int(C[0] - hw), top + 1 + k, z1 - 4), (int(C[0] + hw), top + 1 + k, z1), MASONRY)
        for sx in (-hw, hw):
            px = int(math.floor(C[0] + sx))
            s.box((px, top + 1 + k, z1 + 1), (px, top + 3 + k, z1 + 1), TRIM)
            s.set(px, top + 4 + k, z1 + 1, cu("", "rod"))
    # gate towers (the pair)
    towers = []
    for (gx, gz) in GATE_TOWERS:
        c = (gx, 0, gz)
        rad = 3.6
        y_top = FLOOR + 30
        s.fill(shapes.cylinder(c, 0.6, FLOOR - 22, FLOOR - 9, rad + 0.5), Gradient("y", [(FLOOR - 16, "tuff"), (999, MASONRY)]))
        s.fill(shapes.cylinder(c, rad, FLOOR - 10, y_top), MASONRY)
        s.fill(shapes.cylinder(c, rad + 0.9, FLOOR - 3, FLOOR + 2), Mix({"deepslate_bricks": 2, "polished_deepslate": 1}))
        for k in range(6):
            ang = math.radians(k * 60 + 30)
            px, pz = gx + math.cos(ang) * (rad + 0.4), gz + math.sin(ang) * (rad + 0.4)
            s.fill(shapes.box((px - 0.5, FLOOR + 2, pz - 0.5), (px + 0.5, y_top + 3, pz + 0.5)), TRIM)
        s.fill(shapes.cylinder(c, rad + 1.3, y_top - 2, y_top + 1) - shapes.cylinder(c, rad - 0.2, 0, 999), MASONRY)
        crown_pagoda(s, c, rad, y_top + 1, 90)
        skin(s, (gx - rad - 4, y_top - 2, gz - rad - 4), (gx + rad + 5, y_top + 30, gz + rad + 5))
        # lit lanterns on the jambs (paired fixtures)
        towers.append(dict(c=(gx, gz), rad=rad, top=y_top))
    for sx in (-4, 4):
        s.set(int(C[0] + sx), FLOOR + 6, z1 + 1, cu("", "lantern"))
        s.set(int(C[0] + sx), FLOOR + 5, z1 + 1, "calcite")
    # forecourt terrace (outside) + bridge-head pylons
    s.box((94, FLOOR - 1, z1 + 1), (114, FLOOR, z1 + 7), Mix({"polished_tuff": 3, "tuff_bricks": 2, "calcite": 0.5}))
    for sx in (-10, 10):
        px = int(C[0] + sx)
        s.box((px, FLOOR - 4, z1 + 7), (px, FLOOR + 6, z1 + 7), MASONRY)
        s.box((px, FLOOR + 7, z1 + 7), (px, FLOOR + 7, z1 + 7), cu("", "bulb", lit="true", powered="false"))
        s.set(px, FLOOR + 8, z1 + 7, cu("", "rod"))
    gate_face(s, ctx, top)
    ctx["gate_room"] = (x0 + 2, WALK + 1, z0 + 1, x1 - 2, WALK + 16, z1 - 1)
    ctx["gate_towers"] = towers


ASTRO_C = (104.0, FLOOR + 25.0)     # the Astrolabe's centre on the gate face (x, y)


def gate_face(s, ctx, top):
    """The Astrolabe Gate: the densest face of the build. Over the nested portal hangs a 14-block astrolabe (calcite
    mater with copper hour ticks, a copper rete of star lines and a fresh-copper alidade over violet glass: the Gate
    Room's window); two stepped buttresses (three setbacks, stair caps, copper pinnacles) frame it, with a copper
    star-gazer statue and a lantern on each first setback."""
    z1 = GATE_Z1
    ax, ay = ASTRO_C
    b = Box(s, (ax - 10, FLOOR, z1), (ax + 10, top + 8, z1 + 4))
    u, v = b.x - ax, b.y - ay
    r = np.hypot(u, v)
    ang = np.degrees(np.arctan2(v, u)) % 360
    zc = b.z - 0.5                           # integer cell z
    R_GL, R_IN, R_OUT = 5.6, 5.6, 7.0
    b.fill((zc == z1) & (r < R_GL), "purple_stained_glass")
    b.fill((zc == z1 + 1) & (r >= R_IN) & (r < R_OUT), "calcite")
    tick = np.abs(((ang + 15) % 30) - 15) * np.pi / 180 * r < 0.55
    b.fill((zc == z1 + 2) & (r >= R_IN) & (r < R_OUT) & tick, cu("oxidized", "chiseled"))
    # rete: three star lines, an inner ring (the ecliptic) and the alidade
    for a in (0, 60, 120):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        b.fill((zc == z1 + 1) & (r < R_IN) & (np.abs(-u * sa + v * ca) < 0.5), cu("", "cut"))
    b.fill((zc == z1 + 1) & (r >= 2.6) & (r < 3.6), cu("exposed", "cut"))
    ca, sa = math.cos(math.radians(75)), math.sin(math.radians(75))
    b.fill((zc == z1 + 2) & (r < R_OUT + 0.6) & (np.abs(-u * sa + v * ca) < 0.5) & (u * ca + v * sa > -1.5), cu("", "chiseled"))
    b.fill((zc == z1 + 2) & (r < 1.0), "amethyst_block")
    b.fill((zc == z1 + 3) & (r < 0.75), cu("", "bulb", lit="true", powered="false"))
    # buttresses
    for sgn in (-1, 1):
        xs = [int(ax + sgn * 6.5 - 0.5), int(ax + sgn * 7.5 - 0.5)] if sgn > 0 else [int(ax - 7), int(ax - 8)]
        for (ya, yb, d, mat) in ((FLOOR + 1, FLOOR + 9, 3, Mix({"deepslate_bricks": 3, "polished_deepslate": 1})),
                                 (FLOOR + 10, FLOOR + 17, 2, Mix({"tuff_bricks": 3, "polished_tuff": 1})),
                                 (FLOOR + 18, top - 1, 1, Mix({"tuff_bricks": 2, "polished_tuff": 1}))):
            for x in xs:
                s.box((x, ya, z1 + 1), (x, yb, z1 + d), mat)
                s.set(x, yb + 1, z1 + d, "calcite" if d == 1 else "polished_tuff_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]")
        inner, outer = xs[0], xs[1]
        s.set(inner, FLOOR + 10, z1 + 3, "waxed_copper_golem_statue[facing=south,copper_golem_pose=star,waterlogged=false]")
        s.set(outer, FLOOR + 10, z1 + 3, cu("", "lantern", hanging="false"))
        for x in xs:                                   # pinnacles
            s.set(x, top + 1, z1 + 1, cu("", "chiseled"))
            s.set(x, top + 2, z1 + 1, cu("", "rod"))
    ctx["astrolabe"] = dict(c=(ax, ay, z1), r=R_OUT)


def outer_terrace(s, ctx):
    """The lawn outside the ring wall (the berm) joins the forecourt: a paved apron round each gate tower and a
    forecourt widened to the berm, so a player knocked off the wall-walk can walk back to the gate."""
    apron = Mix({"polished_tuff": 3, "tuff_bricks": 2, "mossy_stone_bricks": 0.5})
    for (gx, gz) in GATE_TOWERS:
        c = (gx, 0, gz)
        ring = shapes.cylinder(c, 8.2, FLOOR - 0.5, FLOOR + 0.5) - shapes.cylinder(c, 4.4, 0, 999)
        s.fill(ring, apron, replace="air")
        s.fill(shapes.cylinder(c, 0.5, FLOOR - 9, FLOOR - 0.5, 8.0).displace(0.8, 3, seed=int(gx)), MASONRY, replace="air")
    s.box((86, FLOOR - 1, GATE_Z1 + 1), (122, FLOOR, GATE_Z1 + 6), apron, replace="air")


def tower_wing_doors(s, ctx):
    """A tower whose court door runs into a wing gets the door carried through the wing wall (an inner door)."""
    for t in ctx["towers"]:
        x, z = t["c"]
        a = math.atan2(z - C[1], x - C[0])
        ux, uz = math.cos(a), math.sin(a)
        for d in np.arange(t["rad"] - 1.0, t["rad"] + 6.0, 0.5):
            for w in (-0.5, 0.5):
                px, pz = x - ux * d - uz * w, z - uz * d + ux * w
                for yy in range(FLOOR + 1, FLOOR + 4):
                    xi, zi = int(math.floor(px)), int(math.floor(pz))
                    if s.get(xi, yy, zi) not in ("minecraft:air", "air") and "ladder" not in s.get(xi, yy, zi):
                        s.set(xi, yy, zi, "air")


def service_floors(s, ctx):
    """The Service house is two storeys: Kitchen (ground) and Quarters (upper, FLOOR + 7), a straight stair along the
    north wall, rising west."""
    x0, y0, z0, x1, y1, z1 = ctx["wings"]["service"]["box"]
    fy = FLOOR + 7
    s.box((x0, fy, z0), (x1, fy, z1), Mix({"spruce_planks": 3, "stripped_spruce_wood": 1}))
    for i in range(fy - FLOOR - 1):
        x = x1 - 1 - i
        s.set(x, FLOOR + 1 + i, z0, "polished_tuff_stairs[facing=west,half=bottom,shape=straight]")
        s.set(x, FLOOR + 1 + i, z0 + 1, "polished_tuff_stairs[facing=west,half=bottom,shape=straight]")
        for z in (z0, z0 + 1):
            s.set(x, fy, z, "air")
    s.set(x1 - (fy - FLOOR - 1), fy, z0, "air")
    s.set(x1 - (fy - FLOOR - 1), fy, z0 + 1, "air")
    # balustrade along the stair hole
    for i in range(fy - FLOOR):
        s.set(x1 - 1 - i, fy + 1, z0 + 2, "spruce_fence")
    # upper-storey windows on the court side
    for x in range(x0 + 2, x1 - 1, 4):
        for yy in (fy + 2, fy + 3):
            s.set(x, yy, z1 + 1, GLASS_V_PANE)
    ctx["service_floor"] = fy


def build(s, ctx):
    court(s, ctx)
    ring_wall(s, ctx)
    court_lamps(s, ctx)
    ctx["towers"] = [tower(s, ctx, *t) for t in TOWERS]
    ctx["wings"] = {n: wing(s, ctx, n, *w) for n, w in WINGS.items()}
    tower_wing_doors(s, ctx)
    service_floors(s, ctx)
    gatehouse(s, ctx)
    outer_terrace(s, ctx)
