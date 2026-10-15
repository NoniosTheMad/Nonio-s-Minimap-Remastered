#!/usr/bin/env python3
"""mcfilm: film a dev server with a second, real Minecraft 26.3 client, so agents can SEE shaders and builds.

  python tools/mcfilm.py shoot --server shaders --setup "trigger demo.fx set 3" --time midnight \
        --orbit "0.5 64 4.5 10 4" --seconds 6 --out .mcdev/film/thermal
  python tools/mcfilm.py still --server shaders --shot "0.5 70 -6 0 20" --shot "10 66 10 135 10" --out .mcdev/film/stills
  python tools/mcfilm.py up --server shaders      # keep the cam session running between shots
  python tools/mcfilm.py status | close

How it works (docs/mcfilm.md):
- cam server: a copy of .mcdev/servers/<target> (world + datapacks, junctions copied as files) in .mcdev/cam/servers/<target>,
  online-mode=false, own ports (25700+), never registered with mcdev (the daemon ignores it). The target is only read
  (`list` + `save-all flush` over its RCON when it is up).
- cam client: vanilla 26.3 launched from the CurseForge install with its own gameDir (.mcdev/cam/client), offline user
  ClaudeCam, 1280x720 window, sound off, the target's resource pack enabled as a client pack, `--quickPlayMultiplayer`.
- camera: RCON on the cam server (spectator, tp along the path every tick, setup commands `as ClaudeCam`).
- capture: PrintWindow(PW_RENDERFULLCONTENT) of the cam window (works while covered by other windows, not minimized),
  raw frames piped to ffmpeg -> mp4; contact sheet + key frames as PNG (agents can Read PNGs, not videos).
- a detached watchdog kills the cam client/server after MCFILM_IDLE (default 600 s) without a mcfilm command, or when
  mcfilm crashed: no stray Java processes. Processes are only ever killed by PID, after checking their command line.
"""
import argparse
import ctypes
import ctypes.wintypes as wt
import hashlib
import io
import json
import math
import os
import re
import secrets
import shutil
import socket
import struct
import subprocess
import sys
import threading
import time
import uuid
import zipfile
from pathlib import Path

# The watchdog has no console, so every console child (tasklist, taskkill, git, ...) would flash its own window
# and steal focus from the user's game. Default every child process to no window (same as mcdev.py).
if os.name == "nt":
    _popen_init = subprocess.Popen.__init__
    def _popen_no_window(self, *a, creationflags=0, **k):
        _popen_init(self, *a, creationflags=creationflags | subprocess.CREATE_NO_WINDOW, **k)
    subprocess.Popen.__init__ = _popen_no_window


def repo_root():
    """The main checkout (owner of .mcdev), also when this file runs from a worktree."""
    here = Path(__file__).resolve().parent.parent
    r = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=here, capture_output=True, text=True)
    return Path(r.stdout.strip()).parent if r.returncode == 0 and r.stdout.strip() else here


ROOT = repo_root()
STATE_DIR = ROOT / ".mcdev"
CAM = STATE_DIR / "cam"
STATE = CAM / "state.json"
LOG = CAM / "mcfilm.log"
JAVA_SERVER = ROOT / ".tools" / "jre25" / "bin" / "java.exe"
SERVER_JAR = ROOT / ".tools" / "server-26.3.jar"
MC_INSTALL = Path(os.environ.get("MCFILM_INSTALL", r"C:\Users\danir\curseforge\minecraft\Install"))
MC_VERSION = "26.3"
USER = "ClaudeCam"
CAM_PORTS = range(25700, 25720)
WIDTH, HEIGHT = 1280, 720
IDLE_SECS = int(os.environ.get("MCFILM_IDLE") or 600)
TIMES = {"dawn": 23400, "sunrise": 23400, "day": 1000, "noon": 6000, "dusk": 12600, "sunset": 12600, "night": 14000, "midnight": 18000}

# ---------------------------------------------------------------- small utils
def log(*a):
    msg = " ".join(str(x) for x in a)
    print(msg, flush=True)
    try:
        CAM.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(time.strftime("%H:%M:%S ") + msg + "\n")
    except OSError:
        pass


def die(msg):
    log("ERROR:", msg)
    raise SystemExit(1)


def load_state():
    try:
        return json.loads(STATE.read_text())
    except (OSError, ValueError):
        return {}


def save_state(st):
    CAM.mkdir(parents=True, exist_ok=True)
    st["touched"] = time.time()
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(st, indent=2))
    os.replace(tmp, STATE)


def touch():
    st = load_state()
    if st:
        save_state(st)


def offline_uuid(name):
    h = bytearray(hashlib.md5(f"OfflinePlayer:{name}".encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x30
    h[8] = (h[8] & 0x3F) | 0x80
    return uuid.UUID(bytes=bytes(h))


def port_busy(port):
    with socket.socket() as s:
        try:
            s.bind(("0.0.0.0", port))
            return False
        except OSError:
            return True


def free_port():
    for p in CAM_PORTS:
        if not port_busy(p) and not port_busy(p + 10000):
            return p
    die("no free cam port in 25700-25719")


def proc_cmdline(pid):
    """Command line of a PID ('' if gone). Used to make sure a PID is still OUR cam process before killing it."""
    if not pid:
        return ""
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
                        f"(Get-CimInstance Win32_Process -Filter 'ProcessId={int(pid)}').CommandLine"],
                       capture_output=True, text=True, timeout=30)
    return r.stdout.strip()


def ours(pid):
    return str(CAM).lower() in proc_cmdline(pid).lower().replace("/", "\\")


def kill(pid, what):
    if pid and ours(pid):
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)
        log(f"killed {what} (pid {pid})")


def pid_alive(pid):
    if not pid:
        return False
    out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout
    return str(pid) in out


# ---------------------------------------------------------------- rcon
class Rcon:
    def __init__(self, port, password, timeout=10):
        self.s = socket.create_connection(("127.0.0.1", port), timeout=timeout)
        self.lock = threading.Lock()
        if self._req(3, password)[0] == -1:
            raise RuntimeError("rcon auth failed")

    def _req(self, typ, body):
        b = struct.pack("<ii", 7, typ) + body.encode() + b"\0\0"
        self.s.sendall(struct.pack("<i", len(b)) + b)
        n = struct.unpack("<i", self._exact(4))[0]
        data = self._exact(n)
        return struct.unpack("<i", data[:4])[0], data[8:-2].decode("utf-8", "replace")

    def _exact(self, n):
        d = b""
        while len(d) < n:
            c = self.s.recv(n - len(d))
            if not c:
                raise ConnectionError("rcon closed")
            d += c
        return d

    def __call__(self, cmd):
        with self.lock:
            return self._req(2, cmd)[1]

    def close(self):
        try:
            self.s.close()
        except OSError:
            pass


def mcdev_rcon(port):
    return Rcon(port + 10000, (STATE_DIR / "rcon.secret").read_text().strip(), timeout=5)


# ---------------------------------------------------------------- cam server
def registry():
    return json.loads((STATE_DIR / "registry.json").read_text())


def build_pack(s):
    """Same zip as mcdev's build_resource_pack: game pack + demo overlay (later layers win)."""
    src = Path(s["src"])
    layers = [src / "resourcepack"] + ([src / "demos" / s["demo"] / "resourcepack"] if s.get("demo") else [])
    files = {}
    for layer in layers:
        if layer.exists():
            files.update({f.relative_to(layer).as_posix(): f for f in layer.rglob("*") if f.is_file()})
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        if "pack.mcmeta" not in files:
            z.writestr("pack.mcmeta", json.dumps({"pack": {"description": "empty", "min_format": 97, "max_format": 97}}))
        for rel in sorted(files):
            z.writestr(zipfile.ZipInfo(rel, (2026, 1, 1, 0, 0, 0)), files[rel].read_bytes(), zipfile.ZIP_DEFLATED)
    return buf.getvalue()


def prepare_server(target):
    reg = registry()
    if target not in reg:
        die(f"unknown server {target!r} (see `mcdev ls`)")
    s = reg[target]
    src = STATE_DIR / "servers" / target
    if not (src / "world" / "level.dat").exists():
        die(f"{src}\\world has no level.dat")
    if s.get("status") == "up" and s.get("port"):
        try:
            r = mcdev_rcon(s["port"])
            log(f"{target}: {r('list').strip()}  (read-only: save-all flush only)")
            r("save-all flush")
            r.close()
            time.sleep(1.5)
        except OSError as e:
            log(f"{target}: rcon not reachable ({e}); copying the world as saved on disk")
    d = CAM / "servers" / target
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    # junctions (datapacks/game, demo, devnav) are followed: the copy is independent of the checkout
    shutil.copytree(src / "world", d / "world", ignore=shutil.ignore_patterns("session.lock"))
    port, pw = free_port(), secrets.token_hex(8)
    props = {}
    for line in (src / "server.properties").read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            props[k] = v
    props.update({
        "server-port": port, "rcon.port": port + 10000, "rcon.password": pw, "enable-rcon": "true",
        "online-mode": "false", "enforce-secure-profile": "false", "white-list": "false", "accepts-transfers": "false",
        "pause-when-empty-seconds": -1,
        "motd": f"mcfilm cam - {target}", "max-players": 2, "spawn-protection": 0, "broadcast-rcon-to-ops": "false",
        "view-distance": 12, "sync-chunk-writes": "false",
    })
    (d / "eula.txt").write_text("eula=true\n")
    (d / "ops.json").write_text(json.dumps([{"uuid": str(offline_uuid(USER)), "name": USER, "level": 4, "bypassesPlayerLimit": True}]))
    pack = build_pack(s)
    sha = hashlib.sha1(pack).hexdigest()
    www = CAM / "www"
    www.mkdir(parents=True, exist_ok=True)
    (www / f"{sha}.zip").write_bytes(pack)
    http = port + 100  # 25800+: served by the watchdog process
    props.update({"resource-pack": f"http\\://localhost\\:{http}/{sha}.zip", "resource-pack-sha1": sha,
                  "require-resource-pack": "true", "resource-pack-prompt": "",
                  "resource-pack-id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "mcfilm-" + target))})
    (d / "server.properties").write_text("".join(f"{k}={v}\n" for k, v in props.items()))
    return d, port, pw, sha, http


def launch_server(d, port):
    out = open(d / "console.log", "ab")
    flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
    # the gameDir path ('...\.mcdev\cam\...') in the command line is what `ours()` checks before any kill
    p = subprocess.Popen([str(JAVA_SERVER), "-Xmx2G", "-Xms512M", "-XX:+UseZGC", f"-Dmcfilm.dir={d}", "-jar", str(SERVER_JAR), "--nogui"],
                         cwd=d, stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=flags)
    return p.pid


def wait_for(path, pattern, timeout, pid=None, since=0):
    t0 = time.time()
    rx = re.compile(pattern)
    while time.time() - t0 < timeout:
        if pid and not pid_alive(pid):
            return None
        if path.exists():
            txt = path.read_text(errors="replace")[since:]
            m = rx.search(txt)
            if m:
                return m
        time.sleep(0.3)
    return None


# ---------------------------------------------------------------- cam client
def client_java():
    for p in (MC_INSTALL / "java" / "java_25" / "bin" / "javaw.exe", MC_INSTALL / "runtime" / "java-runtime-epsilon" / "windows-x64" /
              "java-runtime-epsilon" / "bin" / "javaw.exe", ROOT / ".tools" / "jre25" / "bin" / "javaw.exe"):
        if p.exists():
            return p
    die("no Java 25 runtime found (CurseForge Install/java/java_25 or .tools/jre25)")


def rules_ok(rules):
    if not rules:
        return True
    ok = False
    for r in rules:
        os_ = r.get("os", {})
        match = (not os_.get("name") or os_["name"] == "windows") and (not os_.get("arch") or os_["arch"] in ("x86_64", "x64"))
        if r.get("features"):
            match = False
        if match:
            ok = r["action"] == "allow"
    return ok


def client_command(game_dir, host_port):
    vdir = MC_INSTALL / "versions" / MC_VERSION
    v = json.loads((vdir / f"{MC_VERSION}.json").read_text())
    libs = MC_INSTALL / "libraries"
    cp = []
    for lib in v["libraries"]:
        if not rules_ok(lib.get("rules")):
            continue
        art = lib.get("downloads", {}).get("artifact")
        if art:
            p = libs / art["path"]
            if not p.exists():
                die(f"missing library {p}")
            cp.append(str(p))
    cp.append(str(vdir / f"{MC_VERSION}.jar"))
    natives = game_dir / "natives"
    jvm = ["-Xms1G", "-Xmx3G", "-XX:+UseZGC", "-XX:StackShadowPages=32", "--enable-native-access=ALL-UNNAMED",
           "--add-exports", "java.base/jdk.internal.misc=ALL-UNNAMED",
           f"-Djava.library.path={natives / 'java'}", f"-Djna.tmpdir={natives / 'jna'}",
           f"-Dorg.lwjgl.system.SharedLibraryExtractPath={natives / 'lwjgl'}", f"-Dio.netty.native.workdir={natives / 'netty'}",
           "-Dminecraft.launcher.brand=mcfilm", "-Dminecraft.launcher.version=1", "-cp", os.pathsep.join(cp)]
    game = ["--username", USER, "--version", MC_VERSION, "--gameDir", str(game_dir), "--assetsDir", str(MC_INSTALL / "assets"),
            "--assetIndex", v["assetIndex"]["id"], "--uuid", offline_uuid(USER).hex, "--accessToken", "0", "--clientId", "0",
            "--xuid", "0", "--userType", "legacy", "--versionType", "release", "--width", str(WIDTH), "--height", str(HEIGHT),
            "--quickPlayMultiplayer", host_port]
    return [str(client_java()), *jvm, v["mainClass"], *game]


def write_options(game_dir, fov, render_distance):
    base = Path(r"C:\Users\danir\curseforge\minecraft\Instances\Nonios's Map Remastered") / "options.txt"
    version = "5023"
    if base.exists():  # only the data version is taken from the user's options (read-only)
        m = re.search(r"^version:(\d+)", base.read_text(), re.M)
        version = m.group(1) if m else version
    opts = {
        "version": version, "fov": round((fov - 70) / 40, 4), "renderDistance": render_distance, "simulationDistance": 8,
        "guiScale": 2, "fullscreen": "false", "enableVsync": "false", "maxFps": 60, "inactivityFpsLimit": '"minimized"',
        "pauseOnLostFocus": "false", "bobView": "false", "chatVisibility": 2, "narrator": 0, "narratorHotkey": "false",
        "tutorialStep": "none", "onboardAccessibility": "false", "joinedFirstServer": "true", "skipMultiplayerWarning": "true",
        "realmsNotifications": "false", "telemetryOptInExtra": "false", "musicToast": '"never"', "showAutosaveIndicator": "false",
        "hideServerAddress": "true", "particles": 0, "graphicsPreset": '"fancy"', "renderClouds": '"true"', "ao": "true",
        "entityShadows": "true", "vignette": "true", "allowServerListing": "false", "sharePresence": '"none"', "showSubtitles": "false",
        "resourcePacks": '["vanilla"]',
        "darkMojangStudiosBackground": "true", "hideSplashTexts": "true", "inGameNotification": "false",
        "notificationDisplayTime": 0.5, "key_key.toggleGui": "key.keyboard.f1", "key_key.screenshot": "key.keyboard.f2", "lang": "en_us",
    }
    for cat in ("master", "music", "record", "weather", "block", "hostile", "neutral", "player", "ambient", "voice", "ui"):
        opts[f"soundCategory_{cat}"] = "0.0"
    (game_dir / "options.txt").write_text("".join(f"{k}:{v}\n" for k, v in opts.items()))


def write_servers_dat(game_dir, addr):
    """Uncompressed NBT: {servers:[{ip, name, acceptTextures:1b, hidden:0b}]}. Quick play picks the entry with this ip."""
    def tag_str(name, val):
        n, v = name.encode(), val.encode()
        return bytes([8]) + struct.pack(">H", len(n)) + n + struct.pack(">H", len(v)) + v

    def tag_byte(name, val):
        n = name.encode()
        return bytes([1]) + struct.pack(">H", len(n)) + n + bytes([val])
    entry = tag_str("ip", addr) + tag_str("name", "mcfilm") + tag_byte("acceptTextures", 1) + tag_byte("hidden", 0) + bytes([0])
    lst = bytes([9]) + struct.pack(">H", 7) + b"servers" + bytes([10]) + struct.pack(">i", 1) + entry
    (game_dir / "servers.dat").write_bytes(bytes([10, 0, 0]) + lst + bytes([0]))


# ---------------------------------------------------------------- windows: find / key / capture
user32, gdi32 = ctypes.windll.user32, ctypes.windll.gdi32
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass
WNDENUMPROC = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)


def find_window(pid):
    found = []

    def cb(hwnd, _):
        p = wt.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if p.value == pid and user32.IsWindowVisible(hwnd):
            n = user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(n + 1)
            user32.GetWindowTextW(hwnd, buf, n + 1)
            if buf.value.startswith("Minecraft"):
                found.append((hwnd, buf.value))
        return True
    user32.EnumWindows(WNDENUMPROC(cb), 0)
    return found[0] if found else (None, None)


VK = {"F1": (0x70, 0x3B), "F2": (0x71, 0x3C), "F3": (0x72, 0x3D), "T": (0x54, 0x14), "ESC": (0x1B, 0x01)}


def key(hwnd, name, down=True, up=True):
    """Keystroke straight into the cam window's message queue: no focus needed, the user's keyboard is untouched."""
    vk, sc = VK[name]
    if down:
        user32.PostMessageW(hwnd, 0x0100, vk, 1 | (sc << 16))
    if up:
        user32.PostMessageW(hwnd, 0x0101, vk, 1 | (sc << 16) | (1 << 30) | (1 << 31))


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wt.DWORD), ("biWidth", wt.LONG), ("biHeight", wt.LONG), ("biPlanes", wt.WORD), ("biBitCount", wt.WORD),
                ("biCompression", wt.DWORD), ("biSizeImage", wt.DWORD), ("biXPelsPerMeter", wt.LONG), ("biYPelsPerMeter", wt.LONG),
                ("biClrUsed", wt.DWORD), ("biClrImportant", wt.DWORD)]


class Grabber:
    """PrintWindow(PW_CLIENTONLY | PW_RENDERFULLCONTENT): the window's own rendered content, even when other windows cover it."""

    def __init__(self, hwnd):
        self.hwnd = hwnd
        r = wt.RECT()
        user32.GetClientRect(hwnd, ctypes.byref(r))
        self.w, self.h = r.right - r.left, r.bottom - r.top
        if self.w <= 0 or self.h <= 0:
            die("cam window has no client area (minimized?)")
        self.wdc = user32.GetDC(hwnd)
        self.mdc = gdi32.CreateCompatibleDC(self.wdc)
        self.bmp = gdi32.CreateCompatibleBitmap(self.wdc, self.w, self.h)
        gdi32.SelectObject(self.mdc, self.bmp)
        self.bi = BITMAPINFOHEADER(ctypes.sizeof(BITMAPINFOHEADER), self.w, -self.h, 1, 32, 0, 0, 0, 0, 0, 0)
        self.buf = ctypes.create_string_buffer(self.w * self.h * 4)

    def grab(self):
        """BGRA bytes, top-down."""
        user32.PrintWindow(self.hwnd, self.mdc, 3)
        gdi32.GetDIBits(self.mdc, self.bmp, 0, self.h, self.buf, ctypes.byref(self.bi), 0)
        return self.buf.raw

    def image(self):
        from PIL import Image
        return Image.frombuffer("RGBA", (self.w, self.h), self.grab(), "raw", "BGRA", 0, 1).convert("RGB")

    def close(self):
        gdi32.DeleteObject(self.bmp)
        gdi32.DeleteDC(self.mdc)
        user32.ReleaseDC(self.hwnd, self.wdc)


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    tools = STATE_DIR / "tools"
    hits = sorted(tools.glob("ffmpeg*/bin/ffmpeg.exe"))
    if hits:
        return str(hits[-1])
    # the imageio-ffmpeg wheel on PyPI carries a static gyan.dev build (x264 included), ~30 MB, fast CDN
    log("ffmpeg not found: fetching the imageio-ffmpeg wheel into .mcdev/tools (~30 MB, once)")
    tmp = tools / "wheel"
    subprocess.run([sys.executable, "-m", "pip", "download", "imageio-ffmpeg", "--no-deps", "--only-binary=:all:",
                    "--platform", "win_amd64", "-d", str(tmp), "-q"], check=True)
    whl = zipfile.ZipFile(next(tmp.glob("imageio_ffmpeg-*.whl")))
    exe = next(n for n in whl.namelist() if n.endswith(".exe"))
    out = tools / "ffmpeg-imageio" / "bin" / "ffmpeg.exe"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(whl.read(exe))
    whl.close()
    shutil.rmtree(tmp, ignore_errors=True)
    return str(out)


# ---------------------------------------------------------------- session
def session_alive(st):
    return bool(st) and pid_alive(st.get("server_pid")) and pid_alive(st.get("client_pid"))


def close_session(st=None, reason="close"):
    st = st if st is not None else load_state()
    if not st:
        return
    log(f"closing cam session ({reason})")
    if st.get("rcon_port") and pid_alive(st.get("server_pid")):
        try:
            r = Rcon(st["rcon_port"], st["rcon_pw"], timeout=3)
            r("stop")
            r.close()
        except (OSError, RuntimeError):
            pass
    kill(st.get("client_pid"), "cam client")
    for _ in range(40):
        if not pid_alive(st.get("server_pid")):
            break
        time.sleep(0.5)
    kill(st.get("server_pid"), "cam server")
    STATE.unlink(missing_ok=True)


def start_watchdog(http_port):
    flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
    pyw = Path(sys.executable)
    p = subprocess.Popen([str(pyw), str(Path(__file__).resolve()), "_watchdog", "--dir", str(CAM), "--http", str(http_port)],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)
    return p.pid


def watchdog(_a):
    """Detached: kills the cam session once no mcfilm command touched it for IDLE_SECS (or its owner died mid-shoot)."""
    import functools
    import http.server
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(CAM / "www"))
    h.log_message = lambda *x: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", int(_a.http)), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    while True:
        time.sleep(5)
        st = load_state()
        if not st or st.get("watchdog_pid") != os.getpid():
            return
        idle = time.time() - st.get("touched", 0)
        owner = st.get("owner_pid")
        orphan = owner and not st.get("keep") and not pid_alive(owner)
        if idle > IDLE_SECS or orphan or not (pid_alive(st.get("server_pid")) or pid_alive(st.get("client_pid"))):
            close_session(st, "watchdog: " + ("owner gone" if orphan else f"idle {int(idle)}s"))
            return


def up(target, fov=70, render_distance=12, keep=False):
    """Start (or reuse) the cam server + client for target. Returns (state, rcon, hwnd)."""
    st = load_state()
    same_pack = st.get("pack_sha1") == hashlib.sha1(build_pack(registry()[target])).hexdigest() if st.get("target") == target else False
    if session_alive(st) and st.get("target") == target and same_pack:
        hwnd, _ = find_window(st["client_pid"])
        if hwnd:
            r = Rcon(st["rcon_port"], st["rcon_pw"])
            st["owner_pid"] = None if keep or st.get("keep") else os.getpid()
            st["keep"] = keep or st.get("keep")
            save_state(st)
            return st, r, hwnd
    if st:
        close_session(st, "switching target" if st.get("target") != target else "resource pack changed" if not same_pack else "stale session")
    t0 = time.time()
    d, port, pw, sha, http = prepare_server(target)
    game = CAM / "client"
    game.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(game / "resourcepacks", ignore_errors=True)
    write_options(game, fov, render_distance)
    write_servers_dat(game, f"localhost:{port}")
    for f in (game / "logs" / "latest.log", d / "logs" / "latest.log"):
        f.unlink(missing_ok=True)
    st = {"target": target, "port": port, "rcon_port": port + 10000, "rcon_pw": pw, "server_dir": str(d),
          "pack_sha1": sha, "http_port": http, "keep": keep, "owner_pid": None if keep else os.getpid(), "started": time.time()}
    st["server_pid"] = launch_server(d, port)
    save_state(st)
    st["watchdog_pid"] = start_watchdog(http)
    save_state(st)
    log(f"cam server {target} copy on :{port} (pid {st['server_pid']}) booting...")
    if not wait_for(d / "logs" / "latest.log", r"Done \(", 180, st["server_pid"]):
        close_session(st, "server failed")
        die(f"cam server did not start, see {d / 'console.log'}")
    log(f"cam server up in {time.time() - t0:.0f}s; launching client")
    cout = open(game / "console.log", "wb")
    cp = subprocess.Popen(client_command(game, f"localhost:{port}"), cwd=game, stdout=cout, stderr=subprocess.STDOUT,
                          stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW)
    st["client_pid"] = cp.pid
    save_state(st)
    prev = user32.GetForegroundWindow()
    if not wait_for(d / "logs" / "latest.log", rf"{USER} joined the game", 240, cp.pid):
        close_session(st, "client failed")
        die(f"cam client did not join, see {game / 'logs' / 'latest.log'}")
    hwnd = None
    for _ in range(40):
        hwnd, title = find_window(cp.pid)
        if hwnd:
            break
        time.sleep(0.25)
    if not hwnd:
        close_session(st, "no window")
        die("cam client window not found")
    if prev and prev != hwnd:  # hand focus back to whatever the user had in front (best effort)
        user32.SetForegroundWindow(prev)
    r = Rcon(st["rcon_port"], st["rcon_pw"])
    # No F1: 26.3's window is SDL3, which ignores keys posted to an unfocused window (and stealing focus would disturb the
    # user). Spectator mode already drops hotbar, hand and (mostly) the crosshair; chat is hidden in options.txt;
    # this copy of the server is ours, so the sidebar goes and the action bar/titles are blanked while filming (clean_hud).
    r(f"gamemode spectator {USER}")
    for slot in ("sidebar", "list", "below_name"):
        r(f"scoreboard objectives setdisplay {slot}")
    clean_hud(r)
    save_state(st)
    time.sleep(4)  # the join toast ("Chat messages can't be verified", offline server) must expire first
    log(f"cam client joined in {time.time() - t0:.0f}s total (pid {cp.pid}, window '{title}')")
    return st, r, hwnd


# ---------------------------------------------------------------- camera paths
def look(pos, at):
    dx, dy, dz = at[0] - pos[0], at[1] - pos[1], at[2] - pos[2]
    yaw = -math.degrees(math.atan2(dx, dz))
    pitch = -math.degrees(math.atan2(dy, math.hypot(dx, dz)))
    return yaw, pitch


def floats(t, n=None):
    v = [float(x) for x in str(t).replace(",", " ").split()]
    if n and len(v) not in (n if isinstance(n, tuple) else (n,)):
        die(f"expected {n} numbers, got {t!r}")
    return v


def lerp_angle(a, b, f):
    d = (b - a + 180) % 360 - 180
    return a + d * f


def smooth(f):
    return f * f * (3 - 2 * f)


class Path_:
    """pose(f) for f in 0..1 -> (x, y, z, yaw, pitch).
    JSON: {"look_at":[x,y,z]?, "ease":true?, "keys":[{"t":0,"pos":[x,y,z],"yaw":0,"pitch":10}, ...]}
       or {"orbit":{"center":[x,y,z],"radius":10,"height":4,"start":0,"degrees":90}} (looks at the centre)."""

    def __init__(self, spec):
        self.spec = spec
        self.at = spec.get("look_at")
        self.ease = spec.get("ease", True)
        if "orbit" in spec:
            o = spec["orbit"]
            self.at = self.at or o["center"]
        else:
            keys = spec["keys"]
            if len(keys) == 1:
                keys = keys * 2
            t0, t1 = keys[0].get("t", 0), keys[-1].get("t", len(keys) - 1)
            for i, k in enumerate(keys):
                k["_f"] = (k.get("t", i) - t0) / ((t1 - t0) or 1)
            self.keys = keys

    def pose(self, f):
        f = min(max(f, 0.0), 1.0)
        if "orbit" in self.spec:
            o = self.spec["orbit"]
            g = smooth(f) if self.ease and o.get("ease", False) else f
            a = math.radians(o.get("start", 0) + o.get("degrees", 90) * g)
            c = o["center"]
            pos = (c[0] - math.sin(a) * o["radius"], c[1] + o.get("height", 0), c[2] + math.cos(a) * o["radius"])
            return (*pos, *look(pos, self.at))
        k = self.keys
        i = max(j for j in range(len(k)) if k[j]["_f"] <= f) if f > 0 else 0
        i = min(i, len(k) - 2)
        a, b = k[i], k[i + 1]
        g = (f - a["_f"]) / ((b["_f"] - a["_f"]) or 1)
        g = smooth(g) if self.ease else g
        pos = tuple(a["pos"][n] + (b["pos"][n] - a["pos"][n]) * g for n in range(3))
        if self.at:
            return (*pos, *look(pos, self.at))
        return (*pos, lerp_angle(a.get("yaw", 0), b.get("yaw", 0), g), a.get("pitch", 0) + (b.get("pitch", 0) - a.get("pitch", 0)) * g)


def path_from_args(a):
    if a.path:
        p = Path(a.path)
        if not p.exists():
            p = ROOT / a.path
        return Path_(json.loads(p.read_text()))
    if a.orbit:
        v = floats(a.orbit, (4, 5, 6, 7))
        cx, cy, cz, rad = v[:4]
        return Path_({"orbit": {"center": [cx, cy, cz], "radius": rad, "height": v[4] if len(v) > 4 else 3,
                                "degrees": v[5] if len(v) > 5 else 90, "start": v[6] if len(v) > 6 else 0}})
    if a.at:
        v = floats(a.at, (5, 6))
        return Path_({"keys": [{"t": 0, "pos": v[:3], "yaw": v[3], "pitch": v[4]}]})
    if a.dolly:  # "x1 y1 z1 x2 y2 z2 lx ly lz": move from 1 to 2 looking at l
        v = floats(a.dolly, 9)
        return Path_({"look_at": v[6:9], "keys": [{"t": 0, "pos": v[0:3]}, {"t": 1, "pos": v[3:6]}]})
    return None


def clean_hud(r):
    """Blank the action bar and titles (demos keep printing status there); --hud skips this."""
    r(f'title {USER} actionbar ""')
    r(f"title {USER} clear")


def tp(r, pose):
    x, y, z, yaw, pitch = pose
    r(f"tp {USER} {x:.3f} {y:.3f} {z:.3f} {yaw % 360:.2f} {pitch:.2f}")


# ---------------------------------------------------------------- setup / filming
def apply_setup(r, a):
    if a.time is not None:
        t = TIMES.get(str(a.time).lower(), a.time)
        r(f"time set {t}")
    if a.weather:
        r(f"weather {a.weather}")
    for c in a.setup or []:
        c = c.strip().lstrip("/").replace("{cam}", USER)
        if c.startswith("trigger "):  # a trigger fires once per tick (the demo re-enables it next tick)
            c = f"execute as {USER} at @s run {c}"
            time.sleep(0.12)
        out = r(c)
        log(f"  /{c}" + (f"  -> {out.strip()[:120]}" if out.strip() else ""))


def is_black(img):
    from PIL import ImageStat
    return max(ImageStat.Stat(img.convert("L").resize((64, 36))).extrema[0][1], 0) < 12


def contact_sheet(frames, out, cols=3, label=None):
    """frames: list of (seconds, PIL image) -> one PNG grid, each tile captioned with its time."""
    from PIL import Image, ImageDraw
    tw = 640
    th = round(frames[0][1].height * tw / frames[0][1].width)
    rows = math.ceil(len(frames) / cols)
    head = 28 if label else 0
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 4, head + rows * th + (rows + 1) * 4), (24, 24, 24))
    dr = ImageDraw.Draw(sheet)
    if label:
        dr.text((8, 8), label, fill=(230, 230, 230))
    for i, (t, im) in enumerate(frames):
        x, y = 4 + (i % cols) * (tw + 4), head + 4 + (i // cols) * (th + 4)
        sheet.paste(im.resize((tw, th)), (x, y))
        cap = f"{t:.1f}s" if isinstance(t, (int, float)) else str(t)
        dr.rectangle((x, y, x + 8 + 7 * len(cap), y + 16), fill=(0, 0, 0))
        dr.text((x + 4, y + 2), cap, fill=(255, 255, 0))
    sheet.save(out)


CLIENT_LOG = CAM / "client" / "logs" / "latest.log"
SHADER_RX = re.compile(r"/(WARN|ERROR)\]: .*(shader|post effect|post_effect|program|uniform|sampler|compil|link|pipeline|Failed to load|Couldn't)", re.I)
NOISE_RX = re.compile(r"end_of_frame|realms|profile properties|user properties", re.I)


def log_mark():
    return CLIENT_LOG.stat().st_size if CLIENT_LOG.exists() else 0


def client_warnings(mark):
    """New WARN/ERROR lines about shaders/post effects/resources in the cam client log since mark (agents: read these)."""
    if not CLIENT_LOG.exists():
        return []
    with open(CLIENT_LOG, "rb") as f:
        f.seek(mark)
        txt = f.read().decode("utf-8", "replace")
    out = [l.strip() for l in txt.splitlines() if SHADER_RX.search(l) and not NOISE_RX.search(l)]
    for l in out:
        log("client:", l[:300])
    return out


def out_dir(a, default):
    d = Path(a.out) if a.out else STATE_DIR / "film" / default
    if not d.is_absolute():
        d = ROOT / d
    d.mkdir(parents=True, exist_ok=True)
    return d


def cmd_shoot(a):
    path = path_from_args(a)
    if not path:
        die("need a camera: --path file.json, --orbit, --dolly or --at")
    out = out_dir(a, time.strftime("%Y%m%d-%H%M%S"))
    fps, secs = a.fps, a.seconds
    had = session_alive(load_state())
    st, r, hwnd = up(a.server, a.fov, a.render_distance, keep=a.keep)
    try:
        mark = log_mark()
        tp(r, path.pose(0))
        apply_setup(r, a)
        time.sleep(a.settle)
        if not a.hud:
            clean_hud(r)
            time.sleep(0.15)
        g = Grabber(hwnd)
        mp4 = out / "video.mp4"
        ff = subprocess.Popen([ffmpeg(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{g.w}x{g.h}",
                               "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                               "-movflags", "+faststart", str(mp4)], stdin=subprocess.PIPE)
        n = int(secs * fps)
        want = sorted({round(i * (n - 1) / (a.tiles - 1)) for i in range(a.tiles)}) if a.tiles > 1 else [0]
        keep_frames, last, dup = {}, None, 0
        t0 = time.perf_counter()
        for i in range(n):
            tgt = t0 + i / fps
            f = i / max(n - 1, 1)
            tp(r, path.pose(f))
            if not a.hud:
                clean_hud(r)
            now = time.perf_counter()
            if now < tgt:
                time.sleep(tgt - now)
            if time.perf_counter() - tgt > 1.5 / fps and last is not None:
                frame, dup = last, dup + 1  # running late: repeat the last frame so the video stays real-time
            else:
                frame = g.grab()
            ff.stdin.write(frame)
            last = frame
            if i in want:
                from PIL import Image
                keep_frames[i] = Image.frombuffer("RGBA", (g.w, g.h), frame, "raw", "BGRA", 0, 1).convert("RGB")
            if i % fps == 0:
                touch()
        ff.stdin.close()
        ff.wait(timeout=120)
        g.close()
        took = time.perf_counter() - t0
        frames_dir = out / "frames"
        frames_dir.mkdir(exist_ok=True)
        for old in frames_dir.glob("*.png"):
            old.unlink()
        tiles = []
        for i in want:
            im = keep_frames[i]
            im.save(frames_dir / f"t{i / fps:05.2f}s.png")
            tiles.append((i / fps, im))
        label = f"{a.server}  {' | '.join(a.setup or [])}  time={a.time}  {secs}s @ {fps}fps"
        contact_sheet(tiles, out / "sheet.png", cols=math.ceil(math.sqrt(len(tiles))), label=label)
        black = sum(is_black(im) for _, im in tiles)
        meta = {"server": a.server, "setup": a.setup, "time": a.time, "seconds": secs, "fps": fps, "frames": n,
                "late_frames_repeated": dup, "wall_secs": round(took, 2), "black_tiles": black, "path": path.spec,
                "client_warnings": client_warnings(mark)}
        (out / "shot.json").write_text(json.dumps(meta, indent=2))
        log(f"shot: {mp4}  sheet: {out / 'sheet.png'}  ({n} frames, {dup} repeated, {black} black tiles)")
        if black:
            log("WARNING: black frames in the sheet (window minimized? chunks not loaded? try --settle 6)")
    finally:
        r.close()
        if not (a.keep or had):
            close_session(load_state(), "shot done")


def cmd_still(a):
    shots = [floats(s, (5, 6)) for s in a.shot or []]
    if a.path_still:
        spec = json.loads(Path(a.path_still).read_text())
        shots += [[*s["pos"], *(look(s["pos"], s["look_at"]) if "look_at" in s else (s.get("yaw", 0), s.get("pitch", 0)))]
                  for s in spec["shots"]]
    if not shots:
        die("need --shot 'x y z yaw pitch' (repeatable) or --shots file.json")
    out = out_dir(a, "still-" + time.strftime("%Y%m%d-%H%M%S"))
    had = session_alive(load_state())
    st, r, hwnd = up(a.server, a.fov, a.render_distance, keep=a.keep)
    try:
        mark = log_mark()
        tp(r, shots[0][:5])
        apply_setup(r, a)
        g = Grabber(hwnd)
        tiles = []
        for i, s in enumerate(shots):
            tp(r, s[:5])
            time.sleep(a.settle)
            if not a.hud:
                clean_hud(r)
                time.sleep(0.15)
            im = g.image()
            p = out / f"still{i + 1}.png"
            im.save(p)
            tiles.append((f"#{i + 1} {s[0]:.0f} {s[1]:.0f} {s[2]:.0f}", im))
            touch()
            log(f"still {p}" + ("  (BLACK)" if is_black(im) else ""))
        g.close()
        if len(tiles) > 1:
            contact_sheet(tiles, out / "sheet.png", cols=min(3, len(tiles)), label=f"{a.server}  {' | '.join(a.setup or [])}  time={a.time}")
            log(f"sheet: {out / 'sheet.png'}")
        (out / "shot.json").write_text(json.dumps({"server": a.server, "setup": a.setup, "time": a.time, "shots": shots,
                                                   "client_warnings": client_warnings(mark)}, indent=2))
    finally:
        r.close()
        if not (a.keep or had):
            close_session(load_state(), "stills done")


def cmd_up(a):
    st, r, hwnd = up(a.server, a.fov, a.render_distance, keep=True)
    r.close()
    log(f"cam session up: {a.server} copy on localhost:{st['port']}; closes after {IDLE_SECS}s without mcfilm commands")


def cmd_cmd(a):
    st = load_state()
    if not session_alive(st):
        die("no cam session (mcfilm up --server X)")
    r = Rcon(st["rcon_port"], st["rcon_pw"])
    print(r(" ".join(a.command).replace("{cam}", USER)))
    r.close()
    touch()


def cmd_status(_a):
    st = load_state()
    if not st:
        print("no cam session")
        return
    print(json.dumps({k: st.get(k) for k in ("target", "port", "server_pid", "client_pid", "watchdog_pid", "keep")}, indent=1))
    print("alive:", session_alive(st), " idle:", int(time.time() - st.get("touched", 0)), "s")


def cmd_close(_a):
    close_session(reason="close")
    # leftovers from a crashed run: any java whose command line points into .mcdev\cam
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
                        "Get-CimInstance Win32_Process -Filter \"Name like 'java%'\" | ForEach-Object { \"$($_.ProcessId)`t$($_.CommandLine)\" }"],
                       capture_output=True, text=True)
    for line in r.stdout.splitlines():
        pid, _, cl = line.partition("\t")
        if str(CAM).lower() in cl.lower():
            kill(int(pid), "stray cam java")
    print("cam closed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--server", required=True, help="mcdev server to clone (world + datapacks + resource pack)")
        p.add_argument("--setup", action="append", help="command run before filming (repeatable); 'trigger ...' runs as the camera; {cam} = camera name")
        p.add_argument("--time", help="dawn|noon|dusk|midnight|<ticks>")
        p.add_argument("--weather", help="clear|rain|thunder")
        p.add_argument("--fov", type=float, default=70)
        p.add_argument("--render-distance", type=int, default=12)
        p.add_argument("--settle", type=float, default=3.0, help="seconds to wait after setup/teleport before capturing")
        p.add_argument("--hud", action="store_true", help="keep the action bar / titles (blanked by default)")
        p.add_argument("--keep", action="store_true", help="leave the cam session running afterwards (watchdog closes it when idle)")
        p.add_argument("--out", help="output dir (default .mcdev/film/<timestamp>)")

    p = sub.add_parser("shoot", help="record a video + contact sheet along a camera path")
    common(p)
    p.add_argument("--path", help="camera path JSON (see docs/mcfilm.md)")
    p.add_argument("--orbit", help="'cx cy cz radius [height] [degrees] [start]' around a point, looking at it")
    p.add_argument("--dolly", help="'x1 y1 z1 x2 y2 z2 lookx looky lookz'")
    p.add_argument("--at", help="'x y z yaw pitch' fixed camera")
    p.add_argument("--seconds", type=float, default=6)
    p.add_argument("--fps", type=int, default=20)
    p.add_argument("--tiles", type=int, default=9, help="frames in the contact sheet")
    p.set_defaults(fn=cmd_shoot)

    p = sub.add_parser("still", help="single frames from fixed positions")
    common(p)
    p.add_argument("--shot", action="append", help="'x y z yaw pitch' (repeatable)")
    p.add_argument("--shots", dest="path_still", help='JSON {"shots":[{"pos":[x,y,z],"look_at":[x,y,z]}|{"pos":..,"yaw":..,"pitch":..}]}')
    p.set_defaults(fn=cmd_still)

    p = sub.add_parser("up", help="start/keep a cam session")
    p.add_argument("--server", required=True)
    p.add_argument("--fov", type=float, default=70)
    p.add_argument("--render-distance", type=int, default=12)
    p.set_defaults(fn=cmd_up)
    p = sub.add_parser("cmd", help="RCON command on the cam server ({cam} = camera)")
    p.add_argument("command", nargs="+")
    p.set_defaults(fn=cmd_cmd)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    sub.add_parser("close", help="stop the cam client + server (and any stray cam java)").set_defaults(fn=cmd_close)
    p = sub.add_parser("_watchdog")
    p.add_argument("--dir")
    p.add_argument("--http", default="25800")
    p.set_defaults(fn=watchdog)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
