"""Light: emitter table, a block+sky light estimate (flood fill like the game's, without smooth-lighting subtleties),
an audit of walkable cells below a threshold, and an auto-light pass that adds style-appropriate fixtures.

    python -m tools.voxel light SCENE [--min 7] [--render] [--auto STYLE [--outdoor] [--max N] [--patch]]

Block light: every emitter seeds its level; light spreads to the 6 neighbours losing 1 per step through cells that
don't block it (air, glass, plants, slabs/stairs... are treated as transparent unless they are full opaque cubes).
Sky light: 15 straight down every column until the first opaque or filtering block, then it spreads sideways like
block light (minus 1 per step). Walkable = an air-ish cell with a solid top face below and room for the head above."""
import functools

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


# ------------------------------------------------------------------ propagation
@functools.lru_cache(None)
def _opacity(state):
    """0 = light passes (losing the usual 1 per step), 1 = one extra (water, leaves, ice), 15 = blocks."""
    from .models import bank
    name, p = bs.parse(state)
    s = name.split(":")[-1]
    if s in ("air", "cave_air", "void_air", "structure_void"):
        return 0
    if s in ("water", "bubble_column") or p.get("waterlogged") == "true" or s.endswith("_leaves") \
            or s in ("ice", "frosted_ice", "cobweb"):
        return 1
    if "glass" in s or s in ("barrier", "light", "beacon", "slime_block", "honey_block"):
        return 0
    try:
        return 15 if bank().is_occluder(state) else 0
    except Exception:
        return 15


def _tables(scene):
    pal = scene.palette
    return (np.array([emission(p) for p in pal], np.int16), np.array([_opacity(p) for p in pal], np.int16))


def _spread(L, op, iters=15):
    """Relax L (int16 levels) through non-blocking cells: each step loses 1 + opacity. Emitters that block light
    (glowstone) keep their level and light their neighbours."""
    blk = op >= 15
    loss = 1 + op
    for _ in range(iters):
        n = L.copy()
        n[1:] = np.maximum(n[1:], L[:-1]); n[:-1] = np.maximum(n[:-1], L[1:])
        n[:, 1:] = np.maximum(n[:, 1:], L[:, :-1]); n[:, :-1] = np.maximum(n[:, :-1], L[:, 1:])
        n[:, :, 1:] = np.maximum(n[:, :, 1:], L[:, :, :-1]); n[:, :, :-1] = np.maximum(n[:, :, :-1], L[:, :, 1:])
        new = np.where(blk, L, np.maximum(L, n - loss))
        if np.array_equal(new, L):
            break
        L = new
    return L


def block_light(scene):
    em, op = _tables(scene)
    return np.clip(_spread(em[scene.idx].astype(np.int16), op[scene.idx]), 0, 15)


def sky_light(scene):
    """Sky 15 down every column from the scene top (open sky assumed above), then spread sideways."""
    _, op = _tables(scene)
    o = op[scene.idx]
    X, Y, Z = o.shape
    S = np.zeros(o.shape, np.int16)
    cur = np.full((X, Z), 15, np.int16)
    for y in range(Y - 1, -1, -1):
        cur = np.where(o[:, y] >= 15, 0, np.maximum(cur - o[:, y], 0))
        S[:, y] = cur
    return np.clip(_spread(S, o), 0, 15)


def walkable(scene, floors_only=True):
    """Cells a player can stand in: passable, passable above, collision below. floors_only: the block below is a
    floor (full opaque cube, bottom slab, stairs, path, farmland...), so tops of tables and lanterns don't count."""
    from .stats import passable
    pal = scene.palette
    pas = np.array([passable(p) for p in pal])
    P = pas[scene.idx]
    W = np.zeros(P.shape, bool)
    W[:, 1:-1] = P[:, 1:-1] & P[:, 2:] & ~P[:, :-2]
    if floors_only:
        fl = np.array([_opacity(p) >= 15 or p.endswith("_stairs") or "_stairs[" in p or "type=bottom" in p
                       or "type=double" in p or bs.name_of(p).endswith(("dirt_path", "farmland", "soul_sand", "mud"))
                       for p in pal])
        W[:, 1:] &= fl[scene.idx[:, :-1]]
    return W


def audit(scene, minimum=7):
    """Light at walkable cells. dark_night = block light < minimum (what you see at night and in deep interiors);
    dark_day = also sky light < minimum (dark even at noon: interiors); spawnable = block light 0 (hostile mobs)."""
    from scipy import ndimage
    W = walkable(scene)
    B = block_light(scene)
    S = sky_light(scene)
    dark = W & (B < minimum)
    dark_day = dark & (S < minimum)
    lab, n = ndimage.label(dark_day, structure=np.ones((3, 3, 3)))
    clusters = []
    if n:
        sizes = ndimage.sum(dark_day, lab, range(1, n + 1))
        cents = ndimage.center_of_mass(dark_day, lab, range(1, n + 1))
        for i in np.argsort(-sizes)[:12]:
            clusters.append({"cells": int(sizes[i]), "centre": [round(float(v), 1) for v in cents[i]]})
    nw = int(W.sum())
    rep = {"walkable": nw, "min": minimum,
           "dark_night": int(dark.sum()), "dark_night_share": round(float(dark.sum()) / max(nw, 1), 3),
           "dark_day": int(dark_day.sum()), "dark_day_share": round(float(dark_day.sum()) / max(nw, 1), 3),
           "spawnable": int((W & (B == 0)).sum()),
           "fixtures": int(sum(c for p, c in scene.counts() if is_fixture(p))),
           "dark_day_clusters": clusters}
    return rep, {"W": W, "B": B, "S": S, "dark": dark, "dark_day": dark_day}


def overlay_tint(scene, grids, minimum=7):
    """Per-voxel render tint on the floor block under each walkable cell, by block light (night view):
    red = 0 (mobs spawn), orange = below the minimum, green = lit."""
    X, Y, Z = scene.shape
    t = np.ones((X, Y, Z, 3), np.float32)
    W, B = grids["W"], grids["B"]
    xs, ys, zs = np.nonzero(W)
    b = B[xs, ys, zs][:, None]
    col = np.where(b == 0, np.array([1.7, 0.25, 0.25]),
                   np.where(b < minimum, np.array([1.5, 0.95, 0.3]), np.array([0.55, 1.3, 0.55])))
    t[xs, ys - 1, zs] = col
    return t


def format_report(rep):
    lines = [f"walkable cells {rep['walkable']}, fixtures {rep['fixtures']}, minimum block light {rep['min']}",
             f"  dark at night  {rep['dark_night']:6d}  ({rep['dark_night_share']:.1%})",
             f"  dark at noon   {rep['dark_day']:6d}  ({rep['dark_day_share']:.1%})   <- interiors that need lights",
             f"  mob-spawnable  {rep['spawnable']:6d}  (block light 0)"]
    for c in rep["dark_day_clusters"][:8]:
        lines.append(f"    dark area {c['cells']:5d} cells around {c['centre']}")
    return "\n".join(lines)


# ------------------------------------------------------------------ auto-light
def autolight(scene, style="keep", minimum=7, max_new=200, outdoor=False):
    """Add style fixtures until walkable cells reach `minimum` block light (or max_new lights). Greedy: each light
    goes where it covers the most dark cells: a hanging lantern on a chain when a ceiling is 3-7 above, else a wall
    torch on a nearby wall, else a floor lantern. outdoor=False: only cells dark at noon too (interiors)."""
    from scipy import ndimage
    from .kits.style import STYLES
    st = STYLES[style] if isinstance(style, str) else style
    W = walkable(scene)
    B = block_light(scene)
    S = None if outdoor else sky_light(scene)
    X, Y, Z = scene.shape
    added = []
    skip = np.zeros(W.shape, bool)
    r = max(1, 15 - minimum - 1)
    for _ in range(max_new):
        dark = W & (B < minimum) & ~skip
        if S is not None:
            dark &= S < minimum
        if not dark.any():
            break
        cover = ndimage.uniform_filter(dark.astype(np.float32), size=(2 * r + 1, 5, 2 * r + 1), mode="constant")
        cover[~dark] = -1
        x, y, z = np.unravel_index(int(np.argmax(cover)), cover.shape)
        spot = _fixture_spot(scene, x, y, z, st)
        if spot is None:
            skip[max(0, x - 1):x + 2, y, max(0, z - 1):z + 2] = True
            continue
        for (px, py, pz), state in spot:
            scene.set(px, py, pz, state)
        (lx, ly, lz), state = spot[-1]
        added.append({"pos": [int(lx), int(ly), int(lz)], "state": state})
        lo = [max(0, lx - 16), max(0, ly - 16), max(0, lz - 16)]
        hi = [min(X, lx + 17), min(Y, ly + 17), min(Z, lz + 17)]
        sub = scene.idx[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
        em, op = _tables(scene)
        L = np.zeros(sub.shape, np.int16)
        L[lx - lo[0], ly - lo[1], lz - lo[2]] = em[scene.idx[lx, ly, lz]]
        L = _spread(L, op[sub])
        B[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]] = np.maximum(B[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]], L)
        if "hanging=false" in state:
            W[lx, ly, lz] = False
    return added


def _inb(scene, x, y, z):
    X, Y, Z = scene.shape
    return 0 <= x < X and 0 <= y < Y and 0 <= z < Z


def _air(scene, x, y, z):
    return _inb(scene, x, y, z) and scene.idx[x, y, z] == 0


def _solid(scene, x, y, z):
    return _inb(scene, x, y, z) and _opacity(scene.palette[scene.idx[x, y, z]]) >= 15


def _fixture_spot(scene, x, y, z, st):
    """[(pos, state), ...] lighting walkable cell (x, y, z); the last entry is the light itself."""
    for h in range(3, 8):   # 1. hang from a ceiling (lantern at y+2 or higher: head room)
        if not _air(scene, x, y + h - 1, z):
            break
        if _solid(scene, x, y + h, z):
            chain = [((x, yy, z), st.chain + "[axis=y]") for yy in range(y + 3, y + h)]
            return chain + [((x, y + 2, z), st.lantern + "[hanging=true]")] if h > 3 else \
                [((x, y + 2, z), st.lantern + "[hanging=true]")]
    for rr in (0, 1, 2):     # 2. wall torch at head height on a wall nearby
        for dx in range(-rr, rr + 1):
            for dz in range(-rr, rr + 1):
                if max(abs(dx), abs(dz)) != rr:
                    continue
                cx, cz = x + dx, z + dz
                if not _air(scene, cx, y + 1, cz):
                    continue
                for f, (ox, oz) in (("south", (0, -1)), ("north", (0, 1)), ("east", (-1, 0)), ("west", (1, 0))):
                    if _solid(scene, cx + ox, y + 1, cz + oz):
                        return [((cx, y + 1, cz), f"{st.torch[1]}[facing={f}]")]
    if _air(scene, x, y, z):  # 3. floor lantern
        return [((x, y, z), st.lantern + "[hanging=false]")]
    return None
