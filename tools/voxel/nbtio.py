"""Vanilla structure templates (.nbt) for 26.3: write (fast, numpy-encoded) and read.

26.3 layout (verified with /place template on a 26.3 server): DataVersion 5023, size [x,y,z],
palette [{id:"minecraft:oak_stairs", properties:{facing:"east",...}}, ...]  (the pre-26 Name/Properties places NOTHING),
blocks [{pos:[x,y,z], state:i}], entities []. Cells missing from `blocks` leave the world untouched on placement."""
import gzip, io, struct
from pathlib import Path

import numpy as np

from . import blockstate as bs
from .paths import DATA_VERSION
from .scene import AIR, VOID, Scene


# ------------------------------------------------------------------ minimal NBT writer
def _s(x: str) -> bytes:
    b = x.encode("utf-8")
    return struct.pack(">H", len(b)) + b


def _tag(t, name):
    return bytes([t]) + _s(name)


def _int_list(name, vals):
    return _tag(9, name) + bytes([3]) + struct.pack(">i", len(vals)) + b"".join(struct.pack(">i", v) for v in vals)


def _palette_entry(state):
    name, props = bs.parse(state)
    out = _tag(8, "id") + _s(name)
    if props:
        out += _tag(10, "properties") + b"".join(_tag(8, k) + _s(v) for k, v in sorted(props.items())) + b"\0"
    return out + b"\0"


_BLOCK = np.dtype([("t1", "u1"), ("n1", "S5"), ("et", "u1"), ("len", ">i4"), ("x", ">i4"), ("y", ">i4"), ("z", ">i4"),
                   ("t2", "u1"), ("n2", "S7"), ("state", ">i4"), ("end", "u1")])


def structure_bytes(idx, palette, include_air=True):
    """gzip'd structure for a palette-index grid. Air written explicitly when include_air (carves); structure_void omitted."""
    keep = np.ones(idx.shape, bool)
    used = np.unique(idx)
    void_ids = [i for i in used if palette[i] == VOID or (not include_air and palette[i] == AIR)]
    for v in void_ids:
        keep &= idx != v
    xs, ys, zs = np.nonzero(keep)
    vals = idx[xs, ys, zs]
    used = np.unique(vals)
    local = np.zeros(len(palette), np.int32)
    local[used] = np.arange(len(used))
    n = len(xs)
    rec = np.zeros(n, _BLOCK)
    rec["t1"] = 9; rec["n1"] = b"\x00\x03pos"; rec["et"] = 3; rec["len"] = 3
    rec["x"], rec["y"], rec["z"] = xs, ys, zs
    rec["t2"] = 3; rec["n2"] = b"\x00\x05state"; rec["state"] = local[vals]; rec["end"] = 0
    out = io.BytesIO()
    out.write(bytes([10]) + _s(""))
    out.write(_tag(3, "DataVersion") + struct.pack(">i", DATA_VERSION))
    out.write(_int_list("size", list(idx.shape)))
    out.write(_tag(9, "palette") + bytes([10]) + struct.pack(">i", len(used)))
    for i in used:
        out.write(_palette_entry(palette[i]))
    out.write(_tag(9, "blocks") + bytes([10 if n else 0]) + struct.pack(">i", n))
    out.write(rec.tobytes())
    out.write(_tag(9, "entities") + bytes([0]) + struct.pack(">i", 0))
    out.write(b"\0")
    return gzip.compress(out.getvalue(), 6), n


def tiles(scene, tile=64):
    """Yield (ix, iz, x0, z0, sub_idx) chunks of the scene, tile x full height x tile, skipping all-void tiles."""
    X, Y, Z = scene.shape
    void = scene._lut.get(VOID)
    for x0 in range(0, X, tile):
        for z0 in range(0, Z, tile):
            sub = scene.idx[x0:x0 + tile, :, z0:z0 + tile]
            if void is not None and (sub == void).all():
                continue
            yield x0 // tile, z0 // tile, x0, z0, sub


def write_tiles(scene, out_dir, prefix, include_air=True, tile=64):
    """Write <prefix>_<ix>_<iz>.nbt files; returns [(name, (x0, 0, z0), blocks), ...]."""
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    res = []
    for ix, iz, x0, z0, sub in tiles(scene, tile):
        data, n = structure_bytes(np.ascontiguousarray(sub), scene.palette, include_air)
        if not n:
            continue
        name = f"{prefix}_{ix}_{iz}"
        (out_dir / f"{name}.nbt").write_bytes(data)
        res.append((name, (x0, 0, z0), n))
    return res


# ------------------------------------------------------------------ reader
def _state_from_nbt(p):
    if isinstance(p, str):
        return str(p)
    if "" in p:  # heterogeneous-list wrapper
        return str(p[""])
    name = str(p.get("id") or p.get("Name"))
    props = p.get("properties") or p.get("Properties") or {}
    return bs.fmt(name, {str(k): str(v) for k, v in props.items()})


def read_structure(path, name=None):
    """Structure .nbt (any version the DataFixer would accept, block states must still exist in 26.3) -> Scene.
    Cells not in the file become structure_void."""
    import nbtlib
    f = nbtlib.load(path)
    root = f.root if hasattr(f, "root") else f
    size = [int(v) for v in root["size"]]
    pal = root.get("palette")
    if pal is None:
        pal = root["palettes"][0]
    s = Scene(size, name or Path(path).stem)
    void = s.id(VOID)
    s.idx[:] = void
    ids = []
    for p in pal:
        st = _state_from_nbt(p)
        try:
            ids.append(s.id(st))
        except bs.BlockStateError as e:
            print(f"[voxel] {path}: {e} -> structure_void")
            ids.append(void)
    for b in root["blocks"]:
        x, y, z = (int(v) for v in b["pos"])
        s.idx[x, y, z] = ids[int(b["state"])]
    return s
