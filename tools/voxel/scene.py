"""Scene = a numpy grid of palette indices + a palette of canonical block states + named markers.

    s = Scene((96, 64, 96), name="tower")
    s.fill(shapes.sphere((48, 10, 48), 14), Mix({"minecraft:stone": 6, "minecraft:andesite": 2}))
    s.box((40, 20, 40), (56, 20, 56), "minecraft:stone_bricks")    # inclusive corners, like /fill
    s.mark("spawn_white", (10, 21, 48), look_at=(48, 25, 48))

Axes are idx[x, y, z] (x = east, y = up, z = south), scene-local; the scene's (0,0,0) lands at the placement origin.
Index 0 is always air. "minecraft:structure_void" means "not part of the build" (placement leaves the world as is).

Block entities and entities (v2):
    s.set(x, y, z, "chest[facing=south]", nbt=nbt.chest([nbt.item("apple", 3)]))      # s.be[(x, y, z)] = Compound
    s.entity(nbt.item_frame(nbt.item("iron_sword"), facing="south"), (x + .5, y + .5, z + .03))
s.be holds block entity data by cell; an entry whose cell no longer holds a matching block is dropped on export
(block_entities()). s.entities is a list of {"pos": [x, y, z] (scene coords, floats), "nbt": Compound with id}.
Both follow stamp / transformed / crop / save / load."""
import json
from pathlib import Path

import numpy as np

from . import blockstate as bs
from .palette import FillContext, resolve
from .shapes import SDF

AIR = "minecraft:air"
VOID = "minecraft:structure_void"


class Scene:
    def __init__(self, size, name="scene", seed=0):
        self.idx = np.zeros(tuple(int(v) for v in size), np.uint16)
        self.palette = [AIR]
        self._lut = {AIR: 0}
        self._names = [AIR]
        self.name = name
        self.seed = seed
        self.markers = {}   # name -> {"pos": [x,y,z], "yaw": deg|None, "look_at": [x,y,z]|None}
        self.meta = {}      # free-form (e.g. {"origin": [x, y, z]} suggested placement)
        self.be = {}        # (x, y, z) -> nbtlib Compound (block entity data, without x/y/z/id)
        self.entities = []  # [{"pos": [x, y, z], "nbt": Compound with "id"}]

    # ------------------------------------------------------------ palette
    @property
    def shape(self):
        return self.idx.shape

    def id(self, state: str) -> int:
        i = self._lut.get(state)
        if i is not None:
            return i
        c = bs.canonical(state)
        i = self._lut.get(c)
        if i is None:
            i = len(self.palette)
            if i >= 65535:
                raise OverflowError("palette full")
            self.palette.append(c)
            self._names.append(bs.name_of(c))
            self._lut[c] = i
        self._lut[state] = i
        return i

    def names(self):
        return np.array(self._names, dtype=object)

    # ------------------------------------------------------------ queries
    def get(self, x, y, z) -> str:
        return self.palette[self.idx[x, y, z]]

    def match(self, what) -> np.ndarray:
        """Bool grid. what: 'air' | 'solid' | block name (any props) | full state | list of those | bool grid | callable(name)->bool."""
        if isinstance(what, np.ndarray):
            return what.astype(bool)
        if isinstance(what, (list, tuple, set)):
            m = np.zeros(self.shape, bool)
            for w in what:
                m |= self.match(w)
            return m
        if what == "solid":
            return self.solid()
        if callable(what):
            ok = np.array([bool(what(n)) for n in self._names])
            return ok[self.idx]
        if what == "air":
            what = AIR
        name, props = bs.parse(what)
        if props:
            sel = np.array([p == bs.canonical(what) for p in self.palette])
        else:
            sel = np.array([n == name for n in self._names])
        return sel[self.idx]

    def solid(self) -> np.ndarray:
        """Anything but air / structure_void."""
        ok = np.array([n not in (AIR, VOID) for n in self._names])
        return ok[self.idx]

    def counts(self):
        u, c = np.unique(self.idx, return_counts=True)
        return sorted(((self.palette[i], int(n)) for i, n in zip(u, c)), key=lambda t: -t[1])

    def bounds(self):
        """((x0,y0,z0),(x1,y1,z1)) inclusive bounds of non-air content, or None."""
        nz = np.nonzero(self.solid())
        if not len(nz[0]):
            return None
        return tuple(int(a.min()) for a in nz), tuple(int(a.max()) for a in nz)

    def surface(self, where="solid"):
        """2D int array: y of the topmost matching block per column (-1 if none)."""
        m = self.match(where)
        Y = m.shape[1]
        top = Y - 1 - np.argmax(m[:, ::-1, :], axis=1)
        return np.where(m.any(axis=1), top, -1)

    # ------------------------------------------------------------ edits
    def _mask(self, where):
        if isinstance(where, SDF):
            return where.mask(self.shape)
        if isinstance(where, np.ndarray):
            return np.broadcast_to(where.astype(bool), self.shape).copy()
        if isinstance(where, tuple) and len(where) == 2 and len(where[0]) == 3:
            (x0, y0, z0), (x1, y1, z1) = where
            m = np.zeros(self.shape, bool)
            m[min(x0, x1):max(x0, x1) + 1, min(y0, y1):max(y0, y1) + 1, min(z0, z1):max(z0, z1) + 1] = True
            return m
        raise TypeError("where: SDF, bool grid or ((x0,y0,z0),(x1,y1,z1))")

    def fill(self, where, spec, replace=None):
        """Fill `where` (SDF / bool grid / inclusive box corners) with `spec` (state, Mix, Gradient, ... see palette.py).
        replace: only overwrite voxels matching this (see match()), e.g. replace='air'. Returns voxels written."""
        m = self._mask(where)
        if replace is not None:
            m &= self.match(replace)
        xs, ys, zs = np.nonzero(m)
        if not len(xs):
            return 0
        ids = resolve(spec, FillContext(self, xs, ys, zs, m))
        ok = ids >= 0
        self.idx[xs[ok], ys[ok], zs[ok]] = ids[ok]
        return int(ok.sum())

    def box(self, p0, p1, spec, hollow=False, replace=None):
        """Inclusive corners like /fill. hollow=True: only the outer shell."""
        m = self._mask((tuple(p0), tuple(p1)))
        if hollow:
            lo = [min(a, b) for a, b in zip(p0, p1)]; hi = [max(a, b) for a, b in zip(p0, p1)]
            m[lo[0] + 1:hi[0], lo[1] + 1:hi[1], lo[2] + 1:hi[2]] = False
        return self.fill(m, spec, replace)

    def set(self, x, y, z, state, nbt=None):
        """One block; nbt = block entity data (SNBT / Compound / tools.voxel.nbt builder)."""
        if 0 <= x < self.shape[0] and 0 <= y < self.shape[1] and 0 <= z < self.shape[2]:
            self.idx[x, y, z] = self.id(state)
            k = (int(x), int(y), int(z))
            if nbt is not None:
                from .nbt import to_tag
                self.be[k] = to_tag(nbt)
            elif k in self.be:
                del self.be[k]

    def set_nbt(self, pos, nbt):
        from .nbt import to_tag
        self.be[tuple(int(v) for v in pos)] = to_tag(nbt)

    def entity(self, nbt, pos):
        """Add an entity (Compound with "id", e.g. nbt.painting(...)) at scene position pos (floats, block units)."""
        from .nbt import to_tag
        t = to_tag(nbt)
        if "id" not in t:
            raise ValueError("entity nbt needs an id")
        self.entities.append({"pos": [float(v) for v in pos], "nbt": t})
        return t

    def block_entities(self):
        """{(x,y,z): Compound with id} for cells whose block carries a block entity. Stale entries (the block was
        overwritten later) are skipped."""
        from .nbt import be_id
        from nbtlib import String
        out = {}
        for (x, y, z), t in self.be.items():
            if not (0 <= x < self.shape[0] and 0 <= y < self.shape[1] and 0 <= z < self.shape[2]):
                continue
            i = be_id(self._names[self.idx[x, y, z]])
            if i is None:
                continue
            t = type(t)(t)
            t["id"] = String(i)
            out[(x, y, z)] = t
        return out

    def line(self, p0, p1, spec, radius=0.0):
        from .shapes import capsule
        a = np.array(p0, float) + 0.5; b = np.array(p1, float) + 0.5
        return self.fill(capsule(a, b, max(radius, 0.5)), spec)

    def replace(self, old, spec, where=None):
        m = self.match(old)
        if where is not None:
            m &= self._mask(where)
        return self.fill(m, spec)

    def decorate(self, on, spec, chance=1.0, seed=0, where=None):
        """Put `spec` in the air block above every top face of `on` blocks (grass, flowers, snow layers...)."""
        from .noise import hash01
        base = self.match(on)
        air_above = np.zeros(self.shape, bool)
        air_above[:, :-1] = self.match("air")[:, 1:]
        m = base & air_above
        if where is not None:
            m &= self._mask(where)
        xs, ys, zs = np.nonzero(m)
        keep = hash01(xs, ys, zs, seed=seed + 101) < chance
        tgt = np.zeros(self.shape, bool)
        tgt[xs[keep], ys[keep] + 1, zs[keep]] = True
        return self.fill(tgt, spec)

    # ------------------------------------------------------------ modules
    def stamp(self, module, at, rotate=0, mirror=False, air=False):
        """Paste another Scene with its (0,0,0) at `at`. rotate = quarter turns clockwise (from above).
        air=False: the module's air doesn't overwrite. structure_void never overwrites."""
        m = module.transformed(rotate, mirror)
        x0, y0, z0 = at
        X, Y, Z = self.shape
        sx, sy, sz = m.shape
        a0 = [max(0, -v) for v in (x0, y0, z0)]
        b0 = [max(0, v) for v in (x0, y0, z0)]
        n = [min(s - a, S - b) for s, a, S, b in zip((sx, sy, sz), a0, (X, Y, Z), b0)]
        if min(n) <= 0:
            return
        src = m.idx[a0[0]:a0[0] + n[0], a0[1]:a0[1] + n[1], a0[2]:a0[2] + n[2]]
        remap = np.array([self.id(s) for s in m.palette], np.int32)
        ids = remap[src]
        ok = np.ones(src.shape, bool)
        void = m._lut.get(VOID)
        if void is not None:
            ok &= src != void
        if not air:
            ok &= src != 0
        dst = self.idx[b0[0]:b0[0] + n[0], b0[1]:b0[1] + n[1], b0[2]:b0[2] + n[2]]
        dst[ok] = ids[ok]
        # block entities: drop ours under written cells, then copy the module's
        for k in [k for k in self.be if all(b0[i] <= k[i] < b0[i] + n[i] for i in range(3))
                  and ok[k[0] - b0[0], k[1] - b0[1], k[2] - b0[2]]]:
            del self.be[k]
        for (mx, my, mz), t in m.be.items():
            lx, ly, lz = mx - a0[0], my - a0[1], mz - a0[2]
            if 0 <= lx < n[0] and 0 <= ly < n[1] and 0 <= lz < n[2] and ok[lx, ly, lz]:
                self.be[(mx + x0, my + y0, mz + z0)] = t
        for e in m.entities:
            p = [e["pos"][0] + x0, e["pos"][1] + y0, e["pos"][2] + z0]
            if 0 <= p[0] < X and 0 <= p[1] < Y and 0 <= p[2] < Z:
                self.entities.append({"pos": p, "nbt": e["nbt"]})
        for k, v in m.markers.items():
            self.markers.setdefault(k, {**v, "pos": [p + o for p, o in zip(v["pos"], at)]})

    def transformed(self, rotate=0, mirror=False):
        """Copy rotated k quarter turns clockwise (seen from above), optionally mirrored east<->west first."""
        out = Scene(self.shape, self.name, self.seed)
        idx = self.idx
        pal = list(self.palette)
        if mirror:
            idx = idx[::-1]
            pal = [bs.mirror_x(p) for p in pal]
        k = rotate % 4
        if k:
            idx = np.rot90(idx, k, axes=(0, 2))
            pal = [bs.rotate(p, k) for p in pal]
        out.idx = np.zeros(idx.shape, np.uint16)
        remap = np.array([out.id(p) for p in pal], np.uint16)
        out.idx = remap[idx]
        from .nbt import transform_entity
        for (x, y, z), t in self.be.items():
            px, _, pz = self._tf_point((x + 0.5, y, z + 0.5), k, mirror)
            out.be[(int(px), y, int(pz))] = t
        for e in self.entities:
            out.entities.append({"pos": list(self._tf_point(e["pos"], k, mirror)), "nbt": transform_entity(e["nbt"], k, mirror)})
        for name, mk in self.markers.items():
            out.markers[name] = {**mk, "pos": list(self._tf_point(mk["pos"], k, mirror))}
            if mk.get("look_at"):
                out.markers[name]["look_at"] = list(self._tf_point(mk["look_at"], k, mirror))
            if mk.get("yaw") is not None:
                out.markers[name]["yaw"] = ((-mk["yaw"] if mirror else mk["yaw"]) + 90 * k) % 360
        return out

    def _tf_point(self, p, k, mirror):
        """Continuous point (block units, corner-based) through mirror + k clockwise turns."""
        X, _, Z = self.shape
        x, y, z = p
        if mirror:
            x = X - x
        for _ in range(k):  # clockwise from above: (x, z) -> (Z - z, x) on a Z x X grid
            x, z = Z - z, x
            X, Z = Z, X
        return x, y, z

    def crop(self, p0, p1):
        """Sub-scene (inclusive corners)."""
        lo = [min(a, b) for a, b in zip(p0, p1)]; hi = [max(a, b) + 1 for a, b in zip(p0, p1)]
        out = Scene([h - l for l, h in zip(lo, hi)], self.name, self.seed)
        sub = self.idx[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
        u = np.unique(sub)
        remap = np.zeros(len(self.palette), np.uint16)
        for i in u:
            remap[i] = out.id(self.palette[i])
        out.idx = remap[sub]
        for (x, y, z), t in self.be.items():
            if all(lo[i] <= v < hi[i] for i, v in enumerate((x, y, z))):
                out.be[(x - lo[0], y - lo[1], z - lo[2])] = t
        for e in self.entities:
            if all(lo[i] <= v < hi[i] for i, v in enumerate(e["pos"])):
                out.entities.append({"pos": [v - lo[i] for i, v in enumerate(e["pos"])], "nbt": e["nbt"]})
        return out

    # ------------------------------------------------------------ markers
    def mark(self, name, pos, yaw=None, look_at=None):
        """Named point (scene coords): cameras ("spawn_*", "cam_*" are rendered at eye level), notes for the build."""
        self.markers[name] = {"pos": [float(v) for v in pos], "yaw": yaw,
                              "look_at": None if look_at is None else [float(v) for v in look_at]}

    # ------------------------------------------------------------ io
    def compacted(self):
        """Copy with unused palette entries dropped (air stays 0)."""
        u = np.unique(self.idx)
        out = Scene(self.shape, self.name, self.seed)
        remap = np.zeros(len(self.palette), np.uint16)
        for i in u:
            remap[i] = out.id(self.palette[i])
        out.idx = remap[self.idx]
        out.markers, out.meta = dict(self.markers), dict(self.meta)
        out.be, out.entities = dict(self.be), list(self.entities)
        return out

    def save(self, path):
        c = self.compacted()
        from .nbt import snbt
        info = {"name": self.name, "markers": self.markers, "meta": self.meta,
                "be": [[x, y, z, snbt(t)] for (x, y, z), t in sorted(self.be.items())],
                "entities": [{"pos": e["pos"], "nbt": snbt(e["nbt"])} for e in self.entities]}
        np.savez_compressed(path, idx=c.idx, palette=np.array(json.dumps(c.palette)), info=np.array(json.dumps(info)))

    @classmethod
    def load(cls, path):
        d = np.load(path, allow_pickle=False)
        info = json.loads(str(d["info"]))
        s = cls(d["idx"].shape, info.get("name", Path(path).stem))
        pal = json.loads(str(d["palette"]))
        remap = np.array([s.id(p) for p in pal], np.uint16)
        s.idx = remap[d["idx"]]
        s.markers, s.meta = info.get("markers", {}), info.get("meta", {})
        if info.get("be") or info.get("entities"):
            from .nbt import to_tag
            s.be = {(x, y, z): to_tag(t) for x, y, z, t in info.get("be", [])}
            s.entities = [{"pos": e["pos"], "nbt": to_tag(e["nbt"])} for e in info.get("entities", [])]
        return s

    def __repr__(self):
        return f"<Scene {self.name} {self.shape} {len(self.palette)} states>"
