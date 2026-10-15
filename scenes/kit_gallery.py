"""Kit gallery: every furniture kit in front of a wall, one row per style. Cameras cam_<style>_<n> per bay group.

    python -m tools.voxel render scenes/kit_gallery.py --only eye
"""
import os

from tools.voxel.scene import Scene
from tools.voxel.kits import STYLES, furniture as F

ROW_STYLES = os.environ.get("KIT_STYLES", "keep,noble").split(",")
GAP = 2
ROW_D = 12
H = 7


def build():
    rows = []
    for name in ROW_STYLES:
        st = STYLES[name]
        rows.append((name, F.catalogue(st)))
    width = max(sum(k.shape[0] + GAP for _, k in cat) for _, cat in rows) + GAP
    s = Scene((width, H + 1, ROW_D * len(rows) + 2), "kit_gallery")
    for r, (name, cat) in enumerate(rows):
        z0 = r * ROW_D + 1          # wall at z0, kits from z0+1
        s.box((0, 0, r * ROW_D), (width - 1, 0, r * ROW_D + ROW_D - 1), STYLES[name].w("planks") if r % 2 else "minecraft:spruce_planks")
        s.box((0, 1, z0), (width - 1, H, z0), "minecraft:stone_bricks")
        s.box((0, H, z0 + 1), (width - 1, H, z0 + 5), "minecraft:dark_oak_planks")  # ceiling for hanging kits
        x = GAP
        group, gx = [], x
        for i, (label, kit) in enumerate(cat):
            y = 3 if "sconce" in label or label in ("torch", "tapestry") else H - kit.shape[1] if label in ("chandelier", "great chandelier", "lantern chandelier", "hanging lantern") else 1
            if y not in (1, 3):   # hang from the lip: kit centre under the lip row
                F.place(s, kit, (x, y, z0 + 3 - kit.shape[2] // 2))
            else:
                F.place(s, kit, (x, y, z0 + 1))
            group.append(label)
            x += kit.shape[0] + GAP
            if x - gx >= 13 or i == len(cat) - 1:
                cx = (gx + x - GAP) / 2
                s.mark(f"cam_{name}_{len([m for m in s.markers if m.startswith('cam_' + name)])}",
                       (cx, 2.2, z0 + 7.5), look_at=(cx, 1.2, z0 + 1.5))
                gx = x
                group = []
    return s
