"""Scene -> triangle mesh with real block models, face culling, per-vertex ambient occlusion and biome tints.
Shared by the offscreen renderer (render.py) and the WebGL viewer (viewer.py)."""
import numpy as np
from PIL import Image

from . import blockstate as bs
from .models import DVEC, INVISIBLE, bank
from .noise import hash01
from . import special

# Plains-ish biome tints (the game samples colormaps per biome; one fixed biome is enough for critique).
GRASS, FOLIAGE, WATER = (0x91, 0xBD, 0x59), (0x77, 0xAB, 0x2F), (0x3F, 0x76, 0xE4)
TINTS = {"spruce_leaves": (0x61, 0x99, 0x61), "birch_leaves": (0x80, 0xA7, 0x55), "lily_pad": (0x20, 0x80, 0x30),
         "water": WATER, "bubble_column": WATER, "water_cauldron": WATER, "redstone_wire": (0xB0, 0x10, 0x00),
         "attached_melon_stem": (0xE0, 0xC7, 0x1C), "attached_pumpkin_stem": (0xE0, 0xC7, 0x1C),
         "melon_stem": (0x7F, 0xB0, 0x38), "pumpkin_stem": (0x7F, 0xB0, 0x38),
         # untinted in game (no block colour provider) although their models carry a tintindex
         "cherry_leaves": (0xFF, 0xFF, 0xFF), "pale_oak_leaves": (0xFF, 0xFF, 0xFF), "azalea_leaves": (0xFF, 0xFF, 0xFF),
         "flowering_azalea_leaves": (0xFF, 0xFF, 0xFF)}
FOLIAGE_BLOCKS = ("oak_leaves", "jungle_leaves", "acacia_leaves", "dark_oak_leaves", "mangrove_leaves", "vine")
SELF_CULL = ("glass", "ice", "water", "lava", "slime_block", "honey_block")  # same-block faces between them vanish
AO_CURVE = np.array([0.42, 0.62, 0.8, 1.0], np.float32)

# Block light emitted (vanilla 26.3 luminance). "lit" blocks only when lit=true. Used by mood renders (render --mood).
LUMINANCE = {"lava": 15, "fire": 15, "glowstone": 15, "sea_lantern": 15, "shroomlight": 15, "jack_o_lantern": 15,
             "beacon": 15, "conduit": 15, "ochre_froglight": 15, "verdant_froglight": 15, "pearlescent_froglight": 15,
             "lantern": 15, "end_rod": 14, "torch": 14, "wall_torch": 14, "end_gateway": 15, "end_portal": 15,
             "soul_fire": 10, "soul_lantern": 10, "soul_torch": 10, "soul_wall_torch": 10, "crying_obsidian": 10,
             "magma_block": 3, "amethyst_cluster": 5, "large_amethyst_bud": 4, "medium_amethyst_bud": 2,
             "glow_lichen": 7, "sea_pickle": 6, "respawn_anchor": 15, "enchanting_table": 7, "ender_chest": 7,
             "copper_torch": 14, "copper_wall_torch": 14, "copper_lantern": 15, "brewing_stand": 1, "dragon_egg": 1}
LIT_LUMINANCE = {"campfire": 15, "soul_campfire": 10, "redstone_lamp": 15, "copper_bulb": 15, "exposed_copper_bulb": 12,
                 "weathered_copper_bulb": 8, "oxidized_copper_bulb": 4, "furnace": 13, "blast_furnace": 13, "smoker": 13,
                 "candle": 3, "redstone_ore": 9, "deepslate_redstone_ore": 9}
# faces drawn full-bright in mood renders (the block glows, not just lights its neighbours)
EMISSIVE = ("lava", "fire", "soul_fire", "glowstone", "sea_lantern", "shroomlight", "froglight", "lantern", "end_rod",
            "torch", "magma_block", "crying_obsidian", "jack_o_lantern", "beacon", "amethyst_cluster", "_bud", "campfire",
            "redstone_lamp[lit=true", "copper_bulb[lit=true")


def luminance(state):
    name = bs.name_of(state).split(":")[-1]
    if name in LUMINANCE:
        return LUMINANCE[name]
    if name in LIT_LUMINANCE or name.endswith("_candle"):
        if "lit=true" in state:
            n = 3
            if "candles=" in state:
                n = 3 * int(state.split("candles=")[1][0])
            return LIT_LUMINANCE.get(name, n) if not name.endswith("candle") else min(15, n)
    if name.endswith("_copper_lantern"):
        return 15
    return 0


def block_light(scene, occ_state):
    """Vanilla-like block light (0..15): each emitter floods non-opaque cells, -1 per step (6-neighbour)."""
    lum = np.array([luminance(p) for p in scene.palette], np.int16)
    src = lum[scene.idx]
    if not src.any():
        return np.zeros(scene.shape, np.int16)
    opaque = occ_state[scene.idx]
    lvl = src.copy()
    for _ in range(14):
        n = lvl.copy()
        n[1:] = np.maximum(n[1:], lvl[:-1]); n[:-1] = np.maximum(n[:-1], lvl[1:])
        n[:, 1:] = np.maximum(n[:, 1:], lvl[:, :-1]); n[:, :-1] = np.maximum(n[:, :-1], lvl[:, 1:])
        n[:, :, 1:] = np.maximum(n[:, :, 1:], lvl[:, :, :-1]); n[:, :, :-1] = np.maximum(n[:, :, :-1], lvl[:, :, 1:])
        n = np.where(opaque, 0, np.maximum(n - 1, 0))
        lvl = np.maximum(lvl, np.maximum(n, src))
    return lvl


def tint_of(name):
    short = name.split(":")[-1]
    if short in TINTS:
        return TINTS[short]
    if short in FOLIAGE_BLOCKS:
        return FOLIAGE
    return GRASS


class TextureArray:
    """Every texture used by a mesh as one 16x16 layer (+ per-layer kind: 0 opaque, 1 cutout, 2 translucent)."""

    def __init__(self):
        self.root = bank().root
        self.layers, self.index, self.kind = [], {}, []

    def layer(self, name):
        i = self.index.get(name)
        if i is None:
            i = len(self.layers)
            img = self._load(name)
            a = np.asarray(img)[..., 3]
            forced = name in type(bank()).forced_translucent or "stained_glass" in name or name.endswith(("ice", "water_still"))
            self.kind.append(2 if forced and a.min() < 255 else 0 if a.min() == 255 else (1 if np.isin(a, (0, 255)).all() or "leaves" in name else 2))
            self.layers.append(np.asarray(img, np.uint8))
            self.index[name] = i
        return i

    def _load(self, name):
        if name.startswith("@"):
            from .special import load
            img = load(name)
            if img is not None:
                return img
            name = "missing"
        f = self.root / "textures" / (name + ".png")
        if not f.exists():
            chk = np.zeros((16, 16, 4), np.uint8); chk[..., 3] = 255
            chk[(np.indices((16, 16)).sum(0) // 8) % 2 == 0] = (255, 0, 255, 255)
            return Image.fromarray(chk)
        img = Image.open(f).convert("RGBA")
        w, h = img.size
        if h > w:  # animated strip: first frame
            img = img.crop((0, 0, w, w))
        if img.size != (16, 16):
            img = img.resize((16, 16), Image.BOX)
        return img

    def array(self):
        return np.stack(self.layers) if self.layers else np.zeros((1, 16, 16, 4), np.uint8)


class Mesh:
    """Triangle soup in world block units: pos (V,3), uvl (V,3) = u, v, layer, nrm (V,3) shading normal,
    col (V,3) tint*AO (0..1); idx (T*3,) for opaque+cutout and tidx for translucent."""

    def __init__(self):
        self.pos = self.uvl = self.nrm = self.col = None
        self.idx = self.tidx = None
        self.tex = TextureArray()
        self.quads = 0


def build(scene, origin=(0, 0, 0), ao=True, vtint=None, light=False):
    """vtint: optional (X,Y,Z,3) per-voxel colour multiplier (diff highlighting).
    light: compute block light + emissive faces; stored in the shading normal's length (|n| = 1 + level, +32 if emissive),
    which only the mood renderer reads (it normalises n)."""
    b = bank()
    tex = TextureArray()
    pal = scene.palette
    names = [bs.name_of(p) for p in pal]
    X, Y, Z = scene.shape

    # occluders: opaque full cubes whose textures are all opaque
    occ_state = np.zeros(len(pal), bool)
    for i, s in enumerate(pal):
        if b.is_occluder(s):
            q = b.bake(s)[0][1]
            occ_state[i] = all(tex.kind[tex.layer(t)] == 0 for t in q.tex)
    occ = np.zeros((X + 2, Y + 2, Z + 2), bool)
    occ[1:-1, 1:-1, 1:-1] = occ_state[scene.idx]
    ids = np.zeros((X + 2, Y + 2, Z + 2), np.int32) - 1
    ids[1:-1, 1:-1, 1:-1] = scene.idx
    selfcull = np.array([any(k in n for k in SELF_CULL) and not occ_state[i] for i, n in enumerate(names)])

    flat = scene.idx.ravel()
    order = np.argsort(flat, kind="stable")
    counts = np.bincount(flat, minlength=len(pal))
    starts = np.concatenate([[0], np.cumsum(counts)])

    if light:
        bl = np.zeros((X + 2, Y + 2, Z + 2), np.int16)
        bl[1:-1, 1:-1, 1:-1] = block_light(scene, occ_state)
        emis = np.array([any(e in p for e in EMISSIVE) for p in pal])
    P, UV, L, N, C, A, TR = [], [], [], [], [], [], []
    for k, state in enumerate(pal):
        if not counts[k] or names[k] in INVISIBLE or (special.kind(names[k]) and special.kind(names[k]) != "bell"):
            continue
        lin = order[starts[k]:starts[k + 1]]
        pos = np.stack(np.unravel_index(lin, scene.shape), 1).astype(np.int32)
        alts = b.bake(state)
        if len(alts) > 1:
            w = np.array([a[0] for a in alts], float); cw = np.cumsum(w / w.sum())
            pick = np.searchsorted(cw, hash01(pos[:, 0], pos[:, 1], pos[:, 2], seed=17), side="right")
            groups = [(alts[j][1], pos[pick == j]) for j in range(len(alts))]
        else:
            groups = [(alts[0][1], pos)]
        tint = np.array(tint_of(names[k]), np.float32) / 255
        for q, p in groups:
            if not len(q) or not len(p):
                continue
            layers = np.array([tex.layer(t) for t in q.tex], np.int32)
            for i in range(len(q)):
                pp = p
                c = q.cull[i]
                if c >= 0:
                    nb = pp + 1 + DVEC[c].astype(np.int32)
                    hide = occ[nb[:, 0], nb[:, 1], nb[:, 2]]
                    if selfcull[k]:
                        hide |= ids[nb[:, 0], nb[:, 1], nb[:, 2]] == k
                    pp = pp[~hide]
                if not len(pp):
                    continue
                v = pp[:, None, :].astype(np.float32) + q.pos[i][None]  # (m,4,3)
                P.append(v)
                UV.append(np.broadcast_to(q.uv[i], (len(pp), 4, 2)))
                L.append(np.full((len(pp), 4), layers[i], np.float32))
                if light:
                    nv = np.asarray(q.shade[i], np.float32)
                    nb = pp + 1 + np.round(nv).astype(np.int32)
                    lv = np.maximum(bl[nb[:, 0], nb[:, 1], nb[:, 2]], bl[pp[:, 0] + 1, pp[:, 1] + 1, pp[:, 2] + 1])
                    ln = 1.0 + lv.astype(np.float32) + (32.0 if emis[k] else 0.0)
                    N.append(np.broadcast_to(nv[None, None, :] * ln[:, None, None], (len(pp), 4, 3)))
                else:
                    N.append(np.broadcast_to(q.shade[i], (len(pp), 4, 3)))
                col = tint if q.tint[i] >= 0 else np.ones(3, np.float32)
                if vtint is not None:
                    col = col[None] * vtint[pp[:, 0], pp[:, 1], pp[:, 2]]
                    C.append(np.broadcast_to(col[:, None, :], (len(pp), 4, 3)))
                else:
                    C.append(np.broadcast_to(col, (len(pp), 4, 3)))
                if ao and q.ao[i] and np.abs(q.normal[i]).max() > 0.99:
                    A.append(_ao(occ, v, q.normal[i]))
                else:
                    A.append(np.ones((len(pp), 4), np.float32))
                TR.append(np.full(len(pp), tex.kind[layers[i]] == 2))
    _extras(scene, pal, names, counts, order, starts, tex, vtint, P, UV, L, N, C, A, TR)
    m = Mesh()
    m.tex = tex
    if not P:
        m.pos = np.zeros((0, 3), np.float32); m.uvl = m.nrm = m.col = m.pos
        m.idx = m.tidx = np.zeros(0, np.uint32)
        return m
    P = np.concatenate(P); A = np.concatenate(A); TR = np.concatenate(TR)
    nq = len(P)
    m.quads = nq
    m.pos = (P + np.array(origin, np.float32)).reshape(-1, 3)
    uv = np.concatenate(UV).reshape(-1, 2)
    m.uvl = np.concatenate([uv, np.concatenate(L).reshape(-1, 1)], 1).astype(np.float32)
    m.nrm = np.concatenate(N).reshape(-1, 3).astype(np.float32)
    m.col = (np.concatenate(C) * A[..., None]).reshape(-1, 3).astype(np.float32)
    m.ao = A.reshape(-1)
    # two triangles per quad; flip the diagonal where AO is anisotropic (the classic voxel AO fix)
    base = (np.arange(nq, dtype=np.uint32) * 4)[:, None]
    flip = (A[:, 0] + A[:, 2]) < (A[:, 1] + A[:, 3])
    tri = np.where(flip[:, None], np.array([1, 2, 3, 1, 3, 0], np.uint32), np.array([0, 1, 2, 0, 2, 3], np.uint32)) + base
    m.idx = tri[~TR].ravel()
    m.tidx = tri[TR].ravel()
    return m


def _extras(scene, pal, names, counts, order, starts, tex, vtint, P, UV, L, N, C, A, TR):
    """Block-entity geometry (chests, banners, heads, pots, shulkers, bell bodies) and entities (frames, paintings,
    armour stands): special.py quads appended to the same arrays."""
    def add(q, off, cell):
        if q is None or not len(q):
            return
        n = len(q)
        layers = np.array([tex.layer(t) for t in q.tex], np.float32)
        P.append(q.pos + np.asarray(off, np.float32))
        UV.append(q.uv)
        L.append(np.repeat(layers[:, None], 4, 1))
        N.append(np.repeat(q.shade[:, None], 4, 1))
        col = np.ones(3, np.float32)
        if vtint is not None and cell is not None:
            c = np.clip(np.array(cell), 0, np.array(scene.shape) - 1)
            col = col * vtint[c[0], c[1], c[2]]
        C.append(np.broadcast_to(col, (n, 4, 3)))
        A.append(np.ones((n, 4), np.float32))
        TR.append(np.array([tex.kind[int(l)] == 2 for l in layers]))

    cache = {}
    for k, state in enumerate(pal):
        if not counts[k] or not special.kind(names[k]):
            continue
        lin = order[starts[k]:starts[k + 1]]
        for x, y, z in np.stack(np.unravel_index(lin, scene.shape), 1):
            be = scene.be.get((int(x), int(y), int(z)))
            key = (state, str(be) if be is not None else "")
            if key not in cache:
                cache[key] = special.block_quads(state, be)
            add(cache[key], (x, y, z), (x, y, z))
    for e in scene.entities:
        r = special.entity_quads(e)
        if r:
            add(r[0], (0, 0, 0), r[1])


def _ao(occ, v, n):
    """Per-vertex AO (0..1) for quads with an axis-aligned normal. v: (m,4,3) world corners."""
    ax = int(np.argmax(np.abs(n)))
    t1, t2 = [a for a in range(3) if a != ax]
    centre = v.mean(1, keepdims=True)
    s1 = np.sign(v[..., t1] - centre[..., t1])
    s2 = np.sign(v[..., t2] - centre[..., t2])
    base = v + n * 0.01
    e1 = np.zeros(3, np.float32); e1[t1] = 1
    e2 = np.zeros(3, np.float32); e2[t2] = 1
    front = np.floor(base - (s1[..., None] * e1 + s2[..., None] * e2) * 0.5).astype(np.int32) + 1
    def at(off):
        c = front + off
        for a, lim in enumerate(occ.shape):
            c[..., a] = np.clip(c[..., a], 0, lim - 1)
        return occ[c[..., 0], c[..., 1], c[..., 2]]
    d1 = (s1[..., None] * e1).astype(np.int32)
    d2 = (s2[..., None] * e2).astype(np.int32)
    a1, a2, ac = at(d1), at(d2), at(d1 + d2)
    lvl = np.where(a1 & a2, 0, 3 - (a1.astype(int) + a2 + ac))
    return AO_CURVE[lvl]
