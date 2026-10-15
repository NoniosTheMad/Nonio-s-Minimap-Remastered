"""Room decorators: furnish an empty room shell with kits, keeping walkable paths between the doors and to every piece.

    from tools.voxel.kits import rooms
    rep = rooms.furnish(scene, (x0, y0, z0, x1, y1, z1), "hall", "keep", doors=[(x, y0, z0 - 1)], seed=3)

box = the room's interior AIR volume, inclusive: y0 = first air row above the floor, y1 = last air row under the ceiling;
walls are the cells just outside the box. doors = wall cells (door openings) the room is entered through; the wall
opposite the first door is the room's "back" (focal end: throne, altar, hearth, bed).

How it works: greedy placement of a per-kind program (focal piece, wall pieces, centre pieces, clutter, lights).
Every placement is tried at candidate spots in order of preference and kept only if, afterwards, all doors still
connect and every placed piece's front ("use") cells are reachable on foot (2 tall passable). Ceiling beams, hanging
lights and wall sconces don't touch the floor. Kinds: hall, bedroom, library, kitchen, chapel, armoury, cellar, lab."""
import random
from collections import deque

import numpy as np

from .. import blockstate as bs
from ..stats import passable
from . import furniture as F
from .style import STYLES

WALLS = {  # wall side -> (facing into the room, axis along the wall)
    "N": "south", "S": "north", "W": "east", "E": "west",
}
OPP = {"N": "S", "S": "N", "W": "E", "E": "W"}


class Room:
    def __init__(self, s, box, style, doors=(), seed=0):
        self.s = s
        self.x0, self.y0, self.z0, self.x1, self.y1, self.z1 = box
        self.st = STYLES[style] if isinstance(style, str) else style
        self.rng = random.Random(seed)
        self.seed = seed
        self.doors = [tuple(d) for d in doors]
        self.entries = [self._entry(d) for d in self.doors]
        self.uses = []          # cells that must stay reachable
        self.placed = []        # (label, lo, hi)
        self.W = self.x1 - self.x0 + 1
        self.D = self.z1 - self.z0 + 1
        self.H = self.y1 - self.y0 + 1
        self.back = OPP[self._side(self.doors[0])] if self.doors else "N"
        self.long_x = self.W >= self.D

    # ---------------------------------------------------------------- geometry
    def _side(self, d):
        x, _, z = d
        if z < self.z0: return "N"
        if z > self.z1: return "S"
        if x < self.x0: return "W"
        return "E"

    def _entry(self, d):
        x, y, z = d
        return (min(max(x, self.x0), self.x1), min(max(z, self.z0), self.z1))

    def inside(self, x, z):
        return self.x0 <= x <= self.x1 and self.z0 <= z <= self.z1

    def walk(self):
        """Walkable floor cells: 2 tall passable column at y0, y0+1."""
        s = self.s
        sub = s.idx[self.x0:self.x1 + 1, self.y0:self.y0 + 2, self.z0:self.z1 + 1]
        u = np.unique(sub)
        ok = np.zeros(len(s.palette), bool)
        for i in u:
            ok[i] = passable(s.palette[i]) and "_bed" not in s.palette[i]
        p = ok[sub]
        return p[:, 0, :] & p[:, 1, :]

    def connected(self):
        w = self.walk()
        if not self.entries:
            return True
        seen = np.zeros_like(w)
        q = deque()
        for ex, ez in self.entries:
            i, j = ex - self.x0, ez - self.z0
            if not w[i, j]:
                return False
            seen[i, j] = True
            q.append((i, j))
        q = deque([q[0]]); seen[:] = False; seen[q[0]] = True
        while q:
            i, j = q.popleft()
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = i + di, j + dj
                if 0 <= a < w.shape[0] and 0 <= b < w.shape[1] and w[a, b] and not seen[a, b]:
                    seen[a, b] = True
                    q.append((a, b))
        need = [(ex - self.x0, ez - self.z0) for ex, ez in self.entries] + \
               [(x - self.x0, z - self.z0) for x, z in self.uses if self.inside(x, z)]
        return all(seen[i, j] for i, j in need)

    def _air(self, lo, hi):
        sub = self.s.idx[lo[0]:hi[0] + 1, lo[1]:hi[1] + 1, lo[2]:hi[2] + 1]
        return bool((sub == 0).all())

    # ---------------------------------------------------------------- placement
    def try_place(self, label, kit, at, facing, uses=True, need_floor=True, check=True):
        """Stamp if the kit's box is inside the room and empty; keep it only if paths survive. Returns bool."""
        sx, sy, sz = kit.shape if facing in ("south", "north") else (kit.shape[2], kit.shape[1], kit.shape[0])
        lo = tuple(at); hi = (at[0] + sx - 1, at[1] + sy - 1, at[2] + sz - 1)
        if not (self.x0 <= lo[0] and hi[0] <= self.x1 and self.z0 <= lo[2] and hi[2] <= self.z1
                and self.y0 <= lo[1] and hi[1] <= self.y1):
            return False
        if not self._air(lo, hi):
            return False
        if any(lo[0] <= ex <= hi[0] and lo[2] <= ez <= hi[2] for ex, ez in self.entries) and need_floor:
            return False
        snap = (self.s.idx[lo[0]:hi[0] + 1, lo[1]:hi[1] + 1, lo[2]:hi[2] + 1].copy(), dict(self.s.be), list(self.s.entities))
        F.place(self.s, kit, lo, facing)
        new_uses = self._front(lo, hi, facing) if uses else []
        self.uses += new_uses
        if check and need_floor and not self.connected():
            self.s.idx[lo[0]:hi[0] + 1, lo[1]:hi[1] + 1, lo[2]:hi[2] + 1] = snap[0]
            self.s.be.clear(); self.s.be.update(snap[1])
            self.s.entities[:] = snap[2]
            del self.uses[len(self.uses) - len(new_uses):]
            return False
        self.placed.append((label, lo, hi))
        return True

    def _front(self, lo, hi, facing):
        if facing == "south":
            return [((lo[0] + hi[0]) // 2, hi[2] + 1)]
        if facing == "north":
            return [((lo[0] + hi[0]) // 2, lo[2] - 1)]
        if facing == "east":
            return [(hi[0] + 1, (lo[2] + hi[2]) // 2)]
        return [(lo[0] - 1, (lo[2] + hi[2]) // 2)]

    def wall_spots(self, side, kit, y=None, order="centre"):
        """Candidate min corners for `kit` with its back against wall `side`, ordered."""
        y = self.y0 if y is None else y
        f = WALLS[side]
        w, d = kit.shape[0], kit.shape[2]
        if side in ("N", "S"):
            z = self.z0 if side == "N" else self.z1 - d + 1
            xs = list(range(self.x0, self.x1 - w + 2))
            c = (self.x0 + self.x1 - w + 1) / 2
            key = (lambda v: abs(v - c)) if order == "centre" else (lambda v: min(v - self.x0, self.x1 - w + 1 - v))
            return [((x, y, z), f) for x in sorted(xs, key=key)]
        x = self.x0 if side == "W" else self.x1 - d + 1
        zs = list(range(self.z0, self.z1 - w + 2))
        c = (self.z0 + self.z1 - w + 1) / 2
        key = (lambda v: abs(v - c)) if order == "centre" else (lambda v: min(v - self.z0, self.z1 - w + 1 - v))
        return [((x, y, z), f) for z in sorted(zs, key=key)]

    def on_wall(self, label, kit, sides, order="centre", y=None, n=1, **kw):
        """Place up to n copies along the given walls (first fitting spots in `order`: centre-out or ends-in)."""
        got = 0
        for side in sides:
            for at, f in self.wall_spots(side, kit, y, order):
                if got >= n:
                    return got
                if self.try_place(label, kit, at, f, **kw):
                    got += 1
        return got

    def side_walls(self):
        b = self.back
        return [s for s in ("N", "S", "W", "E") if s not in (b, OPP[b])]

    def centre(self, label, kit, facing=None, dz=0):
        """Centre piece on the room's middle, long side along the room's long axis."""
        facing = facing or ("south" if self.long_x else "east")
        sx, sz = (kit.shape[0], kit.shape[2]) if facing in ("south", "north") else (kit.shape[2], kit.shape[0])
        cx = (self.x0 + self.x1 + 1 - sx) // 2
        cz = (self.z0 + self.z1 + 1 - sz) // 2
        for d in (0, 1, -1, 2, -2):
            at = (cx + (0 if self.long_x else d), self.y0, cz + (d if self.long_x else 0))
            if self.try_place(label, kit, at, facing, uses=False):
                return True
        return False

    def ceiling(self, label, kit, spacing=5):
        """Hanging kits along the long axis, top row touching the ceiling (or a beam)."""
        n = 0
        L = self.W if self.long_x else self.D
        k = max(1, round(L / spacing))
        for i in range(k):
            t = (i + 0.5) / k
            sx, sy, sz = kit.shape
            y = self.y1 - sy + 1
            if self.long_x:
                at = (int(self.x0 + t * self.W - sx / 2), y, (self.z0 + self.z1 + 1 - sz) // 2)
            else:
                at = ((self.x0 + self.x1 + 1 - sx) // 2, y, int(self.z0 + t * self.D - sz / 2))
            done = False
            for dy in (0, 1):
                for d in (0, 1, -1, 2, -2):
                    p = (at[0] + (d if self.long_x else 0), at[1] - dy, at[2] + (0 if self.long_x else d))
                    cx, cz = p[0] + sx // 2, p[2] + sz // 2
                    if dy and self.s.idx[cx, p[1] + sy, cz] == 0:
                        continue   # must hang from something
                    if self.try_place(label, kit, p, "south", uses=False, need_floor=False):
                        n += 1; done = True
                        break
                if done:
                    break
        return n

    def sconces(self, kind="bracket", spacing=5, y=None):
        """Wall lights on the side walls (and back), skipping door columns and filled wall slots."""
        kit = F.sconce(self.st, kind)
        y = self.y0 + 2 if y is None else y
        y = min(y, self.y1 - kit.shape[1] + 1)
        n = 0
        for side in self.side_walls() + [self.back]:
            spots = self.wall_spots(side, kit, y, order="ends")
            spots.sort(key=lambda p: p[0][0] + p[0][2])
            last = -99
            for at, f in spots:
                along = at[0] if side in ("N", "S") else at[2]
                if along - last < spacing:
                    continue
                lo = along - (self.x0 if side in ("N", "S") else self.z0)
                if lo < 1:
                    continue
                bx, bz = {"N": (at[0], at[2] - 1), "S": (at[0], at[2] + 1), "W": (at[0] - 1, at[2]),
                          "E": (at[0] + 1, at[2])}[side]
                if not all(self.s.idx[bx, yy, bz] for yy in range(at[1], at[1] + kit.shape[1])):
                    continue
                if self.try_place("sconce", kit, at, f, uses=False, need_floor=False):
                    last = along
                    n += 1
        return n

    def beams(self, every=4):
        """Ceiling beams across the short axis (logs at y1) with upside-down stair corbels at the walls. Call it after
        the tall pieces and hanging lights: beams only replace air (and chains, so chandeliers hang from them)."""
        if self.H < 5:
            return 0
        st, s = self.st, self.s

        def put(x, y, z, state):
            cur = s.get(x, y, z)
            if cur == "minecraft:air" or "chain" in cur:
                s.set(x, y, z, state)
        n = 0
        L = self.W if self.long_x else self.D
        for i in range(every // 2 + 1, L - 1, every):
            if self.long_x:
                x = self.x0 + i
                for z in range(self.z0, self.z1 + 1):
                    put(x, self.y1, z, F.P(st.w2("log"), axis="z"))
                put(x, self.y1 - 1, self.z0, F.P(st.w2("stairs"), facing="north", half="top"))
                put(x, self.y1 - 1, self.z1, F.P(st.w2("stairs"), facing="south", half="top"))
            else:
                z = self.z0 + i
                for x in range(self.x0, self.x1 + 1):
                    put(x, self.y1, z, F.P(st.w2("log"), axis="x"))
                put(self.x0, self.y1 - 1, z, F.P(st.w2("stairs"), facing="west", half="top"))
                put(self.x1, self.y1 - 1, z, F.P(st.w2("stairs"), facing="east", half="top"))
            n += 1
        return n

    def corners(self, kinds, n=4):
        """Clutter in the room corners (never the corners next to a door)."""
        got = 0
        cs = [(self.x0, self.z0, "N"), (self.x1, self.z0, "N"), (self.x0, self.z1, "S"), (self.x1, self.z1, "S")]
        self.rng.shuffle(cs)
        for (cx, cz, side) in cs:
            if got >= n:
                break
            if any(abs(cx - ex) + abs(cz - ez) <= 2 for ex, ez in self.entries):
                continue
            kit = F.clutter(self.st, self.rng.choice(kinds), seed=self.rng.randrange(999))
            w = kit.shape[0]
            x = cx if cx == self.x0 else cx - w + 1
            z = cz if side == "N" else cz
            if self.try_place("clutter", kit, (x, self.y0, z), WALLS[side], uses=False):
                got += 1
        return got

    def scatter(self, kinds, n):
        """Clutter along free wall stretches."""
        got = 0
        sides = ["N", "S", "W", "E"]
        for _ in range(n * 6):
            if got >= n:
                break
            side = self.rng.choice(sides)
            kit = F.clutter(self.st, self.rng.choice(kinds), seed=self.rng.randrange(999))
            spots = self.wall_spots(side, kit)
            if not spots:
                continue
            at, f = self.rng.choice(spots)
            if self.try_place("clutter", kit, at, f, uses=False):
                got += 1
        return got

    def report(self, kind):
        w = self.walk()
        area = self.W * self.D
        props = len([p for p in self.placed if p[0] not in ("sconce", "beam")])
        return {"kind": kind, "area": area, "pieces": len(self.placed), "props_per_8m2": round(8 * props / max(area, 1), 2),
                "walkable_share": round(float(w.mean()), 2), "connected": self.connected(),
                "labels": [p[0] for p in self.placed]}


# -------------------------------------------------------------------- programs
def _hall(r):
    st = r.st
    L = (r.W if r.long_x else r.D)
    r.on_wall("throne", F.throne(st), [r.back]) or r.on_wall("high table", F.table(st, 5, 1, seats=None, seed=r.seed), [r.back])
    r.on_wall("tapestry", F.tapestry(st, 1, design=0), [r.back], y=r.y0 + 2, n=2, uses=False, need_floor=False)
    for tl in range(max(3, L - 10), 2, -2):
        if r.centre("feast table", F.table(st, tl, 2 if min(r.W, r.D) >= 9 else 1, kind="cloth", seats="benches",
                                           head=True, seed=r.seed), facing="south" if r.long_x else "east"):
            break
    for side in r.side_walls():
        r.on_wall("tapestry", F.tapestry(st, 1, design=r.rng.randrange(5)), [side], y=r.y0 + 2, n=max(1, L // 6),
                  uses=False, need_floor=False, order="ends")
    r.on_wall("armour", F.armour(st), [r.back], n=2, order="ends", uses=False)
    for side in r.side_walls():
        r.on_wall("bench", F.bench(st, 3), [side], n=max(1, L // 8), order="ends")
        r.on_wall("shelf", F.shelf(st, 2, r.rng.randrange(99)), [side], y=r.y0 + 1, n=1, uses=False, need_floor=False)
    r.ceiling("chandelier", F.chandelier(st, 2 if min(r.W, r.D) >= 9 else 1, max(0, r.H - 6)), spacing=6)
    r.beams(5)
    r.sconces("bracket", 5)
    r.corners(["barrels", "pots", "candles", "plants"], 4)


def _bedroom(r):
    st = r.st
    big = r.W * r.D >= 30
    r.on_wall("bed", F.bed(st, double=big, canopy=big and r.H >= 4, seed=r.seed), [r.back])
    sides = r.side_walls()
    r.on_wall("wardrobe", F.wardrobe(st), sides, order="ends")
    r.on_wall("desk", F.desk(st, r.seed), sides[::-1], order="ends")
    r.on_wall("shelf", F.shelf(st, 2, r.seed), sides, y=r.y0 + 1, uses=False, need_floor=False)
    rw, rd = max(3, min(5, r.W - 4)), max(3, min(4, r.D - 4))
    r.centre("rug", F.rug(st, rw, rd, "border"))
    r.ceiling("chandelier", F.chandelier(st, 1, 0, kind="candle"), spacing=99)
    r.sconces("candle", 6)
    r.corners(["plants", "pots", "candles"], 2)


def _library(r):
    st = r.st
    for side in [r.back] + r.side_walls():
        L = (r.W if side in ("N", "S") else r.D)
        r.on_wall("bookshelf", F.bookshelf(st, min(5, L - 2), min(3, r.H - 1), seed=r.rng.randrange(99)), [side], n=2)
        r.on_wall("bookshelf", F.bookshelf(st, 3, min(3, r.H - 1), seed=r.rng.randrange(99)), [side], n=2, order="ends")
    r.centre("reading table", F.table(st, max(3, min(5, (r.W if r.long_x else r.D) - 6)), 1, seed=r.seed))
    r.on_wall("lectern", F.clutter(st, "books"), r.side_walls() + [OPP[r.back]], order="ends")
    r.on_wall("desk", F.desk(st, r.seed), [OPP[r.back]], order="ends")
    r.on_wall("armchair", F.chair(st, arms=True), r.side_walls(), y=r.y0, order="centre", n=1)
    r.on_wall("globe", F.clutter(st, "plants", r.seed), [OPP[r.back]], order="ends", uses=False)
    r.ceiling("chandelier", F.chandelier(st, 1, 1), spacing=6)
    r.corners(["plants", "candles"], 2)


def _kitchen(r):
    st = r.st
    r.on_wall("hearth", F.hearth(st, 5, r.H), [r.back])
    for side in r.side_walls():
        r.on_wall("counter", F.counter(st, min(5, (r.W if side in ("N", "S") else r.D) - 3), seed=r.rng.randrange(99)),
                  [side], order="centre")
    r.centre("table", F.table(st, max(3, min(4, (r.W if r.long_x else r.D) - 6)), 1, seed=r.seed))
    r.on_wall("cauldron", F.cauldron(st), r.side_walls() + [r.back], order="ends")
    r.ceiling("lantern", F.hanging_lantern(st, 1), spacing=4)
    r.corners(["barrels", "sacks", "hay", "firewood", "crates"], 4)
    r.scatter(["barrels", "pots", "sacks"], 2)


def _chapel(r):
    st = r.st
    r.on_wall("altar", F.altar(st, 5 if min(r.W, r.D) >= 7 else 5), [r.back])
    r.on_wall("tapestry", F.tapestry(st, 1, design=3), [r.back], y=r.y0 + 3, n=1, uses=False, need_floor=False)
    # pews: rows facing the altar, aisle down the middle
    toward = WALLS[OPP[r.back]]  # pews' front faces the altar => facing = direction toward the back wall
    face = {"N": "north", "S": "south", "W": "west", "E": "east"}[r.back]
    across = r.D if r.back in ("W", "E") else r.W
    n = max(1, (across - 3) // 2 - 1)
    pew = F.bench(st, n, arms=True)
    depth_axis = r.W if r.back in ("W", "E") else r.D
    for row in range(4, depth_axis - 1, 2):
        for half in (0, 1):
            if r.back == "N":
                z = r.z0 + row; x = r.x0 + (0 if half == 0 else r.W - pew.shape[0])
            elif r.back == "S":
                z = r.z1 - row; x = r.x0 + (0 if half == 0 else r.W - pew.shape[0])
            elif r.back == "W":
                x = r.x0 + row; z = r.z0 + (0 if half == 0 else r.D - pew.shape[0])
            else:
                x = r.x1 - row; z = r.z0 + (0 if half == 0 else r.D - pew.shape[0])
            r.try_place("pew", pew, (x, r.y0, z), face, uses=False)
    del toward
    for side in r.side_walls():
        r.on_wall("tapestry", F.tapestry(st, 1, design=r.rng.randrange(5)), [side], y=r.y0 + 2,
                  n=max(1, depth_axis // 6), uses=False, need_floor=False, order="ends")
    r.sconces("candle", 4)
    r.ceiling("chandelier", F.chandelier(st, 1, 1), spacing=6)
    r.corners(["candles", "plants"], 2)


def _armoury(r):
    st = r.st
    for side in [r.back] + r.side_walls():
        r.on_wall("weapon rack", F.weapon_rack(st, 3, seed=r.rng.randrange(99)), [side], n=2, order="ends")
    r.on_wall("workbench", F.workbench(st), [r.back] + r.side_walls())
    for g in ("iron", "chain", "leather"):
        r.on_wall("armour", F.armour(st, g, r.rng.choice(F.WEAPONS)), r.side_walls() + [r.back], order="centre", uses=False)
    r.centre("table", F.table(st, max(3, min(4, (r.W if r.long_x else r.D) - 6)), 1, seats=None, seed=r.seed))
    r.ceiling("lantern", F.hanging_lantern(st, 1), spacing=4)
    r.corners(["barrels", "crates"], 3)


def _cellar(r):
    st = r.st
    for side in [r.back] + r.side_walls():
        r.on_wall("barrels", F.clutter(st, "barrels", r.rng.randrange(99)), [side], n=3, order="ends", uses=False)
    r.corners(["barrels", "sacks", "crates", "hay", "firewood", "pots"], 4)
    r.centre("rack", F.clutter(st, "barrels", r.seed + 1))
    r.scatter(["barrels", "sacks", "crates", "pots"], 8)
    r.ceiling("lantern", F.hanging_lantern(st, 1), spacing=5)


def _lab(r):
    st = r.st
    r.on_wall("alchemy", F.alchemy(st, min(5, (r.W if r.back in ("N", "S") else r.D) - 2), seed=r.seed), [r.back])
    for side in r.side_walls():
        r.on_wall("bookshelf", F.bookshelf(st, 3, min(3, r.H - 1), seed=r.rng.randrange(99)), [side], order="ends")
        r.on_wall("alchemy", F.alchemy(st, 3, seed=r.rng.randrange(99)), [side], order="centre")
    r.centre("table", F.table(st, 3, 1, seats=None, seed=r.seed))
    r.on_wall("cauldron", F.cauldron(st), r.side_walls(), order="ends")
    r.ceiling("chandelier", F.chandelier(st, 1, 1, kind="lantern"), spacing=6)
    r.corners(["candles", "pots", "books"], 3)


PROGRAMS = {"hall": _hall, "bedroom": _bedroom, "library": _library, "kitchen": _kitchen, "chapel": _chapel,
            "armoury": _armoury, "cellar": _cellar, "lab": _lab}


def furnish(s, box, kind, style="keep", doors=(), seed=0):
    """Furnish the room; returns a report dict (pieces, density, walkable share, connectivity)."""
    r = Room(s, box, style, doors, seed)
    PROGRAMS[kind](r)
    return r.report(kind)
