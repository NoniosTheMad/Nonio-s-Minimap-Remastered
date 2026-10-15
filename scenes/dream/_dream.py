"""Shared kit for Emerald Dream exploration sites (scenes/dream/*.py -> datapack structure templates).

CONTRACT (tools/build_dream.py reads it; break it and the site won't spawn right)
  build() -> Scene, then `return finish(s, tier=..., kind=..., anchor=(x, y, z))` as the last line.
  tier   "minor" (<= 17 x 17 footprint), "major" (<= 41 x 41), "grand" (<= 64 x 64). Height <= 96.
  kind   "ground": stands on an island. anchor = the scene cell that lands on the FIRST AIR BLOCK above the terrain at
                   the site centre (so anchor y-1 is the ground the site sits on). Build a foundation skirt down to
                   anchor_y - 8 (skirt() helps) so it never floats over uneven ground.
         "sky":    hangs in open air (y 130..200, checked empty at runtime). anchor = the scene centre-ish cell that goes
                   to the chosen sky point. It must carry its own island/rock (island() helps).
  Plain air       = "leave the world alone" (not written).  cave_air = carve (interiors, doors, headroom).
                    finish() auto-carves ground sites: every column that has built blocks at/above anchor_y is cleared
                    from anchor_y up to its highest built block, so terrain bumps never poke through floors.
  Loot            loot_chest() only (chest + marker). Never hand-write LootTable. Grand: vault() (Dream Key, per-player).
  Beacon          majors and the grand get one beacon() (verdant froglight base, lime glass): the far-read beam that
                   switches off once the site's loot chest has been opened. Its column above must be open sky.
  Deposits        deposit(s, x, y, z) = a regrowing ore vein (the Dream's mining lives at sites; user #80): the block at
                   (x, y, z) becomes ore at runtime, regrows ~30 s after being mined and sometimes spreads into an
                   adjacent stone/calcite/dirt block. Put them where a player can stand and mine (exposed faces, a
                   seam in a wall, a crystal bed). minor 2-4, major 5-8, grand 8-12. Host block must be solid stone-like.
  Forbidden       paid ores / emerald blocks (they pay coins when mined in the Dream): emerald_block, *_ore,
                   raw_*_block, gold_block, diamond_block, lapis_block, redstone_block. Also: spawners, creaking_heart,
                   unwaxed copper (oxidises), non-persistent leaves (finish() fixes leaves), sand/gravel overhangs.
  Render          python -m tools.voxel render scenes/dream/<name>.py --mood dream   (sheet: .mcdev/voxel/out/<name>/sheet.png)

ART DIRECTION: "wonderland". Pale dream-stone (calcite / diorite / quartz) as the primary mass, verdigris (waxed oxidised
copper) as the secondary, emerald-green glow (verdant froglight, sea lantern, prismarine, lime glass) and amethyst as the
feature, warm gold (ochre froglight, lanterns, gold-ish wood) as the contrast. Oversized flora, gentle impossible
geometry (hovering stones, upside-down things, rings), soft glow. The dimension itself is floating grass/moss islands with
calcite and amethyst undersides over a green void with fog from 24 to 176 blocks, fixed light.
"""
import numpy as np

from tools.voxel import nbt, shapes
from tools.voxel.palette import Gradient, Mix, Noise

TIERS = {"minor": 17, "major": 41, "grand": 64, "nightmare": 64}
MAX_H = 96

# ------------------------------------------------------------------ palette roles
DREAMSTONE = Mix({"calcite": 5, "diorite": 2, "polished_diorite": 1, "smooth_quartz": 1})
DREAM_BRICK = Mix({"quartz_bricks": 3, "calcite": 1, "polished_diorite": 1})
DREAM_TRIM = "smooth_quartz"
VERDIGRIS = Mix({"waxed_oxidized_cut_copper": 3, "waxed_oxidized_copper": 1, "waxed_weathered_cut_copper": 0.4})
VERDIGRIS_SOLID = "waxed_oxidized_copper"
GLOW_GREEN = "verdant_froglight"
GLOW_SEA = "sea_lantern"
GLOW_WARM = "ochre_froglight"
GLOW_PEARL = "pearlescent_froglight"
PRISM = Mix({"prismarine": 2, "prismarine_bricks": 2, "dark_prismarine": 1})
AMETHYST = "amethyst_block"
# terrain-matching materials (the dimension's own surface rules)
TURF = Noise([(-0.2, "moss_block"), (1, "grass_block")], scale=6)
SOIL = Mix({"dirt": 4, "coarse_dirt": 1, "rooted_dirt": 1})
ROCK = Mix({"stone": 4, "calcite": 3, "andesite": 1})
UNDERSIDE = Mix({"calcite": 4, "stone": 2, "amethyst_block": 1})

FORBIDDEN_SUBSTR = ("_ore", "emerald_block", "raw_iron_block", "raw_gold_block", "raw_copper_block", "gold_block",
                    "diamond_block", "lapis_block", "redstone_block", "spawner", "creaking_heart", "trial_spawner")

# The Dream Key (grand vaults). Must match the item the loot tables give EXACTLY (vaults compare all components).
DREAM_KEY_COMPONENTS = {
    "minecraft:custom_data": "{nx_dkey:1b}",
    "minecraft:item_model": '"minecraft:ominous_trial_key"',
    "minecraft:item_name": "{text:'Dream Key',color:'#7dffc8'}",
    "minecraft:rarity": '"rare"',
}


# ------------------------------------------------------------------ markers / special blocks
def marker(s, pos, tag):
    """Marker entity (stays in the template) - the datapack finds sites by these tags."""
    s.entity({"id": "minecraft:marker", "Tags": ["nx.dream", tag]}, (pos[0] + 0.5, pos[1] + 0.5, pos[2] + 0.5))


def loot_chest(s, x, y, z, tier, facing="north", block="chest"):
    """The site's loot. tier: minor | major | key (small key cache) . block: chest | barrel."""
    st = f"{block}[facing={facing}]"
    s.set(x, y, z, st, nbt=nbt.container([], loot_table=f"nonios:dream/{tier}"))
    marker(s, (x, y, z), "nx.dream_loot")


def vault(s, x, y, z, facing="north"):
    """Grand site's vault: opens once per player with a Dream Key."""
    comps = "{" + ",".join(f'"{k}":{v}' for k, v in DREAM_KEY_COMPONENTS.items()) + "}"
    cfg = ("{config:{key_item:{id:\"minecraft:trial_key\",count:1,components:" + comps + "},"
           "loot_table:\"nonios:dream/grand\",activation_range:5.0d,deactivation_range:6.0d}}")
    s.set(x, y, z, f"vault[facing={facing},ominous=false,vault_state=inactive]", nbt=cfg)
    marker(s, (x, y, z), "nx.dream_vault")


def beacon(s, x, y, z, glass="lime_stained_glass", base=GLOW_GREEN):
    """Beacon at (x, y, z) on a 3x3 base (y-1) of `base` (tagged as beacon base in the datapack) + tinting glass above.
    Everything above (x, y+2.., z) must stay open to the sky."""
    s.box((x - 1, y - 1, z - 1), (x + 1, y - 1, z + 1), base)
    s.set(x, y, z, "beacon")
    s.set(x, y + 1, z, glass)
    marker(s, (x, y, z), "nx.dream_beam")


def deposit(s, x, y, z, host="calcite"):
    """Regrowing ore vein seed: `host` now (rendered), ore at runtime (marker sits in the cell above the ore)."""
    s.set(x, y, z, host)
    marker(s, (x, y + 1, z), "nx.dream_vseed")


def guard(s, x, y, z, mob):
    """Nightmare site only: a guard spawn point. mob = warden | vindicator | evoker | wither_skeleton | breeze | ravager."""
    marker(s, (x, y, z), "nx.dream_guard_" + mob)


def exodia_altar(s, x, y, z):
    """Nightmare site only: the claim altar (the datapack adds the clickable part). Block at (x, y, z) is the plinth top."""
    s.set(x, y, z, "lodestone")
    marker(s, (x, y + 1, z), "nx.dream_exodia")


# ------------------------------------------------------------------ shapes
def island(s, cx, top_y, cz, r, depth, seed=0, turf=True):
    """Floating island: grass/moss top at top_y, dirt, rock, a calcite/amethyst taproot cone `depth` deep."""
    gx, gz = np.meshgrid(np.arange(s.shape[0]), np.arange(s.shape[2]), indexing="ij")
    rng = np.random.default_rng(seed)
    ang = np.arctan2(gz - cz, gx - cx)
    wob = 1 + 0.12 * np.sin(3 * ang + rng.uniform(0, 6)) + 0.08 * np.sin(5 * ang + rng.uniform(0, 6))
    d = np.hypot(gx - cx, gz - cz) / (r * wob)
    inside = d < 1
    bottom = top_y - depth * np.clip(1 - d, 0, 1) ** 0.7 - 1
    ys = np.arange(s.shape[1])[None, :, None]
    m = inside[:, None, :] & (ys <= top_y) & (ys >= bottom[:, None, :])
    s.fill(m, Gradient("y", [(top_y - 6, UNDERSIDE), (top_y - 2, ROCK), (top_y - 1, SOIL), (999, TURF if turf else SOIL)],
                       jitter=1.5, jitter_scale=4, seed=seed))
    return m


def skirt(s, footprint, anchor_y, depth=8, seed=0):
    """Ground sites: tapering earth/rock foundation under a 2D bool footprint (x, z), anchor_y-1 down to anchor_y-depth."""
    from scipy.ndimage import binary_erosion
    fp = footprint.copy()
    for k in range(depth):
        y = anchor_y - 1 - k
        if y < 0 or not fp.any():
            break
        m = np.zeros(s.shape, bool)
        m[:, y, :] = fp
        s.fill(m, ROCK if k > 1 else SOIL, replace="air")
        if k % 2 == 1:
            fp = binary_erosion(fp)


# ------------------------------------------------------------------ finish
def finish(s, tier, kind, anchor, lint=True):
    assert tier in TIERS and kind in ("ground", "sky")
    W, H, D = s.shape
    lim = TIERS[tier]
    if lint:
        assert W <= lim and D <= lim, f"{tier} footprint {W}x{D} > {lim}"
        assert H <= MAX_H, f"height {H} > {MAX_H}"
        bad = [n for n in s.names() if any(b in n for b in FORBIDDEN_SUBSTR)]
        assert not bad, f"forbidden blocks: {bad}"
    _persist_leaves(s)   # leaves never decay
    if kind == "ground":
        ay = int(anchor[1])
        air = s.idx == 0
        built = ~air
        built[:, :ay, :] = False
        has = built.any(axis=1)
        top = np.where(has, H - 1 - np.argmax(built[:, ::-1, :], axis=1), -1)
        ys = np.arange(H)[None, :, None]
        carve = air & (ys >= ay) & (ys <= top[:, None, :])
        s.fill(carve, "cave_air")
    else:
        # sky sites are placed into a sky full of islands: carve whatever island sits inside the site's own
        # silhouette (per column, between its lowest and highest block), so no stone fills a room
        air = s.idx == 0
        built = ~air
        has = built.any(axis=1)
        bot = np.where(has, np.argmax(built, axis=1), H)
        top = np.where(has, H - 1 - np.argmax(built[:, ::-1, :], axis=1), -1)
        ys = np.arange(H)[None, :, None]
        carve = air & (ys >= bot[:, None, :]) & (ys <= top[:, None, :])
        s.fill(carve, "cave_air")
    tags = [e["nbt"]["Tags"] for e in s.entities if "Tags" in e["nbt"]]
    n_loot = sum("nx.dream_loot" in [str(t) for t in tg] for tg in tags)
    n_vault = sum("nx.dream_vault" in [str(t) for t in tg] for tg in tags)
    n_beam = sum("nx.dream_beam" in [str(t) for t in tg] for tg in tags)
    if lint:
        n_seed = sum("nx.dream_vseed" in [str(t) for t in tg] for tg in tags)
        assert n_seed >= 2, "add deposit() veins (minor 2-4, major 5-8, grand 8-12)"
        if tier == "nightmare":
            assert n_beam == 1, "nightmare: one beacon (red glass)"
        elif tier == "grand":
            assert n_vault >= 1 and n_beam == 1, "grand: vault(s) + exactly one beacon"
        elif tier == "major":
            assert n_loot == 1 and n_beam == 1, "major: exactly one loot_chest + one beacon"
        else:
            assert n_loot == 1 and n_beam == 0, "minor: exactly one loot_chest, no beacon"
    s.meta["dream"] = {"tier": tier, "kind": kind, "anchor": [int(v) for v in anchor]}
    s.meta.setdefault("mood", "dream")
    return s


def _persist_leaves(s):
    for i, st in enumerate(list(s.palette)):
        if "_leaves" in st:
            if "persistent=" in st:
                new = st.replace("persistent=false", "persistent=true")
            else:
                new = st.replace("]", ",persistent=true]") if "[" in st else st + "[persistent=true]"
            if new != st:
                s.idx[s.idx == i] = s.id(new)
