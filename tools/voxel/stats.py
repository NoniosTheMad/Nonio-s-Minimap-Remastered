"""Quantitative floors (docs/voxel-playbook.md §5) measured on a scene, with the definitions of
docs/voxel-research-2.md §5. They catch emptiness; they do not prove beauty.

    python -m tools.voxel stats SCENE [--json F]

Definitions (research-2 §5):
  exposed    a solid block (not air, not liquid) with an air or water 6-neighbour
  facade     an exposed, non-natural block face with a horizontal air/water neighbour (1 face = 1 m²)
  break      a lateral neighbour of a facade face that does not continue the same plane (corner, recess, protrusion);
             break ratio = breaks / lateral links (4 per face)
  partial    any block whose model is not a full cube (stairs, slabs, walls, fences, trapdoors, panes, lanterns...)
  natural    stone, dirt, grass, tuff, deepslate, blackstone, sand, ores, leaves, plants... (excluded from facades)
Canvas metrics use a ground level G = 10th percentile of column top heights: a column is "built" when its top rises
2+ blocks above G (rock and landscape count, a flat lawn does not)."""
import functools, json

import numpy as np
from scipy import ndimage

from . import blockstate as bs
from .light import emission, is_fixture
from .models import bank

LIQUID = ("water", "lava", "bubble_column")
NATURAL = {
    "stone", "granite", "diorite", "andesite", "deepslate", "tuff", "calcite", "dirt", "grass_block", "coarse_dirt",
    "podzol", "rooted_dirt", "mud", "gravel", "sand", "red_sand", "clay", "blackstone", "basalt", "smooth_basalt",
    "netherrack", "moss_block", "pale_moss_block", "snow_block", "snow", "ice", "packed_ice", "blue_ice", "bedrock",
    "dripstone_block", "pointed_dripstone", "mycelium", "dirt_path", "farmland", "terracotta", "sandstone",
    "red_sandstone", "end_stone", "soul_sand", "soul_soil", "magma_block", "obsidian", "amethyst_block",
    "budding_amethyst", "short_grass", "tall_grass", "fern", "large_fern", "dead_bush", "bush", "seagrass",
    "tall_seagrass", "kelp", "kelp_plant", "sugar_cane", "vine", "glow_lichen", "moss_carpet", "hanging_roots",
    "sweet_berry_bush", "leaf_litter", "pink_petals", "wildflowers", "firefly_bush", "short_dry_grass",
    "tall_dry_grass", "cactus", "lily_pad", "mushroom_stem", "brown_mushroom_block", "red_mushroom_block",
}
FLOWERS = {"dandelion", "poppy", "blue_orchid", "allium", "azure_bluet", "red_tulip", "orange_tulip", "white_tulip",
           "pink_tulip", "oxeye_daisy", "cornflower", "lily_of_the_valley", "torchflower", "sunflower", "lilac",
           "rose_bush", "peony", "open_eyeblossom", "closed_eyeblossom", "cactus_flower"}

# ------------------------------------------------------------------ decoration categories (block name rules)
def category(name):
    s = name.split(":")[-1].removeprefix("waxed_")
    if s.endswith(("_trapdoor", "_fence", "_fence_gate", "_door", "_sign", "_button", "_hanging_sign")) or s == "ladder":
        return "joinery"
    if s in ("barrel", "chest", "trapped_chest", "ender_chest", "decorated_pot", "lectern", "bookshelf",
             "chiseled_bookshelf", "brewing_stand", "cauldron", "water_cauldron", "lava_cauldron",
             "powder_snow_cauldron", "crafting_table", "furnace", "smoker", "blast_furnace", "loom", "cartography_table",
             "fletching_table", "smithing_table", "stonecutter", "grindstone", "composter", "barrel", "flower_pot",
             "jukebox", "note_block", "crafter", "hopper", "dispenser", "dropper") \
            or s.endswith(("shulker_box", "_bed", "copper_chest")) or s.startswith("potted_"):
        return "containers"
    if s.endswith(("chain", "_bars", "lightning_rod")) or s in ("iron_bars", "bell", "anvil", "chipped_anvil",
                                                                 "damaged_anvil", "heavy_core"):
        return "metal"
    if s.endswith(("_head", "_skull")) and s != "piston_head":
        return "heads"
    return None


BE_PROPS = ("decorated_pot", "barrel", "chiseled_bookshelf", "banner", "sign", "bed", "lectern", "campfire",
            "brewing_stand")

FLOORS = [  # key, label, op, floor, group
    ("footprint", "Built footprint (share of canvas columns)", ">=", 0.60, "canvas"),
    ("height_ratio", "Landmark height / canvas width", ">=", 0.8, "canvas"),
    ("tiers", "Height tiers", ">=", 3, "canvas"),
    ("tier_ratio", "Tallest tier / second tier", ">=", 1.7, "canvas"),
    ("facade_breaks", "Facade plane breaks per 100 m²", ">=", 200, "facade"),
    ("facade_partial", "Facade partial-block share", ">=", 0.30, "facade"),
    ("facade_top5", "Facade top-5 states' share", "<=", 0.45, "facade"),
    ("facade_lights", "Lights within 2 of a facade per 100 m²", ">=", 1.2, "facade"),
    ("lights", "Light fixtures per 1,000 exposed", ">=", 10, "decoration"),
    ("joinery", "Joinery per 1,000 exposed", ">=", 9, "decoration"),
    ("containers", "Containers + furniture per 1,000 exposed", ">=", 6, "decoration"),
    ("metal", "Metal + rigging per 1,000 exposed", ">=", 3, "decoration"),
    ("heads", "Heads + skulls per 1,000 exposed", ">=", 0.25, "decoration"),
    ("props_per_8m2", "Block-entity props per 8 m² interior floor", ">=", 1.0, "decoration"),
]


def _short(n):
    return n.split(":")[-1]


@functools.lru_cache(None)
def _partial(state):
    name = bs.name_of(state)
    if name in ("minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"):
        return False
    return not bank().is_occluder(state)


def _natural(name):
    s = _short(name)
    return s in NATURAL or s in FLOWERS or s.endswith(("_ore", "_leaves", "_sapling", "_coral", "_coral_fan",
                                                        "_mushroom", "_propagule"))


def passable(state):
    """No collision box (people walk through): air, carpets, plates, torches, signs, banners, plants, rails..."""
    name, p = bs.parse(state)
    s = _short(name)
    if s in ("air", "cave_air", "void_air", "structure_void", "light", "redstone_wire", "tripwire", "lever",
             "short_grass", "tall_grass", "fern", "large_fern", "dead_bush", "bush", "vine", "glow_lichen",
             "cobweb", "sculk_vein", "leaf_litter", "pink_petals", "wildflowers", "firefly_bush", "hanging_roots",
             "short_dry_grass", "tall_dry_grass", "sugar_cane", "sweet_berry_bush", "nether_portal", "fire",
             "soul_fire", "tripwire_hook"):
        return True
    if s == "snow":
        return p.get("layers", "1") == "1"
    return s.endswith(("_carpet", "_pressure_plate", "torch", "_button", "_sign", "_banner", "rail", "_sapling",
                       "_mushroom", "_roots", "_fungus")) or s in FLOWERS or (s.endswith("_hanging_sign"))


def compute(scene):
    X, Y, Z = scene.shape
    pal = scene.palette
    names = [bs.name_of(p) for p in pal]
    idx = scene.idx
    is_air = np.array([_short(n) in ("air", "cave_air", "void_air", "structure_void") for n in names])
    is_liq = np.array([_short(n) in LIQUID for n in names])
    is_nat = np.array([_natural(n) for n in names])
    is_part = np.array([_partial(p) for p in pal])
    is_fix = np.array([is_fixture(p) for p in pal])
    cat = [category(n) for n in names]
    is_pass = np.array([passable(p) for p in pal])

    air = is_air[idx]
    liq = is_liq[idx]
    solid = ~air & ~liq
    airw = air | liq
    out = {"size": [X, Y, Z]}

    # ---------------------------------------------------------------- canvas
    anyb = solid.any(1)
    top = np.where(anyb, Y - 1 - np.argmax(solid[:, ::-1, :], axis=1), -1)
    G = float(np.percentile(top[anyb], 10)) if anyb.any() else 0.0
    h = np.where(anyb, top - G, 0)
    built = h >= 2
    out["ground"] = G
    out["footprint"] = float(built.mean())
    out["landmark_height"] = float(h.max())
    out["height_ratio"] = float(h.max() / max(X, Z))
    hb = h[built]
    out["height_p50_p90"] = [float(np.percentile(hb, 50)), float(np.percentile(hb, 90))] if len(hb) else [0, 0]
    # tiers: regional peaks (15x15 maxima at >= 25% of the landmark), grouped while within 25% of the group's top
    mx = ndimage.maximum_filter(h, size=15, mode="constant")
    lab, n = ndimage.label((h == mx) & (h >= max(4, 0.25 * h.max())))
    peaks = np.sort(ndimage.maximum(h, lab, range(1, n + 1)) if n else np.zeros(0))[::-1]
    tiers = []
    for v in peaks:
        if not tiers or v < 0.75 * tiers[-1][0]:
            tiers.append([v])
        else:
            tiers[-1].append(v)
    tops = [t[0] for t in tiers]
    out["tiers"] = len(tiers)
    out["tier_tops"] = [float(v) for v in tops[:6]]
    out["tier_ratio"] = float(tops[0] / tops[1]) if len(tops) > 1 and tops[1] > 0 else 0.0

    # ---------------------------------------------------------------- exposure
    def pad(a, v):
        return np.pad(a, 1, constant_values=v)
    S = pad(solid, False)
    A = pad(airw, True)
    exposed = solid & (A[2:, 1:-1, 1:-1] | A[:-2, 1:-1, 1:-1] | A[1:-1, 2:, 1:-1] | A[1:-1, :-2, 1:-1] |
                       A[1:-1, 1:-1, 2:] | A[1:-1, 1:-1, :-2])
    n_exp = int(exposed.sum())
    out["blocks"] = int(solid.sum())
    out["exposed"] = n_exp

    # ---------------------------------------------------------------- facades
    fac_mat = solid & ~is_nat[idx]
    F = pad(fac_mat, False)
    face_states = []
    faces = breaks = 0
    facade_block = np.zeros(scene.shape, bool)
    sl = lambda dx, dy, dz: (slice(1 + dx, 1 + dx + X), slice(1 + dy, 1 + dy + Y), slice(1 + dz, 1 + dz + Z))
    for d in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)):
        f = fac_mat & A[sl(*d)]
        nf = int(f.sum())
        if not nf:
            continue
        faces += nf
        facade_block |= f
        face_states.append(idx[f])
        lat = [(0, 1, 0), (0, -1, 0)] + ([(0, 0, 1), (0, 0, -1)] if d[0] else [(1, 0, 0), (-1, 0, 0)])
        for t in lat:
            cont = S[sl(*t)] & A[sl(t[0] + d[0], t[1] + d[1], t[2] + d[2])]
            breaks += int((f & ~cont).sum())
    out["facade_area"] = faces
    if faces:
        fs = np.concatenate(face_states)
        out["facade_breaks"] = 100.0 * breaks / faces
        out["facade_break_ratio"] = breaks / (4.0 * faces)
        out["facade_partial"] = float(is_part[fs].mean())
        cnt = np.bincount(fs, minlength=len(pal))
        top5 = np.argsort(cnt)[::-1][:5]
        out["facade_top5"] = float(cnt[top5].sum() / faces)
        out["facade_top5_states"] = [(_short(pal[i]) if "[" not in pal[i] else _short(names[i]) + "[..]",
                                      round(cnt[i] / faces, 3)) for i in top5 if cnt[i]]
        near = ndimage.binary_dilation(facade_block, structure=np.ones((5, 5, 5), bool))
        out["facade_lights"] = 100.0 * float((is_fix[idx] & near).sum()) / faces
    else:
        out.update(facade_breaks=0.0, facade_break_ratio=0.0, facade_partial=0.0, facade_top5=1.0,
                   facade_top5_states=[], facade_lights=0.0)

    # ---------------------------------------------------------------- decoration
    per = 1000.0 / max(n_exp, 1)
    counts = np.bincount(idx.ravel(), minlength=len(pal))
    out["lights"] = float(sum(counts[i] for i in range(len(pal)) if is_fix[i])) * per
    for c in ("joinery", "containers", "metal", "heads"):
        out[c] = float(sum(counts[i] for i in range(len(pal)) if cat[i] == c)) * per
    out["emitting_blocks"] = int(sum(counts[i] for i in range(len(pal)) if emission(pal[i]) > 0))

    # block entities + entities
    from .nbt import be_id
    be = {}
    for i, n in enumerate(names):
        if counts[i]:
            b = be_id(n)
            if b:
                if _short(n).endswith("_bed") and bs.parse(pal[i])[1].get("part") == "foot":
                    continue
                be[_short(b)] = be.get(_short(b), 0) + int(counts[i])
    out["block_entities"] = dict(sorted(be.items(), key=lambda kv: -kv[1]))
    ents = {}
    for e in scene.entities:
        k = _short(str(e["nbt"].get("id", "?")))
        ents[k] = ents.get(k, 0) + 1
    out["entities"] = ents
    props = sum(v for k, v in be.items() if k in BE_PROPS)
    out["be_props"] = props
    out["be_prop_types"] = sum(1 for k in be if k in BE_PROPS)

    # interior floor: walkable cells (passable, passable above, solid non-passable below) with a roof within 24
    pas = is_pass[idx]
    walk = np.zeros(scene.shape, bool)
    walk[:, 1:-1, :] = pas[:, 1:-1, :] & pas[:, 2:, :] & solid[:, :-2, :] & ~pas[:, :-2, :]
    roof = np.zeros(scene.shape, bool)
    run = np.zeros((X, Z), int)
    for y in range(Y - 1, -1, -1):  # distance to the nearest solid above
        roof[:, y, :] = run > 0
        run = np.where(solid[:, y, :] & ~pas[:, y, :], 24, np.maximum(run - 1, 0))
    interior = walk & roof
    out["interior_floor"] = int(interior.sum())
    out["props_per_8m2"] = props / (out["interior_floor"] / 8.0) if out["interior_floor"] else 0.0
    from .stability import analyze
    out["stability"] = analyze(scene)
    return out


def table(m):
    """[(group, label, value, op, floor, ok)]"""
    rows = []
    for key, label, op, floor, group in FLOORS:
        v = m.get(key, 0.0)
        ok = v >= floor if op == ">=" else v <= floor
        rows.append((group, label, v, op, floor, ok))
    return rows


def report(m, name=""):
    L = [f"stats {name} {m['size'][0]}x{m['size'][1]}x{m['size'][2]}: {m['blocks']:,} blocks, {m['exposed']:,} exposed, "
         f"facade {m['facade_area']:,} m², interior floor {m['interior_floor']:,} m², ground y={m['ground']:.0f}"]
    L.append(f"  {'metric':<46} {'value':>9}   floor     ")
    g0 = None
    rows = table(m)
    for group, label, v, op, floor, ok in rows:
        if group != g0:
            L.append(f"  [{group}]"); g0 = group
        fv = f"{v:.2f}" if isinstance(v, float) and abs(v) < 100 else f"{v:,.0f}" if isinstance(v, float) else str(v)
        L.append(f"  {label:<46} {fv:>9}   {op} {floor:<6} {'PASS' if ok else 'FAIL'}")
    if "stability" in m:
        from .stability import format_line
        L.append(format_line(m["stability"]))
    n_ok = sum(r[-1] for r in rows)
    L.append(f"  {n_ok}/{len(rows)} floors met. Not measured here (judge by eye): distinct sub-places (4-6), "
             f"named elements (>= 25), depth planes (>= 4), props types per room (>= 5).")
    L.append(f"  height above ground p50/p90/max {m['height_p50_p90'][0]:.0f}/{m['height_p50_p90'][1]:.0f}/"
             f"{m['landmark_height']:.0f}; tier tops {m['tier_tops']}; break ratio {m['facade_break_ratio']:.2f}")
    L.append("  facade top-5: " + ", ".join(f"{n} {v:.0%}" for n, v in m["facade_top5_states"]))
    be = m["block_entities"]
    L.append(f"  block entities ({sum(be.values()):,}): " + (", ".join(f"{k} {v}" for k, v in be.items()) or "none"))
    L.append(f"  entities ({sum(m['entities'].values())}): " + (", ".join(f"{k} {v}" for k, v in m["entities"].items()) or "none"))
    L.append(f"  block-entity props {m['be_props']} of {m['be_prop_types']} types; emitting blocks {m['emitting_blocks']:,}")
    return "\n".join(L)


def to_json(m):
    return json.dumps({**m, "floors": [dict(zip(("group", "label", "value", "op", "floor", "ok"), r)) for r in table(m)]},
                      indent=1, default=float)
