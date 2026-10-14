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
  In-game "Refresh resource pack": `say [MCDEV] repack <name>` → hop to hub → daemon rebuilds, restarts server if sha changed, transfers player back.
- In-game menu: G (Quick Actions) / pause menu → "Nonios Dev": server list (`/transfer`), refresh pack, reload, feedback.
  Feedback is `say [FEEDBACK] [server] text` → daemon appends to `.mcdev/feedback.log` → `mcdev feedback [--all] [--ack]`.
- Client log (to trace what the user does): `C:\Users\danir\curseforge\minecraft\Instances\Nonios's Map Remastered\logs\latest.log`.
  Client jar (vanilla assets/shaders reference): `C:\Users\danir\curseforge\minecraft\Install\versions\26.3\26.3.jar`.

## 26.3 facts verified so far
- `/dialog show @s {inline SNBT}` parses; `/posteffect add <player> <id>` exists. Vanilla post effects: blur, creeper, entity_outline, invert, spider.
- Gamerules are snake_case (`advance_time`, `spawn_mobs`, …). `/transfer` needs op 3; servers need `accepts-transfers=true`.
- Server needs a resource-pack sha1, else client caches by URL.
- Dialog `run_command` buttons whose command needs op show a "run this command?" confirmation. **Always use `/trigger <obj> set N`**
  in dialogs (permission 0, no prompt) and do the privileged work in a tick function. (Only the feedback text box still prompts.)
- Empty servers pause (pause-when-empty-seconds=120): `/reload` applies but load functions run only on unpause.
- Harmless server noise on transfer: netty `IoRegistration` NPE and `ServerboundResourcePackPacket ... prepare_spawn` error.
