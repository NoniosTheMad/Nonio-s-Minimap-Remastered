# Nonios's Map — Remaster (working instructions)

Read this first, then `PROGRESS.md` (live state / next steps) and `DESIGN.md` (game design + tech plan).

## Hard rules
- **Never modify `../V1.0` or `../V2.0 - Just substitute thee world`** (original maps, read-only reference).
- Target: **Minecraft Java 26.3, vanilla** (server + client). Data pack format **121**, resource pack format **97**
  (`pack.mcmeta`: `{"pack":{"description":..,"min_format":N,"max_format":N}}`). Java 25 (portable JRE in `.tools/jre25`).
  Don't move to 26.4 (Vulkan default, shader pipeline churn) without the user's say-so.
- No mods, no command blocks. Datapack functions + resource pack + `/posteffect` shaders. Namespace `nonios:`, scoreboard prefix `nx.`.
- Keep the original objective: two teams, own build fields, contested arena, destroy enemy Nexus (obsidian) to win.
- User = Nonios (MC name **NoniosTheMad**, uuid e5e9dc0e-ef3c-41ca-b943-08ddfb204f02), Spanish speaker, pronouns they/them, prefers concise replies.
  Remote: https://github.com/NoniosTheMad/Nonio-s-Minimap-Remastered
- Context compacts at ~256k tokens: keep `PROGRESS.md` current after every meaningful step.

## Working protocol (agreed with user 2026-10-14)
- **One main channel**: the main session owns design decisions, integration and merges to `main`. Subagents only get
  isolated, well-specified tasks (spikes, demos) in their own worktree/branch; the main session reviews and merges.
- **Feedback is a queue, not an interrupt**: in-game feedback lands in `.mcdev/feedback.log` (daemon, live).
  Read it with `mcdev feedback` at checkpoints (task done / before next task / when asked), act, then `mcdev feedback --ack`.
- **Monitoring is quiet**: only watch new feedback + crashes/function-load errors (`Failed to load function`,
  `Exception in server tick`, OOM). Never stream joins/transfers/http noise. Arm a monitor only while the user is testing.
- Don't react mid-task to routine events; batch them into the next checkpoint. Record outcomes in PROGRESS.md.
- **Keep the user's view readable (user request 2026-10-14):**
  - Roadmap page = the user's single overview: `docs/roadmap.html`, published at https://claude.ai/artifact/4WajBmJQ4aNWKq1LYBnxMM.
    Update it and republish (same file path, or pass that URL from a new session) at every checkpoint. Keep it in sync with PROGRESS.md.
  - Implementation work (features, demos, framework fixes) runs in **background subagents** in their own worktree/branch.
    This session only specs, reviews diffs, merges and talks to the user. No streams of tool calls here.
  - **No live monitors.** Check feedback and crash lines at checkpoints only (`mcdev feedback`, grep the logs).
  - Message the user only at checkpoints, in this format: **Done** / **Waiting on you** (exact in-game steps) / **Next**, plus the roadmap link. A few lines.
  - When the user writes mid-task: answer briefly, then continue.

## Layout
```
DESIGN.md          game/system design, milestones, open questions
PROGRESS.md        current state, decisions log, next steps  <- update often
datapack/          game logic (namespace nonios)
resourcepack/      assets, shaders (assets/<ns>/post_effect, shaders)
demos/<name>/      minimal feature showcases: datapack/ (+ optional resourcepack/ overlay, README.md)
tools/mcdev.py     dev-server manager (mcdev.cmd wrapper)
.tools/            jre25, server-26.3.jar (gitignored)
.mcdev/            servers/<name>/, registry.json, packs/, daemon.log, feedback.log (gitignored)
.worktrees/<b>/    git worktree per branch (gitignored)
```

## Dev framework (mcdev)
- `python tools/mcdev.py up hub|main|test` — persistent: hub :25565 (lobby, void), main :25566 (the map, build here), test :25567 (copy of main's world).
- `mcdev up <name> --branch feat/x --demo <demo> --desc "..."` — ephemeral server on :25570+, worktree `.worktrees/feat-x`; `mcdev down <name>` deletes it.
- `ls`, `reload [name]`, `cmd <name> <cmd>` (RCON, port+10000), `logs <name>`, `feedback`, `restart`, `reset test`.
- Datapacks are **junctions** into the checkout. **Auto reload (#33, `DataWatch`)**: the daemon watches each up server's game + demo
  datapack sources; once they change and stay quiet 5 s it `/reload`s the server (reload errors → daemon.log `WARNING`, players get a gray
  actionbar note). If a registry-only file changed (anything under `data/<ns>/` except function, advancement, loot_table, predicate,
  item_modifier, recipe, structure and tags of function/block/item/entity_type/fluid/game_event: so dialog, worldgen, dimension,
  enchantment, …) or the shared devnav pack changed since the server started (`s["devnav_sig"]`; a /reload then broke the tick tag),
  it restarts instead, like PackWatch. `mcdev reload <name>` still exists for manual use.
- Resource packs: zipped deterministically at start into `.mcdev/packs/<name>.zip`, served on :8800 by the daemon with sha1.
  **Auto reload (#33)**: the daemon (`PackWatch`) watches each up server's pack sources; once they change and stay quiet 5 s and the
  zip's sha1 differs, it restarts that server (players on it: 1 s actionbar warning (`PACK_WARN_SECS`, user request), parked on the hub,
  sent back). The hub only when empty. No reload buttons in the menu.
- Every `mcdev` command (not only `up`) calls `ensure_daemon()`: a killed daemon comes back with the next `mcdev ls`.
- In-game menu: G (Quick Actions) / pause menu → "Nonios Dev" (same 4 buttons, 2x2, in the same places everywhere): Inbox, Servers,
  Feedback (book), Reset this server (ephemeral + test only, greyed elsewhere; restores `.mcdev/servers/<name>/world.pristine`
  if present, else a fresh world). Welcome = title only (hub adds one "press G" line).
  **What to try here** (try.txt) is a button inside the demo's own G dialog (#34): `write_demo_dialogs` copies each dialog in the demo's
  `quick_actions` tag into the self pack (loads after `demo`, so it overrides) with that button appended; its Back returns to the demo dialog.
  Demo authors: nothing to do, just keep the demo dialog a `multi_action` listed in the demo's quick_actions tag.
  G → Servers rows are all `[▸][★] name [✔]`, status = colour only (user request): gold/aqua running, dark gray asleep; no status words.
  ▸ = the server you're on (the list is built per server), ✔ = approved. Tooltip ≤6 lines of ≤34 chars (`tip_lines`): desc, branch/demo, step headlines.
  G → Servers / Archive are built by the daemon in storage `devnav:ui nav|arch` (`dialog_commands`, one RCON command per button) on every
  registry change and after each start, shown by `$dialog show @s $(nav)`. Nothing is /reloaded when a server sleeps/wakes.
- **Spawn (void worlds, #27)**: `s["spawn"]` = `up --spawn "x y z [yaw]"` / `demos/<demo>/spawn.txt` / kept / default 0 64 0. Self pack `devnav:spawn_set` (on load):
  setworldspawn there, `respawn_radius 0`, forceload its chunk, 7x7 smooth stone under it if air (`keep`). On join/transfer `devnav:ground_check` runs for 2 s:
  no block anywhere in the player's column (or below the world) → `devnav:to_spawn`. Spectators skipped.
  Menu buttons are `trigger devnav.act set N` (1 servers, 2 repack (legacy), 3 reload (legacy), 4 and 9 feedback book, 5 reset, 6 inbox, 7 back to menu,
  8 todo, 10 archive, 11 back to the demo dialog, 12 this-server dialog: handled by the self pack's tick; the shared nav_tick only resets 1..11).
- **Feedback** (`.mcdev/feedback.log`, entries `#N ...`; read with `mcdev feedback`, `--ack`):
  - Text box (legacy, no longer in the menu, #33; the daemon still parses it): topic + multiline text; Send = `dynamic/custom` id `devnav:feedback`.
    The server logs it only at DEBUG ("Received custom click action <id> with payload <snbt>"), so servers launch with
    `-Dlog4j2.configurationFile=.mcdev/log4j2.xml` = vanilla's config (from the com/mojang/logging lib) + MinecraftServer at DEBUG with a RegexFilter
    letting only that line through. The daemon tails it, parses the SNBT payload (`snbt_compound`), writes an entry and replies "✔ noted (#N)".
    The line has no player name: attributed to whoever is online there. Unparseable payloads are logged raw to daemon.log.
  - Chat: every line the user types on a dev server is feedback. The daemon tails each `logs/latest.log` (`<Name> text`, opt. `[Not Secure]`),
    acks each line with a gray "✔ noted (#N)", groups lines per player+server until 90s quiet (or they leave) into one entry titled "chat".
    The open group is persisted in `.mcdev/chat_pending.json` (survives daemon restarts).
  - Book & Quill (menu → Feedback (book), the only menu feedback): signing fires advancement devnav:fb_signed → book copied to storage devnav:fb inbox → request queued in storage devnav:req
    (daemon polls it over persistent RCON) → daemon drains it into the log. Both get context (branch@commit, pos, server log, client chat).
  - Screenshots (F2): the daemon polls the client's `screenshots\` every 2s (files older than the daemon are ignored), copies each new PNG to
    `.mcdev/screenshots/<N>.png`, acks "📷 noted (#N)" and after 60s writes entry "screenshot" (image path first, + the user's chat lines within ±60s,
    with their #ids). Server = last "Connecting to localhost, <port>" in the client log, else wherever the user is online. **Open the image and look for bugs.**
- **Inbox** (user's mailbox): `mcdev notify "text"` (python: `notify(text)`) appends to `.mcdev/inbox.json`; the daemon tellraws undelivered mail
  (gold ✉) to NoniosTheMad on whatever server they are on, or on their next join. `mcdev feedback --resolve N [note]` notifies "Feedback #N [title] resolved: note".
  `mcdev up` of a NEW demo/branch server notifies automatically. G → Inbox shows the last 20: the daemon builds the dialog as a compound in
  storage `devnav:ui d` over RCON (chunked, RCON packets cap ~1.4 KB) on change and after each server start; `devnav:inbox` shows it via `$dialog show @s $(d)`.
  `.mcdev/thread.json` (mail + the user's chat lines, max 200) is replayed dimmed (last 8, one line each) on every join, since the client wipes chat on reconnect
  (skipped if a replay went to them <60s ago, e.g. the hub park during `restart`).
- Every dev server sets `gamerule send_command_feedback false` (self pack `devnav:quiet`, on load): no "Triggered [devnav.act] ..." spam from menu clicks.
  Only success feedback of commands a player runs is hidden; errors, tellraw and RCON replies are unaffected.
- **Idle sleep**: the daemon checks `list` over RCON every 15s; a server (never `hub`) empty for `IDLE_SLEEP_SECS` (10 min) is stopped
  and marked `status: "sleeping"` (kept in `ls` and G → Servers, dark gray, ★ kept). Clicking it = `trigger devnav.wake set <port>`
  → {verb:"wake",uuid,port} in devnav:req → daemon starts it with its saved settings; meanwhile an actionbar countdown (`countdown`, estimate =
  the server's last `boot_secs`) shows wherever the player is, and `start(on_ready=...)` transfers them the moment "Done" appears.
  **Player targets from the daemon are UUIDs: always `execute as <uuid> run <cmd> @s`** (`transfer`/`tellraw`/`title` take player-only
  selectors and reject a UUID at parse time; that silently broke every wake transfer until 2026-10-14, #30/#36). `send_back` confirms arrival.
  `mcdev up <name>` also wakes it. Inbox only hears about failed wakes. Test overrides (read at daemon start): env `MCDEV_IDLE_SECS`, `MCDEV_IDLE_ONLY=fx,..`.
- **Archive** (old tests; don't keep every server open): `mcdev archive <name> [--note ".."]` stops it, keeps `.mcdev/servers/<name>` (world),
  records `archive: {date, note, commit, port, aid}`, pins the commit as `refs/mcdev/archive/<name>`, clears ★, sets `status: "archived"`, `port: 0` (freed).
  `mcdev unarchive <name>` / `up <name>` revives it: worktree re-added from the branch (or from the commit if the branch is gone), new free port.
  `ls` lists archived ones at the bottom; idle sleep ignores them. G → Servers → "Archive (N)" (`devnav.act 10`, inline dialog in `devnav:archive`):
  click = `trigger devnav.revive set <aid>` → {verb:"revive",uuid,id} → daemon unarchives + starts + transfers (same path as wake).
- **Approve / Shelve** (user request 2026-10-15; the user's way to close a review). G → Servers → own row (▸) → dialog `devnav:this`
  [✔ Approve] [Shelve] / [Back] → confirmation (optional Note text input, Yes = `dynamic/custom` `devnav:approve|shelve`, logged like the
  feedback text box) → the daemon runs `retire()` in the background:
  - **Approve** = "I like it as is": feedback entry `✔ APPROVED <name> <branch>@<short> (merge)` (body = note, ctx = full commit, warns on
    uncommitted worktree changes), registry `approved: {date, commit, note, fid}`, then archived with `archive.kind = "approved"`.
    **Claude: merge that branch@commit into main** at the next checkpoint, then `mcdev feedback --resolve N`.
  - **Shelve** = review closed, NOT adopted (the user's feedback on it is considered handled; follow-up demos go to NEW servers):
    entry `■ CLOSED <name> <branch>@<short> (not adopted)`, archived with `kind = "shelved"`. Don't merge; don't reuse the server.
  - Players on it are transferred first (hub, else any other up server), and it is only stopped once empty; if they can't be moved
    the entry is still written but the server stays up. Greyed with a tooltip: both on hub/main/test, Approve on branch `main`.
  - CLI parity: `mcdev approve <name> [--note ..]`, `mcdev archive <name> [--note ..]` (= shelve; re-archiving an archived one only
    updates the note). `mcdev feedback` ends with a `server decisions:` line listing APPROVED/CLOSED entries; `ls` marks + / APPROVED / closed.
  - The own-row button needs a self pack written by this code (`s["ui_ver"] >= UI_VER`); on servers started earlier it is greyed
    ("Restart it to approve here") until their next start.
  Archived 2026-10-14: nexus, shop, purse (merged into m2/econ), fx (old posteffect probe). 2026-10-15: m4 (#51).
- `start` waits (≤30s) until the game + RCON ports are free (bind test) before launching: fixes `restart` failing with "port in use".
- The daemon restarts itself when `tools/mcdev.py` changes (quiet 3 s, compiles, no start/stop in flight; logged "mcdev.py changed: restarting").
  Daemons older than that commit need one manual restart: kill the python process whose command line has `mcdev.py _daemon`, then `mcdev up/restart/notify` (or `ensure_daemon()`).
  Running servers keep the old devnav functions/menus until their next start (dialogs are a registry).
  Only one daemon can run: a second one fails to bind :8800 (SO_REUSEADDR disabled) and exits.
  `start` runs `check_server`: warns on datapack load errors and trigger objectives never left enabled (enable AFTER `reset @a`).
- Client log (to trace what the user does): `C:\Users\danir\curseforge\minecraft\Instances\Nonios's Map Remastered\logs\latest.log`.
  Client jar (vanilla assets/shaders reference): `C:\Users\danir\curseforge\minecraft\Install\versions\26.3\26.3.jar`.

## Dialog UI rules (project-wide, user feedback #41/#44, 2026-10-14)
The user plays at a GUI scale below default; dialogs that put text at the very top and buttons at the very bottom are hard to use.
Applies to every dialog: game pack, demos, devnav.
- **Compact**: body text short (1-2 lines) so it sits right above the buttons. Long explanations go in a button's `tooltip`, a separate
  "What to try here"/info dialog, or try.txt; never a paragraph above the controls. Numbers the player needs (balance, cost) go in the body or the button label.
- **Buttons never move**: the same dialog always has the same buttons in the same order and positions, whatever the state.
- **Unavailable = greyed, not gone**: omit the button's `action` (the client renders it inactive), grey label (`dark_gray`), and a `tooltip` that says why
  ("Need 50 coins", "Only during preparation"). Never drop or reorder buttons to hide an action.
- Prefer `columns: 2` and short labels; a Back/Close button in a fixed last position.
- Check at **GUI scale 2** (Options → Video Settings) before handing a dialog to the user.

## Gear slots (hotbar convention, #34)
Every item the game hands out (kits, respawn kit, classes, shop, talisman, demos) goes through **`nonios:gear/give {item,count}`**
(or `nonios:gear/loot {table}` for a one-item loot table), as the player. Gear lands in a fixed hotbar slot:
**weapon 1, bow 2, pickaxe 3, bucket 4, other tool 5**; if that slot is taken, the first free slot outside 1-5 (hotbar 6-9, inventory,
then the other reserved slots); no room = dropped at the feet. Anything else is a plain `/give`.
- Categories = item tags `#nonios:gear/{weapon,bow,pickaxe,bucket,tool}`; `custom_data.nx_gear` ("weapon"/"bow"/.../"none") overrides
  (class items on plain bases: `"gear"` in `src/classes.json`). How: an `item_display` probe (`nx.gear_probe`) holds the item,
  `gear/category` classifies it, `item replace ... from entity <probe> contents` copies it.
- `item` is pasted raw into the commands: pass it `with storage` when it comes from data (components may hold quotes).

## Shop v3 (#32)
`src/shop.json` (+ optional `--extra` json) -> `tools/build_shop.py` -> `shop/catalog` (storage `nonios:shop items[]`, `nodes[]`).
Node 0 = home (categories); a section with `"sub"` becomes a menu node; item lists are split into pages of 16.
Dialog (`shop/open`, built in storage `ui.d`, `$dialog show`): 4 columns x 120 (2 columns would be 12 rows: the grid would reach the
bottom of the screen). Row 1 Prev | Back | Next | Again, row 2 x1 | x8 | x64 | Stack, then 16 slots padded with blanks; Close = exit
action. Off/greyed buttons have no action. Trigger `nx.shop`: 1 home, 2 again, 3 prev, 4 next, 5 up, 6-9 mode, 10 redraw, 11-99 node,
100+i buy items[i]. Per player: `nx.shop_sec` (node), `nx.shop_pg`, `nx.shop_qm` (mode), `nx.shop_last` (item+1), `nx.shop_lastl` (lots).
Modes buy N lots of a bulk item (Stack = one stack's worth); a buy that doesn't fit gives what fits in empty slots and charges for that.

## 26.3 facts verified so far
- A dialog action button without `action` parses and renders inactive (greyed). `transfer`/`tellraw`/`title` reject a UUID target ("Only players may be affected"): use `execute as <uuid> run ... @s`.
- `/dialog show @s {inline SNBT}` parses; `/posteffect add <player> <id>` exists. Vanilla post effects: blur, creeper, entity_outline, invert, spider.
- Gamerules are snake_case (`advance_time`, `spawn_mobs`, …). `/transfer` needs op 3; servers need `accepts-transfers=true`.
- Server needs a resource-pack sha1, else client caches by URL.
- Dialog `run_command` buttons whose command needs op show a "run this command?" confirmation. **Always use `/trigger <obj> set N`**
  in dialogs (permission 0, no prompt) and do the privileged work in a tick function. Never `reset @a obj` after enabling it in the same tick (re-locks it); reset only triggerers, or enable last.
- Empty servers pause (pause-when-empty-seconds=120): `/reload` applies but load functions run only on unpause. After 10 min empty mcdev stops them (idle sleep).
- Harmless server noise on transfer: netty `IoRegistration` NPE and `ServerboundResourcePackPacket ... prepare_spawn` error.
- Advancement/predicate format changed: conditions use `"type": "minecraft:entity_properties"`; entity predicate keys are namespaced (`"minecraft:entity_type"`, `"minecraft:nbt"`, `"minecraft:flags"`) and `entity` takes one object, not a list. The old format stops the server at startup.
- Item icons in text components: `{type:"object",atlas:"minecraft:items",sprite:"minecraft:item/bread"}`.
- Loot tables: a `group` entry offers its children as alternatives (drops one); to drop everything, one pool per item.
- `tp` with relative yaw grows the stored rotation unbounded; use absolute yaw. Empty servers pause → `schedule` loops stop (test by calling the loop function directly).
- 1.12 structure .nbt files load with `/place template` (auto-upgraded by DataFixer).
- Structure templates written at DataVersion 5023 (no upgrade): palette entries are `{id, properties}` (old `Name/Properties` place nothing).
- Dev servers run `generate-structures=false` (the map too): worldgen structures never generate; place them at runtime (`place template`).
- Density function `y_clamped_gradient` is gone: `{type:"minecraft:gradient",axis:"y",from_coordinate,from_value,to_coordinate,to_value}`.
- Interaction entities swallow melee before vanilla's attack-charge maths (charge unreadable) and projectiles fly through them.
  Firework rockets / wind charges / fireballs explode on a block inside their own move: predict a move ahead. Summoned rockets need `LifeTime`.
- `loot spawn <pos> fish <table> <pos> minecraft:air` works (air as the tool). `tick step` does nothing on a paused (empty) server: use `tick sprint N`.
- Shared names across branches: coins = `nx.coins`, teams = `white` / `black`.
- Worldgen: surface rules live in the `worldgen/material_rule` registry; ore veins are a `minecraft:ore_vein` material rule. Sky/fog/particles/music via `attributes` maps (`minecraft:visual/...`) on dimension_type and biome.
- **Loot tables changed format:** `functions`/`function` → `modifier` (object or list, each with `type`); `conditions`/`condition` → one `condition` object with `type`. Old keys are silently ignored (count 1, chances always pass). Check vanilla tables in the server jar.
- `block_display.block_state` = `{id:"minecraft:vault",properties:{...}}` or a plain id string; the old `{Name,Properties}` only WARNs and renders air.
- `use_cooldown` applies only when a consumable finishes (item consumed) → give the item back next tick. `minecraft:use_effects {can_sprint, speed_multiplier}` removes the use slowdown. `minecraft:movement` predicate speeds are blocks/s.
- In-game text stays terse and diegetic (user feedback #15): no instructions/tutorial lines in the game pack; those go in try.txt / demo dialogs.
