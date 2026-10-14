"""Auto-connect pass: derive the neighbour-dependent states the game would compute on placement
(fence / pane / iron bars / wall connections, stair corner shapes), so renders match the game and diffs are clean.

    connect(scene)   # call last in build(); the CLI does it automatically unless the scene sets meta["connect"] = False

SHAPE_PROPS(name) lists the properties the game recomputes from neighbours (diff/verify ignore them by default)."""
import numpy as np

from . import blockstate as bs
from .models import bank

H = {"north": (0, 0, -1), "east": (1, 0, 0), "south": (0, 0, 1), "west": (-1, 0, 0)}
CCW = {"north": "west", "west": "south", "south": "east", "east": "north"}
OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}


def kind(name):
    n = name.split(":")[-1]
    if n.endswith("_fence_gate"):
        return "gate"
    if n.endswith("_fence"):
        return "nfence" if n == "nether_brick_fence" else "fence"
    if n.endswith("_wall") and not n.endswith(("_wall_sign", "_wall_banner", "_wall_head", "_wall_skull", "_wall_torch", "_wall_hanging_sign", "wall_fan")):
        return "wall"
    if n.endswith("glass_pane") or n == "iron_bars" or n.endswith("_bars"):
        return "pane"
    if n.endswith("_stairs"):
        return "stairs"
    return None


def SHAPE_PROPS(name):
    k = kind(name)
    if k in ("fence", "nfence", "pane"):
        return {"north", "east", "south", "west"}
    if k == "wall":
        return {"north", "east", "south", "west", "up"}
    if k == "stairs":
        return {"shape"}
    if k == "gate":
        return {"in_wall"}
    return set()


def strip_shape(state):
    name, props = bs.parse(state)
    sp = SHAPE_PROPS(name)
    return bs.fmt(name, {k: v for k, v in props.items() if k not in sp}) if sp else state


def connect(scene):
    pal = scene.palette
    names = [bs.name_of(p) for p in pal]
    kinds = [kind(n) for n in names]
    if not any(kinds):
        return 0
    b = bank()
    sturdy = np.array([b.is_occluder(p) and not n.endswith("_leaves") for p, n in zip(pal, names)])
    X, Y, Z = scene.shape
    idx = scene.idx

    def at(x, y, z):
        if 0 <= x < X and 0 <= y < Y and 0 <= z < Z:
            return int(idx[x, y, z])
        return 0

    changed = 0
    targets = [i for i, k in enumerate(kinds) if k and k != "gate"]
    todo = np.argwhere(np.isin(idx, targets))
    todo = todo[np.argsort(-todo[:, 1], kind="stable")]  # top-down: a wall's post depends on the (new) wall above it
    new = {}

    def state_at(x, y, z):
        return new.get((x, y, z)) or pal[at(x, y, z)]

    for x, y, z in todo:
        x, y, z = int(x), int(y), int(z)
        i = int(idx[x, y, z]); k = kinds[i]
        name, props = bs.parse(pal[i])
        if k == "stairs":
            props["shape"] = _stair_shape(props, lambda d: _get(at, x, y, z, d), kinds, pal)
        else:
            above = at(x, y + 1, z)
            ap = bs.parse(state_at(x, y + 1, z))[1] if kinds[above] == "wall" else {}
            for d, (dx, _, dz) in H.items():
                j = at(x + dx, y, z + dz)
                nk = kinds[j]
                if k in ("fence", "nfence"):
                    ok = nk == k or sturdy[j] or (nk == "gate" and _gate_ok(pal[j], d))
                elif k == "pane":
                    ok = nk in ("pane", "wall") or sturdy[j]
                else:  # wall
                    ok = nk in ("wall", "pane", "fence", "nfence") or sturdy[j] or (nk == "gate" and _gate_ok(pal[j], d))
                if k == "wall":
                    tall = sturdy[above] or ap.get(d, "none") != "none"
                    props[d] = ("tall" if tall else "low") if ok else "none"
                else:
                    props[d] = "true" if ok else "false"
            if k == "wall":
                props["up"] = "true" if _raise_post(props, ap, sturdy[above] or POST_OVERRIDE(names[above])) else "false"
        st = bs.fmt(name, props)
        if st != pal[i]:
            new[(x, y, z)] = st
    for (x, y, z), st in new.items():
        idx[x, y, z] = scene.id(st)
        changed += 1
    return changed


def POST_OVERRIDE(name):
    n = name.split(":")[-1]
    return n.endswith(("torch", "lantern", "_sign", "_banner", "_pressure_plate")) or n in ("redstone_wall_torch",)


def _raise_post(p, above_wall, above_covers):
    """WallBlock.shouldRaisePost."""
    if above_wall.get("up") == "true":
        return True
    n, e, s, w = (p[d] for d in ("north", "east", "south", "west"))
    if (n == s == e == w == "none") or ((n == "none") != (s == "none")) or ((w == "none") != (e == "none")):
        return True
    if (n == "tall" and s == "tall") or (e == "tall" and w == "tall"):
        return False
    return bool(above_covers)


def _get(at, x, y, z, d):
    dx, _, dz = H[d]
    return at(x + dx, y, z + dz)


def _gate_ok(gate_state, side):
    f = bs.parse(gate_state)[1].get("facing", "north")
    return (f in ("north", "south")) == (side in ("east", "west"))


def _stair_shape(props, nb, kinds, pal):
    f, half = props["facing"], props["half"]

    def stair(j):
        if kinds[j] != "stairs":
            return None
        p = bs.parse(pal[j])[1]
        return p if p.get("half") == half else None

    def can_take(face):
        j = nb(face)
        if kinds[j] != "stairs":
            return True
        p = bs.parse(pal[j])[1]
        return p.get("facing") != f or p.get("half") != half

    s1 = stair(nb(f))
    if s1:
        d1 = s1["facing"]
        if (d1 in ("north", "south")) != (f in ("north", "south")) and can_take(OPP[d1]):
            return "outer_left" if d1 == CCW[f] else "outer_right"
    s2 = stair(nb(OPP[f]))
    if s2:
        d2 = s2["facing"]
        if (d2 in ("north", "south")) != (f in ("north", "south")) and can_take(d2):
            return "inner_left" if d2 == CCW[f] else "inner_right"
    return "straight"


def sturdy(scene):
    """Bool grid: full-cube blocks (what vines, torches, ladders and wall connections can attach to)."""
    b = bank()
    ok = np.array([b.is_occluder(p) and not bs.name_of(p).endswith("_leaves") for p in scene.palette])
    return ok[scene.idx]
