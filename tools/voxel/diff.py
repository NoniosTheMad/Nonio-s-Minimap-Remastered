"""Diff two scenes of the same size (usually: the source scene vs. what was pulled back from the server).

    d = diff(source, pulled)       # ignores neighbour-shape props (fence/wall/pane connections, stair shape) by default
    print(d.summary())             # counts, top transitions, clusters with bounding boxes
    d.write_patch("x.patch.json")  # [[x,y,z,"state"], ...]: the in-game edits, in scene coordinates
    d.render(out_dir)              # pulled scene, unchanged blocks dimmed, added green, changed yellow, removed = red glass

Block entities (chest contents, sign text, banner patterns, ...) and entities (item frames, paintings, armour stands)
are compared too: the source's data must be contained in what the world holds (the game adds defaults), see nbt.subset.
Patch cells are [x,y,z,state] or [x,y,z,state,snbt]; entity edits are {"entity_add": {pos, nbt}} / {"entity_remove": {pos, id}}.

A patch named <scene>.patch.json next to the scene file is applied automatically by the CLI after build()
(merge an edit for good by moving it into the scene code and deleting the patch)."""
import json
from collections import Counter
from pathlib import Path

import numpy as np

from . import blockstate as bs
from .connect import strip_shape
from .scene import AIR, VOID, Scene

REMOVED = "minecraft:red_stained_glass"


class Diff:
    def __init__(self, a: Scene, b: Scene, ignore_shape=True):
        if a.shape != b.shape:
            raise ValueError(f"size mismatch {a.shape} vs {b.shape}")
        self.a, self.b = a, b
        key = strip_shape if ignore_shape else (lambda s: s)
        # map both palettes into one key space
        keys = {}
        ka = np.array([keys.setdefault(key(s), len(keys)) for s in a.palette], np.int32)
        kb = np.array([keys.setdefault(key(s), len(keys)) for s in b.palette], np.int32)
        va, vb = ka[a.idx], kb[b.idx]
        void_a = a._lut.get(VOID, -1); void_b = b._lut.get(VOID, -1)
        valid = (a.idx != void_a) & (b.idx != void_b)
        self.changed = (va != vb) & valid
        air_a = a.idx == 0
        air_b = b.idx == 0
        self.added = self.changed & air_a
        self.removed = self.changed & air_b
        self.replaced = self.changed & ~air_a & ~air_b
        self.unknown = ~valid
        self._extras(valid)

    DECOR = ("item_frame", "glow_item_frame", "painting", "armor_stand", "item_display", "block_display", "text_display",
             "leash_knot")

    def _extras(self, valid):
        """Block entity + entity differences (only where the block itself didn't change)."""
        from .nbt import norm, subset
        a, b = self.a, self.b
        abe = a.block_entities()
        self.be_changed = []   # [(pos, path)]
        for pos, t in abe.items():
            if self.changed[pos] or not valid[pos]:
                continue
            got = b.be.get(pos)
            ok, path = subset(norm(t), norm(got) if got is not None else {})
            if not ok:
                self.be_changed.append((pos, path or "(missing)"))
        # entities: greedy match by id + distance
        used = set()
        self.ent_missing, self.ent_changed, self.ent_extra = [], [], []
        for e in a.entities:
            eid = str(e["nbt"]["id"])
            best, bd = None, 0.75
            for j, f in enumerate(b.entities):
                if j in used or str(f["nbt"].get("id")) != eid:
                    continue
                d = sum((u - v) ** 2 for u, v in zip(e["pos"], f["pos"])) ** 0.5
                if d < bd:
                    best, bd = j, d
            if best is None:
                self.ent_missing.append(e)
                continue
            used.add(best)
            ok, path = subset(norm(e["nbt"]), norm(b.entities[best]["nbt"]))
            if not ok:
                self.ent_changed.append((e, b.entities[best], path))
        for j, f in enumerate(b.entities):
            if j not in used and str(f["nbt"].get("id")).split(":")[-1] in self.DECOR:
                self.ent_extra.append(f)

    @property
    def n(self):
        return int(self.changed.sum())

    @property
    def n_extra(self):
        return len(self.be_changed) + len(self.ent_missing) + len(self.ent_changed) + len(self.ent_extra)

    def transitions(self, top=12):
        pts = np.argwhere(self.changed)
        c = Counter((bs.short(self.a.palette[self.a.idx[tuple(p)]]), bs.short(self.b.palette[self.b.idx[tuple(p)]])) for p in pts)
        return c.most_common(top)

    def clusters(self, top=10):
        from scipy import ndimage
        lab, n = ndimage.label(self.changed, structure=np.ones((3, 3, 3)))
        if not n:
            return []
        sl = ndimage.find_objects(lab)
        sizes = np.bincount(lab.ravel())[1:]
        out = []
        for i in np.argsort(-sizes)[:top]:
            s = sl[i]
            out.append(dict(blocks=int(sizes[i]), min=[s[0].start, s[1].start, s[2].start],
                            max=[s[0].stop - 1, s[1].stop - 1, s[2].stop - 1]))
        return out

    def patch(self):
        from .nbt import be_id, snbt
        out = []
        cells = [tuple(int(v) for v in p) for p in np.argwhere(self.changed)] + [p for p, _ in self.be_changed]
        for x, y, z in cells:
            st = self.b.palette[self.b.idx[x, y, z]]
            t = self.b.be.get((x, y, z))
            out.append([x, y, z, st] + ([snbt(t)] if t is not None and be_id(bs.name_of(st)) else []))
        for e in self.ent_missing:
            out.append({"entity_remove": {"pos": e["pos"], "id": str(e["nbt"]["id"])}})
        for e, f, _ in self.ent_changed:
            out.append({"entity_remove": {"pos": e["pos"], "id": str(e["nbt"]["id"])}})
            out.append({"entity_add": {"pos": f["pos"], "nbt": snbt(f["nbt"])}})
        for f in self.ent_extra:
            out.append({"entity_add": {"pos": f["pos"], "nbt": snbt(f["nbt"])}})
        return out

    def write_patch(self, path):
        return write_patch_list(path, self.patch())

    def summary(self, origin=None):
        L = [f"{self.n} changed block(s): {int(self.added.sum())} added, {int(self.removed.sum())} removed, "
             f"{int(self.replaced.sum())} replaced" + (f"  ({int(self.unknown.sum())} cells not comparable: void/unsaved)" if self.unknown.any() else "")]
        if self.n:
            L.append("top transitions (before -> after):")
            L += [f"  {k:5d}  {a} -> {b}" for (a, b), k in self.transitions()]
            L.append("clusters (scene coords" + (", world = scene + origin " + str(list(origin)) if origin is not None else "") + "):")
            for c in self.clusters():
                w = ""
                if origin is not None:
                    w = f"   world {[m + o for m, o in zip(c['min'], origin)]}..{[m + o for m, o in zip(c['max'], origin)]}"
                L.append(f"  {c['blocks']:5d} blocks  {c['min']}..{c['max']}{w}")
        def plural(n, one, many):
            return f"{n} {one if n == 1 else many}"
        if self.be_changed:
            L.append(plural(len(self.be_changed), "block entity", "block entities") + " changed (block kept):")
            for pos, path in self.be_changed[:12]:
                L.append(f"  {list(pos)}  {bs.short(self.b.palette[self.b.idx[pos]])}  at {path}")
        def ep(e):
            return f"{str(e['nbt']['id']).replace('minecraft:', '')} @ {[round(v, 2) for v in e['pos']]}"
        if self.ent_missing:
            L.append(plural(len(self.ent_missing), "entity", "entities") + " missing: " + ", ".join(ep(e) for e in self.ent_missing[:8]))
        if self.ent_changed:
            L.append(plural(len(self.ent_changed), "entity", "entities") + " changed: " + ", ".join(f"{ep(e)} at {p}" for e, _, p in self.ent_changed[:8]))
        if self.ent_extra:
            L.append(plural(len(self.ent_extra), "new decor entity", "new decor entities") + ": " + ", ".join(ep(e) for e in self.ent_extra[:8]))
        return "\n".join(L)

    def render(self, out, **kw):
        """Views of the AFTER scene with the changes highlighted (removed blocks as red glass)."""
        from .render import render_views
        s = Scene(self.b.shape, self.b.name + "_diff")
        s.palette = list(self.b.palette); s._lut = dict(self.b._lut); s._names = list(self.b._names)
        s.idx = self.b.idx.copy()
        s.markers = dict(self.a.markers)
        void = s._lut.get(VOID)
        if void is not None:
            s.idx[s.idx == void] = 0
        s.idx[self.removed] = s.id(REMOVED)
        t = np.full(s.shape + (3,), 0.55, np.float32)  # unchanged: dimmed
        t[self.added] = (0.7, 1.35, 0.7)
        t[self.replaced] = (1.4, 1.25, 0.45)
        t[self.removed] = (1.3, 0.7, 0.7)
        for pos, _ in self.be_changed:
            t[pos] = (1.4, 1.25, 0.45)
        s.be, s.entities = dict(self.b.be), list(self.b.entities)
        return render_views(s, out, vtint=t, sightlines=False, **kw)


def diff(a, b, ignore_shape=True):
    return Diff(a, b, ignore_shape)


def write_patch_list(path, cells):
    """One cell per line: readable in a git diff."""
    Path(path).write_text("[\n" + ",\n".join(json.dumps(c) for c in cells) + "\n]\n")
    return path


def apply_patch(scene: Scene, patch):
    """patch = path or list of [x,y,z,state]. Out-of-range cells are ignored. Returns the number of cells set."""
    if not isinstance(patch, list):
        patch = json.loads(Path(patch).read_text())
    n = 0
    X, Y, Z = scene.shape
    for c in patch:
        if isinstance(c, dict):
            if "entity_remove" in c:
                r = c["entity_remove"]
                for e in list(scene.entities):
                    if str(e["nbt"]["id"]) == r["id"] and sum((u - v) ** 2 for u, v in zip(e["pos"], r["pos"])) < 0.5:
                        scene.entities.remove(e)
                        n += 1
                        break
            elif "entity_add" in c:
                scene.entity(c["entity_add"]["nbt"], c["entity_add"]["pos"])
                n += 1
            continue
        x, y, z, st = c[:4]
        if 0 <= x < X and 0 <= y < Y and 0 <= z < Z:
            scene.set(x, y, z, st, nbt=c[4] if len(c) > 4 else None)
            n += 1
    return n
