"""Light: emitter table, a block+sky light estimate (flood fill like the game's, without smooth-lighting subtleties),
an audit of walkable cells below a threshold, and an auto-light pass that adds style-appropriate fixtures.

    python -m tools.voxel light SCENE [--min 7] [--auto STYLE] [--render]

Block light: every emitter seeds its level; light spreads to the 6 neighbours losing 1 per step through cells that
don't block it (air, glass, plants, slabs/stairs... are treated as transparent unless they are full opaque cubes).
Sky light: 15 straight down every column until the first opaque or filtering block, then it spreads sideways like
block light (minus 1 per step). Walkable = an air-ish cell with a solid top face below and room for the head above."""
import functools, heapq

import numpy as np

from . import blockstate as bs

# ------------------------------------------------------------------ emitters (vanilla 26.x levels)
_FIXED = {
    "lantern": 15, "copper_lantern": 15, "exposed_copper_lantern": 15, "weathered_copper_lantern": 15,
    "oxidized_copper_lantern": 15, "soul_lantern": 10, "torch": 14, "wall_torch": 14, "soul_torch": 10,
    "soul_wall_torch": 10, "copper_torch": 14, "copper_wall_torch": 14, "redstone_torch": 7, "redstone_wall_torch": 7,
    "sea_lantern": 15, "glowstone": 15, "shroomlight": 15, "ochre_froglight": 15, "verdant_froglight": 15,
    "pearlescent_froglight": 15, "jack_o_lantern": 15, "end_rod": 14, "beacon": 15, "conduit": 15, "lava": 15,
    "fire": 15, "soul_fire": 10, "crying_obsidian": 10, "magma_block": 3, "glow_lichen": 7, "amethyst_cluster": 5,
    "large_amethyst_bud": 4, "medium_amethyst_bud": 2, "small_amethyst_bud": 1, "brewing_stand": 1,
    "enchanting_table": 7, "ender_chest": 7, "nether_portal": 11, "end_portal": 15, "end_gateway": 15,
    "dragon_egg": 1, "brown_mushroom": 1, "sculk_sensor": 1, "calibrated_sculk_sensor": 1, "sculk_catalyst": 6,
    "lava_cauldron": 15, "light": 15, "firefly_bush": 2, "creaking_heart": 0,
}
_LIT = {"campfire": 15, "soul_campfire": 10, "furnace": 13, "smoker": 13, "blast_furnace": 13, "redstone_lamp": 15,
        "redstone_ore": 9, "deepslate_redstone_ore": 9, "copper_bulb": 15, "exposed_copper_bulb": 12,
        "weathered_copper_bulb": 8, "oxidized_copper_bulb": 4, "candle_cake": 3}


@functools.lru_cache(None)
def emission(state):
    """Light level a block state emits (0..15)."""
    name, p = bs.parse(state)
    s = name.split(":")[-1].removeprefix("waxed_")
    if s.endswith("candle_cake"):
        return 3 if p.get("lit") == "true" else 0
    if s.endswith("candle"):
        return 3 * int(p.get("candles", "1")) if p.get("lit") == "true" else 0
    if s in _LIT:
        return _LIT[s] if p.get("lit", "true") == "true" else 0
    if s == "light":
        return int(p.get("level", "15"))
    if s == "sea_pickle":
        return 3 * (int(p.get("pickles", "1")) + 1) if p.get("waterlogged") == "true" else 0
    if s in ("cave_vines", "cave_vines_plant"):
        return 14 if p.get("berries") == "true" else 0
    if s == "respawn_anchor":
        return {0: 0, 1: 3, 2: 7, 3: 11, 4: 15}.get(int(p.get("charges", "0")), 0)
    return _FIXED.get(s, 0)


def is_fixture(state):
    """A designed light (lanterns, candles, torches, campfires, lamps...) as opposed to a glowing material."""
    s = bs.name_of(state).split(":")[-1]
    return emission(state) >= 3 and not s.endswith(("lava", "fire", "magma_block", "portal", "crying_obsidian"))
