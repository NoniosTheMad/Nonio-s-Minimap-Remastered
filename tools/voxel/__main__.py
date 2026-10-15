"""Voxel studio CLI.   python -m tools.voxel <command> ...   (see docs/voxel-studio.md)

  info    SCENE                                  size, palette, lint (bad states, floating sand/gravel, ...)
  render  SCENE [--only iso,top,eye] [--size 1280x800] [--no-shadows]   PNG views + sheet.png
  view    SCENE [--serve]                        single-file WebGL1 viewer.html (orbit camera; publishable, < 16 MB)
  serve   [--port 8765] [--host 127.0.0.1]       HTTP server over .mcdev/voxel/out/ (viewers, sheets, renders)
  export  SCENE [--out DIR] [--tile 64] [--no-air]                        structure .nbt tiles
  place   SCENE --server NAME [--at X Y Z] [--no-air] [--verify N] [--pristine]      place over RCON (+ execute-if-block sample)
  verify  SCENE --server NAME [--at X Y Z] [-n N]
  pull    --server NAME (--box X0 Y0 Z0 X1 Y1 Z1 | --scene SCENE) [--out F.npz]
  light   SCENE [--min 7] [--render] [--auto STYLE] [--patch]   light audit (block+sky flood fill), overlay, auto-light
  stats   SCENE [--json F]                       quantitative floors (playbook §5): canvas, facades, decoration density
  diff    SCENE (--server NAME [--at X Y Z] | --against F.npz|F.nbt) [--patch] [--no-render] [--strict]

SCENE = scenes/x.py (build() -> Scene, or a module-level SCENE), a .npz saved by Scene.save, or a structure .nbt.
A <scene>.patch.json beside a .py scene is applied after build() (in-game edits kept by `diff --patch`).
Outputs go to .mcdev/voxel/out/<scene name>/ (main checkout, gitignored)."""
import argparse, importlib.util, json, sys, time
from pathlib import Path

import numpy as np

from .paths import out_dir


def load_scene(path, patch=True, quiet=False):
    p = Path(path)
    if p.suffix == ".py":
        spec = importlib.util.spec_from_file_location(f"voxel_scene_{p.stem}", p)
        mod = importlib.util.module_from_spec(spec)
        t0 = time.time()
        spec.loader.exec_module(mod)
        s = mod.build() if hasattr(mod, "build") else mod.SCENE
        if s.meta.get("connect", True):
            from .connect import connect
            connect(s)
        pf = p.with_suffix(".patch.json")
        if patch and pf.exists():
            from .diff import apply_patch
            n = apply_patch(s, pf)
            if not quiet:
                print(f"[voxel] applied {n} cell(s) from {pf.name}")
        if not quiet:
            print(f"[voxel] built {s.name} {s.shape} in {time.time() - t0:.1f}s")
        s.meta.setdefault("source", str(p.resolve()))
        return s
    if p.suffix == ".npz":
        from .scene import Scene
        return Scene.load(p)
    if p.suffix == ".nbt":
        from .nbtio import read_structure
        return read_structure(p)
    raise SystemExit(f"don't know how to load {p}")


def lint(s):
    from .blockstate import name_of
    from .scene import AIR, VOID
    msgs = []
    names = s.names()
    grav = np.array([n.endswith(("sand", "gravel", "concrete_powder")) or n.endswith(("anvil", "_anvil")) or n in
                     ("minecraft:dragon_egg", "minecraft:pointed_dripstone", "minecraft:scaffolding") for n in names])
    g = grav[s.idx]
    if g.any():
        below = np.zeros_like(g)
        below[:, 1:, :] = s.idx[:, :-1, :] == 0
        fl = g & below
        fl[:, 0, :] = False
        if fl.any():
            pts = np.argwhere(fl)
            msgs.append(f"{len(pts)} gravity block(s) over air will fall, e.g. {pts[:3].tolist()}")
    for k, m in s.markers.items():
        x, y, z = (int(v) for v in m["pos"])
        if not (0 <= x < s.shape[0] and 0 <= z < s.shape[2]):
            msgs.append(f"marker {k} outside the scene")
            continue
        if 0 <= y < s.shape[1] and s.idx[x, y, z] not in (0,) and names[s.idx[x, y, z]] != VOID:
            msgs.append(f"marker {k} {m['pos']} is inside a block ({names[s.idx[x, y, z]]})")
        elif y - 1 >= 0 and s.idx[x, y - 1, z] == 0:
            msgs.append(f"marker {k} {m['pos']} stands on air")
    return msgs


def _origin(args, s, server=None):
    if getattr(args, "at", None):
        return [int(v) for v in args.at]
    from .server import last_placement
    rec = last_placement(s.name, server)
    if rec:
        return rec["at"]
    if "origin" in s.meta:
        return [int(v) for v in s.meta["origin"]]
    raise SystemExit("no --at, no previous placement and no meta['origin'] in the scene")


def serve(host, port):
    """Static server over .mcdev/voxel/out/ with a scene index at /. Opening viewer.html from disk works too
    (everything is inline); this is for other devices on the LAN (--host 0.0.0.0) and for browsers that block file://."""
    import functools, http.server, html
    from .paths import voxel_dir
    root = voxel_dir() / "out"; root.mkdir(parents=True, exist_ok=True)

    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                rows = []
                for d in sorted(p for p in root.iterdir() if p.is_dir()):
                    links = [f'<a href="{d.name}/{f}">{f}</a>' for f in ("viewer.html", "sheet.png") if (d / f).exists()]
                    if links:
                        rows.append(f"<li><b>{html.escape(d.name)}</b> {' &middot; '.join(links)}</li>")
                body = ("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width'>"
                        "<title>Voxel scenes</title><body style='font:14px system-ui;margin:16px'><h3>Voxel scenes</h3><ul>"
                        + "".join(rows) + "</ul>").encode()
                self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
                return
            super().do_GET()

        def end_headers(self):
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

    srv = http.server.ThreadingHTTPServer((host, port), functools.partial(H, directory=str(root)))
    print(f"[voxel] serving {root} at http://{'127.0.0.1' if host in ('', '0.0.0.0') else host}:{port}/  (Ctrl+C stops)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m tools.voxel", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("info"); a.add_argument("scene")
    a = sub.add_parser("render"); a.add_argument("scene"); a.add_argument("--only"); a.add_argument("--size", default="1280x800")
    a.add_argument("--no-shadows", action="store_true"); a.add_argument("--out")
    a = sub.add_parser("view"); a.add_argument("scene"); a.add_argument("--out")
    a.add_argument("--no-merge", action="store_true", help="skip greedy meshing (debug)")
    a = sub.add_parser("serve"); a.add_argument("--port", type=int, default=8765); a.add_argument("--host", default="127.0.0.1")
    a = sub.add_parser("export"); a.add_argument("scene"); a.add_argument("--out"); a.add_argument("--tile", type=int, default=64)
    a.add_argument("--no-air", action="store_true")
    a = sub.add_parser("place"); a.add_argument("scene"); a.add_argument("--server", required=True)
    a.add_argument("--at", nargs=3, type=int); a.add_argument("--no-air", action="store_true"); a.add_argument("--verify", type=int, default=100)
    a.add_argument("--pristine", action="store_true", help="then snapshot the world as world.pristine (Reset this server restores it)")
    a = sub.add_parser("verify"); a.add_argument("scene"); a.add_argument("--server", required=True)
    a.add_argument("--at", nargs=3, type=int); a.add_argument("-n", type=int, default=300)
    a = sub.add_parser("pull"); a.add_argument("--server", required=True); a.add_argument("--box", nargs=6, type=int)
    a.add_argument("--scene"); a.add_argument("--out")
    a = sub.add_parser("diff"); a.add_argument("scene"); a.add_argument("--server"); a.add_argument("--at", nargs=3, type=int)
    a.add_argument("--against"); a.add_argument("--patch", action="store_true", help="write <scene>.patch.json beside the scene")
    a.add_argument("--no-render", action="store_true"); a.add_argument("--strict", action="store_true", help="compare neighbour-shape props too")
    a = sub.add_parser("stats"); a.add_argument("scene"); a.add_argument("--json", help="also write the metrics here")
    a = sub.add_parser("light"); a.add_argument("scene"); a.add_argument("--min", type=int, default=7)
    a.add_argument("--render", action="store_true", help="overlay views: floor tinted by block light (red 0, orange < min)")
    a.add_argument("--auto", metavar="STYLE", help="add fixtures in this kit style until interiors reach --min")
    a.add_argument("--outdoor", action="store_true", help="--auto also lights cells that are only dark at night")
    a.add_argument("--max", type=int, default=200); a.add_argument("--patch", action="store_true",
                   help="with --auto: append the new fixtures to <scene>.patch.json")
    args = ap.parse_args(argv)

    if args.cmd == "serve":
        serve(args.host, args.port)
        return

    if args.cmd == "pull":
        from . import server
        if args.box:
            p0, p1, name = args.box[:3], args.box[3:], "pulled"
        elif args.scene:
            s = load_scene(args.scene, quiet=True)
            o = _origin(args, s, args.server)
            p0, p1, name = o, [o[i] + s.shape[i] - 1 for i in range(3)], s.name + "_pulled"
        else:
            raise SystemExit("pull needs --box or --scene")
        p = server.pull(args.server, p0, p1, name=name)
        out = Path(args.out) if args.out else out_dir(name.removesuffix("_pulled")) / "pulled.npz"
        p.save(out)
        print(f"[voxel] saved {out}")
        return

    s = load_scene(args.scene)
    if args.cmd == "stats":
        from . import stats
        m = stats.compute(s)
        print(stats.report(m, s.name))
        jf = Path(args.json) if args.json else out_dir(s.name) / "stats.json"
        jf.write_text(stats.to_json(m))
        print(f"[voxel] {jf}")
        return
    if args.cmd == "light":
        from . import light
        out = out_dir(s.name)
        rep, g = light.audit(s, args.min)
        print(light.format_report(rep))
        if args.auto:
            add = light.autolight(s, args.auto, args.min, args.max, outdoor=args.outdoor)
            print(f"[voxel] auto-light: {len(add)} fixture(s) added")
            rep2, g = light.audit(s, args.min)
            print(light.format_report(rep2))
            rep = {"before": rep, "after": rep2, "added": add}
            if args.patch and str(args.scene).endswith(".py"):
                from .diff import write_patch_list
                tgt = Path(args.scene).with_suffix(".patch.json")
                old = json.loads(tgt.read_text()) if tgt.exists() else []
                cells = {tuple(c[:3]): c for c in old if isinstance(c, list)}
                for a_ in add:
                    for (x, y, z) in [tuple(a_["pos"])]:
                        cells[(x, y, z)] = [x, y, z, a_["state"]]
                # chains above hanging lanterns
                for (x, y, z), st_ in [((x, y, z), s.get(x, y, z)) for x, y, z in np.argwhere(s.match("chain"))]:
                    cells.setdefault((int(x), int(y), int(z)), [int(x), int(y), int(z), st_])
                write_patch_list(tgt, list(cells.values()) + [c for c in old if isinstance(c, dict)])
                print(f"[voxel] patch {tgt}")
        (out / "light.json").write_text(json.dumps(rep, indent=1))
        print(f"[voxel] {out / 'light.json'}")
        if args.render:
            from .render import render_views
            res = render_views(s, out / "light", 1280, 800, only=["top", "iso", "eye"], vtint=light.overlay_tint(s, g, args.min),
                               sightlines=False)
            for k, v in res.items():
                print(f"  {k:18s} {v}")
        return
    if args.cmd == "info":
        print(s)
        print("bounds (non-air):", s.bounds())
        from .blockstate import short
        for st, k in s.counts()[:40]:
            print(f"  {k:8d}  {short(st) if st != 'minecraft:structure_void' else st}")
        print("markers:", json.dumps(s.markers))
        print("meta:", json.dumps({k: v for k, v in s.meta.items() if k != "source"}))
        for m in lint(s):
            print("LINT", m)
    elif args.cmd == "render":
        from .render import render_views
        for m in lint(s):
            print("LINT", m)
        w, h = (int(v) for v in args.size.split("x"))
        res = render_views(s, Path(args.out) if args.out else out_dir(s.name), w, h,
                           only=args.only.split(",") if args.only else None, shadows=not args.no_shadows)
        for k, v in res.items():
            print(f"  {k:18s} {v}")
    elif args.cmd == "view":
        from .viewer import write_viewer
        p = write_viewer(s, Path(args.out) if args.out else out_dir(s.name) / "viewer.html", merge=not args.no_merge)
        try:
            rel = p.resolve().relative_to(out_dir(s.name).parent.resolve()).as_posix()
            print(f"[voxel] with `python -m tools.voxel serve`: http://127.0.0.1:8765/{rel}")
        except ValueError:
            pass
    elif args.cmd == "export":
        from .nbtio import write_tiles
        out = Path(args.out) if args.out else out_dir(s.name) / "structures"
        for name, at, n in write_tiles(s, out, s.name, not args.no_air, args.tile):
            print(f"  {name}.nbt  offset {list(at)}  {n} blocks")
        print(f"[voxel] -> {out}")
    elif args.cmd == "place":
        from . import server
        at = _origin(args, s, args.server) if args.at or "origin" in s.meta else None
        if at is None:
            raise SystemExit("place needs --at X Y Z (or meta['origin'] in the scene)")
        rec, err = server.place(s, args.server, at, include_air=not args.no_air)
        if args.verify:
            server.verify(s, args.server, at, n=args.verify)
        if args.pristine:
            server.snapshot_pristine(args.server)
        if err:
            sys.exit(1)
    elif args.cmd == "verify":
        from . import server
        ok, fails = server.verify(s, args.server, _origin(args, s, args.server), n=args.n)
        sys.exit(1 if fails else 0)
    elif args.cmd == "diff":
        from .diff import diff
        o = None
        if args.against:
            b = load_scene(args.against)
        elif args.server:
            from . import server
            o = _origin(args, s, args.server)
            b = server.pull(args.server, o, [o[i] + s.shape[i] - 1 for i in range(3)], name=s.name + "_pulled")
            b.save(out_dir(s.name) / "pulled.npz")
        else:
            raise SystemExit("diff needs --server or --against")
        if b.shape != s.shape:
            raise SystemExit(f"size mismatch: scene {s.shape} vs {b.shape}")
        b.markers = dict(s.markers)
        d = diff(s, b, ignore_shape=not args.strict)
        print(d.summary(origin=o))
        od = out_dir(s.name) / "diff"
        od.mkdir(exist_ok=True)
        if d.n or d.n_extra:
            pf = d.write_patch(od / "patch.json")
            print(f"[voxel] patch {pf}")
            if args.patch:
                src = s.meta.get("source")
                if not src or not src.endswith(".py"):
                    raise SystemExit("--patch needs a .py scene")
                tgt = Path(src).with_suffix(".patch.json")
                old = json.loads(tgt.read_text()) if tgt.exists() else []
                merged = {tuple(c[:3]): c for c in old if isinstance(c, list)}
                merged.update({tuple(c[:3]): c for c in d.patch() if isinstance(c, list)})
                ents = [c for c in old if isinstance(c, dict)] + [c for c in d.patch() if isinstance(c, dict)]
                from .diff import write_patch_list
                write_patch_list(tgt, list(merged.values()) + ents)
                print(f"[voxel] wrote {tgt} (applied on every build; fold it into the scene code, then delete it)")
            if not args.no_render and d.n:
                res = d.render(od, only=["iso", "top"])
                print(f"[voxel] diff views: {res.get('sheet')}")


if __name__ == "__main__":
    main()
