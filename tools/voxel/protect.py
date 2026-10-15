"""Protected builds: the placed scene can't be broken or changed, players can still build and break their own blocks.

    python -m tools.voxel protect SCENE [--at X Y Z] [--install SERVER [--setup]]

Generates a vanilla datapack (functions only, no command blocks) for one placed scene; several scenes can share the pack
(`--install` merges into <world>/datapacks/voxel_protect, one folder per scene id). Generalises arena v3's backup +
`clone masked` (#43) from one box to any size:

* Backup C: a copy of the build taken in game by `<ns>:<id>/setup` (run it once, on the pristine build), split in 16^3
  tiles (one chunk section each; `execute if blocks` and clone are capped at 32768 blocks). Cells that may legitimately
  change are cleared to air in C (`fill ... air replace #<ns>:<id>/free strict`), so `masked` ignores them:
    - FREE (never protected): air, fluids, fire, replaceable plants and snow layers (a player placing a block there
      replaces them; restoring them would delete the player's block).
    - LOOSE (protected by block id only): doors, trapdoors, gates, buttons, containers, beds, candles, crops... blocks
      players may use without gaining an item. Each loose group (door halves, bed, double chest) is copied once into
      a small store S; a tile check `execute unless block <pos> <id>` clones it back. Containers come back EMPTY
      (their contents drop when broken; the loot is handed out once, never twice).
    - LOCK (exact, untouchable): blocks whose interaction hands out an item (flower pots, chiseled bookshelves,
      lecterns, jukeboxes, campfires, composters, cauldrons, suspicious sand/gravel, beehives, decorated pots, berry
      bushes and vines, pumpkins, rooted dirt, cakes). Kept in C like solid blocks, and each is covered by an invisible
      `interaction` entity (tag vp.<id>) that swallows use and attack.
  Air cells of the build are air in C too: everything players place there stays.
* Detection, three paths, all in one tick function:
    1. a player whose `minecraft.mined:<id>` score rose (one objective per protected block id) -> tiles within reach;
    2. a new item entity in the box (explosions, anything that drops) -> its tile;
    3. a sweep: every tile with protected cells is compared once per `sweep` ticks (fire, pistons, creative, axes, hoes).
  A mismatch clones the tile's backup over it (`clone C tile masked`, ~4096 blocks) and kills the item entities first
  seen this tick in that tile (the drops of what was just broken).
* Entities in the box (armour stands, item frames, paintings) get Invulnerable / Fixed / DisabledSlots at setup.

Functions (namespace default `vprot`, id = scene name): setup, on, off, status. Storage: none; scoreboard `vp.<id>`
(#on, #c sweep cursor, #restores, #fixes)."""
import json, math, shutil
from pathlib import Path

import numpy as np

from . import blockstate as bs

FREE_IDS = {
    "air", "cave_air", "void_air", "structure_void", "light", "water", "lava", "bubble_column", "fire", "soul_fire",
    "short_grass", "tall_grass", "fern", "large_fern", "dead_bush", "bush", "short_dry_grass", "tall_dry_grass",
    "vine", "glow_lichen", "snow", "seagrass", "tall_seagrass", "kelp", "kelp_plant", "crimson_roots", "warped_roots",
    "nether_sprouts", "hanging_roots", "leaf_litter", "resin_clump", "sculk_vein", "cobweb", "powder_snow",
    "pale_hanging_moss", "firefly_bush",
}
LOOSE_PARTS = (
    "door", "trapdoor", "fence_gate", "button", "lever", "pressure_plate", "chest", "barrel", "shulker_box", "hopper",
    "dispenser", "dropper", "furnace", "smoker", "brewing_stand", "lectern", "jukebox", "note_block", "candle",
    "campfire", "cake", "_bed", "repeater", "comparator", "redstone_wire", "redstone_lamp", "redstone_torch",
    "daylight_detector", "decorated_pot", "chiseled_bookshelf", "crafter", "composter", "cauldron", "respawn_anchor",
    "flower_pot", "potted_", "farmland", "wheat", "carrots", "potatoes", "beetroots", "sweet_berry_bush", "cave_vines",
    "copper", "bell", "tripwire", "target", "observer", "piston", "rail", "beehive", "bee_nest", "suspicious_",
    "turtle_egg", "sniffer_egg", "frogspawn", "scaffolding", "sculk_sensor", "sculk_shrieker", "vault", "trial_spawner",
    "creaking_heart", "dried_ghast", "end_portal_frame", "pumpkin_stem", "melon_stem", "cocoa", "nether_wart",
    "sugar_cane", "bamboo", "cactus", "chorus_flower", "pitcher_crop", "torchflower_crop", "big_dripleaf", "small_dripleaf",
)
# LOCK: an interaction would hand the player an item (pot plant, shelf/lectern book, disc, cauldron fluid, bone meal,
# brushing loot, honey/honeycomb, berries, pumpkin seeds, hanging roots, cake slices). Protected exactly (state + NBT)
# AND covered by an invisible `interaction` entity, which swallows both use and attack: the block can't be touched.
LOCK_PARTS = (
    "flower_pot", "potted_", "chiseled_bookshelf", "lectern", "jukebox", "campfire", "composter", "cauldron",
    "suspicious_sand", "suspicious_gravel", "beehive", "bee_nest", "decorated_pot", "sweet_berry_bush", "cave_vines",
    "rooted_dirt", "cake", "end_portal_frame", "respawn_anchor",
)
LOCK_EXACT = {"pumpkin"}
# containers among LOOSE: restored EMPTY (the store copy keeps the original loot, but handing it out again would dupe);
# their contents drop normally when broken, only the container's own item drop is removed.
CONTAINERS = ("chest", "barrel", "shulker_box", "hopper", "dispenser", "dropper", "furnace", "smoker", "brewing_stand",
              "crafter")
TILE = 16


def category(state, free=(), loose=()):
    """'free' | 'loose' | 'solid' (protected exactly)."""
    name = bs.name_of(state).split(":", 1)[1]
    if name in FREE_IDS or any(p in name for p in free):
        return "free"
    if name in LOCK_EXACT or any(p in name for p in LOCK_PARTS):
        return "lock"
    if name.startswith("waxed_") and "copper" in name and not any(p in name for p in ("door", "trapdoor", "bulb", "chest", "golem")):
        return "solid"     # waxed copper never oxidises
    if any(p in name for p in LOOSE_PARTS) or any(p in name for p in loose):
        return "loose"
    return "solid"


def _groups(scene, loose_mask):
    """Union loose cells that form one block: door/plant halves (half=lower/upper), bed parts, double chests."""
    cells = [tuple(int(v) for v in c) for c in np.argwhere(loose_mask)]
    idset = set(cells)
    parent = {c: c for c in cells}

    def find(c):
        while parent[c] != c:
            parent[c] = parent[parent[c]]
            c = parent[c]
        return c

    for c in cells:
        name, p = bs.parse(scene.palette[scene.idx[c]])
        nbrs = []
        if p.get("half") in ("lower", "upper"):
            nbrs = [(0, 1, 0)]
        elif p.get("part") in ("head", "foot") or p.get("type") in ("left", "right"):
            nbrs = [(1, 0, 0), (0, 0, 1)]
        for d in nbrs:
            o = (c[0] + d[0], c[1] + d[1], c[2] + d[2])
            if o in idset and bs.name_of(scene.palette[scene.idx[o]]) == name:
                parent[find(o)] = find(c)
    g = {}
    for c in cells:
        g.setdefault(find(c), []).append(c)
    out = []
    for cs in g.values():
        a = np.array(cs)
        out.append((tuple(int(v) for v in a.min(0)), tuple(int(v) for v in a.max(0)), cs))
    return out


def plan(scene, at, backup=None, store=None, free=(), loose=()):
    X, Y, Z = scene.shape
    at = [int(v) for v in at]
    cats = np.array([category(s, free, loose) for s in scene.palette])
    cat = cats[scene.idx]
    loose_mask = cat == "loose"
    prot_mask = cat != "free"
    if backup is None:
        backup = [at[0], -64, at[2]] if at[1] - (-64) >= Y else [at[0] + X + 32, at[1], at[2]]
    backup = [int(v) for v in backup]
    groups = _groups(scene, loose_mask)
    # store S: shelf-pack the groups (1-block gaps) in rows <= 64 wide, beside the backup's footprint
    if store is None:
        store = [backup[0] + X + 8, backup[1], backup[2]]
    store = [int(v) for v in store]
    slots, sx, sz, row_d = [], 0, 0, 0
    for g0, g1, _ in groups:
        w, d = g1[0] - g0[0] + 1, g1[2] - g0[2] + 1
        if sx + w > 64:
            sx, sz, row_d = 0, sz + row_d + 1, 0
        slots.append((store[0] + sx, store[1], store[2] + sz))
        sx += w + 1
        row_d = max(row_d, d)
    store_size = (64, max([g1[1] - g0[1] + 1 for g0, g1, _ in groups] or [1]), sz + row_d + 1)
    tiles = []
    for tx in range(0, X, TILE):
        for ty in range(0, Y, TILE):
            for tz in range(0, Z, TILE):
                sl = (slice(tx, min(tx + TILE, X)), slice(ty, min(ty + TILE, Y)), slice(tz, min(tz + TILE, Z)))
                if prot_mask[sl].any():
                    tiles.append(((tx, ty, tz), (sl[0].stop - 1, sl[1].stop - 1, sl[2].stop - 1)))
    from .stability import analyze
    stab = analyze(scene)
    locks = [tuple(int(v) for v in c) for c in np.argwhere(cat == "lock")]
    ids = sorted({bs.name_of(s) for s, c in zip(scene.palette, cats) if c != "free"})
    free_ids = sorted({bs.name_of(s) for s, c in zip(scene.palette, cats) if c in ("free", "loose")} - {"minecraft:air"})
    return {"at": at, "size": [X, Y, Z], "backup": backup, "store": store, "store_size": list(store_size),
            "groups": groups, "slots": slots, "tiles": tiles, "mined_ids": ids, "clear_ids": free_ids, "locks": locks, "stability": stab,
            "counts": {"protected": int((cat == "solid").sum()), "loose": int(loose_mask.sum()),
                       "locked": len(locks),
                       "free_nonair": int(((cat == "free") & (scene.idx != 0)).sum()),
                       "unstable_soil": stab["unstable_soil"], "spreading": sum(stab["spreading"].values())}}


def write_pack(scene, pl, root, ns="vprot", ident=None, sweep=40):
    """Write <root>/data/<ns>/function/<id>/... and the tags; refresh pack.mcmeta and the tick/load tags."""
    ident = ident or scene.name.lower().replace("-", "_")
    root = Path(root)
    fdir = root / "data" / ns / "function" / ident
    if fdir.exists():
        shutil.rmtree(fdir)
    (fdir / "t").mkdir(parents=True)
    (fdir / "r").mkdir()
    (fdir / "s").mkdir()
    F = f"{ns}:{ident}"
    O = f"vp.{ident}"
    seen, new = f"vp.{ident}.seen", f"vp.{ident}.new"
    ax, ay, az = pl["at"]
    bx, by, bz = pl["backup"]
    X, Y, Z = pl["size"]

    def W(path, lines):
        p = fdir / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def box(x0, y0, z0, x1, y1, z1, r):
        return f"x={x0 - r},y={y0 - r},z={z0 - r},dx={x1 - x0 + 2 * r},dy={y1 - y0 + 2 * r},dz={z1 - z0 + 2 * r}"

    region = box(ax, ay, az, ax + X - 1, ay + Y - 1, az + Z - 1, 8)
    tag = f"{ns}:{ident}/free"
    tdir = root / "data" / ns / "tags" / "block" / ident
    tdir.mkdir(parents=True, exist_ok=True)
    (tdir / "free.json").write_text(json.dumps({"values": pl["clear_ids"]}, indent=1), encoding="utf-8")

    # loose checks per tile (a group cell in tile t)
    loose_by_tile = {}
    for gi, ((g0, g1, cells), slot) in enumerate(zip(pl["groups"], pl["slots"])):
        dx, dy, dz = (g1[i] - g0[i] for i in range(3))
        arg = (f"{{a:{slot[0]},b:{slot[1]},c:{slot[2]},d:{slot[0] + dx},e:{slot[1] + dy},f:{slot[2] + dz},"
               f"x:{ax + g0[0]},y:{ay + g0[1]},z:{az + g0[2]}}}")
        for c in cells:
            t = (c[0] // TILE * TILE, c[1] // TILE * TILE, c[2] // TILE * TILE)
            nm = bs.name_of(scene.palette[scene.idx[c]])
            if any(k in nm for k in CONTAINERS):
                # only the broken cell (the other half of a double chest keeps its current contents)
                o = (slot[0] + c[0] - g0[0], slot[1] + c[1] - g0[1], slot[2] + c[2] - g0[2])
                carg = f"{{a:{o[0]},b:{o[1]},c:{o[2]},x:{ax + c[0]},y:{ay + c[1]},z:{az + c[2]},i:\"{nm}\"}}"
                line = f"execute unless block {ax + c[0]} {ay + c[1]} {az + c[2]} {nm} run function {F}/fixc {carg}"
            else:
                line = f"execute unless block {ax + c[0]} {ay + c[1]} {az + c[2]} {nm} run function {F}/fix {arg}"
            loose_by_tile.setdefault(t, []).append(line)
    tiles = list(pl["tiles"])
    tile_set = {t0 for t0, _ in tiles}
    for t in loose_by_tile:            # a loose-only tile still needs its checks
        if t not in tile_set:
            t1 = tuple(min(t[i] + TILE, pl["size"][i]) - 1 for i in range(3))
            tiles.append((t, t1)); tile_set.add(t)

    setup = [f"# {scene.name}: take the backup from the build as it is NOW (run once, on the pristine build).",
             f"scoreboard objectives add {O} dummy", f"scoreboard players set #on {O} 0",
             f"function {F}/init"]
    # forceload: build, backup, store (rectangles of <= 16x16 chunks)
    def fl(x0, z0, x1, z1):
        out = []
        for a in range(x0, x1 + 1, 256):
            for b in range(z0, z1 + 1, 256):
                out.append(f"forceload add {a} {b} {min(a + 255, x1)} {min(b + 255, z1)}")
        return out
    setup += fl(ax, az, ax + X - 1, az + Z - 1) + fl(bx, bz, bx + X - 1, bz + Z - 1)
    sx, sy, sz = pl["store"]; sw, sh, sd = pl["store_size"]
    if pl["groups"]:
        setup += fl(sx, sz, sx + sw - 1, sz + sd - 1)
    near_p, near_i = [], []
    for n, (t0, t1) in enumerate(tiles):
        w0 = (ax + t0[0], ay + t0[1], az + t0[2]); w1 = (ax + t1[0], ay + t1[1], az + t1[2])
        c0 = (bx + t0[0], by + t0[1], bz + t0[2]); c1 = (bx + t1[0], by + t1[1], bz + t1[2])
        setup.append(f"clone {w0[0]} {w0[1]} {w0[2]} {w1[0]} {w1[1]} {w1[2]} {c0[0]} {c0[1]} {c0[2]} strict replace")
        setup.append(f"fill {c0[0]} {c0[1]} {c0[2]} {c1[0]} {c1[1]} {c1[2]} minecraft:air replace #{tag} strict")
        lines = [f"execute unless blocks {c0[0]} {c0[1]} {c0[2]} {c1[0]} {c1[1]} {c1[2]} {w0[0]} {w0[1]} {w0[2]} masked "
                 f"run function {F}/r/{n}"]
        lines += loose_by_tile.get(t0, [])
        W(f"t/{n}.mcfunction", lines)
        W(f"r/{n}.mcfunction", [
            f"clone {c0[0]} {c0[1]} {c0[2]} {c1[0]} {c1[1]} {c1[2]} {w0[0]} {w0[1]} {w0[2]} masked",
            f"kill @e[type=item,tag={new},{box(*w0, *w1, 1)}]",
            f"scoreboard players add #restores {O} 1"])
        near_p.append(f"execute if entity @s[{box(*w0, *w1, 7)}] run function {F}/t/{n}")
        near_i.append(f"execute if entity @s[{box(*w0, *w1, 1)}] run function {F}/t/{n}")
    for (g0, g1, _), slot in zip(pl["groups"], pl["slots"]):
        setup.append(f"clone {ax + g0[0]} {ay + g0[1]} {az + g0[2]} {ax + g1[0]} {ay + g1[1]} {az + g1[2]} "
                     f"{slot[0]} {slot[1]} {slot[2]} strict replace")
    eb = box(ax, ay, az, ax + X - 1, ay + Y - 1, az + Z - 1, 0)
    locks = [f"kill @e[type=interaction,tag={O}]"]
    for c in pl["locks"]:
        locks.append(f"summon interaction {ax + c[0] + 0.5} {ay + c[1] - 0.005} {az + c[2] + 0.5} "
                     f"{{width:1.01f,height:1.01f,Tags:[\"{O}\",\"vp.lock\"]}}")
    W("locks.mcfunction", locks)
    setup.append(f"function {F}/locks")
    setup += [
        f"execute as @e[type=armor_stand,{eb}] run data merge entity @s {{Invulnerable:1b,DisabledSlots:4144959}}",
        f"execute as @e[type=item_frame,{eb}] run data merge entity @s {{Invulnerable:1b,Fixed:1b}}",
        f"execute as @e[type=glow_item_frame,{eb}] run data merge entity @s {{Invulnerable:1b,Fixed:1b}}",
        f"execute as @e[type=painting,{eb}] run data merge entity @s {{Invulnerable:1b}}",
        f"kill @e[type=item,{box(bx, by, bz, bx + X - 1, by + Y - 1, bz + Z - 1, 1)}]",
        f"scoreboard players set #c {O} 0", f"scoreboard players set #restores {O} 0", f"scoreboard players set #fixes {O} 0",
        f"scoreboard players set #on {O} 1",
        f'tellraw @a[{region}] {{"text":"{scene.name}: protected","color":"gray"}}',
    ]
    W("setup.mcfunction", setup)

    mined = pl["mined_ids"]
    W("init.mcfunction", [f"scoreboard objectives add {O} dummy"] +
      [f"scoreboard objectives add {O}.m{i} minecraft.mined:{m.replace(':', '.')}" for i, m in enumerate(mined)])
    W("player.mcfunction", [f"execute if score @s {O}.m{i} matches 1.. run return run function {F}/hit"
                            for i in range(len(mined))])
    W("hit.mcfunction", [f"scoreboard players reset @s {O}.m{i}" for i in range(len(mined))] + [f"function {F}/near_p"])
    W("near_p.mcfunction", near_p)
    W("near_i.mcfunction", near_i)
    W("fixc.mcfunction", [
        "# macro: a broken container comes back EMPTY (no loot dupe); its contents dropped normally, its own item is removed",
        "$clone $(a) $(b) $(c) $(a) $(b) $(c) $(x) $(y) $(z) replace",
        "$data remove block $(x) $(y) $(z) Items",
        f"$execute positioned $(x) $(y) $(z) run kill @e[type=item,tag={new},distance=..3,nbt={{Item:{{id:\"$(i)\"}}}}]",
        f"scoreboard players add #fixes {O} 1"])
    W("fix.mcfunction", [
        "# macro: put a loose group back from the store (a..f = its copy, x y z = its min corner)",
        "$clone $(a) $(b) $(c) $(d) $(e) $(f) $(x) $(y) $(z) replace",
        f"$execute positioned $(x) $(y) $(z) run kill @e[type=item,tag={new},distance=..3]",
        f"scoreboard players add #fixes {O} 1"])
    # sweep: P slots, each checking K tiles
    P = max(1, min(sweep, len(tiles)))
    K = math.ceil(len(tiles) / P) if tiles else 0
    for s_ in range(P):
        W(f"s/{s_}.mcfunction", [f"function {F}/t/{n}" for n in range(s_ * K, min((s_ + 1) * K, len(tiles)))] or ["return 0"])
    W("sweep.mcfunction", [f"scoreboard players add #c {O} 1",
                           f"execute if score #c {O} matches {P}.. run scoreboard players set #c {O} 0"] +
      [f"execute if score #c {O} matches {s_} run return run function {F}/s/{s_}" for s_ in range(P)])
    W("tick.mcfunction", [
        f"execute unless score #on {O} matches 1 run return 0",
        f"tag @e[type=item,tag=!{seen},{region}] add {new}",
        f"tag @e[type=item,tag={new}] add {seen}",
        f"execute as @a[{region}] at @s run function {F}/player",
        f"execute as @e[type=item,tag={new}] at @s run function {F}/near_i",
        f"function {F}/sweep",
        f"tag @e[type=item,tag={new}] remove {new}"])
    W("on.mcfunction", [f"scoreboard players set #on {O} 1", f"function {F}/locks"])
    W("off.mcfunction", [f"scoreboard players set #on {O} 0", f"kill @e[type=interaction,tag={O}]"])
    W("status.mcfunction", [
        f'tellraw @s ["",{{"text":"{scene.name} protection: "}},{{"score":{{"name":"#on","objective":"{O}"}}}},'
        f'{{"text":" on, restores "}},{{"score":{{"name":"#restores","objective":"{O}"}}}},'
        f'{{"text":", loose fixes "}},{{"score":{{"name":"#fixes","objective":"{O}"}}}}]'])
    _refresh_tags(root, ns)
    meta = {"id": ident, "function": F, "tiles": len(tiles), "sweep_slots": P, "tiles_per_tick": K,
            "loose_groups": len(pl["groups"]), "mined_objectives": len(mined), **pl["counts"],
            "at": pl["at"], "size": pl["size"], "backup": pl["backup"], "store": pl["store"], "store_size": pl["store_size"]}
    (fdir / "info.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    return meta


def _refresh_tags(root, ns):
    root = Path(root)
    (root / "pack.mcmeta").write_text(json.dumps(
        {"pack": {"description": "Voxel studio: protected builds (generated)", "min_format": 121, "max_format": 121}}),
        encoding="utf-8")
    ids = sorted(p.name for p in (root / "data" / ns / "function").iterdir() if (p / "tick.mcfunction").exists())
    tg = root / "data" / "minecraft" / "tags" / "function"
    tg.mkdir(parents=True, exist_ok=True)
    (tg / "tick.json").write_text(json.dumps({"values": [f"{ns}:{i}/tick" for i in ids]}), encoding="utf-8")
    (tg / "load.json").write_text(json.dumps({"values": [f"{ns}:{i}/init" for i in ids]}), encoding="utf-8")
