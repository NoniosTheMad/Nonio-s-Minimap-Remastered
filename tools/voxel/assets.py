"""Local cache of Mojang data (never committed): block models/textures from the client jar, block list from the
server jar's data-generator report. Both are built on first use under .mcdev/voxel/."""
import functools, json, shutil, subprocess, tempfile, zipfile
from pathlib import Path

from .paths import MC_VERSION, client_jar, java, server_jar, voxel_dir

PREFIXES = ("assets/minecraft/blockstates/", "assets/minecraft/models/block/", "assets/minecraft/textures/block/",
            "assets/minecraft/textures/colormap/",
            # v2: block entities / entities are rendered from these (chests, beds, signs, banners, heads, pots,
            # paintings, item frames, armour stands) plus the font for sign text
            "assets/minecraft/textures/entity/", "assets/minecraft/textures/item/", "assets/minecraft/textures/painting/",
            "assets/minecraft/textures/trims/", "assets/minecraft/textures/font/", "assets/minecraft/items/",
            "assets/minecraft/models/item/")
ASSET_STAMP = ".done-v2"


def assets_root() -> Path:
    root = voxel_dir() / "assets" / MC_VERSION
    stamp = root / ASSET_STAMP
    if not stamp.exists():
        jar = client_jar()
        print(f"[voxel] extracting block assets from {jar} ...")
        with zipfile.ZipFile(jar) as z:
            for n in z.namelist():
                if n.startswith(PREFIXES) and not n.endswith("/"):
                    dst = root / n[len("assets/minecraft/"):]
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_bytes(z.read(n))
        stamp.write_text(str(jar))
    return root


@functools.lru_cache(None)
def blocks_info() -> dict:
    """{name: {"props": {prop: [values]}, "default": {prop: value}}} for every 26.3 block."""
    f = voxel_dir() / f"blocks-{MC_VERSION}.json"
    if not f.exists():
        print("[voxel] generating block report from the server jar ...")
        tmp = Path(tempfile.mkdtemp())
        subprocess.run([str(java()), "-DbundlerMainClass=net.minecraft.data.Main", "-jar", str(server_jar()),
                        "--reports", "--output", str(tmp)], check=True, capture_output=True, cwd=tmp)
        raw = json.loads((tmp / "reports" / "blocks.json").read_text(encoding="utf-8"))
        out = {}
        for name, b in raw.items():
            d = next((s.get("properties", {}) for s in b["states"] if s.get("default")), {})
            out[name] = {"props": b.get("properties", {}), "default": d}
        f.write_text(json.dumps(out, separators=(",", ":")))
        shutil.rmtree(tmp, ignore_errors=True)
    return json.loads(f.read_text())
