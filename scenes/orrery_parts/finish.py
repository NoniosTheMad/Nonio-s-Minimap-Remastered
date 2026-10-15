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
    s.mark("cam_crater", (60, ground_y(s, 60, 120, below=60), 120), look_at=(104, 95, 104))     # on the inner slope
    s.mark("cam_below", (104, ground_y(s, 104, 136, below=60), 136), look_at=(104, 90, 104))
    s.markers["cam_below"]["fov"] = 85
    s.mark("cam_gate", (104, FLOOR + 1, 158), look_at=(104, 127, 138))
    s.markers["cam_gate"]["fov"] = 75
    s.mark("cam_arc", (67, ground_y(s, 67, 67, below=60), 67), look_at=(40, 58, 40))      # on the crater rim, under the arch
    s.markers["cam_arc"]["fov"] = 85
    s.mark("cam_observatory", (150, 113, 82), look_at=(180, 58, 69))
    s.markers["cam_observatory"]["fov"] = 50
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


def build(s, ctx):
    courses(s, ctx)
    n = stability.fix_soil(s)
    ctx["fix_soil"] = n
    loose_dripstone(s, ctx)
    markers(s, ctx)
    plug_pockets(s, ctx)
