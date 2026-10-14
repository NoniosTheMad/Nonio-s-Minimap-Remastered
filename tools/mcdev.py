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
  mcdev feedback [--all] [--ack]      inbox of feedback sent from the in-game menu
  mcdev nav                           regenerate the in-game server list
  mcdev review <name> [--done]        star/unstar a server as waiting for the user's review
"""
import argparse, io, json, os, re, secrets, shutil, socket, struct, subprocess, sys, time, uuid, zipfile
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
_rcon_conns, _rcon_locks = {}, {}

def rcon(port, command, timeout=5):
    """RCON command; connections are kept open and reused (servers log every new connection)."""
    import threading
    lock = _rcon_locks.setdefault(port, threading.Lock())
    with lock:
        for attempt in (0, 1):
            try:
                if port not in _rcon_conns:
                    _rcon_conns[port] = _rcon_open(port, timeout)
                return _rcon_send(_rcon_conns[port], command)
            except (OSError, struct.error):
                c = _rcon_conns.pop(port, None)
                if c:
                    c.close()
                if attempt:
                    raise

def _rcon_pkt(rid, typ, body):
    b = struct.pack("<ii", rid, typ) + body.encode("utf-8") + b"\0\0"
    return struct.pack("<i", len(b)) + b

def _rcon_recv(s):
    n = struct.unpack("<i", _rcon_exact(s, 4))[0]
    data = _rcon_exact(s, n)
    rid, _ = struct.unpack("<ii", data[:8])
    return rid, data[8:-2].decode("utf-8", "replace")

def _rcon_exact(s, n):
    data = b""
    while len(data) < n:
        chunk = s.recv(n - len(data))
        if not chunk:
            raise ConnectionError("rcon closed")
        data += chunk
    return data

def _rcon_open(port, timeout):
    s = socket.create_connection(("127.0.0.1", port), timeout=timeout)
    s.sendall(_rcon_pkt(1, 3, secret()))
    if _rcon_recv(s)[0] == -1:
        raise RuntimeError("rcon auth failed")
    return s

def _rcon_send(s, command):
    s.sendall(_rcon_pkt(2, 2, command))
    return _rcon_recv(s)[1]


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
        if log.exists() and "Done (" in log.read_text(errors="replace"):
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
    live = [(n, s) for n, s in sorted(reg.items(), key=lambda kv: (not kv[1].get("review"), kv[1]["port"])) if s.get("status") == "up"]
    actions = []
    for n, s in live:
        label = ([text("\u2605 ", "yellow")] if s.get("review") else []) + \
                [text(n, "gold" if s["persistent"] else "aqua", bold=True), text(f"  {s['desc'] or s['branch']}", "gray")]
        tip = f"{s['branch']}" + (f" / demo {s['demo']}" if s.get("demo") else "") + (f"\n\n{s['todo']}" if s.get("todo") else "")
        actions.append({"label": label, "tooltip": text(tip), "width": 310,
                        "action": {"type": "minecraft:run_command", "command": f"trigger devnav.go set {s['port']}"}})
    return {"type": "minecraft:multi_action", "title": text("Dev servers", "gold"),
            "body": [{"type": "minecraft:plain_message", "contents": text(f"{len(live)} running. \u2605 = waiting for your review. Hover a server to see what to try.", "gray"), "width": 300}],
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
    # Feedback = a tagged Book & Quill. Signing it queues the book content in storage and pings the
    # daemon, which pulls the pages over RCON (no quoting/length/newline limits, unlike dialog text + say).
    (fn / "fb_give.mcfunction").write_text(
        "clear @s minecraft:writable_book[minecraft:custom_data~{devnav_fb:1b}]\n"
        'give @s minecraft:writable_book[minecraft:custom_data={devnav_fb:1b},'
        'minecraft:item_name={"text":"Feedback for Claude","color":"green"},'
        'minecraft:lore=[{"text":"Write, then Sign. The title is the topic.","color":"gray","italic":false}]]\n'
        'tellraw @s {"text":"[dev] Feedback book in your inventory: write, then Sign (title = topic). Any length, any characters.","color":"green"}\n')
    (fn / "fb_book.mcfunction").write_text(
        "advancement revoke @s only devnav:fb_signed\n"
        "data modify storage devnav:fb inbox append from entity @s Inventory"
        '[{id:"minecraft:written_book",components:{"minecraft:custom_data":{devnav_fb:1b}}}].components."minecraft:written_book_content"\n'
        "clear @s minecraft:written_book[minecraft:custom_data~{devnav_fb:1b}]\n"
        "function devnav:fb_give\nfunction devnav:fb_notify\n")
    adv = d / "data" / "devnav" / "advancement"
    adv.mkdir(parents=True, exist_ok=True)
    (adv / "fb_signed.json").write_text(json.dumps({
        "criteria": {"signed": {"trigger": "minecraft:inventory_changed", "conditions": {"items": [
            {"items": "minecraft:written_book", "predicates": {"minecraft:custom_data": "{devnav_fb:1b}"}}]}}},
        "rewards": {"function": "devnav:fb_book"}}))
    # Dialog buttons only use /trigger (permission 0 -> no "run this command?" prompt);
    # the privileged part (transfer, reload, ...) runs here at function permission level.
    (fn / "nav_load.mcfunction").write_text(
        "scoreboard objectives add devnav.go trigger\nscoreboard objectives add devnav.act trigger\n")
    (fn / "nav_tick.mcfunction").write_text(
        "scoreboard players enable @a devnav.go\nscoreboard players enable @a devnav.act\n"
        "execute as @a[scores={devnav.go=1..}] run function devnav:go\n"
        "execute as @a[scores={devnav.act=1}] run function devnav:list\n"
        "execute as @a[scores={devnav.act=2}] run function devnav:refresh\n"
        "execute if entity @a[scores={devnav.act=3}] run reload\n"
        "execute as @a[scores={devnav.act=4}] run function devnav:fb_give\n"
        "execute as @a[scores={devnav.act=5}] run function devnav:reset_world\n"
        "scoreboard players reset @a[scores={devnav.act=1..}] devnav.act\n")
    (fn / "go.mcfunction").write_text(
        "execute store result storage devnav:tmp port int 1 run scoreboard players get @s devnav.go\n"
        "scoreboard players reset @s devnav.go\nfunction devnav:go_port with storage devnav:tmp\n")
    (fn / "go_port.mcfunction").write_text(f"$transfer {HOST} $(port) @s\n")
    ftags = d / "data" / "minecraft" / "tags" / "function"
    ftags.mkdir(parents=True, exist_ok=True)
    (ftags / "load.json").write_text(json.dumps({"values": ["devnav:nav_load"]}))
    (ftags / "tick.json").write_text(json.dumps({"values": ["devnav:nav_tick"]}))
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
        f'data modify storage devnav:req q append value {{verb:"repack"}}\ndata modify storage devnav:req q[-1].uuid set from entity @s UUID\ntransfer {HOST} {hub_port} @s\n' if name != "hub" else f"transfer {HOST} {hub_port} @s\n")
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
    ] + ([
        "tellraw @s " + json.dumps([text("\nWhat to try here:\n", "yellow", bold=True), text(s["todo"], "white")]),
    ] if s.get("todo") else [])
    if name == "hub":
        welcome += ["fill -8 63 -8 8 63 8 minecraft:polished_blackstone keep", "tp @s 0.5 64 0.5", "function devnav:rules"]
    elif void:
        # first login on a fresh void world spawns at y=-63, before setworldspawn applies
        welcome += ["fill -6 63 -6 6 63 6 minecraft:smooth_stone keep",
                    "execute if entity @s[y=-70,dy=60] run tp @s 0.5 64 0.5"]
    (fn / "welcome.mcfunction").write_text("\n".join(welcome) + "\n")
    tags = d / "data" / "minecraft" / "tags" / "function"
    tags.mkdir(parents=True)
    (tags / "load.json").write_text(json.dumps({"values": ["devnav:load"]}))
    (tags / "tick.json").write_text(json.dumps({"values": ["devnav:tick"]}))
    (fn / "fb_notify.mcfunction").write_text('data modify storage devnav:req q append value {verb:"feedback"}\ndata modify storage devnav:req q[-1].uuid set from entity @s UUID\n')
    resettable = not s["persistent"] or name == "test"
    (fn / "reset_world.mcfunction").write_text(  # daemon wipes the world, restarts, sends you back
        f'data modify storage devnav:req q append value {{verb:"resetworld"}}\ndata modify storage devnav:req q[-1].uuid set from entity @s UUID\ntransfer {HOST} {hub_port} @s\n' if resettable else
        'tellraw @s {"text":"[dev] Only demo/branch servers (and test) can be reset from here.","color":"red"}\n')
    menu = {"type": "minecraft:multi_action", "title": text("Nonios Dev", "gold"),
            "external_title": text("Nonios Dev"),
            "body": [{"type": "minecraft:plain_message", "width": 300, "contents": [
                text("You are on ", "gray"), text(name, "yellow", bold=True), text(f"  ({where})\n", "gray"),
                text(s["desc"] or "", "white")]}]
            + ([{"type": "minecraft:plain_message", "width": 310, "contents": [
                text("What to try here:\n", "yellow", bold=True), text(s["todo"], "white")]}] if s.get("todo") else []),
            "actions": [
                {"label": text("Servers...", "aqua"), "action": {"type": "minecraft:run_command", "command": "trigger devnav.act set 1"}},
                {"label": "Refresh resource pack", "tooltip": text("Hop to the hub, rebuild the pack, come back"),
                 "action": {"type": "minecraft:run_command", "command": "trigger devnav.act set 2"}},
                {"label": "Reload datapacks", "action": {"type": "minecraft:run_command", "command": "trigger devnav.act set 3"}},
                {"label": text("Feedback (book)", "green"), "tooltip": text("Gives a Book & Quill: write, then Sign. Title = topic."),
                 "action": {"type": "minecraft:run_command", "command": "trigger devnav.act set 4"}}]
            + ([{"label": text("Reset this server", "red"), "tooltip": text("Fresh world: wipes everything built/broken here, restarts, brings you back (~15s)"),
                 "action": {"type": "minecraft:run_command", "command": "trigger devnav.act set 5"}}]
               if resettable else []),
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
    """Serves .mcdev/packs over HTTP and handles in-game requests queued in storage devnav:req (polled via RCON)."""
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
    while True:
        for n, s in load_reg().items():
            if s.get("status") != "up":
                continue
            try:
                r = rcon(s["port"] + 10000, "data get storage devnav:req q", timeout=2)
            except (OSError, RuntimeError):
                continue
            if "contents: [{" not in r:
                continue
            rcon(s["port"] + 10000, "data remove storage devnav:req q")
            for verb, ints in re.findall(r'verb: "(\w+)"(?:, uuid: \[I; ([-\d, ]+)\])?', r):
                player = uuid_str(ints) if ints else None
                print(time.strftime("%H:%M:%S"), "request", n, verb, player, flush=True)
                if verb == "repack":
                    threading.Thread(target=repack, args=(n, player), daemon=True).start()
                elif verb == "resetworld":
                    threading.Thread(target=reset_world, args=(n, player), daemon=True).start()
                elif verb == "feedback":
                    try:
                        pull_feedback(n, s)
                    except Exception as e:  # never let the daemon die on a bad book
                        print("feedback pull failed:", e, flush=True)
        time.sleep(1)

def uuid_str(ints):
    """'[I; a, b, c, d]' ints -> canonical UUID string (usable as an entity selector)."""
    h = "".join(f"{int(i) & 0xFFFFFFFF:08x}" for i in ints.split(","))
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"

def snbt_value(resp):
    """Value part of a '... has the following contents: <snbt>' RCON reply, unquoted if it is a string."""
    import ast, re
    v = resp.split("contents: ", 1)[1].strip()
    if v[:1] in "\"'":
        return ast.literal_eval(v)  # SNBT string escapes are a subset of Python's
    m = re.search(r'text:\s*("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', v)
    return ast.literal_eval(m.group(1)) if m else v

CLIENT_LOG = Path(r"C:\Users\danir\curseforge\minecraft\Instances\Nonios's Map Remastered\logs\latest.log")
NOISE = re.compile(r"IoRegistration|ServerboundResourcePackPacket|prepare_spawn|^\s+at |logged in with entity|lost connection|"
                   r"left the game|joined the game|RCON|Loaded [0-9]+ |Server empty for|Disconnecting|UUID of player|\[MCDEV\]|Saving|Saved")

def feedback_context(name, s, player):
    """Indented context block appended to each feedback entry: where the user was + what just happened."""
    port = s["port"] + 10000
    ctx = [f"branch {s.get('branch')} @ {git_head(s['src'])}" + (f", demo {s['demo']}" if s.get("demo") else "")
           + f", worktree {s['src']}"]
    try:
        pos = rcon(port, f"data get entity {player} Pos").split("data: ", 1)[-1]
        dim = rcon(port, f"data get entity {player} Dimension").split("data: ", 1)[-1]
        mode = rcon(port, f"data get entity {player} playerGameType").split("data: ", 1)[-1]
        if "No entity" not in pos:
            ctx.append(f"at {pos} in {dim}, gamemode {mode}")
    except OSError:
        pass
    def tail(path, n):
        try:
            lines = Path(path).read_text(errors="replace").splitlines()[-400:]
        except OSError:
            return []
        done = max((i for i, l in enumerate(lines) if "Done (" in l), default=-1)  # skip startup chatter
        return [l.strip() for l in lines[done + 1:] if not NOISE.search(l)][-n:]
    srv = tail(SERVERS / name / "logs" / "latest.log", 12)
    cli = [l for l in tail(CLIENT_LOG, 200) if "[CHAT]" in l or "Connecting to" in l][-12:]
    if srv: ctx += ["server log:"] + ["  " + l for l in srv]
    if cli: ctx += ["client chat:"] + ["  " + l for l in cli]
    return "".join(f"  | {l}\n" for l in ctx)

def git_head(src):
    try:
        return subprocess.run(["git", "-C", str(src), "log", "-1", "--format=%h %s"], capture_output=True, text=True).stdout.strip()
    except OSError:
        return "?"

def pull_feedback(name, s):
    """Drain storage devnav:fb inbox (signed feedback books) into the feedback log."""
    port = s["port"] + 10000
    while "passed" in rcon(port, "execute if data storage devnav:fb inbox[0]"):
        a = rcon(port, "data get storage devnav:fb inbox[0].author")
        player = snbt_value(a) if "contents" in a else "?"
        r = rcon(port, "data get storage devnav:fb inbox[0].title.raw")
        title = snbt_value(r) if "contents" in r else "(untitled)"
        pages, i = [], 0
        while "contents" in (r := rcon(port, f"data get storage devnav:fb inbox[0].pages[{i}].raw")):
            pages.append(snbt_value(r))
            i += 1
        rcon(port, "data remove storage devnav:fb inbox[0]")
        body = "\n\n".join(pages).strip().replace("\n", "\n    ")
        with open(FEEDBACK, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M')} {name} ({s.get('branch')}) [{player}] {title}:\n    {body}\n"
                    + feedback_context(name, s, player))
        print(time.strftime("%H:%M:%S"), f"feedback from {player} on {name}: {title}", flush=True)

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
    send_back(reg, s, player)

def reset_world(name, player):
    """Player was sent to the hub; wipe this server's world (test: re-copy main), restart, send them back."""
    reg = load_reg()
    s = reg.get(name)
    if not s or (s["persistent"] and name != "test"):
        return
    print(time.strftime("%H:%M:%S"), f"resetting world of {name}", flush=True)
    stop(name, s)
    rmtree_safe(SERVERS / name / "world")
    start(name, s, reg)
    send_back(reg, s, player)

def send_back(reg, s, player):
    hub = reg.get("hub", {})
    for _ in range(60):  # wait until the player has landed on the hub
        try:
            if player and "passed" in rcon(hub["port"] + 10000, f"execute if entity {player}"):
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
    s["todo"] = a.todo or read_todo(src, s["demo"]) or reg.get(name, {}).get("todo", "")
    s["review"] = reg.get(name, {}).get("review", not s["persistent"])
    t = start(name, s)
    print(f"{name} up on {HOST}:{port} ({t:.0f}s)  branch={branch}" + (f" demo={s['demo']}" if s['demo'] else ""))

def start(name, s, _reg=None):
    ensure_daemon()
    s["pack_sha1"] = build_resource_pack(name, s)
    reg = load_reg()
    reg[name] = s
    write_devnav(reg)
    write_server(name, s)
    harvest_feedback(name)  # then drop the old log so wait_ready can't see a stale "Done ("
    for f in (SERVERS / name / "logs" / "latest.log", SERVERS / name / ".feedback_seen"):
        f.unlink(missing_ok=True)
    s.update(pid=launch(name, s), started=time.time(), status="up")
    reg = load_reg()
    reg[name] = s
    save_reg(reg)
    t = wait_ready(name, s)
    refresh_nav(sync_status(reg))
    for w in check_server(name, s):
        print("WARNING:", w)
    return t

def check_server(name, s):
    """Catch breakage before the user does: datapack load errors + trigger objectives that can never fire."""
    import re
    warn = []
    log = (SERVERS / name / "logs" / "latest.log").read_text(errors="replace")
    warn += [l.strip() for l in log.splitlines()
             if re.search(r"Failed to load function|Couldn't load tag|Failed to parse|Couldn't parse element", l)]
    packs = [Path(s["src"]) / "datapack"] + ([Path(s["src"]) / "demos" / s["demo"] / "datapack"] if s.get("demo") else [])
    for pack in packs:
        files = list(pack.rglob("*.mcfunction")) + list(pack.rglob("*.json"))
        text = {f: f.read_text(errors="replace") for f in files}
        used = {o for t in text.values() for o in re.findall(r"trigger ([\w.]+)", t)}
        for obj in used:
            # the last enable/reset of obj in a function decides whether it is triggerable between ticks
            ok = False
            for f, t in text.items():
                ev = re.findall(rf"scoreboard players (enable|reset) (\S+) {re.escape(obj)}\b", t)
                if any(e == "enable" for e, _ in ev):
                    last = [e for e, sel in ev if e == "enable" or sel == "@a"][-1]
                    ok = ok or last == "enable"
            if not ok:
                warn.append(f"{pack.parent.name}: trigger '{obj}' is never left enabled (enable it after any 'reset @a {obj}')")
    return warn

def read_todo(src, demo):
    """demos/<demo>/try.txt: short plain-text 'what to do' shown in game."""
    f = Path(src) / "demos" / str(demo) / "try.txt"
    return f.read_text().strip() if demo and f.exists() else ""

def cmd_review(a):
    reg = load_reg()
    reg[a.name]["review"] = not a.done
    save_reg(reg)
    refresh_nav(sync_status(reg))
    print(a.name, "marked", "reviewed" if a.done else "awaiting review")

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

def online(s):
    try:
        r = rcon(s["port"] + 10000, "list")
        return [p.strip() for p in r.split(":", 1)[1].split(",") if p.strip()]
    except (OSError, IndexError):
        return []

def cmd_restart(a):
    """Restart; players on it are parked on the hub and sent back when it's up."""
    reg = sync_status(load_reg())
    s = reg[a.name]
    hub = reg.get("hub") if a.name != "hub" else None
    players = online(s) if hub and hub.get("status") == "up" else []
    for p in players:
        rcon(s["port"] + 10000, f"transfer {HOST} {hub['port']} {p}")
    stop(a.name, s)
    save_reg(reg)
    a.branch = a.demo = a.desc = a.mem = a.todo = None
    cmd_up(a)
    for p in players:
        for _ in range(20):
            if p in online(hub):
                rcon(hub["port"] + 10000, f"transfer {HOST} {s['port']} {p}")
                break
            time.sleep(0.5)

def cmd_reset(a):
    if a.name != "test":
        sys.exit("only `reset test` is supported (copies main's world)")
    reg = load_reg()
    if "test" in reg:
        stop("test", reg["test"])
        save_reg(reg)
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
    """Feedback is captured live by the daemon; kept as a hook for stop/start."""
    return []

def cmd_feedback(a):
    """Inbox: prints entries not yet acknowledged; --all for history, --ack marks them read."""
    if not FEEDBACK.exists():
        print("(no feedback yet)")
        return
    lines = FEEDBACK.read_text().splitlines(True)
    mark = STATE / "feedback.read"
    read = int(mark.read_text()) if mark.exists() else 0
    out = lines if a.all else lines[read:]
    print("".join(out) or "(no new feedback)")
    if a.ack:
        mark.write_text(str(len(lines)))

def main():
    p = argparse.ArgumentParser(prog="mcdev", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    u = sp.add_parser("up"); u.add_argument("name"); u.add_argument("--branch"); u.add_argument("--demo")
    u.add_argument("--desc"); u.add_argument("--mem"); u.add_argument("--todo", help="what the user should try (else demos/<demo>/try.txt)")
    u.set_defaults(f=cmd_up)
    rv = sp.add_parser("review", help="star a server as awaiting review, or --done")
    rv.add_argument("name"); rv.add_argument("--done", action="store_true"); rv.set_defaults(f=cmd_review)
    d = sp.add_parser("down"); d.add_argument("name"); d.add_argument("--purge", action="store_true"); d.set_defaults(f=cmd_down)
    for nm, f in (("restart", cmd_restart), ("reset", cmd_reset)):
        x = sp.add_parser(nm); x.add_argument("name"); x.set_defaults(f=f)
    sp.add_parser("ls").set_defaults(f=cmd_ls)
    r = sp.add_parser("reload"); r.add_argument("name", nargs="?"); r.set_defaults(f=cmd_reload)
    c = sp.add_parser("cmd"); c.add_argument("name"); c.add_argument("command", nargs="+"); c.set_defaults(f=cmd_cmd)
    l = sp.add_parser("logs"); l.add_argument("name"); l.add_argument("-n", type=int, default=40); l.set_defaults(f=cmd_logs)
    fb = sp.add_parser("feedback"); fb.add_argument("--all", action="store_true"); fb.add_argument("--ack", action="store_true"); fb.set_defaults(f=cmd_feedback)
    sp.add_parser("nav").set_defaults(f=lambda a: refresh_nav(sync_status(load_reg())))
    sp.add_parser("_daemon").set_defaults(f=lambda a: daemon())
    a = p.parse_args()
    a.f(a)

if __name__ == "__main__":
    main()
