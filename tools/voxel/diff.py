"""Diff two scenes of the same size (usually: the source scene vs. what was pulled back from the server).

    d = diff(source, pulled)       # ignores neighbour-shape props (fence/wall/pane connections, stair shape) by default
    print(d.summary())             # counts, top transitions, clusters with bounding boxes
    d.write_patch("x.patch.json")  # [[x,y,z,"state"], ...]: the in-game edits, in scene coordinates
    d.render(out_dir)              # pulled scene, unchanged blocks dimmed, added green, changed yellow, removed = red glass

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

    @property
    def n(self):
        return int(self.changed.sum())

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
        return [[int(x), int(y), int(z), self.b.palette[self.b.idx[x, y, z]]] for x, y, z in np.argwhere(self.changed)]

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
    for x, y, z, st in patch:
        if 0 <= x < X and 0 <= y < Y and 0 <= z < Z:
            scene.idx[x, y, z] = scene.id(st)
            n += 1
    return n
