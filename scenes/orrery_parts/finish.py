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
    s.mark("cam_crater", (66, ground_y(s, 66, 134, below=60), 134), look_at=(104, 120, 104))
    s.mark("cam_below", (104, ground_y(s, 104, 136, below=60), 136), look_at=(104, 90, 104))
    s.markers["cam_below"]["fov"] = 85
    s.mark("cam_gate", (104, FLOOR + 1, 143), look_at=(104, 170, 104))
    s.mark("cam_court", (88, FLOOR + 1, 121), look_at=(104, 185, 104))
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


def build(s, ctx):
    n = stability.fix_soil(s)
    ctx["fix_soil"] = n
    markers(s, ctx)
    plug_pockets(s, ctx)
