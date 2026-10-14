# Nonios's Map — Remaster (working instructions)

Read this first, then `PROGRESS.md` (live state / next steps) and `DESIGN.md` (game design + tech plan).

## Hard rules
- **Never modify `../V1.0` or `../V2.0 - Just substitute thee world`** (original maps, read-only reference).
- Target: **Minecraft Java 26.3, vanilla** (server + client). Data pack format **121**, resource pack format **97**
  (`pack.mcmeta`: `{"pack":{"description":..,"min_format":N,"max_format":N}}`). Java 25 (portable JRE in `.tools/jre25`).
  Don't move to 26.4 (Vulkan default, shader pipeline churn) without the user's say-so.
- No mods, no command blocks. Datapack functions + resource pack + `/posteffect` shaders. Namespace `nonios:`, scoreboard prefix `nx.`.
- Keep the original objective: two teams, own build fields, contested arena, destroy enemy Nexus (obsidian) to win.
- User = Nonios (MC name **NoniosTheMad**, uuid e5e9dc0e-ef3c-41ca-b943-08ddfb204f02), Spanish speaker, prefers concise replies.
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
- Datapacks are **junctions** into the checkout → edit + `mcdev reload <name>`. Dynamic registries (dialogs, enchantments, …) need `restart`.
- Resource packs: zipped deterministically at start into `.mcdev/packs/<name>.zip`, served on :8800 by the daemon with sha1.
  In-game "Refresh resource pack": queues {verb:"repack",uuid} in storage devnav:req → hop to hub → daemon rebuilds, restarts server if sha changed, transfers player back.
- In-game menu: G (Quick Actions) / pause menu → "Nonios Dev": What to try here (dialog, if the server has a todo), Inbox, Servers, Feedback (book),
  refresh pack, reload, Reset this server (ephemeral + test only). Welcome = title + one short chat line (no instruction dump in chat).
  Menu buttons are `trigger devnav.act set N` (1 servers, 2 repack, 3 reload, 4 book, 5 reset, 6 inbox, 7 back to menu, 8 todo).
- **Feedback** (`.mcdev/feedback.log`, entries `#N ...`; read with `mcdev feedback`, `--ack`):
  - Chat: every line the user types on a dev server is feedback. The daemon tails each `logs/latest.log` (`<Name> text`, opt. `[Not Secure]`),
    acks each line with a gray "✔ noted (#N)", groups lines per player+server until 90s quiet (or they leave) into one entry titled "chat".
    The open group is persisted in `.mcdev/chat_pending.json` (survives daemon restarts).
  - Book & Quill (menu → Feedback): signing fires advancement devnav:fb_signed → book copied to storage devnav:fb inbox → request queued in storage devnav:req
    (daemon polls it over persistent RCON) → daemon drains it into the log. Both get context (branch@commit, pos, server log, client chat).
- **Inbox** (user's mailbox): `mcdev notify "text"` (python: `notify(text)`) appends to `.mcdev/inbox.json`; the daemon tellraws undelivered mail
  (gold ✉) to NoniosTheMad on whatever server he is on, or on his next join. `mcdev feedback --resolve N [note]` notifies "Feedback #N [title] resolved: note".
  `mcdev up` of a NEW demo/branch server notifies automatically. G → Inbox shows the last 20: the daemon builds the dialog as a compound in
  storage `devnav:ui d` over RCON (chunked, RCON packets cap ~1.4 KB) on change and after each server start; `devnav:inbox` shows it via `$dialog show @s $(d)`.
  `.mcdev/thread.json` (mail + the user's chat lines, max 200) is replayed dimmed (last 8, one line each) on every join, since the client wipes chat on reconnect.
- Daemon code changes need a daemon restart: kill the python process whose command line has `mcdev.py _daemon`, then `mcdev up/restart/notify` (or `ensure_daemon()`) starts it again.
  `start` runs `check_server`: warns on datapack load errors and trigger objectives never left enabled (enable AFTER `reset @a`).
- Client log (to trace what the user does): `C:\Users\danir\curseforge\minecraft\Instances\Nonios's Map Remastered\logs\latest.log`.
  Client jar (vanilla assets/shaders reference): `C:\Users\danir\curseforge\minecraft\Install\versions\26.3\26.3.jar`.

## 26.3 facts verified so far
- `/dialog show @s {inline SNBT}` parses; `/posteffect add <player> <id>` exists. Vanilla post effects: blur, creeper, entity_outline, invert, spider.
- Gamerules are snake_case (`advance_time`, `spawn_mobs`, …). `/transfer` needs op 3; servers need `accepts-transfers=true`.
- Server needs a resource-pack sha1, else client caches by URL.
- Dialog `run_command` buttons whose command needs op show a "run this command?" confirmation. **Always use `/trigger <obj> set N`**
  in dialogs (permission 0, no prompt) and do the privileged work in a tick function. Never `reset @a obj` after enabling it in the same tick (re-locks it); reset only triggerers, or enable last.
- Empty servers pause (pause-when-empty-seconds=120): `/reload` applies but load functions run only on unpause.
- Harmless server noise on transfer: netty `IoRegistration` NPE and `ServerboundResourcePackPacket ... prepare_spawn` error.
