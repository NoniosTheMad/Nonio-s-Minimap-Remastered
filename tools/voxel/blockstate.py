"""Block-state strings ("minecraft:oak_stairs[facing=east,half=top]"): parse, validate, canonicalise, rotate, mirror.

Canonical form = namespaced id + EVERY property (defaults filled in), keys sorted. That makes states comparable with
what the server stores (it omits defaults only when the whole state is the default one)."""
import difflib, functools, re

from .assets import blocks_info

_RE = re.compile(r"^\s*([a-z0-9_.\-:/]+)\s*(?:\[(.*)\])?\s*$")
DIRS = ["north", "east", "south", "west"]  # clockwise seen from above


class BlockStateError(ValueError):
    pass


def parse(s: str):
    m = _RE.match(s)
    if not m:
        raise BlockStateError(f"bad block state {s!r}")
    name, props = m.group(1), m.group(2)
    if ":" not in name:
        name = "minecraft:" + name
    d = {}
    if props:
        for kv in props.split(","):
            if kv.strip():
                k, _, v = kv.partition("=")
                d[k.strip()] = v.strip()
    return name, d


def fmt(name: str, props: dict) -> str:
    return name + ("[" + ",".join(f"{k}={props[k]}" for k in sorted(props)) + "]" if props else "")


@functools.lru_cache(maxsize=100000)
def canonical(s: str) -> str:
    """Validated full state. Raises BlockStateError with a suggestion on typos."""
    name, props = parse(s)
    info = blocks_info()
    b = info.get(name)
    if b is None:
        close = difflib.get_close_matches(name, info.keys(), n=3)
        raise BlockStateError(f"unknown block {name!r}" + (f" (did you mean {', '.join(close)}?)" if close else ""))
    full = dict(b["default"])
    for k, v in props.items():
        if k not in b["props"]:
            raise BlockStateError(f"{name} has no property {k!r} (has: {', '.join(b['props']) or 'none'})")
        if v not in b["props"][k]:
            raise BlockStateError(f"{name}[{k}={v}] invalid; values: {', '.join(b['props'][k])}")
        full[k] = v
    return fmt(name, full)


def compact(s: str) -> str:
    """Canonical state without default-valued properties (short, for display)."""
    name, props = parse(canonical(s))
    d = blocks_info()[name]["default"]
    return fmt(name, {k: v for k, v in props.items() if d.get(k) != v})


def name_of(s: str) -> str:
    return parse(s)[0]


def short(s: str) -> str:
    return compact(s).replace("minecraft:", "")


def with_props(s: str, **kw) -> str:
    name, props = parse(s)
    props.update({k: str(v).lower() if isinstance(v, bool) else str(v) for k, v in kw.items()})
    return canonical(fmt(name, props))


def _rot_dir(d, k):
    return DIRS[(DIRS.index(d) + k) % 4] if d in DIRS else d


def _fix_compound(name, key, val):
    """'west_south' -> 'south_west' if only the latter is valid (rails etc.)."""
    vals = blocks_info()[name]["props"].get(key, [])
    if val in vals:
        return val
    parts = val.split("_")
    for i in range(1, len(parts)):
        alt = "_".join(parts[i:] + parts[:i])
        if alt in vals:
            return alt
    return val


@functools.lru_cache(maxsize=100000)
def rotate(s: str, k: int) -> str:
    """Rotate k quarter turns clockwise (seen from above), as a structure rotation does."""
    k %= 4
    if k == 0:
        return s
    name, props = parse(canonical(s))
    out = dict(props)
    for key, v in props.items():
        if key in ("facing", "horizontal_facing", "orientation_facing"):
            out[key] = _rot_dir(v, k)
        elif key == "orientation":  # jigsaw/crafter: "north_up"
            a, _, b = v.partition("_")
            out[key] = _rot_dir(a, k) + "_" + _rot_dir(b, k)
        elif key == "axis" and v in "xz" and k % 2:
            out[key] = "z" if v == "x" else "x"
        elif key == "rotation" and v.isdigit():
            out[key] = str((int(v) + 4 * k) % 16)
        elif key == "shape" and any(d in v for d in DIRS):
            out[key] = _fix_compound(name, key, "_".join(_rot_dir(p, k) for p in v.split("_")))
    for d in DIRS:  # connection props (fences, walls, redstone, vines...) move with the block
        if d in props:
            out[_rot_dir(d, k)] = props[d]
    return fmt(name, out)


@functools.lru_cache(maxsize=100000)
def mirror_x(s: str) -> str:
    """Mirror across the YZ plane (east <-> west)."""
    name, props = parse(canonical(s))
    sw = {"east": "west", "west": "east"}
    out = dict(props)
    for key, v in props.items():
        if key in ("facing", "horizontal_facing"):
            out[key] = sw.get(v, v)
        elif key == "rotation" and v.isdigit():
            out[key] = str((16 - int(v)) % 16)
        elif key == "shape":
            if v.endswith("_left"):
                out[key] = v[:-5] + "_right"
            elif v.endswith("_right"):
                out[key] = v[:-6] + "_left"
            elif any(d in v for d in DIRS):
                out[key] = _fix_compound(name, key, "_".join(sw.get(p, p) for p in v.split("_")))
        elif key == "hinge":
            out[key] = "right" if v == "left" else "left"
    if "east" in props and "west" in props:
        out["east"], out["west"] = props["west"], props["east"]
    return fmt(name, out)
