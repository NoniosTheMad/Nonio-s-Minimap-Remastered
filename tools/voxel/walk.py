"""Walkability check for a scene: where can a player get from the spawns, and can they get back?

    python -m tools.voxel.walk scenes/orrery.py [--spawn spawn_white,spawn_black] [--json out.json]

Model (conservative, vanilla survival without placing blocks):
- a standing node = a support block (full: top at y+1, bottom slab: y+.5) with two passable cells above;
- walk to a neighbour column: step up <= 1.25 (jump), or walk off and fall to the first support below;
  falls > 3 hurt, falls >= 23 kill a full-health player (lethal: an exit only by dying); water cancels the fall;
- water cells are swimmable in 6 directions; climb out onto a support whose top is <= 2 above the water cell;
- ladders climb up/down; step off a ladder onto supports within 1.5.
Reports: nodes reachable from the spawns; TRAPS = reachable places with no non-lethal way back to a spawn
(hard: no lethal exit either; soft: only by jumping to your death), clustered; lethal drop edges (deliberate fall
risks); per zone in scene.meta['zones'] whether it is reachable both ways.
Standalone module: nothing else in tools.voxel depends on it."""
import argparse
import json
import math
import sys
from collections import deque

import numpy as np

from . import blockstate as bs
from .stats import passable as _passable

LETHAL = 23.0
STEP = 1.25


def _short(n):
    return n.split(":", 1)[-1]


def classify(palette):
    """Per palette entry: (kind, height). kind: 0 passable, 1 support, 2 water, 3 ladder, 4 lava/blocked-tall."""
    out = []
    for st in palette:
        name, p = bs.parse(st)
        s = _short(name)
        if s in ("water", "bubble_column") or p.get("waterlogged") == "true" and _passable(st):
            out.append((2, 0.0))
        elif s in ("ladder", "scaffolding") or s.endswith("vines_plant") or s in ("vine", "cave_vines", "twisting_vines", "weeping_vines"):
            out.append((3, 0.0))
        elif s == "lava":
            out.append((4, 0.0))
        elif _passable(st) or s in ("hanging_roots", "pale_hanging_moss", "amethyst_cluster", "large_amethyst_bud",
                                     "medium_amethyst_bud", "small_amethyst_bud", "pointed_dripstone") or s.endswith(("_chain", "chain")):
            out.append((0, 0.0))
        elif s.endswith("_slab"):
            out.append((1, 0.5 if p.get("type", "bottom") == "bottom" else 1.0))
        elif s.endswith(("_wall", "_fence", "_fence_gate")) or s in ("iron_bars",) or s.endswith("_bars"):
            out.append((4, 1.5))
        elif s.endswith("_carpet") or s in ("moss_carpet", "pale_moss_carpet"):
            out.append((0, 0.0))
        else:
            out.append((1, 1.0))
    return out


class Walk:
    def __init__(self, scene):
        self.s = scene
        cl = classify(scene.palette)
        kind = np.array([k for k, _ in cl], np.int8)
        hgt = np.array([h for _, h in cl], np.float32)
        self.kind = kind[scene.idx]
        self.hgt = hgt[scene.idx]
        X, Y, Z = scene.shape
        self.X, self.Y, self.Z = X, Y, Z
        self.free = (self.kind == 0) | (self.kind == 2) | (self.kind == 3)
        self._nodes()

    # --------------------------------------------------------------- nodes
    def _nodes(self):
        k, free = self.kind, self.free
        sup = (k == 1)
        f1 = np.zeros_like(free); f1[:, :-1] = free[:, 1:]
        f2 = np.zeros_like(free); f2[:, :-2] = free[:, 2:]
        stand = sup & f1 & f2
        xs, ys, zs = np.nonzero(stand)
        L = ys + self.hgt[xs, ys, zs]
        self.ids = {}
        self.pos = []
        self.col = {}
        for x, y, z, l in zip(xs.tolist(), ys.tolist(), zs.tolist(), L.tolist()):
            i = len(self.pos)
            self.pos.append(("s", x, z, l, y))
            self.ids[("s", x, y, z)] = i
            self.col.setdefault((x, z), []).append(i)
        wx, wy, wz = np.nonzero(k == 2)
        for x, y, z in zip(wx.tolist(), wy.tolist(), wz.tolist()):
            i = len(self.pos)
            self.pos.append(("w", x, z, float(y), y))
            self.ids[("w", x, y, z)] = i
        lx, ly, lz = np.nonzero(k == 3)
        for x, y, z in zip(lx.tolist(), ly.tolist(), lz.tolist()):
            i = len(self.pos)
            self.pos.append(("l", x, z, float(y), y))
            self.ids[("l", x, y, z)] = i
        self.n = len(self.pos)

    def _land(self, x, z, fs):
        """Fall in column (x, z) from feet cell fs: -> (node id, landing level) or None if blocked."""
        if not (0 <= x < self.X and 0 <= z < self.Z) or fs < 0:
            return None
        Y = self.Y
        if fs + 1 < Y and not (self.free[x, fs, z] and self.free[x, min(fs + 1, Y - 1), z]):
            return None
        y = min(fs, Y - 1)
        while y >= 0:
            kk = self.kind[x, y, z]
            if kk == 2:
                return self.ids.get(("w", x, y, z)), float(y), True
            if kk == 3:
                return self.ids.get(("l", x, y, z)), float(y), True
            if kk in (1, 4):
                i = self.ids.get(("s", x, y, z))
                if i is None:
                    return None
                return i, y + float(self.hgt[x, y, z]), False
            y -= 1
        return None   # fell out of the world: lethal

    def edges(self, i):
        """[(j, fall_distance_or_0, lethal)]"""
        t, x, z, L, y = self.pos[i]
        out = []
        D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
        if t == "s":
            fs = int(math.ceil(L)) if L != int(L) else int(L)
            for dx, dz in D4:
                nx, nz = x + dx, z + dz
                if not (0 <= nx < self.X and 0 <= nz < self.Z):
                    continue
                best = None
                for j in self.col.get((nx, nz), ()):
                    Lj = self.pos[j][3]
                    if L < Lj <= L + STEP:
                        # jump/step clearance above the source
                        if Lj - L > 0.5 and fs + 2 < self.Y and not self.free[x, fs + 2, z]:
                            continue
                        if best is None or Lj < self.pos[best][3]:
                            best = j
                if best is not None:
                    out.append((best, 0.0, False))
                r = self._land(nx, nz, fs)
                if r is not None and r[0] is not None:
                    j, Lj, soft = r
                    d = 0.0 if soft else L - Lj
                    out.append((j, d, d >= LETHAL))
                elif r is None and self.free[nx, min(fs, self.Y - 1), nz] and self.free[nx, min(fs + 1, self.Y - 1), nz]:
                    out.append((-1, 999.0, True))      # into the void
                # ladder / water at feet level in the neighbour column
                for yy in (fs, fs + 1):
                    if 0 <= yy < self.Y:
                        for tt in ("l", "w"):
                            j = self.ids.get((tt, nx, yy, nz))
                            if j is not None:
                                out.append((j, 0.0, False))
            for yy in (fs, fs + 1):
                j = self.ids.get(("l", x, yy, z))
                if j is not None:
                    out.append((j, 0.0, False))
        else:
            yy = y
            for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0)):
                nx, ny, nz = x + dx, yy + dy, z + dz
                for tt in ("w", "l"):
                    j = self.ids.get((tt, nx, ny, nz))
                    if j is not None:
                        out.append((j, 0.0, False))
            reach = 2.0 if t == "w" else 1.5
            for dx, dz in D4 + ((0, 0),):
                nx, nz = x + dx, z + dz
                for j in self.col.get((nx, nz), ()):
                    Lj = self.pos[j][3]
                    if yy - 1 <= Lj <= yy + reach:
                        out.append((j, 0.0, False))
            if t == "l":   # let go of the ladder: fall
                r = self._land(x, z, yy - 1) if yy - 1 >= 0 else None
                if r and r[0] is not None:
                    d = 0.0 if r[2] else yy - r[1]
                    out.append((r[0], d, d >= LETHAL))
        return out

    def nearest(self, p):
        x, y, z = (int(math.floor(v)) for v in p)
        best, bd = None, 1e9
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                for j in self.col.get((x + dx, z + dz), ()):
                    d = abs(dx) + abs(dz) + abs(self.pos[j][3] - y)
                    if d < bd:
                        best, bd = j, d
        return best

    def analyse(self, starts):
        fwd = np.zeros(self.n, bool)
        adj = [None] * self.n
        lethal_edges = 0
        hurts = 0
        q = deque(s for s in starts if s is not None)
        for s in q:
            fwd[s] = True
        has_lethal = np.zeros(self.n, bool)
        while q:
            i = q.popleft()
            es = self.edges(i)
            adj[i] = es
            for j, d, leth in es:
                if leth:
                    has_lethal[i] = True
                    lethal_edges += 1
                    continue
                if d > 3:
                    hurts += 1
                if j >= 0 and not fwd[j]:
                    fwd[j] = True
                    q.append(j)
        # reverse reachability inside the forward set
        radj = {}
        for i in np.nonzero(fwd)[0].tolist():
            for j, d, leth in adj[i]:
                if not leth and j >= 0:
                    radj.setdefault(j, []).append(i)
        back = np.zeros(self.n, bool)
        q = deque(s for s in starts if s is not None)
        for s in q:
            back[s] = True
        while q:
            j = q.popleft()
            for i in radj.get(j, ()):
                if not back[i]:
                    back[i] = True
                    q.append(i)
        trap = fwd & ~back
        return dict(fwd=fwd, back=back, trap=trap, has_lethal=has_lethal, lethal_edges=lethal_edges, hurts=hurts, adj=adj)

    def clusters(self, mask):
        idx = np.nonzero(mask)[0].tolist()
        sel = set(idx)
        seen = set()
        out = []
        for i in idx:
            if i in seen:
                continue
            comp = []
            q = deque([i]); seen.add(i)
            while q:
                a = q.popleft(); comp.append(a)
                t, x, z, L, y = self.pos[a]
                for dx in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        for dy in (-2, -1, 0, 1, 2):
                            for tt in ("s", "w", "l"):
                                b = self.ids.get((tt, x + dx, y + dy, z + dz))
                                if b is not None and b in sel and b not in seen:
                                    seen.add(b); q.append(b)
            out.append(comp)
        out.sort(key=len, reverse=True)
        return out


def run(scene, spawns=None, quiet=False):
    w = Walk(scene)
    names = spawns or [k for k in scene.markers if k.startswith("spawn_")]
    starts = [w.nearest(scene.markers[k]["pos"]) for k in names]
    r = w.analyse(starts)
    trap_cl = w.clusters(r["trap"])
    rep = {"nodes": w.n, "reachable": int(r["fwd"].sum()), "return": int((r["fwd"] & r["back"]).sum()),
           "lethal_drops": r["lethal_edges"], "hurting_drops": r["hurts"], "traps": []}
    for comp in trap_cl:
        hard = not any(r["has_lethal"][i] for i in comp)
        P = np.array([(w.pos[i][1], w.pos[i][3], w.pos[i][2]) for i in comp], float)
        rep["traps"].append({"size": len(comp), "hard": hard, "centre": [round(v, 1) for v in P.mean(0)],
                             "example": [int(P[0][0]), round(float(P[0][1]), 1), int(P[0][2])]})
    zones = scene.meta.get("zones") or []
    rz = []
    ok = r["fwd"] & r["back"]
    for zn in zones:
        x0, y0, z0, x1, y1, z1 = zn["box"]
        n_in = 0
        for i in np.nonzero(ok)[0].tolist():
            t, x, z, L, y = w.pos[i]
            if x0 <= x <= x1 and z0 <= z <= z1 and y0 - 0.6 <= L <= y1:
                n_in += 1
        rz.append({"zone": zn["name"], "walkable_nodes": n_in, "ok": n_in > 0})
    rep["zones"] = rz
    if not quiet:
        print(f"[walk] {rep['nodes']} nodes; reachable from {','.join(names)}: {rep['reachable']}, with a way back: {rep['return']}")
        print(f"[walk] lethal drop edges {rep['lethal_drops']} (deliberate fall risks), hurting drops {rep['hurting_drops']}")
        hard = [t for t in rep["traps"] if t["hard"]]
        soft = [t for t in rep["traps"] if not t["hard"]]
        print(f"[walk] traps: {len(hard)} hard (no way out), {len(soft)} soft (only by dying); cells {sum(t['size'] for t in rep['traps'])}")
        for t in rep["traps"][:25]:
            print(f"   {'HARD' if t['hard'] else 'soft'} size {t['size']:5d} centre {t['centre']} e.g. {t['example']}")
        for z in rz:
            print(f"   zone {z['zone']:<22} {'OK ' if z['ok'] else 'UNREACHABLE'} ({z['walkable_nodes']} nodes)")
    return rep, w, r


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m tools.voxel.walk")
    ap.add_argument("scene")
    ap.add_argument("--spawn", default=None, help="comma list of marker names (default: every spawn_*)")
    ap.add_argument("--json", default=None)
    a = ap.parse_args(argv)
    from .__main__ import load_scene
    s = load_scene(a.scene)
    rep, _, _ = run(s, a.spawn.split(",") if a.spawn else None)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(rep, f, indent=1)
    hard = sum(1 for t in rep["traps"] if t["hard"] and t["size"] >= 1)
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
