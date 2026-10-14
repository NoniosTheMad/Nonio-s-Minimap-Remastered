# Progress

## Decisions
- 2026-10-14: Version **26.3 vanilla** confirmed by user (client via CurseForge, 8 GB, Java 25). No mod loader.
- 2026-10-14: Dev framework = `tools/mcdev.py` (see CLAUDE.md). Hub/main/test persistent + ephemeral demo servers, `/transfer` navigation.

## Current phase: M0 — dev framework
- [x] Portable JRE 25 + server 26.3 jar in `.tools/`
- [x] git repo (`main`), .gitignore
- [x] mcdev: up/down/ls/reload/cmd/logs/feedback/restart/reset, daemon (pack HTTP + repack), devnav menu
- [x] hub :25565 and main :25566 running; client servers.dat has "Nonios Dev Hub" (localhost)
- [x] User validation in client (2026-10-14): join, G menu, travel, refresh pack all OK
- [x] Feedback = Book & Quill + context; invisible requests via storage devnav:req; Reset this server; check_server lint on start
- [x] Demo trigger bug (reset @a after enable) fixed in all 3 demos
- [x] First demo `posteffect-probe` running as server `fx` (:25570, branch demo/posteffect-probe)
- [x] Pushed to GitHub (origin/main)
- [ ] main server world: decide fresh flat vs. imported terrain

## Next (after M0)
Resume DESIGN.md §5 milestones: M1 spikes. §6 design questions answered (2026-10-14).

## Known unknowns
- Does `/posteffect` persist across death / relog / transfer?
- Does dialog `run_command` with op-level commands (transfer) show a confirmation screen?

## M1 spikes
- [~] Shaders: `spike/shaders` (server `shaders` :25571) — nonios:reaper (depth+luma edges), nonios:reaper_luma, nonios:acid. Compiles with shaderc; awaiting user test in client. Depth input unproven.
- [ ] Shop dialog buying one item (trigger-based)
- [ ] Coin purse: mined-stat → coins, weight slowdown, purse-to-killer
- [x] Nexus barrier: `feat/nexus-barrier` (4fe02ed). Visuals: forcefield (team-tinted), hit flash/pulse, crack stages, shatter, rate-limited actionbar. Awaiting user test (texture render, size, feel, sounds).

## Classes (feat/classes, server `classes` :25580, demo `classes`)
- [x] Framework: `src/classes.json` -> `tools/build_classes.py` (loot tables, enchantments, use advancements, `class/gen/**`).
  API `class/set {num}` / `set_id {id}` / `remove`; hooks `class/on_death` + `class/on_respawn` (for M2 game/death, `#nonios:kit/respawn`).
  Shop tier: binding armour + vanishing, kit re-completed every second, lost on death. Basic tier: re-applied on respawn at team level `#white/#black/#solo nx.cls_lvl`.
- [x] Reaper (lifesteal, souls + 4 s invisibility on kill, souls burst, `nonios:reaper` vision), Cracy Frog (frog legs, broom flight, tongue chaos + RIBBIT,
  rainbow+acid vision, V2 3-step confirmation chain), Warrior placeholder basic class. Server-verified over RCON; client feel untested.
- 26.3 facts: loot tables use `modifier` / `type` / single `condition`; `use_cooldown` only applies when a consumable finishes (item used up -> re-given next tick);
  `use_effects {can_sprint, speed_multiplier}` removes the slow-down while using; movement predicate speeds are blocks/second.

## Inbox (done, f6fdfb8)
- [x] Chat notifications + G → Inbox
- [x] `mcdev notify` and `feedback --resolve`
- [x] Chat = feedback (grouped)
- [x] Persistent "recent" thread replay on join
- [x] Instructions moved to G → "What to try here"

## Inbox follow-up (in flight)
- [ ] Multiline text-box feedback dialog (via logged dialog custom action)
- [ ] Hide "Triggered [...]" chat noise
- [ ] No double replay on rejoin

## Backlog ideas (user feedback, not commitments)
- Healer-class vision shader (M5): HP visualization (infrared-like), hearts >20 glow (log-scaled)
- RTX-like shaders (M5): advanced ray tracing effects (reference: https://www.youtube.com/watch?v=AdTxrggo8e8)
