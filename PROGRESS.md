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

## Framework (in flight)
- [ ] Chat replay on rejoin (inbox agent, to be added to storage devnav:fb replay)
