"""Read a box of blocks straight from a 26.3 world's region files (Anvil .mca).

26.3 layout: <world>/dimensions/minecraft/overworld/region/r.X.Z.mca; chunk NBT has sections[] with Y and
block_states {palette, data}. Palette entries: "minecraft:stone" (default state) or {id, properties}; inside
mixed lists the strings are wrapped as {"": "minecraft:stone"}. Unsaved/ungenerated chunks read as structure_void.
Block entities come from each chunk's block_entities list, entities from <dim>/entities/r.X.Z.mca (chunk "Entities").
Run `save-all flush` on the server first (server.pull does)."""
import io, math, struct, zlib
from pathlib import Path

import numpy as np

from .nbtio import _state_from_nbt
from .scene import VOID, Scene


def region_dir(world, dimension="minecraft:overworld"):
    ns, _, path = dimension.partition(":")
    return Path(world) / "dimensions" / ns / path / "region"


def _chunk_nbt(rdir, cx, cz, cache):
    rx, rz = cx >> 5, cz >> 5
    key = (rx, rz)
    if key not in cache:
        f = rdir / f"r.{rx}.{rz}.mca"
        cache[key] = f.read_bytes() if f.exists() else None
    b = cache[key]
    if not b:
        return None
    i = (cx & 31) + (cz & 31) * 32
    off = int.from_bytes(b[i * 4:i * 4 + 3], "big")
    if not off:
        return None
    o = off * 4096
    n = struct.unpack(">i", b[o:o + 4])[0]
    ctype = b[o + 4]
    if ctype & 128:  # oversized chunk in c.X.Z.mcc
        raw = (rdir / f"c.{cx}.{cz}.mcc").read_bytes()
        ctype &= 127
    else:
        raw = b[o + 5:o + 4 + n]
    if ctype == 2:
        data = zlib.decompress(raw)
    elif ctype == 1:
        import gzip
        data = gzip.decompress(raw)
    elif ctype == 3:
        data = raw
    elif ctype == 4:
        import lz4.block  # region-file-compression=lz4 (not the default)
        data = lz4.block.decompress(raw)
    else:
        raise ValueError(f"chunk {cx},{cz}: unsupported compression {ctype}")
    import nbtlib
    return nbtlib.File.parse(io.BytesIO(data))


def _unpack(longs, bits, n=4096):
    per = 64 // bits
    a = np.asarray(longs, dtype=np.int64).view(np.uint64)
    shifts = (np.arange(per, dtype=np.uint64) * np.uint64(bits))
    vals = (a[:, None] >> shifts[None, :]) & np.uint64((1 << bits) - 1)
    return vals.reshape(-1)[:n].astype(np.int32)


ENTITY_SKIP = {"minecraft:player", "minecraft:item", "minecraft:experience_orb", "minecraft:marker", "minecraft:falling_block",
               "minecraft:arrow", "minecraft:spectral_arrow", "minecraft:trident", "minecraft:fishing_bobber"}


def read_box(world, p0, p1, dimension="minecraft:overworld", name="pulled", entities=True):
    """Inclusive world-coordinate box -> Scene (scene (0,0,0) = min corner), with block entities and (decor) entities."""
    lo = [min(a, b) for a, b in zip(p0, p1)]
    hi = [max(a, b) for a, b in zip(p0, p1)]
    size = [h - l + 1 for l, h in zip(lo, hi)]
    s = Scene(size, name)
    void = s.id(VOID)
    s.idx[:] = void
    rdir = region_dir(world, dimension)
    cache = {}
    missing = 0
    for cx in range(lo[0] >> 4, (hi[0] >> 4) + 1):
        for cz in range(lo[2] >> 4, (hi[2] >> 4) + 1):
            ch = _chunk_nbt(rdir, cx, cz, cache)
            if ch is None:
                missing += 1
                continue
            xa, xb = max(lo[0], cx * 16), min(hi[0], cx * 16 + 15)
            za, zb = max(lo[2], cz * 16), min(hi[2], cz * 16 + 15)
            s.idx[xa - lo[0]:xb - lo[0] + 1, :, za - lo[2]:zb - lo[2] + 1] = 0  # saved chunk: absent sections = air
            for b in ch.get("block_entities", []):
                bx, by, bz = int(b["x"]), int(b["y"]), int(b["z"])
                if lo[0] <= bx <= hi[0] and lo[1] <= by <= hi[1] and lo[2] <= bz <= hi[2]:
                    t = type(b)(b)
                    for k in ("x", "y", "z", "keepPacked"):
                        t.pop(k, None)
                    s.be[(bx - lo[0], by - lo[1], bz - lo[2])] = t
            for sec in ch.get("sections", []):
                sy = int(sec["Y"])
                y0 = sy * 16
                if y0 > hi[1] or y0 + 15 < lo[1]:
                    continue
                bst = sec.get("block_states")
                if bst is None:
                    continue
                pal = [s.id(_state_from_nbt(p)) for p in bst["palette"]]
                if len(pal) == 1 or "data" not in bst:
                    grid = np.full(4096, 0, np.int32)
                else:
                    bits = max(4, math.ceil(math.log2(len(pal))))
                    grid = _unpack(bst["data"], bits)
                grid = np.array(pal, np.uint16)[grid].reshape(16, 16, 16)  # [y, z, x]
                grid = grid.transpose(2, 0, 1)  # -> [x, y, z]
                # intersect section with the box
                bx0, by0, bz0 = cx * 16, y0, cz * 16
                xa, xb = max(lo[0], bx0), min(hi[0], bx0 + 15)
                ya, yb = max(lo[1], by0), min(hi[1], by0 + 15)
                za, zb = max(lo[2], bz0), min(hi[2], bz0 + 15)
                if xa > xb or ya > yb or za > zb:
                    continue
                s.idx[xa - lo[0]:xb - lo[0] + 1, ya - lo[1]:yb - lo[1] + 1, za - lo[2]:zb - lo[2] + 1] = \
                    grid[xa - bx0:xb - bx0 + 1, ya - by0:yb - by0 + 1, za - bz0:zb - bz0 + 1]
    if entities:
        edir = region_dir(world, dimension).parent / "entities"
        ecache = {}
        for cx in range(lo[0] >> 4, (hi[0] >> 4) + 1):
            for cz in range(lo[2] >> 4, (hi[2] >> 4) + 1):
                ch = _chunk_nbt(edir, cx, cz, ecache)
                if ch is None:
                    continue
                for e in ch.get("Entities", []):
                    if str(e.get("id")) in ENTITY_SKIP:
                        continue
                    px, py, pz = (float(v) for v in e["Pos"])
                    if lo[0] <= px < hi[0] + 1 and lo[1] <= py < hi[1] + 1 and lo[2] <= pz < hi[2] + 1:
                        t = type(e)(e)
                        for k in ("UUID", "Pos", "Motion"):
                            t.pop(k, None)
                        s.entities.append({"pos": [px - lo[0], py - lo[1], pz - lo[2]], "nbt": t})
    if missing:
        print(f"[voxel] {missing} chunk(s) not saved/generated in the box -> structure_void")
    s.meta["origin"] = lo
    return s
