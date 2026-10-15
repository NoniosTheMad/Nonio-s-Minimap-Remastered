"""Vanilla block models -> baked quads (the same JSON the game uses: blockstates/*.json, models/block/*.json).

bake(state) -> BakedState: weighted alternatives, each a Quads bundle in block-local units (0..1):
  pos (n,4,3)  corners tl,tr,br,bl     uv (n,4,2) in texture space 0..1     tex [n] texture ids ("block/stone")
  normal (n,3) geometric normal         shade (n,3) normal used for lighting  cull (n,) face dir 0..5 or -1
  tint (n,) tintindex or -1             ao (n,) bool
Directions: 0 down, 1 up, 2 north(-z), 3 south(+z), 4 west(-x), 5 east(+x)."""
import functools, json, math

import numpy as np

from .assets import assets_root
from . import blockstate as bs

DIRS = ["down", "up", "north", "south", "west", "east"]
DVEC = np.array([[0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1], [-1, 0, 0], [1, 0, 0]], np.float32)
INVISIBLE = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void",
             "minecraft:barrier", "minecraft:light", "minecraft:moving_piston"}
LIQUIDS = {"minecraft:water": "block/water_still", "minecraft:lava": "block/lava_still",
           "minecraft:bubble_column": "block/water_still"}


class Quads:
    __slots__ = ("pos", "uv", "tex", "normal", "shade", "cull", "tint", "ao")

    def __init__(self, pos, uv, tex, normal, shade, cull, tint, ao):
        self.pos, self.uv, self.tex, self.normal, self.shade = pos, uv, tex, normal, shade
        self.cull, self.tint, self.ao = cull, tint, ao

    def __len__(self):
        return len(self.tex)

    @staticmethod
    def concat(qs):
        qs = [q for q in qs if len(q)]
        if not qs:
            return EMPTY
        return Quads(*(np.concatenate([getattr(q, k) for q in qs]) if k != "tex" else sum((q.tex for q in qs), [])
                       for k in Quads.__slots__))


EMPTY = Quads(np.zeros((0, 4, 3), np.float32), np.zeros((0, 4, 2), np.float32), [], np.zeros((0, 3), np.float32),
              np.zeros((0, 3), np.float32), np.zeros(0, np.int8), np.zeros(0, np.int8), np.zeros(0, bool))


def _corners(f, t, d):
    """Face corners tl,tr,br,bl (texture orientation) + default uv rect, element bounds f/t in 0..16."""
    x0, y0, z0 = f
    x1, y1, z1 = t
    if d == 1:
        c = [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)]; uv = [x0, z0, x1, z1]
    elif d == 0:
        c = [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)]; uv = [x0, 16 - z1, x1, 16 - z0]
    elif d == 2:
        c = [(x1, y1, z0), (x0, y1, z0), (x0, y0, z0), (x1, y0, z0)]; uv = [16 - x1, 16 - y1, 16 - x0, 16 - y0]
    elif d == 3:
        c = [(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)]; uv = [x0, 16 - y1, x1, 16 - y0]
    elif d == 4:
        c = [(x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)]; uv = [z0, 16 - y1, z1, 16 - y0]
    else:
        c = [(x1, y1, z1), (x1, y1, z0), (x1, y0, z0), (x1, y0, z1)]; uv = [16 - z1, 16 - y1, 16 - z0, 16 - y0]
    return np.array(c, np.float32), uv


def _rot_matrix(axis, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], np.float32)
    if axis == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], np.float32)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], np.float32)


def _block_rot(x, y):
    """Blockstate rotation (degrees, multiples of 90). MC: x first, then y; y is clockwise seen from above
    (north -> east), x=90 turns north -> down."""
    R = np.eye(3, dtype=np.float32)
    for _ in range((x // 90) % 4):  # north (0,0,-1) -> down (0,-1,0): y' = z, z' = -y
        R = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], np.float32) @ R
    for _ in range((y // 90) % 4):  # north -> east: x' = -z, z' = x
        R = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]], np.float32) @ R
    return R


def _dir_of(v):
    return int(np.argmax(DVEC @ v))


class ModelBank:
    def __init__(self):
        self.root = assets_root()

    @functools.lru_cache(None)
    def blockstate(self, name):
        f = self.root / "blockstates" / (name.split(":")[-1] + ".json")
        return json.loads(f.read_text()) if f.exists() else None

    @functools.lru_cache(None)
    def model(self, ref):
        """Resolved model: {"textures": {...}, "elements": [...], "ao": bool}."""
        path = ref.split(":")[-1]
        f = self.root / "models" / (path + ".json")
        if not f.exists():
            return {"textures": {}, "elements": [], "ao": True}
        m = json.loads(f.read_text())
        if "parent" in m and not m["parent"].startswith("builtin/"):
            base = self.model(m["parent"])
        else:
            base = {"textures": {}, "elements": [], "ao": True}
        tex = dict(base["textures"]); tex.update(m.get("textures", {}))
        return {"textures": tex, "elements": m.get("elements", base["elements"]),
                "ao": m.get("ambientocclusion", base["ao"])}

    forced_translucent = set()

    @classmethod
    def _tex(cls, textures, ref, depth=0):
        while depth < 10:
            if isinstance(ref, dict):  # 26.x: {"sprite": "...", "force_translucent": true}
                if ref.get("force_translucent"):
                    cls.forced_translucent.add(ref["sprite"].split(":")[-1])
                ref = ref.get("sprite", "missing")
            if not ref.startswith("#"):
                break
            ref = textures.get(ref[1:], "missing")
            depth += 1
        return ref.split(":")[-1]

    @functools.lru_cache(None)
    def bake_model(self, ref, x=0, y=0, uvlock=False):
        m = self.model(ref)
        R = _block_rot(x, y)
        quads = []
        for el in m["elements"]:
            f, t = el["from"], el["to"]
            er = el.get("rotation")
            for dname, face in el["faces"].items():
                d = DIRS.index(dname)
                c, duv = _corners(f, t, d)
                uv = face.get("uv", duv)
                n = DVEC[d].copy()
                shade = DVEC[DIRS.index(el["shade_direction_override"])].copy() if "shade_direction_override" in el else n.copy()
                # element rotation
                if er:
                    o = np.array(er.get("origin", [8, 8, 8]), np.float32)
                    if "axis" in er:
                        M = _rot_matrix(er["axis"], er.get("angle", 0))
                        c = (c - o) @ M.T
                        if er.get("rescale") and er.get("angle", 0) % 90:
                            k = 1 / math.cos(math.radians(abs(er["angle"])))
                            sc = np.array([k, k, k], np.float32); sc["xyz".index(er["axis"])] = 1
                            c = c * sc
                        c = c + o
                    else:
                        M = np.eye(3, dtype=np.float32)
                        for ax in "xyz":
                            if er.get(ax):
                                M = _rot_matrix(ax, er[ax]) @ M
                        c = (c - o) @ M.T + o
                    n = M @ n; shade = M @ shade
                # block rotation around the centre
                c = (c - 8) @ R.T + 8
                n = R @ n; shade = R @ shade
                cull = face.get("cullface")
                cull = _dir_of(R @ DVEC[DIRS.index(cull)]) if cull else -1
                if uvlock and (x or y) and np.allclose(np.abs(n).max(), 1):
                    lo, hi = c.min(0), c.max(0)
                    _, uv = _corners(lo, hi, _dir_of(n))
                    rot = 0
                else:
                    rot = face.get("rotation", 0) // 90
                u0, v0, u1, v1 = [v / 16 for v in uv]
                uvs = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
                uvs = [uvs[(i - rot) % 4] for i in range(4)]
                quads.append((c / 16, uvs, self._tex(m["textures"], face.get("texture", "#missing")), n, shade, cull,
                              face.get("tintindex", -1), m["ao"]))
        if not quads:
            return EMPTY
        return Quads(np.array([q[0] for q in quads], np.float32), np.array([q[1] for q in quads], np.float32),
                     [q[2] for q in quads], np.array([q[3] for q in quads], np.float32),
                     np.array([q[4] for q in quads], np.float32), np.array([q[5] for q in quads], np.int8),
                     np.array([q[6] for q in quads], np.int8), np.array([q[7] for q in quads], bool))

    @functools.lru_cache(None)
    def bake(self, state):
        """[(weight, Quads), ...] alternatives for a canonical state."""
        name, props = bs.parse(state)
        if name in INVISIBLE:
            return [(1, EMPTY)]
        if name in LIQUIDS:
            return [(1, liquid_quads(LIQUIDS[name], props))]
        b = self.blockstate(name)
        alts = []
        if b and "variants" in b:
            for key, v in b["variants"].items():
                if _match_key(key, props):
                    for vv in (v if isinstance(v, list) else [v]):
                        alts.append((vv.get("weight", 1), self.bake_model(vv["model"], vv.get("x", 0), vv.get("y", 0), vv.get("uvlock", False))))
                    break
        elif b and "multipart" in b:
            parts = []
            for p in b["multipart"]:
                if "when" not in p or _match_when(p["when"], props):
                    a = p["apply"]
                    a = a[0] if isinstance(a, list) else a
                    parts.append(self.bake_model(a["model"], a.get("x", 0), a.get("y", 0), a.get("uvlock", False)))
            alts.append((1, Quads.concat(parts)))
        if not alts or not len(alts[0][1]):
            alts = [(1, fallback_cube(self, name, b))]
        return alts

    @functools.lru_cache(None)
    def is_occluder(self, state):
        """Opaque full cube: hides its neighbours' touching faces (decided with the texture alpha in render)."""
        name, _ = bs.parse(state)
        if name in INVISIBLE or name in LIQUIDS:
            return False
        q = self.bake(state)[0][1]
        full = set()
        for i in range(len(q)):
            if q.cull[i] >= 0:
                p = q.pos[i]
                span = p.max(0) - p.min(0)
                if np.sort(span)[1:].min() > 0.999:
                    full.add(int(q.cull[i]))
        return len(full) == 6


def _match_key(key, props):
    if not key:
        return True
    for kv in key.split(","):
        k, _, v = kv.partition("=")
        if props.get(k) != v:
            return False
    return True


def _match_when(w, props):
    if "OR" in w:
        return any(_match_when(c, props) for c in w["OR"])
    if "AND" in w:
        return all(_match_when(c, props) for c in w["AND"])
    return all(props.get(k) in str(v).split("|") for k, v in w.items())


def _cube(tex_by_dir, top=1.0, tint=-1, cull=True):
    pos, uvs, texs, ns, culls = [], [], [], [], []
    for d in range(6):
        c, uv = _corners((0, 0, 0), (16, top * 16, 16), d)
        u0, v0, u1, v1 = [v / 16 for v in uv]
        pos.append(c / 16); uvs.append([(u0, v0), (u1, v0), (u1, v1), (u0, v1)])
        texs.append(tex_by_dir[d]); ns.append(DVEC[d]); culls.append(d if (cull and (d != 1 or top >= 1)) else -1)
    n = np.array(ns, np.float32)
    return Quads(np.array(pos, np.float32), np.array(uvs, np.float32), texs, n, n.copy(),
                 np.array(culls, np.int8), np.full(6, tint, np.int8), np.ones(6, bool))


def liquid_quads(tex, props):
    level = int(props.get("level", "0") or 0)
    h = 14 / 16 if level == 0 else max(2, 14 - 2 * (level % 8)) / 16
    return _cube([tex] * 6, top=h, tint=0 if "water" in tex else -1)


def fallback_cube(bank, name, b):
    """Blocks without baked geometry (chests, signs, beds, heads...): a cube with the particle texture."""
    tex = "missing"
    m = bank.model("block/" + name.split(":")[-1])
    if m["textures"]:
        tex = bank._tex(m["textures"], m["textures"].get("particle", next(iter(m["textures"].values()))))
    elif b:
        first = next(iter(b.get("variants", {}).values()), None) if "variants" in b else None
        if first:
            first = first[0] if isinstance(first, list) else first
            mm = bank.model(first["model"])
            if mm["textures"]:
                tex = bank._tex(mm["textures"], mm["textures"].get("particle", "missing"))
    q = _cube([tex] * 6)
    q.pos = (q.pos - 0.5) * 0.8 + np.array([0.5, 0.4, 0.5], np.float32)  # inset: reads as "a thing", not a wall
    q.cull[:] = -1
    return q


@functools.lru_cache(None)
def bank():
    return ModelBank()
