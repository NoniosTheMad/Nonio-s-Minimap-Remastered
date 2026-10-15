"""Emerald Dream ruins (feedback #47): structure templates placed at runtime by nonios:dream/ruin/*.

    python tools/build_dream.py      (needs nbtlib)

Writes datapack/data/nonios/structure/dream/ruin_<name>.nbt (26.3 template format: palette entries are {id, properties}).
Each is a small ruin with a loot container (LootTable nonios:dream/ruin). Positions not listed are structure void
(the terrain stays). Floors are at y 0 and replace the ground block (dream/ruin/place puts the origin at ~ ~-1 ~).
Not a worldgen structure on purpose: the map world is created with generate-structures=false, so jigsaw structures
would never appear there; the dream plants ruins around each arrival point instead, like its regrowing veins.
"""
from pathlib import Path

import nbtlib
from nbtlib.tag import Compound, Int, List, String

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "datapack" / "data" / "nonios" / "structure" / "dream"
DATA_VERSION = 5023  # 26.3 (server jar version.json world_version)
LOOT = "nonios:dream/ruin"


class T:
    def __init__(self, sx, sy, sz):
        self.size = (sx, sy, sz)
        self.blocks = {}

    def put(self, x, y, z, name, nbt=None, **props):
        self.blocks[(x, y, z)] = (name, tuple(sorted(props.items())), nbt)

    def box(self, x0, y0, z0, x1, y1, z1, name, **props):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    self.put(x, y, z, name, **props)

    def save(self, path):
        palette, index, blocks = [], {}, []
        for (x, y, z), (name, props, nbt) in sorted(self.blocks.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0])):
            key = (name, props)
            if key not in index:
                index[key] = len(palette)
                e = Compound({"id": String("minecraft:" + name)})
                if props:
                    e["properties"] = Compound({k: String(v) for k, v in props})
                palette.append(e)
            b = Compound({"pos": List[Int]([Int(x), Int(y), Int(z)]), "state": Int(index[key])})
            if nbt:
                b["nbt"] = Compound({k: String(v) for k, v in nbt.items()})
            blocks.append(b)
        root = Compound({
            "DataVersion": Int(DATA_VERSION),
            "size": List[Int]([Int(v) for v in self.size]),
            "palette": List[Compound](palette),
            "blocks": List[Compound](blocks),
            "entities": List[Compound]([]),
        })
        path.parent.mkdir(parents=True, exist_ok=True)
        nbtlib.File(root, gzipped=True).save(path)


def chest(t, x, y, z, facing="south"):
    t.put(x, y, z, "chest", nbt={"id": "minecraft:chest", "LootTable": LOOT}, facing=facing, type="single", waterlogged="false")


def shrine():
    """7x7 mossy floor, four broken corner pillars (one crowned with a froglight), chest on a glowing slab in the middle."""
    t = T(7, 6, 7)
    t.box(0, 0, 0, 6, 0, 6, "stone_bricks")
    for x, z in ((1, 1), (5, 5), (1, 5), (5, 1), (3, 0), (0, 3)):
        t.put(x, 0, z, "mossy_stone_bricks")
    t.put(3, 0, 3, "verdant_froglight", axis="y")
    for (x, z), h in {(0, 0): 4, (6, 0): 2, (0, 6): 3, (6, 6): 1}.items():
        t.box(x, 1, z, x, h, z, "stone_bricks")
        t.put(x, h, z, "chiseled_stone_bricks")
    t.put(0, 5, 0, "verdant_froglight", axis="y")
    t.put(0, 4, 6, "stone_brick_slab", type="bottom", waterlogged="false")
    chest(t, 3, 1, 3)
    for x, z in ((1, 3), (5, 3), (3, 5)):
        t.put(x, 1, z, "amethyst_cluster", facing="up", waterlogged="false")
    for x, z in ((2, 1), (4, 5), (1, 4), (5, 2)):
        t.put(x, 1, z, "moss_carpet")
    t.put(6, 1, 3, "stone_brick_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
    return t


def well():
    """Crystal well: calcite and basalt ring around an emerald pedestal with an amethyst cluster; glass lamps; chest."""
    t = T(5, 5, 5)
    t.box(0, 0, 0, 4, 0, 4, "smooth_basalt")
    t.box(1, 0, 1, 3, 0, 3, "calcite")
    t.put(2, 0, 2, "emerald_block")
    t.put(2, 1, 2, "amethyst_block")
    t.put(2, 2, 2, "amethyst_cluster", facing="up", waterlogged="false")
    for x, z in ((0, 0), (4, 4)):
        t.box(x, 1, z, x, 2, z, "lime_stained_glass")
        t.put(x, 3, z, "verdant_froglight", axis="y")
    for x, z in ((4, 0), (0, 4)):
        t.put(x, 1, z, "calcite")
        t.put(x, 2, z, "end_rod", facing="up")
    chest(t, 2, 1, 0, facing="south")
    t.put(1, 1, 2, "small_amethyst_bud", facing="up", waterlogged="false")
    t.put(3, 1, 2, "medium_amethyst_bud", facing="up", waterlogged="false")
    return t


def arch():
    """Fallen arch: two mossy legs and a broken lintel, a barrel and a lantern under it, rubble around."""
    t = T(7, 6, 3)
    for x in (0, 6):
        t.box(x, 0, 1, x, 4, 1, "mossy_stone_bricks")
    t.box(0, 5, 1, 3, 5, 1, "stone_bricks")
    t.put(4, 5, 1, "stone_brick_slab", type="bottom", waterlogged="false")
    t.put(1, 4, 1, "stone_brick_stairs", facing="east", half="top", shape="straight", waterlogged="false")
    t.box(1, 0, 0, 5, 0, 2, "mossy_cobblestone")
    t.put(3, 0, 1, "verdant_froglight", axis="y")
    t.put(3, 1, 1, "barrel", nbt={"id": "minecraft:barrel", "LootTable": LOOT}, facing="up", open="false")
    t.put(2, 1, 1, "lantern", hanging="false", waterlogged="false")
    t.put(5, 1, 0, "cobblestone_wall", east="none", north="none", south="none", west="none", up="true", waterlogged="false")
    t.put(4, 1, 2, "mossy_stone_bricks")
    t.put(1, 1, 2, "moss_carpet")
    return t


def build():
    for name, fn in (("shrine", shrine), ("well", well), ("arch", arch)):
        fn().save(OUT / f"ruin_{name}.nbt")
    print("dream ruins built:", ", ".join(p.name for p in sorted(OUT.glob("*.nbt"))))


if __name__ == "__main__":
    build()
