"""Where things live. Caches and outputs go to the MAIN checkout's .mcdev/voxel (shared by every worktree,
gitignored): Mojang assets are never committed."""
import functools, os, subprocess
from pathlib import Path

CHECKOUT = Path(__file__).resolve().parents[2]  # repo root or .worktrees/<branch>
MC_VERSION = "26.3"
DATA_VERSION = 5023  # world_version of 26.3 (server jar version.json)


@functools.lru_cache(None)
def main_root() -> Path:
    """Root of the main checkout (owner of .mcdev, .tools), also when running from a worktree."""
    try:
        common = subprocess.check_output(["git", "-C", str(CHECKOUT), "rev-parse", "--git-common-dir"],
                                         text=True, stderr=subprocess.DEVNULL).strip()
        p = Path(common)
        if not p.is_absolute():
            p = (CHECKOUT / p).resolve()
        return p.parent
    except Exception:
        return CHECKOUT


def state_dir() -> Path:
    return main_root() / ".mcdev"


def voxel_dir() -> Path:
    d = state_dir() / "voxel"
    d.mkdir(parents=True, exist_ok=True)
    return d


def out_dir(scene_name: str) -> Path:
    d = voxel_dir() / "out" / scene_name
    d.mkdir(parents=True, exist_ok=True)
    return d


def client_jar() -> Path:
    env = os.environ.get("VOXEL_CLIENT_JAR")
    cands = [Path(env)] if env else []
    cands += [Path.home() / "curseforge/minecraft/Install/versions" / MC_VERSION / f"{MC_VERSION}.jar",
              Path(os.environ.get("APPDATA", "")) / ".minecraft/versions" / MC_VERSION / f"{MC_VERSION}.jar"]
    for c in cands:
        if c.exists():
            return c
    raise FileNotFoundError("26.3 client jar not found; set VOXEL_CLIENT_JAR")


def server_jar() -> Path:
    return main_root() / ".tools" / f"server-{MC_VERSION}.jar"


def java() -> Path:
    return main_root() / ".tools" / "jre25" / "bin" / ("java.exe" if os.name == "nt" else "java")
