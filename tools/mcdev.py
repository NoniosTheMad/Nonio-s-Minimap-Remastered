"""mcdev - local dev-server manager for the Nonios's Map remaster (Minecraft 26.3, vanilla).

Every server is a vanilla 26.3 server under .mcdev/servers/<name>/. Datapacks are
junctioned from a git checkout (repo root for main/test, .worktrees/<branch> for
branches), so editing files + `mcdev reload <name>` is enough for logic changes.
Resource packs are zipped at start and served by the daemon's tiny HTTP server; when a
server's pack sources change the daemon restarts it with the new pack (players hop and return).

In game, press G (Quick Actions) or open the pause menu -> "Nonios Dev" to jump
between servers, reload or leave feedback.

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
  mcdev feedback [--all] [--ack]      feedback sent from the game (book or chat), entries numbered #N
  mcdev feedback --resolve N [note]   tell the user (in-game inbox) that feedback #N is resolved
  mcdev notify "text"                 message the user's in-game inbox (G > Inbox; delivered in chat when online)
  mcdev nav                           regenerate the in-game server list
  mcdev review <name> [--done]        star/unstar a server as waiting for the user's review
  mcdev archive <name> [--note TEXT]  stop it, keep world + branch@commit, free its port (G > Servers > Archive revives it)
  mcdev unarchive <name>              revive (same as `up <name>`): recreates the worktree if needed, new port
"""
import argparse, io, json, os, re, secrets, shutil, socket, struct, subprocess, sys, time, uuid, zipfile
from pathlib import Path

# Windows defaults to cp1252; everything we write (dialogs, properties, logs) is UTF-8.
_wt, _rt = Path.write_text, Path.read_text
Path.write_text = lambda self, data, encoding="utf-8", **k: _wt(self, data, encoding=encoding, **k)
Path.read_text = lambda self, encoding="utf-8", **k: _rt(self, encoding=encoding, **k)

# The daemon has no console, so every console child (tasklist, git, taskkill, ...) would pop up its own
# window and steal focus from the game. Default every child process to no window.
if os.name == "nt":
    _popen_init = subprocess.Popen.__init__
    def _popen_no_window(self, *a, creationflags=0, **k):
        _popen_init(self, *a, creationflags=creationflags | subprocess.CREATE_NO_WINDOW, **k)
    subprocess.Popen.__init__ = _popen_no_window

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / ".tools"
JAVA = TOOLS / "jre25" / "bin" / "java.exe"
JAR = TOOLS / "server-26.3.jar"
STATE = ROOT / ".mcdev"
SERVERS = STATE / "servers"
REG = STATE / "registry.json"
FEEDBACK = STATE / "feedback.log"
INBOX = STATE / "inbox.json"
WORKTREES = ROOT / ".worktrees"
HOST = "localhost"
HTTP_PORT = 8800
OPS = [{"uuid": "e5e9dc0e-ef3c-41ca-b943-08ddfb204f02", "name": "NoniosTheMad", "level": 4, "bypassesPlayerLimit": True}]
USER = OPS[0]["name"]
DATA_FORMAT, RES_FORMAT = 121, 97

PRESETS = {
    "hub":  dict(port=25565, mem="1G", desc="Lobby. Press G to travel.", persistent=True, world="void"),
    "main": dict(port=25566, mem="3G", desc="The map itself - build here.", persistent=True, world="flat"),
    "test": dict(port=25567, mem="3G", desc="Copy of main + everything merged.", persistent=True, world="copy-main"),
}
EPHEMERAL_PORTS = range(25570, 25600)
# Idle sleep: the daemon stops a server (not hub) that has had nobody online for IDLE_SLEEP_SECS -> status "sleeping";
# G > Servers wakes it. Test-only overrides (read once at daemon start): MCDEV_IDLE_SECS, MCDEV_IDLE_ONLY=name,name.
IDLE_SLEEP_SECS = int(os.environ.get("MCDEV_IDLE_SECS") or 600)
IDLE_ONLY = {x for x in os.environ.get("MCDEV_IDLE_ONLY", "").split(",") if x}
IDLE_CHECK_SECS = 15
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

def port_busy(port):
    """Someone listens on / still holds the port (a bind test catches a dying server that no longer accepts)."""
    if port_open(port):
        return True
    with socket.socket() as s:
        try:
            s.bind(("0.0.0.0", port))
            return False
        except OSError:
            return True

def wait_ports_free(name, port, timeout=30):
    """A stopped server can hold its ports for a few seconds after its process exits; starting earlier fails with 'port in use'."""
    t0 = time.time()
    while port_busy(port) or port_busy(port + 10000):
        if time.time() - t0 > timeout:
            sys.exit(f"{name}: port {port} or {port + 10000} still in use after {timeout}s")
        time.sleep(0.5)

def free_port(reg, name=None):
    """First ephemeral port not reserved by another (non-archived) server and not in use."""
    used = {s["port"] for n, s in reg.items() if n != name and s.get("status") != "archived"}
    return next(p for p in EPHEMERAL_PORTS if p not in used and not port_busy(p) and not port_busy(p + 10000))


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

def log4j_config():
    """Vanilla's log4j2.xml (from the com/mojang/logging library in the server jar) + one extra logger: the DEBUG line
    'Received custom click action <id> with payload <snbt>' (dialog dynamic/custom buttons) goes to latest.log; nothing else changes."""
    out = STATE / "log4j2.xml"
    z = zipfile.ZipFile(JAR)
    lib = next(n for n in z.namelist() if re.search(r"com/mojang/logging/[^/]+/logging-[^/]+\.jar$", n))
    xml = zipfile.ZipFile(io.BytesIO(z.read(lib))).read("log4j2.xml").decode()
    extra = ('        <Logger name="net.minecraft.server.MinecraftServer" level="debug">\n'
             '            <Filters>\n'
             '                <RegexFilter regex="(?s)Received custom click action .*" onMatch="ACCEPT" onMismatch="NEUTRAL" />\n'
             '                <ThresholdFilter level="info" onMatch="ACCEPT" onMismatch="DENY" />\n'
             '            </Filters>\n'
             '        </Logger>\n')
    assert "<Root" in xml
    STATE.mkdir(exist_ok=True)
    out.write_text(xml.replace("        <Root", extra + "        <Root", 1))
    return out

def launch(name, s):
    d = SERVERS / name
    log = open(d / "console.log", "ab")
    flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
    p = subprocess.Popen([str(JAVA), f"-Xmx{s['mem']}", f"-Xms{s['mem']}" if name in ("main", "test") else "-Xms256M",
                          "-XX:+UseZGC", f"-Dlog4j2.configurationFile={log4j_config().as_uri()}", "-jar", str(JAR), "--nogui"],
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

TIP_LINES, TIP_COLS = 6, 34  # dialog tooltips wrap narrow and grow upwards: hard cap (feedback #26, #29)

def tip_lines(*parts):
    """Tooltip = at most TIP_LINES short lines (each truncated to TIP_COLS); parts are (text, color) pairs."""
    out = []
    for t, color in parts:
        for ln in str(t).splitlines() or [""]:
            if ln.strip() and len(out) < TIP_LINES:
                out.append(text(("\n" if out else "") + trunc(ln, TIP_COLS), color))
    return out or [text("-", "gray")]

def nav_dialog(reg):
    live = [(n, s) for n, s in sorted(reg.items(), key=lambda kv: (not kv[1].get("review"), kv[1]["port"]))
            if s.get("status") in ("up", "sleeping")]
    actions = []
    for n, s in live:
        asleep = s["status"] == "sleeping"
        # same shape for every row: [★] name + state; the description lives in the tooltip (long labels overflow the button)
        label = ([text("★ ", "yellow")] if s.get("review") else []) + (
            [text(n, "dark_gray", bold=True), text("  (asleep, ~10s)", "dark_gray", italic=True)] if asleep else
            [text(n, "gold" if s["persistent"] else "aqua", bold=True), text("  (running)", "green", italic=True)])
        heads = todo_heads(s.get("todo") or "")
        tip = tip_lines((s["desc"] or n, "white"), (s["branch"] + (f" / {s['demo']}" if s.get("demo") else ""), "dark_gray"),
                        ("Click: start it, you're sent there" if asleep else "", "gray"),
                        ("\n".join(heads[:6]), "gray"))
        actions.append({"label": label, "tooltip": tip, "width": 310,
                        "action": {"type": "minecraft:run_command", "command": f"trigger devnav.{'wake' if asleep else 'go'} set {s['port']}"}})
    n_up = sum(s["status"] == "up" for _, s in live)
    summary = f"{n_up} running" + (f", {len(live) - n_up} asleep" if len(live) > n_up else "")
    n_arch = sum(s.get("status") == "archived" for s in reg.values())
    arch = {"label": text(f"Archive ({n_arch})", "gray" if n_arch else "dark_gray"), "width": 150,
            "tooltip": text("Old tests, stopped. Click one there to revive it." if n_arch else "Nothing archived")}
    if n_arch:  # no action = greyed-out button in the same place (Dialog UI rules)
        arch["action"] = {"type": "minecraft:run_command", "command": "trigger devnav.act set 10"}
    return {"type": "minecraft:multi_action", "title": text("Dev servers", "gold"),
            "body": [{"type": "minecraft:plain_message", "contents": text(f"{summary}. ★ = to review.", "gray"), "width": 300}],
            "actions": actions + [arch, {"label": "Back", "width": 150, "action": {"type": "minecraft:run_command", "command": "trigger devnav.act set 7"}}],
            "columns": 1, "pause": False}

def todo_heads(todo):
    """Step headlines from try.txt ("2. Generator: ..." -> "2. Generator") for the Servers tooltip."""
    heads = []
    for ln in todo.splitlines():
        m = re.match(r"\s*(\d+)[.)]\s*(.+)", ln)
        if m:
            h = m.group(2)
            c = h.find(":")
            head = 0 < c <= 28 and not any(ch in h[:c] for ch in '">')  # "Lobby: ..." yes, 'G > Demo: ...' no
            heads.append(f"{m.group(1)}. " + (h[:c] if head else h))
    return heads

def archived(reg):
    """Archived servers, most recently archived first."""
    return sorted(((n, s) for n, s in reg.items() if s.get("status") == "archived"), key=lambda kv: kv[1]["archive"]["date"], reverse=True)

def archive_dialog(reg):
    actions = []
    for n, s in archived(reg):
        ar = s["archive"]
        tip = tip_lines((s["desc"] or n, "white"), (f"Note: {ar['note']}" if ar.get("note") else "", "gray"),
                        (f"{s['branch']} @ {(ar.get('commit') or '?')[:7]}", "dark_gray"), (f"Archived {ar['date']}", "dark_gray"),
                        ("Click: revive it, you're sent there", "gray"))
        actions.append({"label": [text(n, "gray", bold=True), text(f"  {ar['date'][5:10]}", "dark_gray"),
                                  text(f"  {trunc(ar.get('note') or s['desc'] or s['branch'], 40)}", "dark_gray", italic=bool(ar.get("note")))],
                        "tooltip": tip, "width": 310,
                        "action": {"type": "minecraft:run_command", "command": f"trigger devnav.revive set {ar['aid']}"}})
    return {"type": "minecraft:multi_action", "title": text("Archive", "gray"),
            "body": [{"type": "minecraft:plain_message", "contents": text(f"{len(actions)} archived. Click one to revive it.", "gray"), "width": 300}],
            "actions": actions + [{"label": "Back", "width": 150, "action": {"type": "minecraft:run_command", "command": "trigger devnav.act set 1"}}],
            "columns": 1, "pause": False}

def dialog_commands(key, dialog, limit=1300):
    """RCON commands that build a dialog compound in storage devnav:ui <key> (built in a temp key, then swapped in).
    One command per action: RCON request packets are capped (~1.4 KB)."""
    head = dict(dialog, actions=[])
    tmp = f"t_{key}"
    cmds = [f"data modify storage devnav:ui {tmp} set value {snbt(head)}"]
    for a in dialog.get("actions", []):
        c = f"data modify storage devnav:ui {tmp}.actions append value {snbt(a)}"
        if len(c.encode()) > limit:  # drop the tooltip rather than the button
            c = f"data modify storage devnav:ui {tmp}.actions append value {snbt({k: v for k, v in a.items() if k != 'tooltip'})}"
        cmds.append(c)
    return cmds + [f"data modify storage devnav:ui {key} set from storage devnav:ui {tmp}", f"data remove storage devnav:ui {tmp}"]

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

def write_devnav(reg=None):
    """Shared devnav pack (junctioned into every server). Static: per-registry content lives in storage (daemon)."""
    d = STATE / "devnav"
    fn = d / "data" / "devnav" / "function"
    fn.mkdir(parents=True, exist_ok=True)
    (d / "pack.mcmeta").write_text(json.dumps({"pack": {"description": "mcdev navigation", "min_format": DATA_FORMAT, "max_format": DATA_FORMAT}}))
    # G > Servers and its Archive page are built by the daemon in storage devnav:ui (nav, arch) over RCON whenever the
    # registry changes, and shown inline by a macro: no /reload of every server when one sleeps/wakes (a reload re-runs
    # the game's load functions on the server the user is playing on).
    for f, key, what in (("list", "nav", "Server list"), ("archive", "arch", "Archive")):
        (fn / f"{f}.mcfunction").write_text(
            f'execute unless data storage devnav:ui {key} run tellraw @s {{"text":"[dev] {what} not ready yet (daemon down?)","color":"gray"}}\n'
            f"execute if data storage devnav:ui {key} run function devnav:show_{key} with storage devnav:ui\n")
        (fn / f"show_{key}.mcfunction").write_text(f"$dialog show @s $({key})\n")
    # Feedback = a tagged Book & Quill. Signing it queues the book content in storage and pings the
    # daemon, which pulls the pages over RCON (no quoting/length/newline limits, unlike dialog text + say).
    (fn / "fb_give.mcfunction").write_text(
        "clear @s minecraft:writable_book[minecraft:custom_data~{devnav_fb:1b}]\n"
        'give @s minecraft:writable_book[minecraft:custom_data={devnav_fb:1b},'
        'minecraft:item_name={"text":"Feedback for Claude","color":"green"},'
        'minecraft:lore=[{"text":"Write, then Sign. The title is the topic.","color":"gray","italic":false}]]\n'
        'tellraw @s {"text":"[dev] Feedback book: write, then Sign (title = topic).","color":"green"}\n')
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
        "scoreboard objectives add devnav.go trigger\nscoreboard objectives add devnav.act trigger\n"
        "scoreboard objectives add devnav.wake trigger\nscoreboard objectives add devnav.revive trigger\n")
    (fn / "nav_tick.mcfunction").write_text(
        "scoreboard players enable @a devnav.go\nscoreboard players enable @a devnav.act\nscoreboard players enable @a devnav.wake\n"
        "scoreboard players enable @a devnav.revive\n"
        "execute as @a[scores={devnav.go=1..}] run function devnav:go\n"
        "execute as @a[scores={devnav.wake=1..}] run function devnav:wake\n"
        "execute as @a[scores={devnav.revive=1..}] run function devnav:revive\n"
        "execute as @a[scores={devnav.act=10}] run function devnav:archive\n"
        "execute as @a[scores={devnav.act=1}] run function devnav:list\n"
        "execute as @a[scores={devnav.act=2}] run function devnav:refresh\n"
        "execute if entity @a[scores={devnav.act=3}] run reload\n"
        "execute as @a[scores={devnav.act=4}] run function devnav:fb_give\n"
        "execute as @a[scores={devnav.act=9}] run function devnav:fb_give\n"
        "execute as @a[scores={devnav.act=11}] run function devnav:demo_menu\n"
        "execute as @a[scores={devnav.act=5}] run function devnav:reset_world\n"
        "execute as @a[scores={devnav.act=6}] run function devnav:inbox\n"
        "execute as @a[scores={devnav.act=7}] run dialog show @s devnav:menu\n"
        "execute as @a[scores={devnav.act=8}] run function devnav:todo\n"
        "scoreboard players reset @a[scores={devnav.act=1..}] devnav.act\n")
    # Inbox: the daemon keeps the whole dialog (a compound) in storage devnav:ui d; a macro shows it inline.
    (fn / "inbox.mcfunction").write_text(
        'execute unless data storage devnav:ui d run tellraw @s {"text":"[dev] Inbox not ready yet (daemon down?)","color":"gray"}\n'
        "execute if data storage devnav:ui d run function devnav:inbox_show with storage devnav:ui\n")
    (fn / "inbox_show.mcfunction").write_text("$dialog show @s $(d)\n")
    (fn / "go.mcfunction").write_text(
        "execute store result storage devnav:tmp port int 1 run scoreboard players get @s devnav.go\n"
        "scoreboard players reset @s devnav.go\nfunction devnav:go_port with storage devnav:tmp\n")
    (fn / "go_port.mcfunction").write_text(f"$transfer {HOST} $(port) @s\n")
    # Sleeping/archived server: queue {verb:"wake",uuid,port} / {verb:"revive",uuid,id}; the daemon starts it (actionbar
    # countdown wherever you are) and transfers you the moment it accepts connections.
    for verb, obj, key in (("wake", "devnav.wake", "port"), ("revive", "devnav.revive", "id")):
        (fn / f"{verb}.mcfunction").write_text(
            f'data modify storage devnav:req q append value {{verb:"{verb}"}}\n'
            "data modify storage devnav:req q[-1].uuid set from entity @s UUID\n"
            f"execute store result storage devnav:req q[-1].{key} int 1 run scoreboard players get @s {obj}\n"
            f"scoreboard players reset @s {obj}\n")
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
    # Spawn (feedback #27): void worlds have nothing outside the map, so the world spawn is a declared point
    # (s["spawn"]: --spawn / demos/<demo>/spawn.txt, default 0 64 0) with a solid block under it, respawn_radius 0
    # (radius 10 scatters first joins/respawns off a small platform), and a joining player with no ground under
    # them (saved position over the void, map rebuilt, ...) is sent there.
    sx, sy, sz, syaw = spawn_of(s)
    (fn / "load.mcfunction").write_text(
        "scoreboard objectives add devnav.left minecraft.custom:minecraft.leave_game\n"
        "scoreboard objectives add devnav.chk dummy\n"
        + ("function devnav:spawn_set\n" if void else ""))
    (fn / "spawn_set.mcfunction").write_text(
        f"execute in minecraft:overworld run setworldspawn {sx} {sy} {sz} {syaw} 0\n"
        "gamerule respawn_radius 0\n"
        # spawn chunk kept loaded, so the floor check below (and to_spawn's) can always see it
        f"execute in minecraft:overworld run forceload add {sx} {sz}\n"
        # solid floor under the spawn (keep: never overwrites a map); not loaded yet at load time -> done again on join
        f"execute in minecraft:overworld if loaded {sx} {sy} {sz} if block {sx} {sy - 1} {sz} #minecraft:air "
        f"run fill {sx - 3} {sy - 1} {sz - 3} {sx + 3} {sy - 1} {sz + 3} minecraft:smooth_stone keep\n")
    (fn / "to_spawn.mcfunction").write_text(
        f"execute in minecraft:overworld run tp @s {sx + 0.5} {sy} {sz + 0.5} {syaw} 0\n"
        f"execute in minecraft:overworld if block {sx} {sy - 1} {sz} #minecraft:air "
        f"run fill {sx - 3} {sy - 1} {sz - 3} {sx + 3} {sy - 1} {sz + 3} minecraft:smooth_stone keep\n"
        "scoreboard players reset @s devnav.chk\n")
    # Ground = any block in the player's column (world_surface = just above the top non-air block). An empty column gives
    # the world's min height, where "~ ~-1 ~" is out of the world and the test errors -> #g stays 0. Below the world -> spawn.
    (fn / "ground_check.mcfunction").write_text(
        "scoreboard players remove @s devnav.chk 1\n"
        "execute if entity @s[gamemode=spectator] run return run scoreboard players reset @s devnav.chk\n"
        "execute if entity @s[y=-2000,dy=1935] run return run function devnav:to_spawn\n"
        "execute at @s unless loaded ~ ~ ~ run return 0\n"
        "scoreboard players set #g devnav.chk 0\n"
        "execute at @s positioned over world_surface unless block ~ ~-1 ~ #minecraft:air run scoreboard players set #g devnav.chk 1\n"
        "execute if score #g devnav.chk matches 0 run function devnav:to_spawn\n")
    (fn / "rules.mcfunction").write_text(  # separate file: a bad gamerule name only breaks this one
        "gamerule advance_time false\ngamerule advance_weather false\ngamerule spawn_mobs false\ntime set noon\n")
    (fn / "tick.mcfunction").write_text(
        "execute as @a[tag=!devnav.seen] run function devnav:welcome\n"
        "execute as @a[scores={devnav.left=1..}] run function devnav:welcome\n"
        + ("execute as @a[scores={devnav.chk=1..}] run function devnav:ground_check\n" if void and name != "hub" else ""))
    # Welcome = title only (feedback #34: instructions don't show by default; they sit in the demo's own dialog).
    welcome = [
        "tag @s add devnav.seen", "scoreboard players reset @s devnav.left",
        "title @s times 5 50 15",
        f"title @s subtitle {json.dumps(text(where, 'gray'))}",
        f"title @s title {json.dumps(text(name, 'gold'))}",
    ]
    if name == "hub":
        welcome += ["tellraw @s " + json.dumps([text("[dev] ", "dark_gray"), text("Press ", "gray"), text("G", "yellow"),
                                                text(" (Quick Actions) or ", "gray"), text("Esc > Nonios Dev", "yellow"), text(" to travel.", "gray")]),
                    "fill -8 63 -8 8 63 8 minecraft:polished_blackstone keep", "tp @s 0.5 64 0.5", "function devnav:rules"]
    elif void:
        # checked for 2 s after joining/transferring (chunks around a far-off saved position may still be loading)
        welcome += ["scoreboard players set @s devnav.chk 40", "function devnav:ground_check"]
    (fn / "welcome.mcfunction").write_text("\n".join(welcome) + "\n")
    tags = d / "data" / "minecraft" / "tags" / "function"
    tags.mkdir(parents=True)
    (tags / "load.json").write_text(json.dumps({"values": ["devnav:load", "devnav:quiet"]}))
    (tags / "tick.json").write_text(json.dumps({"values": ["devnav:tick"]}))
    # Menu clicks are /trigger -> "Triggered [devnav.act] ..." in chat. Hides only players' command success feedback
    # (errors, tellraw and RCON replies still show). Own file: a bad gamerule name only breaks this one.
    (fn / "quiet.mcfunction").write_text("gamerule send_command_feedback false\n")
    (fn / "fb_notify.mcfunction").write_text('data modify storage devnav:req q append value {verb:"feedback"}\ndata modify storage devnav:req q[-1].uuid set from entity @s UUID\n')
    resettable = not s["persistent"] or name == "test"
    (fn / "reset_world.mcfunction").write_text(  # daemon wipes the world, restarts, sends you back
        f'data modify storage devnav:req q append value {{verb:"resetworld"}}\ndata modify storage devnav:req q[-1].uuid set from entity @s UUID\ntransfer {HOST} {hub_port} @s\n' if resettable else
        'tellraw @s {"text":"[dev] Only demo/branch servers (and test) can be reset from here.","color":"red"}\n')
    def act(n):
        return {"type": "minecraft:run_command", "command": f"trigger devnav.act set {n}"}
    todo = s.get("todo")
    demo_dialogs = write_demo_dialogs(s, d, act(8) if todo else None)
    # Dialog UI rules (CLAUDE.md): short body right above the buttons, same buttons in the same places on every server,
    # an unavailable action is a greyed button (no action) whose tooltip says why.
    reset = {"label": text("Reset this server", "red" if resettable else "dark_gray"),
             "tooltip": text("Fresh world: wipes everything built/broken here, restarts, brings you back (~15s)" if resettable
                             else "Not available: hub/main keep their world (only demo/branch servers and test reset)")}
    if resettable:
        reset["action"] = act(5)
    actions = [
        {"label": text("\u2709 Inbox", "gold"), "tooltip": text("Messages from Claude, newest first"), "action": act(6)},
        {"label": text("Servers...", "aqua"), "action": act(1)},
        {"label": text("Feedback", "green"), "tooltip": text("Gives a Book & Quill: write, then Sign. Title = topic. Short notes: just type in chat."), "action": act(4)},
        {"label": "Reload datapacks", "tooltip": text("/reload here (resource packs reload by themselves when they change)"), "action": act(3)},
        reset]
    if todo and not demo_dialogs:  # no demo dialog to hang the instructions on: keep them reachable here (always last)
        actions.append({"label": text("What to try here", "yellow"), "action": act(8)})
    menu = {"type": "minecraft:multi_action", "title": text("Nonios Dev", "gold"), "external_title": text("Nonios Dev"),
            "body": [{"type": "minecraft:plain_message", "width": 300, "contents": [
                text(name, "yellow", bold=True), text(f"  {trunc(where, 40)}", "gray"),
                text(f"\n{trunc(s['desc'], 60)}" if s.get("desc") else "", "white")]}],
            "actions": actions, "columns": 2, "pause": False}
    (d / "data" / "devnav" / "dialog" / "menu.json").write_text(json.dumps(menu, indent=1))
    back = act(11) if demo_dialogs else act(7)
    (fn / "demo_menu.mcfunction").write_text(f"dialog show @s {demo_dialogs[0]}\n" if demo_dialogs else "dialog show @s devnav:menu\n")
    if todo:  # full instructions live in a dialog (button in the demo's own dialog), not in chat
        (d / "data" / "devnav" / "dialog" / "todo.json").write_text(json.dumps({
            "type": "minecraft:notice", "title": text("What to try here", "yellow"), "external_title": text("What to try here"),
            "body": [{"type": "minecraft:plain_message", "width": 310, "contents": text(todo, "white")}],
            "action": {"label": "Back", "action": back}, "pause": False}, indent=1))
    (fn / "todo.mcfunction").write_text("dialog show @s devnav:todo\n" if todo else
                                        'tellraw @s {"text":"[dev] No instructions for this server.","color":"gray"}\n')

TRY_BUTTON = "What to try here"

def write_demo_dialogs(s, d, try_action):
    """The demo's own G dialogs (its quick_actions tag) get a 'What to try here' button next to the controls (feedback #34):
    patched copies with the same id go in the self pack, which loads after the demo pack and so overrides them.
    Returns the demo's quick_actions dialog ids."""
    if not s.get("demo"):
        return []
    pack = Path(s["src"]) / "demos" / s["demo"] / "datapack"
    try:
        ids = json.loads((pack / "data" / "minecraft" / "tags" / "dialog" / "quick_actions.json").read_text())["values"]
    except (OSError, ValueError, KeyError):
        return []
    ids = [i if isinstance(i, str) else i.get("id", "") for i in ids]
    ids = [i for i in ids if ":" in i and not i.startswith("#") and not i.startswith("devnav:")]
    for did in ids if try_action else []:
        ns, path = did.split(":", 1)
        f = pack / "data" / ns / "dialog" / f"{path}.json"
        try:
            dlg = json.loads(f.read_text())
        except (OSError, ValueError):
            continue
        if dlg.get("type") != "minecraft:multi_action":
            continue
        dlg["actions"] = list(dlg.get("actions", [])) + [{"label": text(TRY_BUTTON, "yellow"),
                                                          "tooltip": text("Step-by-step test instructions for this demo"), "action": try_action}]
        out = d / "data" / ns / "dialog" / f"{path}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(dlg, indent=1))
    return ids

def refresh_nav(reg=None):
    """Rewrite the shared devnav pack. G > Servers / Archive are pushed by the daemon (Mailroom.push_ui) on registry
    changes, so nothing is /reloaded here."""
    write_devnav()


# ---------------------------------------------------------------- resource packs + daemon
PACKS = STATE / "packs"

def pack_layers(s):
    src = Path(s["src"])
    return [src / "resourcepack"] + ([src / "demos" / s["demo"] / "resourcepack"] if s.get("demo") else [])

def build_resource_pack(name, s, write=True):
    """Zip the game resource pack (+ demo overlay) deterministically; return its sha1 (write=False: only the sha1)."""
    import hashlib
    layers = pack_layers(s)
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
    if write:
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
    class Srv(ThreadingHTTPServer):
        allow_reuse_address = False  # on Windows SO_REUSEADDR lets a 2nd daemon bind too -> it must fail and exit instead
    PACKS.mkdir(parents=True, exist_ok=True)
    try:
        srv = Srv(("127.0.0.1", HTTP_PORT), H)
    except OSError:
        print(time.strftime("%H:%M:%S"), "another daemon owns the port, exiting", flush=True)
        return
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    write_devnav()  # shared pack files of this code version (servers pick them up on their next start/reload)
    mail, idle, packs = Mailroom(), IdleWatch(), PackWatch()
    me = Path(__file__)
    my_mtime, my_change = me.stat().st_mtime, None
    print(time.strftime("%H:%M:%S"), f"daemon up (idle sleep after {IDLE_SLEEP_SECS}s"
          + (f", only {sorted(IDLE_ONLY)}" if IDLE_ONLY else "") + ")", flush=True)
    while True:
        reg = load_reg()
        try:
            mail.tick(reg)
        except Exception as e:  # never let the daemon die on mail/chat handling
            print(time.strftime("%H:%M:%S"), "mail tick failed:", repr(e), flush=True)
        try:
            idle.tick(reg)
        except Exception as e:
            print(time.strftime("%H:%M:%S"), "idle tick failed:", repr(e), flush=True)
        try:
            packs.tick(reg)
        except Exception as e:
            print(time.strftime("%H:%M:%S"), "pack watch failed:", repr(e), flush=True)
        # Self-restart when mcdev.py changes (quiet for 3 s, compiles, no start/stop in flight): code fixes apply without
        # anyone having to find and kill this process.
        try:
            m = me.stat().st_mtime
        except OSError:
            m = my_mtime
        if m != my_mtime:
            my_change = my_change if my_change and my_change[0] == m else (m, time.time())
            if time.time() - my_change[1] >= 3 and not _busy:
                import py_compile
                try:
                    py_compile.compile(str(me), cfile=str(STATE / "mcdev_check.pyc"), doraise=True)
                except py_compile.PyCompileError as e:
                    print(time.strftime("%H:%M:%S"), "mcdev.py changed but doesn't compile, not restarting:", e.msg.splitlines()[-1], flush=True)
                    my_mtime = m
                else:
                    print(time.strftime("%H:%M:%S"), "mcdev.py changed: restarting the daemon", flush=True)
                    srv.shutdown()
                    srv.server_close()
                    ensure_daemon()
                    os._exit(0)
        for n, s in reg.items():
            if s.get("status") != "up":
                continue
            try:
                r = rcon(s["port"] + 10000, "data get storage devnav:req q", timeout=2)
            except (OSError, RuntimeError):
                continue
            if "contents: [{" not in r:
                continue
            rcon(s["port"] + 10000, "data remove storage devnav:req q")
            for req in re.findall(r"\{[^{}]*\}", r):  # key order in the printed SNBT is not stable
                verb = (re.search(r'verb: "(\w+)"', req) or [None, None])[1]
                ints = (re.search(r"uuid: \[I; ([-\d, ]+)\]", req) or [None, None])[1]
                port = (re.search(r"port: (\d+)", req) or [None, None])[1]
                aid = (re.search(r"\bid: (\d+)", req) or [None, None])[1]
                player = uuid_str(ints) if ints else None
                print(time.strftime("%H:%M:%S"), "request", n, verb, player, port or aid or "", flush=True)
                if verb == "repack":
                    background(n, repack, n, player)
                elif verb == "resetworld":
                    background(n, reset_world, n, player)
                elif verb == "wake" and port:
                    target = next((m for m, x in reg.items() if x["port"] == int(port)), None)
                    if target:
                        background(target, wake, target, player)
                    else:
                        tell(s, player, [text("[dev] No server on that port any more.", "red")])
                elif verb == "revive" and aid:
                    target = next((m for m, x in reg.items() if x.get("status") == "archived" and x["archive"].get("aid") == int(aid)), None)
                    if target:
                        background(target, wake, target, player)
                    else:
                        tell(s, player, [text("[dev] That server is no longer archived.", "red")])
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
                   r"left the game|joined the game|RCON|Loaded [0-9]+ |Server empty for|Disconnecting|UUID of player|\[MCDEV\]|Saving|Saved|"
                   r"Received custom click action")

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
            lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()[-400:]
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
        fid = write_feedback(name, s, player, title, "\n\n".join(pages))
        tell(s, player, [text(f"\u2714 feedback saved (#{fid})", "gray", italic=True)])

def fb_max_id():
    """Highest feedback id in the log; numbers old entries (#N prefix) in place, line count unchanged."""
    if not FEEDBACK.exists():
        return 0
    lines, n, changed = FEEDBACK.read_text().splitlines(True), 0, False
    for i, l in enumerate(lines):
        m = re.match(r"#(\d+) ", l)
        if m:
            n = max(n, int(m.group(1)))
        elif re.match(r"\d{4}-\d\d-\d\d \d\d:\d\d ", l):
            n += 1
            lines[i], changed = f"#{n} {l}", True
    if changed:
        FEEDBACK.write_text("".join(lines))
    return n

_fb_last = [0]
def alloc_fb_id():
    """Next feedback id (daemon-only; chat groups reserve theirs before they are written)."""
    _fb_last[0] = max(_fb_last[0], fb_max_id()) + 1
    return _fb_last[0]

def write_feedback(name, s, player, title, body, fid=None, ctx=None, when=None):
    fid = fid or alloc_fb_id()
    body = body.strip().replace("\n", "\n    ")
    with open(FEEDBACK, "a", encoding="utf-8") as f:
        f.write(f"#{fid} {time.strftime('%Y-%m-%d %H:%M', time.localtime(when))} {name} ({s.get('branch')}) [{player}] {title}:\n    {body}\n"
                + (feedback_context(name, s, player) if ctx is None else ctx))
    print(time.strftime("%H:%M:%S"), f"feedback #{fid} from {player} on {name}: {title}", flush=True)
    return fid

def tell(s, player, comps):
    # `execute as`: a UUID is an entity selector, and player-only arguments (tellraw/title/transfer targets) reject it at parse time
    try:
        rcon(s["port"] + 10000, f"execute as {player} run tellraw @s {json.dumps(comps)}")
    except (OSError, RuntimeError):
        pass

def actionbar(s, player, comps):
    try:
        rcon(s["port"] + 10000, f"execute as {player} run title @s actionbar {json.dumps(comps)}", timeout=2)
    except (OSError, RuntimeError):
        pass


# ---------------------------------------------------------------- inbox + chat feedback
# inbox.json   messages to the user {id,time,text,delivered} (written by `notify`, delivery flags by the daemon)
# thread.json  the conversation (mail + the user's chat feedback lines), replayed dimmed on every join; daemon-only
# chat_pending.json  chat lines not yet grouped into a feedback entry (survives daemon restarts)
THREAD, CHAT_PENDING = STATE / "thread.json", STATE / "chat_pending.json"
THREAD_MAX, REPLAY_N, REPLAY_GAP = 200, 8, 60

def load_json(p, default):
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError):
        return default

def save_json(p, v):
    STATE.mkdir(exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(v, indent=1, ensure_ascii=False))
    os.replace(tmp, p)

def load_inbox():
    return load_json(INBOX, [])

def save_inbox(msgs):
    save_json(INBOX, msgs)

def notify(msg):
    """Queue a message for the user's in-game inbox; the daemon delivers it in chat when they are online."""
    msgs = load_inbox()
    m = {"id": max((x["id"] for x in msgs), default=0) + 1, "time": time.strftime("%Y-%m-%d %H:%M"), "text": msg, "delivered": False}
    save_inbox(msgs + [m])
    ensure_daemon()
    return m

def chunks(t, n=200):  # RCON packets are capped (~1.4 KB), so long text goes in pieces
    return [t[i:i + n] for i in range(0, len(t), n)] or [""]

def short_time(t):
    return t[11:] if t[:10] == time.strftime("%Y-%m-%d") else t[5:]

def mail_lines(m):
    c = chunks(m["text"])
    return [[text("\u2709 ", "gold"), text(short_time(m["time"]) + " ", "dark_gray"), text(c[0], "white")]] + [[text(x, "white")] for x in c[1:]]

def inbox_commands(msgs, limit=20):
    """RCON commands that build the inbox dialog in storage devnav:ui d (built in t, then swapped in)."""
    shown = list(reversed(msgs))[:limit]
    head = {"type": "minecraft:notice", "title": text("\u2709 Inbox", "gold"), "external_title": text("Inbox"),
            "body": [{"type": "minecraft:plain_message", "width": 300, "contents": text(
                f"{len(shown)} of {len(msgs)} messages, newest first." if msgs else "No messages yet.", "gray")}],
            "action": {"label": "Back", "action": {"type": "minecraft:run_command", "command": "trigger devnav.act set 7"}}, "pause": False}
    cmds = [f"data modify storage devnav:ui t set value {snbt(head)}"]
    for m in shown:
        c = chunks(m["text"])
        cmds.append("data modify storage devnav:ui t.body append value " + snbt(
            {"type": "minecraft:plain_message", "width": 300,
             "contents": [text(m["time"][5:] + "  ", "dark_gray"), text(c[0], "white")]}))
        cmds += [f"data modify storage devnav:ui t.body[-1].contents append value {snbt(text(x, 'white'))}" for x in c[1:]]
    return cmds + ["data modify storage devnav:ui d set from storage devnav:ui t", "data remove storage devnav:ui t"]

CHAT_RE = re.compile(r"^\[[\d:]+\] \[[^\]]*/INFO\]: (?:\[Not Secure\] )?<([A-Za-z0-9_]{1,16})> (.*)$")
JOIN_RE = re.compile(r"^\[[\d:]+\] \[[^\]]*/INFO\]: (?:System chat: )?([A-Za-z0-9_]{1,16}) (joined|left) the game$")
CHAT_GROUP_SECS = 90

CLICK_RE = re.compile(r"^\[[\d:]+\] \[[^\]]*/\w+\]: Received custom click action (\S+) with payload (.*)$")

# screenshots (F2) in the client instance -> feedback entries; copies kept in .mcdev/screenshots/<N>.png
SHOT_DIR = CLIENT_LOG.parent.parent / "screenshots"
SHOT_COPIES, SHOTS_PENDING = STATE / "screenshots", STATE / "shots_pending.json"
SHOT_POLL_SECS, SHOT_CHAT_SECS = 2, 60
CONNECT_RE = re.compile(r"Connecting to [\w.-]+, (\d+)")

def client_server(reg):
    """Dev server the client is on: the last 'Connecting to localhost, <port>' in the client log if the user is
    online there, else any up server with the user online, else the logged one."""
    up = {n: s for n, s in reg.items() if s.get("status") == "up"}
    port = None
    try:
        with open(CLIENT_LOG, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 500_000))
            hits = CONNECT_RE.findall(f.read().decode("utf-8", "replace"))
        port = int(hits[-1]) if hits else None
    except OSError:
        pass
    logged = next((n for n, s in up.items() if s["port"] == port), None)
    if logged and USER in online(up[logged]):
        return logged
    return next((n for n, s in up.items() if n != logged and USER in online(s)), logged)

def parse_log_line(line):
    """Server log line -> ('chat', player, text) | ('joined'|'left', player) | ('click', id, payload_snbt) | None.
    `say`/system lines are not chat."""
    m = CHAT_RE.match(line)
    if m:
        return ("chat", m.group(1), m.group(2))
    m = CLICK_RE.match(line)
    if m:
        return ("click", m.group(1), m.group(2))
    m = JOIN_RE.match(line)
    return (m.group(2), m.group(1)) if m else None

_SNBT_ESC = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "s": " ", "\\": "\\", '"': '"', "'": "'"}

def snbt_compound(s):
    """Tolerant parse of a flat SNBT compound as printed by the server ({topic:"..",text:'..'}):
    string values unescaped (\\n, \\", \\uXXXX, \\N{name}, ...), other values kept as raw text. Raises ValueError."""
    import unicodedata
    i, n = 0, len(s)
    def ws():
        nonlocal i
        while i < n and s[i] in " \t\r\n":
            i += 1
    def string():
        nonlocal i
        q, buf = s[i], []
        i += 1
        while i < n:
            c = s[i]
            if c == "\\" and i + 1 < n:
                e = s[i + 1]
                if e in _SNBT_ESC:
                    buf.append(_SNBT_ESC[e]); i += 2
                elif e in "xuU":
                    k = {"x": 2, "u": 4, "U": 8}[e]
                    buf.append(chr(int(s[i + 2:i + 2 + k], 16))); i += 2 + k
                elif e == "N" and s[i + 2:i + 3] == "{":
                    j = s.index("}", i)
                    buf.append(unicodedata.lookup(s[i + 3:j])); i = j + 1
                else:
                    buf.append(e); i += 2
            elif c == q:
                i += 1
                return "".join(buf)
            else:
                buf.append(c); i += 1
        raise ValueError("unterminated string")
    def raw():  # unquoted / nested value: up to the next , or } at depth 0
        nonlocal i
        start, depth = i, 0
        while i < n:
            c = s[i]
            if c in "\"'":
                string()
                continue
            if c in "{[":
                depth += 1
            elif c in "}]":
                if depth == 0:
                    break
                depth -= 1
            elif c == "," and depth == 0:
                break
            i += 1
        return s[start:i].strip()
    ws()
    if i >= n or s[i] != "{":
        raise ValueError("not a compound")
    i += 1
    out = {}
    while True:
        ws()
        if i < n and s[i] == "}":
            return out
        if i < n and s[i] in "\"'":
            key = string()
        else:
            m = re.compile(r"[\w.+-]+").match(s, i)
            if not m:
                raise ValueError(f"bad key at {i}")
            key, i = m.group(), m.end()
        ws()
        if i >= n or s[i] != ":":
            raise ValueError(f"expected : at {i}")
        i += 1
        ws()
        out[key] = string() if i < n and s[i] in "\"'" else raw()
        ws()
        if i < n and s[i] == ",":
            i += 1
        elif i < n and s[i] == "}":
            return out
        else:
            raise ValueError(f"expected , or }} at {i}")

class ChatGroups:
    """Consecutive chat lines of one player on one server within CHAT_GROUP_SECS = one feedback entry.
    Persisted to chat_pending.json so a daemon restart doesn't lose half-typed feedback."""
    def __init__(self, path=None):
        self.path, self.g = path, {}
        if path:
            for e in load_json(path, []):
                self.g[(e["server"], e["player"])] = {k: e[k] for k in ("id", "s", "lines", "last")}
    def save(self):
        if self.path:
            save_json(self.path, [dict(server=k[0], player=k[1], **g) for k, g in self.g.items()])
    def max_id(self):
        return max((g["id"] for g in self.g.values()), default=0)
    def add(self, server, s, player, line, now, alloc):
        g = self.g.get((server, player))
        if not g:
            g = self.g[(server, player)] = {"id": alloc(), "s": s, "lines": []}
        g["lines"].append(line)
        g["last"] = now
        self.save()
        return g["id"]
    def due(self, now, force=()):
        """Groups to write now (quiet for CHAT_GROUP_SECS, forced, or stale ones left from a previous daemon run)."""
        out = [(k[0], k[1], g) for k, g in self.g.items() if now - g["last"] >= CHAT_GROUP_SECS or k in force]
        return out
    def done(self, server, player):  # only after the entry is written
        del self.g[(server, player)]
        self.save()

def trunc(t, n=120):
    t = " ".join(t.split())
    return t if len(t) <= n else t[:n - 1] + "\u2026"

def replay_lines(thread, skip_mail=(), n=REPLAY_N):
    """Last n thread entries, dimmed, one line each (the client wipes chat on every reconnect)."""
    rec = [e for e in thread if not (e["kind"] == "mail" and e.get("mail") in skip_mail)][-n:]
    out = [[text("\u2014 recent \u2014", "dark_gray")]] if rec else []
    for e in rec:
        hm = short_time(e["time"])
        if e["kind"] == "mail":
            out.append([text(f"\u2709 {hm} ", "dark_gray"), text(trunc(e["text"]), "gray")])
        else:
            out.append([text(f"{hm} you@{e.get('server')}: ", "dark_gray"), text(trunc(e["text"]), "gray"),
                        text(f" \u2714#{e.get('fid')}", "dark_gray")])
    return out

class Mailroom:
    """Daemon side of inbox + chat feedback: tails server logs, groups chat, delivers mail, keeps the inbox dialog
    current, and keeps the thread (mail + chat feedback) that is replayed on every join."""
    def __init__(self):
        self.tails, self.pushed, self.pushed_ui, self.groups = {}, {}, {}, ChatGroups(CHAT_PENDING)
        _fb_last[0] = max(_fb_last[0], self.groups.max_id())  # ids already promised by "noted (#N)"
        self.next_try, self.last_pending, self.replayed = 0, None, 0
        self.mirrored = {e.get("mail") for e in load_json(THREAD, []) if e["kind"] == "mail"}
        # screenshots: files older than the daemon are ignored; an entry waits SHOT_CHAT_SECS to pick up nearby chat
        self.shot_start, self.shot_next, self.shot_size, self.shot_done = time.time(), 0, {}, set()
        self.shots = load_json(SHOTS_PENDING, [])
        _fb_last[0] = max([_fb_last[0]] + [x["id"] for x in self.shots])
        self.recent_chat = []  # [time, server, fid, text] of the user's recent feedback lines

    def shot_tick(self, reg, now):
        if now >= self.shot_next:
            self.shot_next = now + SHOT_POLL_SECS
            try:
                SHOT_DIR.mkdir(parents=True, exist_ok=True)
                files = sorted(SHOT_DIR.glob("*.png"))
            except OSError:
                files = []
            for p in files:
                if p.name in self.shot_done:
                    continue
                try:
                    st = p.stat()
                except OSError:
                    continue
                t = max(st.st_mtime, st.st_ctime)  # ctime = creation on Windows (a copied file keeps its mtime)
                if t < self.shot_start:
                    self.shot_done.add(p.name)
                elif st.st_size and self.shot_size.get(p.name) == st.st_size:  # same size two polls running = written
                    self.shot_done.add(p.name)
                    try:
                        self.new_shot(reg, p, t)
                    except OSError as e:  # e.g. still locked: retry next poll
                        self.shot_done.discard(p.name)
                        print(time.strftime("%H:%M:%S"), f"screenshot {p.name} failed, retrying: {e!r}", flush=True)
                else:
                    self.shot_size[p.name] = st.st_size
        self.recent_chat = [c for c in self.recent_chat if now - c[0] < 5 * SHOT_CHAT_SECS]
        for sh in [x for x in self.shots if now - x["t"] >= SHOT_CHAT_SECS]:
            chat = [c for c in self.recent_chat if abs(c[0] - sh["t"]) <= SHOT_CHAT_SECS]
            body = f"image: {sh['path']}\n(original: {sh['orig']})"
            if chat:
                body += "\nchat within 60s:\n" + "\n".join(f"  ({c[1]} #{c[2]}) {c[3]}" for c in chat)
            write_feedback(sh["server"], {"branch": sh["branch"]}, USER, "screenshot", body, fid=sh["id"], ctx=sh["ctx"], when=sh["t"])
            self.shots.remove(sh)
            save_json(SHOTS_PENDING, self.shots)

    def new_shot(self, reg, p, t):
        """New PNG in the client's screenshots folder: id + copy + context now (position at shot time), entry later."""
        import shutil
        n = client_server(reg)
        s = reg.get(n) if n else None
        fid = alloc_fb_id()
        SHOT_COPIES.mkdir(parents=True, exist_ok=True)
        copy = SHOT_COPIES / f"{fid}.png"
        shutil.copyfile(p, copy)
        ctx = feedback_context(n, s, USER) if s else "  | (user not on any dev server)\n"
        if s:
            tell(s, USER, [text(f"\U0001F4F7 noted (#{fid})" + (" (test)" if p.name.startswith("mcdev-test") else ""), "gray", italic=True)])
        self.shots.append({"id": fid, "t": t, "server": n or "?", "branch": s.get("branch") if s else None,
                           "path": str(copy), "orig": str(p), "ctx": ctx})
        save_json(SHOTS_PENDING, self.shots)
        self.thread_add([{"kind": "chat", "time": time.strftime("%Y-%m-%d %H:%M"), "server": n or "?", "player": USER,
                          "fid": fid, "text": "\U0001F4F7 screenshot"}])
        print(time.strftime("%H:%M:%S"), f"screenshot #{fid} on {n}: {p.name}", flush=True)

    def thread_add(self, entries):
        if entries:
            save_json(THREAD, (load_json(THREAD, []) + entries)[-THREAD_MAX:])

    def read_new(self, n, s):
        p = SERVERS / n / "logs" / "latest.log"
        try:
            size = p.stat().st_size
        except OSError:
            return []
        t = self.tails.get(n)
        if t is None:  # first sight (daemon start): only new lines count
            self.tails[n] = [size, s.get("started")]
            return []
        if t[1] != s.get("started") or size < t[0]:  # restarted -> fresh log
            t[:] = [0, s.get("started")]
        if size == t[0]:
            return []
        with open(p, "rb") as f:
            f.seek(t[0])
            data = f.read()
        end = data.rfind(b"\n") + 1
        t[0] += end
        return data[:end].decode("utf-8", "replace").splitlines()

    def deliver(self, n, s, pending, replay):
        """Send (dimmed recent thread +) undelivered mail in full colour to the user on server n."""
        lines = replay_lines(load_json(THREAD, []), {m["id"] for m in pending}) if replay else []
        for m in pending:
            lines += mail_lines(m)
        for comps in lines:
            tell(s, USER, comps)
        if pending:
            ids = {m["id"] for m in pending}
            fresh = load_inbox()
            for m in fresh:
                if m["id"] in ids:
                    m["delivered"] = True
            save_inbox(fresh)
            print(time.strftime("%H:%M:%S"), f"delivered {len(ids)} message(s) on {n}", flush=True)

    def dialog_feedback(self, n, s, payload, line):
        """G > Feedback text box (dynamic/custom devnav:feedback) -> feedback entry. The log line has no player name:
        it is whoever is online there (the user, if several)."""
        try:
            p = snbt_compound(payload)
        except (ValueError, IndexError) as e:
            print(time.strftime("%H:%M:%S"), f"feedback dialog: unparsed payload on {n} ({e}): {line}", flush=True)
            return None
        topic, body = (p.get("topic") or "").strip(), (p.get("text") or "").strip()
        players = online(s)
        player = USER if USER in players or not players else players[0]
        if not (topic or body):
            tell(s, player, [text("Nothing to send: the feedback box was empty.", "gray", italic=True)])
            return None
        fid = write_feedback(n, s, player, topic or "(no topic)", body or topic)
        tell(s, player, [text(f"\u2714 noted (#{fid})", "gray", italic=True)])
        return {"kind": "chat", "time": time.strftime("%Y-%m-%d %H:%M"), "server": n, "player": player, "fid": fid,
                "text": f"[{topic}] {body}" if topic else body}

    def push_ui(self, reg, up):
        """G > Servers + Archive dialogs into storage devnav:ui (nav, arch) on every up server: on change and after each start."""
        cmds = dialog_commands("nav", nav_dialog(reg)) + dialog_commands("arch", archive_dialog(reg))
        sig = hash(tuple(cmds))
        for n, s in up.items():
            key = (sig, s.get("started"))
            if self.pushed_ui.get(n) != key:
                try:
                    for c in cmds:
                        r = rcon(s["port"] + 10000, c, timeout=2)
                        if "<--[HERE]" in r:
                            print(time.strftime("%H:%M:%S"), f"ui push on {n} rejected: {r[:200]}", flush=True)
                            break
                    self.pushed_ui[n] = key
                except (OSError, RuntimeError):
                    pass

    def tick(self, reg):
        now = time.time()
        up = {n: s for n, s in reg.items() if s.get("status") == "up"}
        joins, left, said = [], set(), []
        for n, s in up.items():
            for line in self.read_new(n, s):
                ev = parse_log_line(line)
                if not ev:
                    continue
                if ev[0] == "chat":
                    fid = self.groups.add(n, s, ev[1], ev[2], now, alloc_fb_id)
                    tell(s, ev[1], [text(f"\u2714 noted (#{fid})", "gray", italic=True)])
                    said.append({"kind": "chat", "time": time.strftime("%Y-%m-%d %H:%M"), "server": n,
                                 "player": ev[1], "fid": fid, "text": ev[2]})
                elif ev[0] == "click":
                    if ev[1] == "devnav:feedback":
                        e = self.dialog_feedback(n, s, ev[2], line)
                        if e:
                            said.append(e)
                elif ev[0] == "joined":
                    if ev[1] == USER:
                        joins.append(n)
                else:
                    left.add((n, ev[1]))
        self.recent_chat += [[now, e["server"], e["fid"], e["text"]] for e in said if e["player"] == USER]
        self.shot_tick(reg, now)
        for n, player, g in self.groups.due(now, left):
            write_feedback(n, g["s"], player, "chat", "\n".join(g["lines"]), fid=g["id"])
            self.groups.done(n, player)
        msgs = load_inbox()
        new_mail = [m for m in msgs if m["id"] not in self.mirrored]
        self.thread_add([{"kind": "mail", "time": m["time"], "mail": m["id"], "text": m["text"]} for m in new_mail] + said)
        self.mirrored |= {m["id"] for m in new_mail}
        sig = json.dumps([(m["id"], m["time"], m["text"]) for m in msgs[-20:]])
        for n, s in up.items():  # inbox dialog: on change and after every (re)start
            key = (sig, s.get("started"))
            if self.pushed.get(n) != key:
                try:
                    for c in inbox_commands(msgs):
                        rcon(s["port"] + 10000, c, timeout=2)
                    self.pushed[n] = key
                except (OSError, RuntimeError):
                    pass
        self.push_ui(reg, up)
        pending = [m for m in msgs if not m.get("delivered")]
        if joins:  # every join (incl. transfers): replay the thread, then any new mail
            for n in joins:
                replay = now - self.replayed >= REPLAY_GAP  # restart = hub park + return: replay once
                self.replayed = now if replay else self.replayed
                self.deliver(n, up[n], pending, replay=replay)
                pending = []
            return
        ids = [m["id"] for m in pending]
        if pending and (ids != self.last_pending or now >= self.next_try):
            self.last_pending, self.next_try = ids, now + 15
            for n, s in up.items():
                if USER in online(s):
                    self.deliver(n, s, pending, replay=False)
                    break

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
    pristine = SERVERS / name / "world.pristine"  # optional snapshot (e.g. a generated landscape) to reset to
    if pristine.exists():
        shutil.copytree(pristine, SERVERS / name / "world")
    start(name, s, reg)
    send_back(reg, s, player)

def where_is(reg, player, exclude_port=None, prefer=None):
    """The up server (registry entry) the player is on, or None. `prefer` (an entry) is asked first."""
    cands = [x for x in reg.values() if x.get("status") == "up" and x.get("port") != exclude_port]
    if prefer in cands:
        cands.remove(prefer)
        cands.insert(0, prefer)
    for x in cands:
        try:
            if "passed" in rcon(x["port"] + 10000, f"execute if entity {player}", timeout=2):
                return x
        except (OSError, KeyError, RuntimeError):
            pass
    return None

def send_back(reg, s, player, anywhere=False, wait=30):
    """Transfer player to server s once they are on the hub (or, with anywhere, on any other up server); True once they
    have arrived there. Bug #30/#36: `transfer host port <uuid>` is rejected ("only players ...": a UUID selector may match
    any entity), and this returned True without checking -> nobody was ever sent. Now `execute as <uuid> run transfer ... @s`
    and arrival is confirmed on the target."""
    if not player:
        return False
    froms = reg if anywhere else {"hub": reg["hub"]} if "hub" in reg else {}
    t0 = time.time()
    while time.time() - t0 < wait:  # wait until the player has landed somewhere we can send them from
        src = where_is(froms, player, exclude_port=s["port"])
        if src:
            try:
                rcon(src["port"] + 10000, f"execute as {player} run transfer {HOST} {s['port']} @s")
            except (OSError, RuntimeError):
                pass
            for _ in range(30):  # login + resource pack take a few seconds
                time.sleep(0.5)
                try:
                    if "passed" in rcon(s["port"] + 10000, f"execute if entity {player}", timeout=2):
                        return True
                except (OSError, RuntimeError):
                    pass
            return False
        time.sleep(0.5)
    return False

# ---------------------------------------------------------------- idle sleep / wake
_busy = set()  # servers a daemon thread is stopping/starting (repack, reset, wake, sleep): the idle watch leaves them alone

def background(name, fn, *args):
    import threading
    def run():
        _busy.add(name)
        try:
            fn(*args)
        except BaseException as e:  # start() reports failures with sys.exit
            print(time.strftime("%H:%M:%S"), f"{fn.__name__} {name} failed: {e!r}", flush=True)
        finally:
            _busy.discard(name)
    threading.Thread(target=run, daemon=True).start()

def player_count(s):
    """Players online via RCON `list`, or None if the server can't be asked (starting, hung)."""
    try:
        return int(re.search(r"There are (\d+)", rcon(s["port"] + 10000, "list", timeout=2)).group(1))
    except (OSError, RuntimeError, AttributeError):
        return None

class IdleWatch:
    """Stops servers (never the hub) that have had nobody online for IDLE_SLEEP_SECS; they become status "sleeping"."""
    def __init__(self):
        self.seen, self.next_check = {}, 0  # name -> (started, last time someone was online / it came up / daemon start)

    def tick(self, reg):
        now = time.time()
        if now < self.next_check:
            return
        self.next_check = now + IDLE_CHECK_SECS
        for n, s in reg.items():
            # only "up" servers: archived/sleeping/down ones are ignored
            if n == "hub" or s.get("status") != "up" or n in _busy or (IDLE_ONLY and n not in IDLE_ONLY):
                continue
            started, last = self.seen.get(n, (None, 0))
            if started != s.get("started"):
                self.seen[n] = (s.get("started"), now)
                continue
            count = player_count(s)
            if count:
                self.seen[n] = (started, now)
            elif count == 0 and now - last >= IDLE_SLEEP_SECS:
                print(time.strftime("%H:%M:%S"), f"{n} empty for {now - last:.0f}s, putting it to sleep", flush=True)
                self.seen.pop(n)
                background(n, sleep_server, n, s.get("started"))

PACK_CHECK_SECS, PACK_QUIET_SECS, PACK_WARN_SECS = 3, 5, 5

def pack_signature(s):
    """Cheap change detector for a server's resource pack sources (paths, sizes, mtimes)."""
    sig = []
    for layer in pack_layers(s):
        if layer.exists():
            for f in layer.rglob("*"):
                try:
                    st = f.stat()
                    sig.append((str(f), st.st_size, st.st_mtime_ns))
                except OSError:
                    pass
    return hash(tuple(sorted(sig)))

class PackWatch:
    """Resource packs reload by themselves (feedback #33): when an up server's pack sources change (then stay quiet for
    PACK_QUIET_SECS) and the built zip's sha1 differs from the one the server sends, the server restarts with the new
    pack. Players on it get an actionbar warning, are parked on the hub and sent back. The hub only restarts when empty."""
    def __init__(self):
        self.sig, self.next_check = {}, 0  # name -> [started, signature, changed_at]

    def tick(self, reg):
        now = time.time()
        if now < self.next_check:
            return
        self.next_check = now + PACK_CHECK_SECS
        for n, s in reg.items():
            if s.get("status") != "up" or n in _busy:
                continue
            sig = pack_signature(s)
            seen = self.sig.get(n)
            if not seen or seen[0] != s.get("started"):
                self.sig[n] = [s.get("started"), sig, None]  # baseline = what it started with (start rebuilt the zip)
                continue
            if sig != seen[1]:
                seen[1], seen[2] = sig, now
                continue
            if seen[2] and now - seen[2] >= PACK_QUIET_SECS:
                seen[2] = None
                if build_resource_pack(n, s, write=False) == s.get("pack_sha1"):
                    continue
                players = online(s)
                if n == "hub" and players:
                    seen[2] = now  # try again when the hub is empty
                    continue
                print(time.strftime("%H:%M:%S"), f"resource pack of {n} changed, reloading it" + (f" ({', '.join(players)} online)" if players else ""), flush=True)
                background(n, pack_reload, n, players)

def pack_reload(name, players):
    """Restart a server with its rebuilt pack; players on it hop to the hub meanwhile and come back."""
    reg = sync_status(load_reg())
    s, hub = reg.get(name), reg.get("hub")
    if not s or s.get("status") != "up":
        return
    players = online(s)
    if players and (not hub or hub.get("status") != "up"):
        return
    for i in range(PACK_WARN_SECS, 0, -1):
        for p in players:
            actionbar(s, p, [text("Resource pack changed: reloading in ", "gray"), text(f"{i}s", "yellow")])
        time.sleep(1 if players else 0)
    for p in players:
        rcon(s["port"] + 10000, f"execute as {p} run transfer {HOST} {hub['port']} @s")
    stop(name, s)
    start(name, s)
    reg = load_reg()
    for p in players:
        send_back(reg, reg[name], p)

def sleep_server(name, started):
    reg = sync_status(load_reg())
    s = reg.get(name)
    if not s or s.get("status") != "up" or s.get("started") != started:  # restarted/stopped meanwhile
        return
    stop(name, s)
    reg = load_reg()  # stop() can take a while; keep other servers' changes
    if reg.get(name, {}).get("started") == started and reg[name].get("status") != "archived":
        reg[name]["status"] = "sleeping"
        save_reg(reg)
    refresh_nav(sync_status(reg))
    print(time.strftime("%H:%M:%S"), f"{name} asleep", flush=True)

def wake(name, player):
    """G > Servers on a sleeping server: start it with its saved settings, then send the player there from wherever they are."""
    import threading
    reg = sync_status(load_reg())
    s = reg[name]
    if s.get("status") != "up":
        reviving = s.get("status") == "archived"
        print(time.strftime("%H:%M:%S"), f"{'reviving' if reviving else 'waking'} {name}", flush=True)
        ready, sent = threading.Event(), []
        if player:
            est = s.get("boot_secs", 8) + (6 if reviving else 3)
            threading.Thread(target=countdown, args=(player, name, est, ready, "Reviving" if reviving else "Waking"), daemon=True).start()
        def go():  # the moment it accepts connections (before the post-start checks)
            ready.set()
            if player:
                sent.append(send_back(load_reg(), load_reg()[name], player, anywhere=True))
                if not sent[-1]:
                    print(time.strftime("%H:%M:%S"), f"{name} is up but {player} wasn't found to transfer", flush=True)
        try:
            if reviving:
                s = unarchive(name)
            start(name, s, on_ready=go)
            return
        except BaseException as e:
            ready.set()
            reason = str(e) if isinstance(e, SystemExit) else repr(e)
            fresh = load_reg()
            if name in fresh and fresh[name].get("status") == "up" and not pid_alive(fresh[name].get("pid")):
                fresh[name]["status"] = "sleeping"
                save_reg(fresh)
                refresh_nav(sync_status(fresh))
            notify(f"Couldn't wake {name}: {reason}")
            raise
    if player and not send_back(reg, reg[name], player, anywhere=True):
        print(time.strftime("%H:%M:%S"), f"{name} is up but {player} wasn't found to transfer", flush=True)

def countdown(player, name, est, done, verb="Waking"):
    """Actionbar 'Waking <name>… Ns' to the player, wherever they are, until `done` is set (target accepts connections)."""
    t0, here = time.time(), None
    while not done.is_set():
        reg = load_reg()
        here = where_is(reg, player, exclude_port=reg.get(name, {}).get("port"), prefer=here)
        left = round(est - (time.time() - t0))
        if here:
            actionbar(here, player, [text(f"{verb} ", "gray"), text(name, "yellow"),
                                     text(f"… {left}s" if left > 0 else "… almost", "gray")])
        done.wait(1)
    if here:
        actionbar(here, player, [text("→ ", "green"), text(name, "yellow")])

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
    if reg.get(name, {}).get("status") == "archived":
        unarchive(name)
        reg = sync_status(load_reg())
    preset = PRESETS.get(name, {})
    port = preset.get("port") or reg.get(name, {}).get("port") or free_port(reg, name)
    branch = a.branch or reg.get(name, {}).get("branch") or "main"
    src = source_for(branch)
    if a.demo and not (src / "demos" / a.demo / "datapack").exists():
        sys.exit(f"no demos/{a.demo}/datapack in {src}")
    s = dict(port=port, branch=branch, src=str(src), demo=a.demo or reg.get(name, {}).get("demo"),
             mem=a.mem or preset.get("mem") or reg.get(name, {}).get("mem", "1536M"), persistent=preset.get("persistent", False),
             world=preset.get("world", "void"),
             desc=a.desc or preset.get("desc") or reg.get(name, {}).get("desc", ""))
    s["todo"] = a.todo or read_todo(src, s["demo"]) or reg.get(name, {}).get("todo", "")
    sp = getattr(a, "spawn", None)
    sp = parse_spawn(sp) if sp else read_spawn(src, s["demo"]) or reg.get(name, {}).get("spawn")
    if sp:
        s["spawn"] = sp
    s["review"] = reg.get(name, {}).get("review", not s["persistent"])
    if reg.get(name, {}).get("archive"):  # note + id survive revive/re-archive
        s["archive"] = reg[name]["archive"]
    t = start(name, s)
    print(f"{name} up on {HOST}:{port} ({t:.0f}s)  branch={branch}" + (f" demo={s['demo']}" if s['demo'] else ""))
    if name not in reg and not s["persistent"]:  # brand-new demo/branch server (not a restart)
        notify(f"New dev server {name}: {s['desc'] or s['branch']}")

def start(name, s, _reg=None, on_ready=None):
    """Launch and wait for 'Done'. on_ready() runs as soon as the server accepts connections (wake: transfer the player),
    before the post-start checks."""
    ensure_daemon()
    s["pack_sha1"] = build_resource_pack(name, s)
    reg = load_reg()
    reg[name] = s
    write_devnav(reg)
    write_server(name, s)
    harvest_feedback(name)  # then drop the old log so wait_ready can't see a stale "Done ("
    for f in (SERVERS / name / "logs" / "latest.log", SERVERS / name / ".feedback_seen"):
        f.unlink(missing_ok=True)
    wait_ports_free(name, s["port"])
    s.update(pid=launch(name, s), started=time.time(), status="up")
    reg = load_reg()
    reg[name] = s
    save_reg(reg)
    t = wait_ready(name, s)
    boot = round(time.time() - s["started"])
    if on_ready:
        on_ready()
    reg = load_reg()
    if reg.get(name, {}).get("started") == s["started"]:  # boot time -> the next wake countdown's estimate
        s["boot_secs"] = reg[name]["boot_secs"] = boot
        save_reg(reg)
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
    # all packs together: a demo pack may show buttons for a trigger the game pack enables (e.g. a generated shop catalog)
    files = [f for pack in packs for f in list(pack.rglob("*.mcfunction")) + list(pack.rglob("*.json"))]
    text = {f: re.sub(r"(?m)^\s*#.*$", "", f.read_text(errors="replace")) for f in files}  # ignore comments
    for pack in packs:
        used = {o for f, t in text.items() if pack in f.parents
                for o in re.findall(r"(?m)(?:^\s*|run |/|\")trigger ([\w.]+)", t)}
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

def spawn_of(s):
    """(x, y, z, yaw) ints: where players land on this server (block coords; the block below is made solid)."""
    v = [int(float(x)) for x in (s.get("spawn") or [0, 64, 0])]
    return v[:3] + [v[3] if len(v) > 3 else 0]

def parse_spawn(t):
    v = [float(x) for x in str(t).replace(",", " ").split()]
    if len(v) not in (3, 4):
        raise ValueError(f"spawn must be 'x y z [yaw]', got {t!r}")
    return [int(x) for x in v]

def read_spawn(src, demo):
    """demos/<demo>/spawn.txt: 'x y z [yaw]' = where players land (world spawn), default 0 64 0."""
    f = Path(src) / "demos" / str(demo) / "spawn.txt"
    return parse_spawn(f.read_text().strip()) if demo and f.exists() else None

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

def restore_source(s):
    """Checkout for an archived server: its worktree, else re-added from the branch, else from the recorded commit."""
    branch = s["branch"]
    if branch in (None, "main"):
        return ROOT
    wt = WORKTREES / branch.replace("/", "-")
    if wt.exists():
        return wt
    commit = s.get("archive", {}).get("commit")
    if git("rev-parse", "--verify", "--quiet", branch).returncode == 0:
        r = git("worktree", "add", str(wt), branch)
    elif commit:
        r = git("worktree", "add", "-b", branch, str(wt), commit)
    else:
        sys.exit(f"branch {branch} is gone and no commit was recorded")
    if r.returncode:
        sys.exit(r.stderr)
    return wt

def unarchive(name):
    """Archived -> down, with a checkout and a fresh port; the caller starts it. Keeps s["archive"] (note, aid) for next time."""
    reg = sync_status(load_reg())
    s = reg[name]
    s["src"] = str(restore_source(s))
    s["port"] = free_port(reg, name)
    s["status"] = "down"
    save_reg(reg)
    print(time.strftime("%H:%M:%S"), f"unarchived {name} -> :{s['port']} ({s['src']})", flush=True)
    return s

def cmd_archive(a):
    reg = sync_status(load_reg())
    s = reg.get(a.name)
    if not s:
        sys.exit(f"unknown server {a.name}")
    if s["persistent"]:
        sys.exit(f"{a.name} is persistent (hub/main/test), not archivable")
    if s.get("status") != "archived":
        stop(a.name, s)
    src = Path(s["src"])
    head = git("rev-parse", "HEAD", cwd=src) if src.exists() else git("rev-parse", "--verify", "--quiet", s["branch"])
    commit = head.stdout.strip() or s.get("archive", {}).get("commit")
    if commit:  # a ref keeps the commit alive even if the branch is deleted later
        git("update-ref", f"refs/mcdev/archive/{a.name}", commit)
    if src.exists() and src != ROOT and git("status", "--porcelain", "--untracked-files=no", cwd=src).stdout.strip():
        print(f"WARNING: {src} has uncommitted changes; they are lost if the worktree is removed")
    reg = load_reg()  # stop() can take a while
    prev = reg[a.name].get("archive", {})
    aid = prev.get("aid") or 1 + max((x.get("archive", {}).get("aid", 0) for x in reg.values()), default=0)
    reg[a.name] = dict(s, status="archived", review=False, port=0,
                       archive=dict(date=time.strftime("%Y-%m-%d %H:%M"), note=a.note or prev.get("note", ""),
                                    commit=commit, port=s["port"] or prev.get("port"), aid=aid))
    save_reg(reg)
    refresh_nav(sync_status(reg))
    print(f"{a.name} archived ({s['branch']}@{(commit or '?')[:7]}, world kept in {SERVERS / a.name})")

def cmd_unarchive(a):
    reg = load_reg()
    if reg.get(a.name, {}).get("status") != "archived":
        sys.exit(f"{a.name} is not archived")
    a.branch = a.demo = a.desc = a.mem = a.todo = None
    cmd_up(a)

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
    print(f"{'name':<22}{'state':<10}{'addr':<17}{'branch':<22}{'demo':<16}desc")
    for n, s in sorted(reg.items(), key=lambda kv: kv[1]["port"]):
        if s.get("status") != "archived":
            print(f"{n:<22}{s['status'] + ('*' if s.get('review') else ''):<10}{HOST + ':' + str(s['port']):<17}{s['branch']:<22}{s.get('demo') or '-':<16}{s['desc']}")
    arch = archived(reg)
    if arch:
        print(f"\narchived ({len(arch)}): `mcdev unarchive <name>` or G > Servers > Archive revives one")
        for n, s in arch:
            ar = s["archive"]
            print(f"{n:<22}{ar['date']:<18}{s['branch'] + '@' + (ar.get('commit') or '?')[:7]:<35}{s.get('demo') or '-':<17}{ar.get('note') or s['desc']}")
    print(f"pack server: http://{HOST}:{HTTP_PORT}  ({'up' if port_open(HTTP_PORT) else 'down'})"
          f"   * = awaiting review; sleeping = stopped after {IDLE_SLEEP_SECS // 60} min empty, `mcdev up <name>` or G > Servers wakes it")

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
    """Inbox: prints entries not yet acknowledged; --all for history, --ack marks them read; --resolve N tells the user."""
    if a.resolve is not None:
        fb_max_id()  # make sure old entries carry ids
        lines = FEEDBACK.read_text().splitlines() if FEEDBACK.exists() else []
        m = next((m for l in lines if (m := re.match(rf"#{a.resolve} \S+ \S+ \S+ \(.*?\) \[.*?\] (.*?):?$", l))), None)
        if not m:
            sys.exit(f"no feedback #{a.resolve}")
        note = " ".join(a.note)
        msg = notify(f"Feedback #{a.resolve} [{m.group(1)}] resolved" + (f": {note}" if note else ""))
        print("inbox:", msg["text"])
        return
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
    u.add_argument("--spawn", help="'x y z [yaw]' where players land (else demos/<demo>/spawn.txt, else kept, else 0 64 0)")
    u.set_defaults(f=cmd_up)
    rv = sp.add_parser("review", help="star a server as awaiting review, or --done")
    rv.add_argument("name"); rv.add_argument("--done", action="store_true"); rv.set_defaults(f=cmd_review)
    d = sp.add_parser("down"); d.add_argument("name"); d.add_argument("--purge", action="store_true"); d.set_defaults(f=cmd_down)
    for nm, f in (("restart", cmd_restart), ("reset", cmd_reset)):
        x = sp.add_parser(nm); x.add_argument("name"); x.set_defaults(f=f)
    sp.add_parser("ls").set_defaults(f=cmd_ls)
    ar = sp.add_parser("archive", help="stop a server and keep it in the archive (port freed)")
    ar.add_argument("name"); ar.add_argument("--note", default=""); ar.set_defaults(f=cmd_archive)
    ua = sp.add_parser("unarchive", help="revive an archived server (= up <name>)"); ua.add_argument("name"); ua.set_defaults(f=cmd_unarchive)
    r = sp.add_parser("reload"); r.add_argument("name", nargs="?"); r.set_defaults(f=cmd_reload)
    c = sp.add_parser("cmd"); c.add_argument("name"); c.add_argument("command", nargs="+"); c.set_defaults(f=cmd_cmd)
    l = sp.add_parser("logs"); l.add_argument("name"); l.add_argument("-n", type=int, default=40); l.set_defaults(f=cmd_logs)
    fb = sp.add_parser("feedback"); fb.add_argument("--all", action="store_true"); fb.add_argument("--ack", action="store_true")
    fb.add_argument("--resolve", type=int, metavar="N"); fb.add_argument("note", nargs="*"); fb.set_defaults(f=cmd_feedback)
    nt = sp.add_parser("notify", help="message the user's in-game inbox"); nt.add_argument("text", nargs="+")
    nt.set_defaults(f=lambda a: print("inbox #%d queued" % notify(" ".join(a.text))["id"]))
    sp.add_parser("nav").set_defaults(f=lambda a: refresh_nav(sync_status(load_reg())))
    sp.add_parser("_daemon").set_defaults(f=lambda a: daemon())
    a = p.parse_args()
    for st in (sys.stdout, sys.stderr):  # cp1252 consoles: don't crash on RCON replies with symbols
        st.reconfigure(errors="backslashreplace")
    a.f(a)

if __name__ == "__main__":
    main()
