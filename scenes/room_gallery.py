"""Room decorator gallery: one shell per room kind, furnished by tools.voxel.kits.rooms.

    python -m tools.voxel render scenes/room_gallery.py --only eye        (cam_<kind> from each door)
    ROOMS_OPEN=1 python -m tools.voxel render scenes/room_gallery.py --only top,iso   (ceilings removed)
    ROOM_STYLE=noble ...                                                  (one style for every room)
"""
import json
import os

from tools.voxel.scene import Scene
from tools.voxel.kits import rooms

# kind, interior W x D x H, style, door side
ROOMS = [
    ("hall", (17, 9, 6), "keep", "S"),
    ("bedroom", (9, 7, 5), "noble", "S"),
    ("library", (11, 8, 5), "noble", "S"),
    ("kitchen", (9, 8, 5), "cottage", "S"),
    ("chapel", (9, 15, 7), "chapel", "S"),
    ("armoury", (9, 7, 5), "keep", "S"),
    ("cellar", (9, 7, 4), "cottage", "S"),
    ("lab", (9, 7, 5), "arcane", "S"),
]
CEIL = "minecraft:stripped_spruce_wood"
FLOORS = {"keep": "minecraft:stone_bricks", "noble": "minecraft:dark_oak_planks", "cottage": "minecraft:spruce_planks",
          "chapel": "minecraft:polished_diorite", "arcane": "minecraft:polished_deepslate"}


def build():
    gap = 4
    width = sum(r[1][0] + 2 + gap for r in ROOMS)
    s = Scene((width + gap, 10, 15 + 2 + 12), "room_gallery")
    x = gap
    reports = {}
    for kind, (W, D, H), st, side in ROOMS:
        st = os.environ.get("ROOM_STYLE", st)
        x0, z0, y0 = x + 1, 1, 1
        x1, z1, y1 = x0 + W - 1, z0 + D - 1, y0 + H - 1
        s.box((x0 - 1, 0, z0 - 1), (x1 + 1, 0, z1 + 1), FLOORS.get(st, "minecraft:stone_bricks"))
        s.box((x0 - 1, 1, z0 - 1), (x1 + 1, y1, z1 + 1), "minecraft:stone_bricks", hollow=True)
        s.box((x0, 1, z0), (x1, y1, z1), "minecraft:air")
        s.box((x0 - 1, y1 + 1, z0 - 1), (x1 + 1, y1 + 1, z1 + 1), CEIL)
        dx = (x0 + x1) // 2
        s.box((dx, 1, z1 + 1), (dx, 2, z1 + 1), "minecraft:air")      # door opening
        rep = rooms.furnish(s, (x0, y0, z0, x1, y1, z1), kind, st, doors=[(dx, 1, z1 + 1)], seed=7)
        reports[kind] = rep
        s.mark(f"cam_{kind}", (dx + 0.5, 1, z1 + 0.3), look_at=(dx + 0.5, 1.8, z0 + 1))
        x = x1 + 2 + gap
    if os.environ.get("ROOMS_OPEN"):
        s.replace(CEIL, "minecraft:air")
    s.meta["rooms"] = reports
    if os.environ.get("ROOMS_REPORT"):
        print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "labels"} for k, v in reports.items()}, indent=1))
    return s
