"""Last pass: soil stability, markers (spawns + cameras)."""
import numpy as np

from tools.voxel import stability

from .common import C, FLOOR, LAKE_Y, column_top


def ground_y(s, x, z, below=None):
    return column_top(s, x, z, below) + 1


def markers(s, ctx):
    s.mark("spawn_white", (104, ground_y(s, 104, 196), 196), look_at=(104, 150, 104))
    s.markers["spawn_white"]["fov"] = 80
    s.mark("spawn_black", (104, ground_y(s, 104, 12), 12), look_at=(104, 150, 104))
    s.markers["spawn_black"]["fov"] = 80
    s.mark("cam_hero", (196, 92, 198), look_at=(104, 136, 100))
    s.markers["cam_hero"]["fov"] = 62
    s.mark("cam_landing", (98, ground_y(s, 98, 166), 166), look_at=(104, 150, 104))
    s.mark("cam_crater", (76, ground_y(s, 76, 126, below=60), 126), look_at=(104, 95, 104))     # on the crater floor, off the wall
    s.mark("cam_below", (104, ground_y(s, 104, 136, below=60), 136), look_at=(104, 90, 104))
    s.markers["cam_below"]["fov"] = 85
    s.mark("cam_gate", (104, FLOOR + 1, 158), look_at=(104, 127, 138))
    s.markers["cam_gate"]["fov"] = 75
    s.mark("cam_arc", (67, ground_y(s, 67, 67, below=60), 67), look_at=(40, 58, 40))      # on the crater rim, under the arch
    s.markers["cam_arc"]["fov"] = 85
    ob = ctx.get("observatory")
    if ob:
        import math
        a = math.radians(335.0)
        cx, cz = 104 + math.cos(a) * 61, 104 + math.sin(a) * 61      # on the heath inside the crater rim, below the tower
        s.mark("cam_observatory", (cx, ground_y(s, cx, cz, below=100), cz), look_at=(ob["c"][0], ob["floor"] + 17, ob["c"][1]))
        s.markers["cam_observatory"]["fov"] = 80
    s.mark("cam_court", (88, FLOOR + 1, 121), look_at=(110, FLOOR + 5, 110))
    s.mark("cam_gallery", (104, 151, 120), look_at=(160, 150, 50))
    L = ctx.get("stair_landings")
    if L:
        import math
        x, z = L[1]["c"]
        a = math.radians(L[1]["a"])
        x, z = x - math.sin(a) * 2.5, z + math.cos(a) * 2.5      # off the hoop, along the stair
        s.mark("cam_stair", (x, L[1]["y"] + 1, z), look_at=(104, 140, 104))


def plug_pockets(s, ctx, max_size=6):
    """Crevices a falling player can land in but never leave (between a tower plinth and a wing wall, behind a
    buttress): fill them with the block they stand on. Bigger traps are design bugs and are fixed at their source."""
    from tools.voxel import walk
    n = 0
    for _ in range(8):      # a crevice is filled 2 blocks at a time until its floor reaches open ground
        rep, w, r = walk.run(s, quiet=True)
        k = 0
        for comp in w.clusters(r["trap"]):
            if len(comp) > max_size or any(r["has_lethal"][i] for i in comp):
                continue
            for i in comp:
                t, x, z, L, y = w.pos[i]
                if t != "s":
                    continue
                st = s.get(x, y, z)
                for dy in (1, 2):
                    s.set(x, y + dy, z, st)
                    k += 1
        n += k
        if not k:
            break
    ctx["plugged"] = n


def courses(s, ctx):
    """String courses every 5 rows on all flat masonry (the castle, the Spire, the cellars, the ruins), with star lamps
    set in them: denser on the castle and Spire (lit for the court and the gallery), sparse on the ruins."""
    from .common import relief
    rows = lambda y: (y - FLOOR) % 5 == 3
    not_gate = lambda x, y, z: ~((np.abs(x - 104) < 16) & (z > 128) & (y < FLOOR + 40))    # the gate face has its own lighting
    up = relief(s, (0, FLOOR + 2, 0), s.shape, rows, lamp_p=0.2, lamp_mask=not_gate)
    down = relief(s, (0, 20, 0), (s.shape[0], FLOOR + 2, s.shape[2]), rows, lamp_p=0.08, seed=1)
    ctx["courses"] = dict(stairs=up[0] + down[0], lamps=up[1] + down[1])


def loose_dripstone(s, ctx):
    """Hanging dripstone must reach a solid block above through its own column; any orphan (its ceiling carved away
    by a later part) would drop as a falling block in game, so it is removed."""
    names = s.names()
    drip = np.array(["pointed_dripstone" in n for n in names])
    removed = 0
    for x, y, z in np.argwhere(drip[s.idx]):
        yy = y + 1
        while yy < s.shape[1] and drip[s.idx[x, yy, z]]:
            yy += 1
        if yy >= s.shape[1] or s.idx[x, yy, z] == 0:
            s.set(int(x), int(y), int(z), "air")
            removed += 1
    ctx["loose_dripstone"] = removed


def rim_kerb(s, ctx):
    """The island's turf shelf outside the ring wall ends in a balustrade of tuff-brick posts along the drop, broken
    every few metres (a fall is always a choice) and open at the gate and the stair: the castle reads as standing on a
    finished terrace, not on a grass ledge."""
    from tools.voxel import noise
    from .common import polar_xz
    H = s.idx.shape[1]
    solid = s.idx != 0
    ys = np.arange(H)[None, :, None]
    top = np.where(solid.any(axis=1), (solid * ys).max(axis=1), -1)
    names = s.names()
    turf = np.array([any(k in n for k in ("grass_block", "moss_block", "dirt", "dirt_path", "podzol")) for n in names])
    X, Z = np.meshgrid(np.arange(s.shape[0]), np.arange(s.shape[2]), indexing="ij")
    tb = s.idx[X, np.clip(top, 0, H - 1), Z]
    shelf = (top >= FLOOR - 3) & (top <= FLOOR + 1) & turf[tb]
    nb = np.full_like(top, 999)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nb = np.minimum(nb, np.roll(np.roll(top, dx, 0), dz, 1))
    edge = shelf & (nb < top - 4)
    r, th = polar_xz(X + 0.5, Z + 0.5)
    keep = noise.hash01(np.floor((th + 180) / 5).astype(int), 0, 0, seed=811) > 0.22
    edge &= keep & ~((np.abs(X - 104) < 18) & (Z > 124))
    P = np.array(ctx.get("stair_path", []))
    if len(P):
        for x, z, y in P[::6]:
            if abs(y - FLOOR) < 8:
                edge &= np.hypot(X - x, Z - z) > 5
    K = set(zip(*np.nonzero(edge)))
    n = 0
    for x, z in K:
        y = int(top[x, z]) + 1
        if s.idx[x, y, z] != 0:
            continue
        sides = {d: ("low" if (x + dx, z + dz) in K and top[x + dx, z + dz] + 1 == y else "none")
                 for d, dx, dz in (("east", 1, 0), ("west", -1, 0), ("south", 0, 1), ("north", 0, -1))}
        post = sum(v == "low" for v in sides.values()) != 2 or noise.hash01(x, y, z, seed=812) < 0.15
        s.set(x, y, z, "tuff_brick_wall[" + ",".join(f"{d}={v}" for d, v in sides.items()) + f",up={'true' if post else 'false'},waterlogged=false]")
        n += 1
    ctx["rim_kerb"] = n
    # revetment: the soil the shelf stands on shows as a brown band on the cliff; face it with masonry
    from tools.voxel.palette import Mix
    y0, y1 = FLOOR - 9, FLOOR + 1
    sub = s.idx[:, y0:y1, :]
    soil = np.array([any(k in n_ for k in ("dirt", "grass_block", "moss_block", "podzol")) for n_ in names])[sub]
    air = sub == 0
    exp = np.zeros_like(soil)
    for ax, d in ((0, 1), (0, -1), (2, 1), (2, -1)):
        exp |= np.roll(air, d, axis=ax)
    face = soil & exp
    face[:, -1, :] &= False          # keep the walking surface turf
    m = np.zeros(s.idx.shape, bool)
    m[:, y0:y1, :] = face
    m[:, :, :] &= (np.hypot(*np.meshgrid(np.arange(s.shape[0]) + 0.5 - C[0], np.arange(s.shape[2]) + 0.5 - C[1], indexing="ij")) < 60)[:, None, :]
    ctx["revet"] = s.fill(m, Mix({"tuff_bricks": 3, "deepslate_bricks": 1, "cracked_deepslate_bricks": 0.4}))


def dial(s, ctx):
    """The lake is the dial: four gnomons (stone obelisks with lit copper heads) stand on the shore at the 60/120/240/300
    deg hours, mirror-symmetric for the two spawns, and calcite hour stones with end rods mark the other hours. Landmarks
    and cover on the crater floor between the Landing and the island's shadow."""
    import math
    from tools.voxel import shapes
    from tools.voxel.palette import Mix
    from .common import cu
    out = []
    for a in range(0, 360, 30):
        gnomon = a in (60, 120, 240, 300)
        r = 40.0 if gnomon else 37.0
        x, z = C[0] + math.cos(math.radians(a)) * r, C[1] + math.sin(math.radians(a)) * r
        xi, zi = int(x), int(z)
        g = column_top(s, xi, zi, 60)
        if g <= LAKE_Y or "water" in s.get(xi, g, zi):
            continue
        if not gnomon:
            s.set(xi, g + 1, zi, "calcite")
            s.set(xi, g + 2, zi, "chiseled_tuff_bricks")
            s.set(xi, g + 3, zi, "end_rod[facing=up]")
            continue
        c = (xi + 0.5, 0, zi + 0.5)
        s.fill(shapes.cylinder(c, 3.6, g - 3, g + 0.5), Mix({"polished_tuff": 3, "tuff_bricks": 1}))
        s.fill(shapes.cylinder(c, 3.6, g - 0.5, g + 0.5) - shapes.cylinder(c, 2.9, 0, 999), "calcite")
        s.fill(shapes.cylinder(c, 3.6, g + 0.5, g + 18), "air", replace="solid")
        for k in range(17):
            y = g + 1 + k
            if k < 6:
                lo, hi = (xi - 1, zi - 1), (xi + 3, zi + 3)
                mat = "calcite" if k == 5 else Mix({"polished_deepslate": 2, "deepslate_bricks": 1})
            elif k < 14:
                lo, hi = (xi, zi), (xi + 2, zi + 2)
                mat = {11: "calcite", 12: cu("", "bulb", lit="true", powered="false"), 13: cu("weathered", "chiseled")}.get(k, Mix({"polished_deepslate": 2, "deepslate_tiles": 1}))
            else:
                s.set(xi, y, zi, cu("", "rod") if k < 16 else cu("", "rod"))
                continue
            s.fill(shapes.box((lo[0], y, lo[1]), (hi[0], y + 1, hi[1])), mat)
        out.append((a, xi, g, zi))
    ctx["dial"] = out


def build(s, ctx):
    dial(s, ctx)
    rim_kerb(s, ctx)
    courses(s, ctx)
    n = stability.fix_soil(s)
    ctx["fix_soil"] = n
    loose_dripstone(s, ctx)
    markers(s, ctx)
    plug_pockets(s, ctx)
