"""mcdev - local dev-server manager for the Nonios's Map remaster (Minecraft 26.3, vanilla).

Every server is a vanilla 26.3 server under .mcdev/servers/<name>/. Datapacks are
junctioned from a git checkout (repo root for main/test, .worktrees/<branch> for
branches), so editing files + `mcdev reload <name>` is enough for logic changes.
Resource packs are zipped on demand by a tiny HTTP server, so "Reconnect" in the
in-game dev menu always fetches the latest pack.

In game, press G (Quick Actions) or open the pause menu -> "Nonios Dev" to jump
between servers, reconnect, reload or leave feedback.

Usage:
  mcdev up <name> [--branch B] [--demo D] [--desc TEXT] [--mem 2G]
  mcdev up hub|main|test              presets (ports 25565/25566/25567)
  mcdev down <name> [--purge]         stop (ephemeral servers are deleted)
  mcdev restart <name>
  mcdev reset test                    re-copy main's world into test
  mcdev ls
  mcdev reload [name|all]             /reload datapacks via RCON
  mcdev cmd <name> <command...>       run a console command via RCON
  mcdev logs <name> [-n 40]
  mcdev feedback [--clear]            feedback sent from the in-game menu
  mcdev nav                           regenerate the in-game server list
"""
import argparse, io, json, os, secrets, shutil, socket, struct, subprocess, sys, time, uuid, zipfile
from pathlib import Path

# Windows defaults to cp1252; everything we write (dialogs, properties, logs) is UTF-8.
_wt, _rt = Path.write_text, Path.read_text
Path.write_text = lambda self, data, encoding="utf-8", **k: _wt(self, data, encoding=encoding, **k)
Path.read_text = lambda self, encoding="utf-8", **k: _rt(self, encoding=encoding, **k)

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / ".tools"
JAVA = TOOLS / "jre25" / "bin" / "java.exe"
JAR = TOOLS / "server-26.3.jar"
STATE = ROOT / ".mcdev"
SERVERS = STATE / "servers"
REG = STATE / "registry.json"
FEEDBACK = STATE / "feedback.log"
WORKTREES = ROOT / ".worktrees"
HOST = "localhost"
HTTP_PORT = 8800
OPS = [{"uuid": "e5e9dc0e-ef3c-41ca-b943-08ddfb204f02", "name": "NoniosTheMad", "level": 4, "bypassesPlayerLimit": True}]
DATA_FORMAT, RES_FORMAT = 121, 97

PRESETS = {
    "hub":  dict(port=25565, mem="1G", desc="Lobby. Press G to travel.", persistent=True, world="void"),
    "main": dict(port=25566, mem="3G", desc="The map itself - build here.", persistent=True, world="flat"),
    "test": dict(port=25567, mem="3G", desc="Copy of main + everything merged.", persistent=True, world="copy-main"),
}
EPHEMERAL_PORTS = range(25570, 25600)
VOID = '{"layers":[{"block":"minecraft:air","height":1}],"biome":"minecraft:the_void"}'
FLAT = '{"layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:stone","height":3},{"block":"minecraft:grass_block","height":1}],"biome":"minecraft:plains"}'


# ---------------------------------------------------------------- registry
def load_reg():
    return json.loads(REG.read_text()) if REG.exists() else {}

def save_reg(reg):
    STATE.mkdir(exist_ok=True)
    REG.write_text(json.dumps(reg, indent=2))

def secret():
    f = STATE / "rcon.secret"
    if not f.exists():
        STATE.mkdir(exist_ok=True)
        f.write_text(secrets.token_hex(12))
    return f.read_text().strip()

def pid_alive(pid):
    if not pid:
        return False
    out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout
    return str(pid) in out

def port_open(port):
    with socket.socket() as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", port)) == 0


# ---------------------------------------------------------------- rcon
def rcon(port, command, timeout=5):
    def pkt(rid, typ, body):
        b = struct.pack("<ii", rid, typ) + body.encode("utf-8") + b"\0\0"
        return struct.pack("<i", len(b)) + b
    def recv(s):
        n = struct.unpack("<i", s.recv(4))[0]
        data = b""
        while len(data) < n:
            data += s.recv(n - len(data))
        rid, _ = struct.unpack("<ii", data[:8])
        return rid, data[8:-2].decode("utf-8", "replace")
    with socket.create_connection(("127.0.0.1", port), timeout=timeout) as s:
        s.sendall(pkt(1, 3, secret()))
        if recv(s)[0] == -1:
            raise RuntimeError("rcon auth failed")
        s.sendall(pkt(2, 2, command))
        return recv(s)[1]


# ---------------------------------------------------------------- git / sources
def git(*a, cwd=ROOT):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)

def source_for(branch):
    """Checkout dir for a branch: repo root for main, a worktree otherwise."""
    if branch in (None, "main"):
        return ROOT
    wt = WORKTREES / branch.replace("/", "-")
    if not wt.exists():
        exists = git("rev-parse", "--verify", "--quiet", branch).returncode == 0
        r = git("worktree", "add", str(wt), branch) if exists else git("worktree", "add", "-b", branch, str(wt), "main")
        if r.returncode:
            sys.exit(r.stderr)
    return wt

def junction(link, target):
    import _winapi
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.exists() or os.path.islink(link):
        os.rmdir(link) if is_junction(link) else shutil.rmtree(link)
    _winapi.CreateJunction(str(target), str(link))

def is_junction(p):
    try:
        return bool(os.readlink(p))
    except OSError:
        return False

def rmtree_safe(p):
    """Delete a server dir without following junctions into the repo."""
    for dirpath, dirnames, _ in os.walk(p, topdown=True):
        for d in list(dirnames):
            full = Path(dirpath) / d
            if is_junction(full):
                os.rmdir(full)
                dirnames.remove(d)
    shutil.rmtree(p, ignore_errors=True)


# ---------------------------------------------------------------- server setup
def props(name, s):
    return {
        "server-port": s["port"], "enable-rcon": "true", "rcon.port": s["port"] + 10000, "rcon.password": secret(),
        "broadcast-rcon-to-ops": "false", "accepts-transfers": "true", "online-mode": "true",
        "enforce-secure-profile": "false", "white-list": "false", "function-permission-level": 4,
        "op-permission-level": 4, "spawn-protection": 0, "motd": f"Nonios Dev - {name} ({s['branch']})",
        "level-type": "minecraft\\:flat", "generator-settings": (FLAT if s["world"] == "flat" else VOID).replace(":", "\\:"),
        "generate-structures": "false", "difficulty": "normal", "gamemode": "creative" if name != "hub" else "adventure",
        "view-distance": 8, "simulation-distance": 6, "pause-when-empty-seconds": 120,
        "resource-pack": f"http://{HOST}:{HTTP_PORT}/{name}.zip", "resource-pack-id": str(uuid.uuid5(uuid.NAMESPACE_DNS, name)),
        "resource-pack-sha1": s.get("pack_sha1", ""), "require-resource-pack": "false", "resource-pack-prompt": "", "log-ips": "false",
    }

def write_server(name, s):
    d = SERVERS / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "eula.txt").write_text("eula=true\n")
    (d / "ops.json").write_text(json.dumps(OPS, indent=2))
    (d / "server.properties").write_text("".join(f"{k}={v}\n" for k, v in props(name, s).items()))
    if s["world"] == "copy-main" and not (d / "world" / "level.dat").exists():
        copy_main_world(d)
    packs = d / "world" / "datapacks"
    packs.mkdir(parents=True, exist_ok=True)
    src = Path(s["src"])
    if name != "hub":
        junction(packs / "game", src / "datapack")
    if s.get("demo"):
        junction(packs / "demo", src / "demos" / s["demo"] / "datapack")
    junction(packs / "devnav", STATE / "devnav")
    write_self_pack(name, s, packs / "devnav_self")

def copy_main_world(d):
    main_world = SERVERS / "main" / "world"
    if not main_world.exists():
        return
    if port_open(PRESETS["main"]["port"]):
        rcon(PRESETS["main"]["port"] + 10000, "save-all flush")
    shutil.copytree(main_world, d / "world", ignore=shutil.ignore_patterns("session.lock", "datapacks"), dirs_exist_ok=True)

def launch(name, s):
    d = SERVERS / name
    log = open(d / "console.log", "ab")
    flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
    p = subprocess.Popen([str(JAVA), f"-Xmx{s['mem']}", f"-Xms{s['mem']}" if name in ("main", "test") else "-Xms256M",
                          "-XX:+UseZGC", "-jar", str(JAR), "--nogui"],
                         cwd=d, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=flags)
    return p.pid

def wait_ready(name, s, timeout=180):
    log = SERVERS / name / "logs" / "latest.log"
    t0 = time.time()
    while time.time() - t0 < timeout:
        if not pid_alive(s["pid"]):
            sys.exit(f"{name} died during startup - see `mcdev logs {name}`")
        if log.exists() and log.stat().st_mtime >= s["started"] - 2 and "Done (" in log.read_text(errors="replace"):
            return time.time() - t0
        time.sleep(0.5)
    sys.exit(f"{name} not ready after {timeout}s")


# ---------------------------------------------------------------- devnav pack
def text(t, color=None, **kw):
    c = {"text": t}
    if color:
        c["color"] = color
    c.update(kw)
    return c

def nav_dialog(reg):
    live = [(n, s) for n, s in sorted(reg.items(), key=lambda kv: kv[1]["port"]) if s.get("status") == "up"]
    actions = []
    for n, s in live:
        label = [text(n, "gold" if s["persistent"] else "aqua", bold=True), text(f"  {s['branch']}" + (f" / {s['demo']}" if s.get("demo") else ""), "gray")]
        actions.append({"label": label, "tooltip": text(s["desc"] or n), "width": 300,
                        "action": {"type": "minecraft:run_command", "command": f"transfer {HOST} {s['port']}"}})
    return {"type": "minecraft:multi_action", "title": text("Dev servers", "gold"),
            "body": [{"type": "minecraft:plain_message", "contents": text(f"{len(live)} running. Gold = persistent, aqua = branch/demo.", "gray"), "width": 300}],
            "actions": actions or [{"label": "(none)", "action": {"type": "minecraft:run_command", "command": "help"}}],
            "columns": 1, "pause": False}

def snbt(v):
    """JSON -> SNBT good enough for /dialog show (strings double-quoted & escaped)."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, list):
        return "[" + ",".join(snbt(x) for x in v) + "]"
    return "{" + ",".join(f"{k}:{snbt(x)}" for k, x in v.items()) + "}"

def write_devnav(reg):
    d = STATE / "devnav"
    fn = d / "data" / "devnav" / "function"
    fn.mkdir(parents=True, exist_ok=True)
    (d / "pack.mcmeta").write_text(json.dumps({"pack": {"description": "mcdev navigation", "min_format": DATA_FORMAT, "max_format": DATA_FORMAT}}))
    (fn / "list.mcfunction").write_text(f"dialog show @s {snbt(nav_dialog(reg))}\n")
    (fn / "fb.mcfunction").write_text('$say [FEEDBACK] $(t)\n')
    tags = d / "data" / "minecraft" / "tags" / "dialog"
    tags.mkdir(parents=True, exist_ok=True)
    for t in ("quick_actions", "pause_screen_additions"):
        (tags / f"{t}.json").write_text(json.dumps({"values": ["devnav:menu"]}))

def write_self_pack(name, s, d):
    """Per-server part: the G-menu dialog (knows which server it is on)."""
    if d.exists():
        shutil.rmtree(d)
    (d / "data" / "devnav" / "dialog").mkdir(parents=True)
    (d / "data" / "devnav" / "function").mkdir(parents=True)
    (d / "pack.mcmeta").write_text(json.dumps({"pack": {"description": f"mcdev {name}", "min_format": DATA_FORMAT, "max_format": DATA_FORMAT}}))
    fn = d / "data" / "devnav" / "function"
    hub_port = PRESETS["hub"]["port"]
    # Refresh: hop to the hub, the daemon rebuilds the pack (restarting this server if it changed), then sends you back.
    (fn / "refresh.mcfunction").write_text(
        f"say [MCDEV] repack {name}\ntransfer {HOST} {hub_port} @s\n" if name != "hub" else f"transfer {HOST} {hub_port} @s\n")
    where = f"{s['branch']}" + (f" / demo {s['demo']}" if s.get("demo") else "")
    void = s["world"] == "void"
    (fn / "load.mcfunction").write_text(
        "scoreboard objectives add devnav.left minecraft.custom:minecraft.leave_game\n"
        + ("setworldspawn 0 64 0\n" if void else ""))
    (fn / "rules.mcfunction").write_text(  # separate file: a bad gamerule name only breaks this one
        "gamerule advance_time false\ngamerule advance_weather false\ngamerule spawn_mobs false\ntime set noon\n")
    (fn / "tick.mcfunction").write_text(
        "execute as @a[tag=!devnav.seen] run function devnav:welcome\n"
        "execute as @a[scores={devnav.left=1..}] run function devnav:welcome\n")
    welcome = [
        "tag @s add devnav.seen", "scoreboard players reset @s devnav.left",
        "title @s times 5 50 15",
        f"title @s subtitle {json.dumps(text(where, 'gray'))}",
        f"title @s title {json.dumps(text(name, 'gold'))}",
        "tellraw @s " + json.dumps([text("[dev] ", "dark_gray"), text("Press ", "gray"), text("G", "yellow"),
                                    text(" (Quick Actions) or ", "gray"), text("Esc > Nonios Dev", "yellow"), text(" to travel.", "gray")]),
    ]
    if name == "hub":
        welcome += ["fill -8 63 -8 8 63 8 minecraft:polished_blackstone keep", "tp @s 0.5 64 0.5", "function devnav:rules"]
    elif void:
        welcome += ["execute at @s run fill ~-6 63 ~-6 ~6 63 ~6 minecraft:smooth_stone keep"]
    (fn / "welcome.mcfunction").write_text("\n".join(welcome) + "\n")
    tags = d / "data" / "minecraft" / "tags" / "function"
    tags.mkdir(parents=True)
    (tags / "load.json").write_text(json.dumps({"values": ["devnav:load"]}))
    (tags / "tick.json").write_text(json.dumps({"values": ["devnav:tick"]}))
    feedback = {"type": "minecraft:notice", "title": text("Feedback", "gold"),
                "body": [{"type": "minecraft:plain_message", "contents": text(f"Goes to Claude, tagged with '{name}'.", "gray")}],
                "inputs": [{"type": "minecraft:text", "key": "t", "label": "Comment", "width": 300, "max_length": 2000,
                            "multiline": {"max_lines": 12, "height": 120}}],
                "action": {"label": "Send", "action": {"type": "minecraft:dynamic/run_command",
                                                       "template": f"function devnav:fb {{t:'[{name}] $(t)'}}"}}}
    menu = {"type": "minecraft:multi_action", "title": text("Nonios Dev", "gold"),
            "external_title": text("Nonios Dev"),
            "body": [{"type": "minecraft:plain_message", "width": 300, "contents": [
                text("You are on ", "gray"), text(name, "yellow", bold=True), text(f"  ({where})\n", "gray"),
                text(s["desc"] or "", "white")]}],
            "actions": [
                {"label": text("Servers...", "aqua"), "action": {"type": "minecraft:run_command", "command": "function devnav:list"}},
                {"label": "Refresh resource pack", "tooltip": text("Hop to the hub, rebuild the pack, come back"),
                 "action": {"type": "minecraft:run_command", "command": "function devnav:refresh"}},
                {"label": "Reload datapacks", "action": {"type": "minecraft:run_command", "command": "reload"}},
                {"label": text("Feedback...", "green"), "action": {"type": "minecraft:show_dialog", "dialog": feedback}}],
            "columns": 2, "pause": False}
    (d / "data" / "devnav" / "dialog" / "menu.json").write_text(json.dumps(menu, indent=1))

def refresh_nav(reg):
    write_devnav(reg)
    for n, s in reg.items():
        if s.get("status") == "up" and port_open(s["port"] + 10000):
            try:
                rcon(s["port"] + 10000, "reload")
            except OSError:
                pass


# ---------------------------------------------------------------- resource packs + daemon
PACKS = STATE / "packs"

def build_resource_pack(name, s):
    """Zip the game resource pack (+ demo overlay) deterministically; return its sha1."""
    import hashlib
    src = Path(s["src"])
    layers = [src / "resourcepack"] + ([src / "demos" / s["demo"] / "resourcepack"] if s.get("demo") else [])
    files = {}
    for layer in layers:  # later layers (demo) override earlier ones (game)
        if layer.exists():
            files.update({f.relative_to(layer).as_posix(): f for f in layer.rglob("*") if f.is_file()})
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        if "pack.mcmeta" not in files:
            z.writestr(zipfile.ZipInfo("pack.mcmeta", (2026, 1, 1, 0, 0, 0)),
                       json.dumps({"pack": {"description": "empty", "min_format": RES_FORMAT, "max_format": RES_FORMAT}}))
        for rel in sorted(files):
            z.writestr(zipfile.ZipInfo(rel, (2026, 1, 1, 0, 0, 0)), files[rel].read_bytes(), zipfile.ZIP_DEFLATED)
    data = buf.getvalue()
    PACKS.mkdir(parents=True, exist_ok=True)
    (PACKS / f"{name}.zip").write_bytes(data)
    return hashlib.sha1(data).hexdigest()

def daemon():
    """Serves .mcdev/packs over HTTP and reacts to '[MCDEV] ...' requests in server logs."""
    import re, threading
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
    class H(SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(PACKS), **k)
        def end_headers(self):
            self.send_header("Cache-Control", "no-store")
            super().end_headers()
        def log_message(self, fmt, *a):
            print(time.strftime("%H:%M:%S"), "http", fmt % a, flush=True)
    PACKS.mkdir(parents=True, exist_ok=True)
    threading.Thread(target=ThreadingHTTPServer(("127.0.0.1", HTTP_PORT), H).serve_forever, daemon=True).start()
    pat = re.compile(r"\[(\w+)\] \[MCDEV\] (\w+) (\S+)")
    offsets = {}
    while True:
        for n, s in load_reg().items():
            log = SERVERS / n / "logs" / "latest.log"
            if s.get("status") != "up" or not log.exists():
                continue
            size = log.stat().st_size
            off = offsets.setdefault(n, size)
            if size < off:
                off = 0
            if size > off:
                with open(log, "rb") as f:
                    f.seek(off)
                    chunk = f.read().decode("utf-8", "replace")
                offsets[n] = size
                for m in pat.finditer(chunk):
                    player, verb, arg = m.groups()
                    print(time.strftime("%H:%M:%S"), "request", player, verb, arg, flush=True)
                    if verb == "repack":
                        threading.Thread(target=repack, args=(arg, player), daemon=True).start()
        time.sleep(0.5)

def repack(name, player):
    """Player was sent to the hub; rebuild the pack, restart if it changed, send them back."""
    reg = load_reg()
    s = reg.get(name)
    if not s:
        return
    sha = build_resource_pack(name, s)
    if sha != s.get("pack_sha1"):
        print(time.strftime("%H:%M:%S"), f"pack changed for {name}, restarting", flush=True)
        stop(name, s)
        start(name, s, reg)
    hub = reg.get("hub", {})
    for _ in range(60):  # wait until the player has landed on the hub
        try:
            if player in rcon(hub["port"] + 10000, "list"):
                rcon(hub["port"] + 10000, f"transfer {HOST} {s['port']} {player}")
                return
        except (OSError, KeyError):
            pass
        time.sleep(0.5)

def ensure_daemon():
    STATE.mkdir(exist_ok=True)
    if port_open(HTTP_PORT):
        return
    flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
    subprocess.Popen([sys.executable, "-u", __file__, "_daemon"], stdout=open(STATE / "daemon.log", "ab"), stderr=subprocess.STDOUT,
                     stdin=subprocess.DEVNULL, creationflags=flags, cwd=ROOT)


# ---------------------------------------------------------------- commands
def sync_status(reg):
    for s in reg.values():
        if s.get("status") == "up" and not pid_alive(s.get("pid")):
            s["status"] = "down"
    return reg

def cmd_up(a):
    reg = sync_status(load_reg())
    name = a.name
    if name in reg and reg[name].get("status") == "up":
        print(f"{name} already up on :{reg[name]['port']}")
        return
    preset = PRESETS.get(name, {})
    used = {s["port"] for s in reg.values() if s.get("status") == "up" or s.get("persistent")}
    port = preset.get("port") or (reg.get(name, {}).get("port") if name in reg else None) or next(p for p in EPHEMERAL_PORTS if p not in used)
    branch = a.branch or reg.get(name, {}).get("branch") or "main"
    src = source_for(branch)
    if a.demo and not (src / "demos" / a.demo / "datapack").exists():
        sys.exit(f"no demos/{a.demo}/datapack in {src}")
    s = dict(port=port, branch=branch, src=str(src), demo=a.demo or reg.get(name, {}).get("demo"),
             mem=a.mem or preset.get("mem", "1536M"), persistent=preset.get("persistent", False),
             world=preset.get("world", "void"),
             desc=a.desc or preset.get("desc") or reg.get(name, {}).get("desc", ""))
    t = start(name, s)
    print(f"{name} up on {HOST}:{port} ({t:.0f}s)  branch={branch}" + (f" demo={s['demo']}" if s['demo'] else ""))

def start(name, s, _reg=None):
    ensure_daemon()
    s["pack_sha1"] = build_resource_pack(name, s)
    reg = load_reg()
    reg[name] = s
    write_devnav(reg)
    write_server(name, s)
    s.update(pid=launch(name, s), started=time.time(), status="up")
    reg = load_reg()
    reg[name] = s
    save_reg(reg)
    t = wait_ready(name, s)
    refresh_nav(sync_status(reg))
    return t

def stop(name, s):
    if pid_alive(s.get("pid")):
        try:
            rcon(s["port"] + 10000, "stop")
        except OSError:
            subprocess.run(["taskkill", "/PID", str(s["pid"]), "/F"], capture_output=True)
        for _ in range(60):
            if not pid_alive(s["pid"]):
                break
            time.sleep(0.5)
        else:
            subprocess.run(["taskkill", "/PID", str(s["pid"]), "/F"], capture_output=True)
    harvest_feedback(name)
    s["status"] = "down"

def cmd_down(a):
    reg = load_reg()
    if a.name not in reg:
        sys.exit(f"unknown server {a.name}")
    s = reg[a.name]
    stop(a.name, s)
    if not s["persistent"] or a.purge:
        rmtree_safe(SERVERS / a.name)
        del reg[a.name]
    save_reg(reg)
    refresh_nav(reg)
    print(f"{a.name} down" + ("" if a.name in reg else " (deleted)"))

def cmd_restart(a):
    reg = load_reg()
    s = reg[a.name]
    stop(a.name, s)
    save_reg(reg)
    a.branch = a.demo = a.desc = a.mem = None
    cmd_up(a)

def cmd_reset(a):
    if a.name != "test":
        sys.exit("only `reset test` is supported (copies main's world)")
    reg = load_reg()
    if "test" in reg:
        stop("test", reg["test"])
        save_reg(reg)
    shutil.rmtree(SERVERS / "test" / "world", ignore_errors=True)
    rmtree_safe(SERVERS / "test" / "world") if (SERVERS / "test" / "world").exists() else None
    a.branch = a.demo = a.desc = a.mem = None
    cmd_up(a)

def cmd_ls(a):
    reg = sync_status(load_reg())
    save_reg(reg)
    print(f"{'name':<22}{'state':<7}{'addr':<17}{'branch':<22}{'demo':<16}desc")
    for n, s in sorted(reg.items(), key=lambda kv: kv[1]["port"]):
        print(f"{n:<22}{s['status']:<7}{HOST + ':' + str(s['port']):<17}{s['branch']:<22}{s.get('demo') or '-':<16}{s['desc']}")
    print(f"pack server: http://{HOST}:{HTTP_PORT}  ({'up' if port_open(HTTP_PORT) else 'down'})")

def targets(name):
    reg = sync_status(load_reg())
    return [(n, s) for n, s in reg.items() if s.get("status") == "up" and (name in (None, "all") or n == name)]

def cmd_reload(a):
    for n, s in targets(a.name):
        print(n, "->", rcon(s["port"] + 10000, "reload") or "reloaded")

def cmd_cmd(a):
    for n, s in targets(a.name):
        print(rcon(s["port"] + 10000, " ".join(a.command)))

def cmd_logs(a):
    log = SERVERS / a.name / "logs" / "latest.log"
    print("".join(log.read_text(errors="replace").splitlines(True)[-a.n:]))

def harvest_feedback(name):
    log = SERVERS / name / "logs" / "latest.log"
    if not log.exists():
        return []
    marker = SERVERS / name / ".feedback_seen"
    seen = int(marker.read_text()) if marker.exists() else 0
    lines = log.read_text(errors="replace").splitlines()
    if seen > len(lines):  # log rotated
        seen = 0
    new = [l for l in lines[seen:] if "[FEEDBACK]" in l]
    marker.write_text(str(len(lines)))
    if new:
        with open(FEEDBACK, "a", encoding="utf-8") as f:
            f.writelines(l + "\n" for l in new)
    return new

def cmd_feedback(a):
    for n in load_reg():
        harvest_feedback(n)
    if FEEDBACK.exists():
        print(FEEDBACK.read_text(encoding="utf-8"))
        if a.clear:
            FEEDBACK.rename(STATE / f"feedback-{time.strftime('%Y%m%d-%H%M%S')}.log")
    else:
        print("(no feedback yet)")

def main():
    p = argparse.ArgumentParser(prog="mcdev", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    u = sp.add_parser("up"); u.add_argument("name"); u.add_argument("--branch"); u.add_argument("--demo")
    u.add_argument("--desc"); u.add_argument("--mem"); u.set_defaults(f=cmd_up)
    d = sp.add_parser("down"); d.add_argument("name"); d.add_argument("--purge", action="store_true"); d.set_defaults(f=cmd_down)
    for nm, f in (("restart", cmd_restart), ("reset", cmd_reset)):
        x = sp.add_parser(nm); x.add_argument("name"); x.set_defaults(f=f)
    sp.add_parser("ls").set_defaults(f=cmd_ls)
    r = sp.add_parser("reload"); r.add_argument("name", nargs="?"); r.set_defaults(f=cmd_reload)
    c = sp.add_parser("cmd"); c.add_argument("name"); c.add_argument("command", nargs="+"); c.set_defaults(f=cmd_cmd)
    l = sp.add_parser("logs"); l.add_argument("name"); l.add_argument("-n", type=int, default=40); l.set_defaults(f=cmd_logs)
    fb = sp.add_parser("feedback"); fb.add_argument("--clear", action="store_true"); fb.set_defaults(f=cmd_feedback)
    sp.add_parser("nav").set_defaults(f=lambda a: refresh_nav(sync_status(load_reg())))
    sp.add_parser("_daemon").set_defaults(f=lambda a: daemon())
    a = p.parse_args()
    a.f(a)

if __name__ == "__main__":
    main()
