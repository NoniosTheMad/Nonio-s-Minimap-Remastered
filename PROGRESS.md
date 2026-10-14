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

## M4 early: Generators (`feat/generators`, server `gens` :25576)
- [x] Game code `nonios:generator/*`: marker + spinning item_display + hologram + interaction; 1 s schedule loop, no tick cost.
- [x] V2 odds recovered (1-of-81 dispenser rolls, per level/team) -> `src/generators.json` -> `tools/build_generators.py` (loot tables, roll functions, config).
- [x] V2 structures imported (`structure/generator/<team>_lvlN.nbt`, 1.12 data upgraded by DataFixer on `/place template`: verified).
- [x] Coins: emerald outcomes fill a per-generator pot (cap 50/150/500); right-click collects into `nx.coins` and pulls drops to you.
- [x] Scaling: rolls per drop = 1 + (team players - 1)/4; item cap 16 stacks per generator.
- [ ] Client test: right-click collect, buy upgrade, spin smoothness, hologram look. Coin values / intervals need the user's call.

## M4 integration (`feat/m4-integration`, server `m4` :25570, demo `m4-match`)
- [x] Merged feat/generators, feat/emerald-dream, feat/arena on top of main (economy included); one `nonios:load` / `nonios:tick`.
- [x] `map/config`: per field `gen` + `dream` pad; `arena_cfg` (3 nodes, rabbit bounds). Built by `map/build`; nodes via `#nonios:arena/config` hook.
- [x] Lifecycle: start = wake dreamers + `game/reset_world`; arena runs only in battle; generators only in prep/battle; to_lobby rebuilds all.
- [x] `portal/`: team unlock 1000 coins (config `dream_cost`) at the pad dialog; way back void after match/team change -> team spawn.
- [x] Generator upgrade dialog at the generator (sneak-click / click with empty pot), 200 / 500 from the purse.
- [x] RCON-verified: build, lifecycle resets, arena gate, portal gate + unlock, dream dimension not hit by prep walls selector.
- [ ] Client test (dialogs, pad step, Dream round trip, captures with the captor dummy). Design questions in the integration report.

## Classes (feat/classes, server `classes` :25580, demo `classes`)
- [x] Framework: `src/classes.json` -> `tools/build_classes.py` (loot tables, enchantments, use advancements, `class/gen/**`).
  API `class/set {num}` / `set_id {id}` / `remove`; hooks `class/on_death` + `class/on_respawn` (for M2 game/death, `#nonios:kit/respawn`).
  Shop tier: binding armour + vanishing, kit re-completed every second, lost on death. Basic tier: re-applied on respawn at team level `#white/#black/#solo nx.cls_lvl`.
- [x] Reaper (lifesteal, souls + 4 s invisibility on kill, souls burst, `nonios:reaper` vision), Cracy Frog (frog legs, broom flight, tongue chaos + RIBBIT,
  rainbow+acid vision, V2 3-step confirmation chain), Warrior placeholder basic class. Server-verified over RCON; client feel untested.
- 26.3 facts: loot tables use `modifier` / `type` / single `condition`; `use_cooldown` only applies when a consumable finishes (item used up -> re-given next tick);
  `use_effects {can_sprint, speed_multiplier}` removes the slow-down while using; movement predicate speeds are blocks/second.

## M5 classes in the match (`feat/m5-classes`, server `m5`, demo `m5-classes`)
- [x] Merged feat/classes on main (one `nonios:load` / `nonios:tick`). `game/death` -> `class/on_death` (every death); `#nonios:kit/respawn` += `class/on_respawn`.
- [x] `nx.tier` owned by classes (`kill_tier` in src/classes.json, basic = team level - 1), read by `economy/kill_bonus/tier` at death time.
- [x] Shop sells classes: `shop/catalog` appends generated `class/gen/shop_items`; `shop/buy_class` (refuse same class, purse, `class/set_id`);
  Cracy Frog = `confirm` -> its 3-question chain (`class/gen/confirm`); bare `trigger nx.cls_ask set 1` only next to your shopkeeper.
- [x] Match reset: `class/reset` in `game/enter` (new match) + `game/lobby_player`; team class levels -> 1 on start.
- [x] Coin minting closed: debt `nx.pdebt` for coin blocks placed while broke; emerald items -> coins on pickup (adv `purse/emerald`, 5/45);
  emerald ores/blocks drop nothing (`data/minecraft/loot_table/blocks`).
- [x] RCON-verified on test husks: shop dialog entries, broke/buy/already/frog-confirm paths, tier 2 -> +90 bonus, death strips + basic back on respawn,
  reset, debt maths, loot overrides. Not verified in the client: dialogs, frog chain, emerald pickup advancement, Reaper souls on match dummies.

## V2 shop classes (`feat/classes-v2`, server `classes2`, demo `classes2`)
- [x] Archer 50, Miner 80, Tank 100, Ninja 100, Berserker 120, Monster 1800, Balrog 10000 in `src/classes.json` (sold by the shop; Warrior untouched).
- [x] Framework: item slot `supply` (plain kit items given once), hook `second` (`class/gen/second`), "a/an" in the apply message,
  `class/fill_hp` (heal to the new max after +HP heads), objectives `nx.cls_quiv`, `nx.cls_ttl`; Balrog trail markers ticked from `class/tick`.
- [x] RCON-verified: clean load (no function/loot/enchantment errors), class loot tables + components, shop catalog lists all 9, Balrog trail curse (Wither II).
  Not verified in the client: everything player-side (apply, flasks, Ninja unarmour, Berserker rage, Monster devour, Balrog climb, Archer mark/quiver).
- Design defaults to confirm: TRACKER "V2 shop classes".

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
