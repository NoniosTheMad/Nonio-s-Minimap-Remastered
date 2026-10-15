"""Scene <-> live mcdev server (RCON + files in the server's world folder).

place   : scene -> structure tiles in <world>/generated/voxel/structure/ -> forceload + `place template` per tile
verify  : random sample of `execute if block` checks (shape props ignored: the game re-shapes fences/walls/stairs)
pull    : `save-all flush` then read the box straight from the region files (anvil.py)
Placements are recorded in .mcdev/voxel/placements.json (+ a snapshot .npz of exactly what was placed) so
`pull`/`diff` can find the box and the source again by scene name."""
import hashlib, importlib.util, json, random, re, time
from pathlib import Path

import numpy as np

from . import anvil, nbtio
from . import blockstate as bs
from .connect import strip_shape
from .paths import main_root, voxel_dir
from .scene import AIR, VOID, Scene

_mcdev = None


def mcdev():
    """tools/mcdev.py of the MAIN checkout (its state dir is the shared .mcdev)."""
    global _mcdev
    if _mcdev is None:
        p = main_root() / "tools" / "mcdev.py"
        spec = importlib.util.spec_from_file_location("mcdev_main", p)
        _mcdev = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_mcdev)
    return _mcdev


class Server:
    def __init__(self, name):
        m = mcdev()
        reg = m.load_reg()
        if name not in reg:
            raise SystemExit(f"no mcdev server '{name}' (have: {', '.join(reg)})")
        self.name, self.info = name, reg[name]
        self.dir = m.SERVERS / name
        self.world = self.dir / "world"
        self.port = self.info["port"]
        if not m.port_open(self.port + 10000):
            raise SystemExit(f"server '{name}' is not running ({self.info.get('status')}): run `mcdev up {name}` first")

    def cmd(self, c):
        return mcdev().rcon(self.port + 10000, c)

    def cmds(self, cs):
        return [self.cmd(c) for c in cs]

    @property
    def structure_dir(self):
        return self.world / "generated" / "voxel" / "structure"


def _chunks(x0, z0, x1, z1):
    return [(cx, cz) for cx in range(x0 >> 4, (x1 >> 4) + 1) for cz in range(z0 >> 4, (z1 >> 4) + 1)]


def _forceload(srv, x0, z0, x1, z1, add=True):
    """forceload add/remove in <=256-chunk rectangles."""
    verb = "add" if add else "remove"
    step = 16 * 16
    for a in range(x0, x1 + 1, step):
        for b in range(z0, z1 + 1, step):
            srv.cmd(f"forceload {verb} {a} {b} {min(a + step - 1, x1)} {min(b + step - 1, z1)}")


def placements():
    f = voxel_dir() / "placements.json"
    return json.loads(f.read_text()) if f.exists() else []


def _save_placements(p):
    f = voxel_dir() / "placements.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(p, indent=1))


def last_placement(scene_name, server=None):
    for p in reversed(placements()):
        if p["scene"] == scene_name and (server is None or p["server"] == server):
            return p
    return None


def place(scene: Scene, server, at, include_air=True, tile=64, log=print):
    """Place the scene with its (0,0,0) at world `at`. Air cells carve (include_air); structure_void cells leave the world alone."""
    srv = Server(server)
    at = [int(v) for v in at]
    X, Y, Z = scene.shape
    if at[1] < -64 or at[1] + Y > 320:
        raise SystemExit(f"scene y range {at[1]}..{at[1] + Y - 1} is outside the world (-64..319)")
    h = hashlib.sha1(scene.idx.tobytes() + "|".join(scene.palette).encode()).hexdigest()[:8]
    prefix = re.sub(r"[^a-z0-9_]", "_", scene.name.lower()) + "_" + h
    t0 = time.time()
    tiles = nbtio.write_tiles(scene, srv.structure_dir, prefix, include_air, tile)
    x0, z0, x1, z1 = at[0], at[2], at[0] + X - 1, at[2] + Z - 1
    _forceload(srv, x0, z0, x1, z1, True)
    errors = []
    try:
        if include_air:  # structures add entities on top of what is there: clear old decor entities in the box first
            sel = f"x={x0},y={at[1]},z={z0},dx={X},dy={Y},dz={Z}"
            for t in ("item_frame", "glow_item_frame", "painting", "armor_stand", "item_display", "block_display",
                      "text_display", "item"):
                srv.cmd(f"kill @e[type={t},{sel}]")
        for name, (tx, _, tz), n in tiles:
            r = srv.cmd(f"place template voxel:{name} {at[0] + tx} {at[1]} {at[2] + tz}")
            if "Loaded template" not in r:
                errors.append(f"{name}: {r.strip()}")
    finally:
        _forceload(srv, x0, z0, x1, z1, False)
    snap = voxel_dir() / "placements" / f"{prefix}.npz"
    snap.parent.mkdir(parents=True, exist_ok=True)
    scene.save(snap)
    rec = dict(scene=scene.name, server=server, at=at, size=[X, Y, Z], prefix=prefix, snapshot=str(snap),
               include_air=include_air, time=time.strftime("%Y-%m-%d %H:%M:%S"),
               blocks=int(sum(n for *_, n in tiles)), tiles=len(tiles))
    p = placements(); p.append(rec); _save_placements(p)
    log(f"[voxel] placed {scene.name} on {server} at {at}: {len(tiles)} tile(s), {rec['blocks']} blocks, {time.time() - t0:.1f}s")
    for e in errors:
        log(f"[voxel]   ERROR {e}")
    return rec, errors


def verify(scene: Scene, server, at, n=200, seed=1, log=print):
    """`execute if block` on n random non-void cells (half solid, half anything). Returns (ok, fails)."""
    srv = Server(server)
    rng = random.Random(seed)
    void = scene._lut.get(VOID)
    solid = np.argwhere(scene.idx > 0) if void is None else np.argwhere((scene.idx > 0) & (scene.idx != void))
    anyc = np.argwhere(scene.idx != void) if void is not None else np.argwhere(np.ones(scene.shape, bool))
    picks = [tuple(solid[rng.randrange(len(solid))]) for _ in range(min(n // 2, len(solid)))] if len(solid) else []
    picks += [tuple(anyc[rng.randrange(len(anyc))]) for _ in range(n - len(picks))]
    X, Y, Z = scene.shape
    x0, z0 = at[0], at[2]
    _forceload(srv, x0, z0, x0 + X - 1, z0 + Z - 1, True)
    fails = []
    try:
        for x, y, z in picks:
            st = strip_shape(scene.palette[scene.idx[x, y, z]])
            if bs.name_of(st) in ("minecraft:air",):
                st = "minecraft:air"
            wx, wy, wz = at[0] + int(x), at[1] + int(y), at[2] + int(z)
            r = srv.cmd(f"execute if block {wx} {wy} {wz} {bs.compact(st)}")
            if "passed" not in r.lower():
                fails.append(((wx, wy, wz), st, r.strip()))
    finally:
        _forceload(srv, x0, z0, x0 + X - 1, z0 + Z - 1, False)
    ok = len(picks) - len(fails)
    log(f"[voxel] verify {scene.name} on {server}: {ok}/{len(picks)} sampled cells match")
    for f in fails[:10]:
        log(f"[voxel]   MISMATCH at {f[0]}: want {f[1]} ({f[2]})")
    return ok, fails


def pull(server, p0, p1, name="pulled", log=print):
    """save-all flush, then read the inclusive world box from disk."""
    srv = Server(server)
    r = srv.cmd("save-all flush")
    time.sleep(0.3)
    s = anvil.read_box(srv.world, p0, p1, name=name)
    log(f"[voxel] pulled {s.shape} from {server} {list(p0)}..{list(p1)} ({r.strip()})")
    return s


def snapshot_pristine(server, log=print):
    """Copy the live world to world.pristine (what mcdev's "Reset this server" restores). Saving is paused meanwhile."""
    import shutil
    srv = Server(server)
    dst = srv.dir / "world.pristine"
    srv.cmd("save-off")
    try:
        srv.cmd("save-all flush")
        time.sleep(0.5)
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(srv.world, dst, ignore=shutil.ignore_patterns("session.lock"))
    finally:
        srv.cmd("save-on")
    log(f"[voxel] snapshot {dst}")
