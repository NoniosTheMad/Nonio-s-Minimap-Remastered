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

## Integration smoke test of main (6db932a, server `full`, demo `full`)
- [x] Clean load (no function/loot/advancement/tag errors), check_server trigger lint clean (demos m5-classes, m4-match, arena2, classes2, full).
- [x] `nonios:load` / `nonios:tick` call each module once (10 loads; 10 ticks + `death`); no objective criteria clashes (126 objectives, 128 referenced, none undefined);
  triggers unique (nx.team, nx.admin, nx.shop, nx.bankt/d/w, nx.genup, nx.portal_t, nx.cls_ask); generated class/generator files match their sources.
- [x] RCON lifecycle with test husks (temporary `integ` pack in the server world, not in git): lobby -> prep -> battle -> end -> lobby, plus skip in every
  phase, stop in battle, a second match, /reload mid-battle. Generators tick only in prep/battle; interest pays only in prep/battle; walls up in prep,
  down in battle; arena loop, gates (`#gon`) and core regrowth only in battle; nexus shields/cores spawned at start and removed in the lobby;
  Dream portals locked again at start. Fixed: the end phase showed the battle clock for its first second (`game/end/begin`).
- Not RCON-testable (need a real player): class apply/strip on death, Dream force-exit, gate teleports, kill rewards on a player kill.
- Test trick: `tick sprint N` runs ticks on an empty, paused server (pause-when-empty), so lifecycle tests don't need a player online.
- `demos/full` = classes2 buttons + arena2 gate/core buttons (46-52): one demo for everything on main.
- V2 gap inventory: `docs/v2-gap-inventory.md` (built / partly / missing, autonomous vs needs user).

## Shop Special page + integration smoke test #2 (main, server `full`)
- [x] Shop page 10 "Special" (V2 page 11, line + prices from the V2 world): Emerald Talisman 200, Tinkiwinki's Touch 200, Nonios's Weakness 500,
  Monster Skull 1800 (= the Monster class, price from src/classes.json, kept off the Classes page), Satan's Blade 2000, Dragon Skull [Disabled] 3200.
  src/shop.json references: `{same: v2}`, `{special: id}` (src/specials.json -> `shop/buy_special`), `{class: id, name, v2}`. "Destroy Magical barriers" not ported (open question).
- [x] Static: load 13 modules / tick 11, each once; 129 objectives, no criteria clash; triggers unique (same 9); no undefined objectives; clean log.
- [x] RCON lifecycle (tick sprint, husks; temp `integ` pack in the `full` world, not in git): altar levels only in prep/battle, enemy clicks ignored,
  silent in lobby/end; altar paid reset at start; guard + talisman counters run only in prep/battle; shop pages build (Special 6 + Back, Classes without
  Monster Skull), talisman/dragon/monster buy paths (broke, ok, already, 3.2M joke). /reload mid-battle fine.
- Fixed: lobby altars showed the last match's kit level (levels now back to 1 in `game/to_lobby`); `nx.shop_sec` carried over between matches (`game/lobby_player`).
- Note: a world built before team-v2 has no altar entities until `map/build` (admin Rebuild / next lobby return). `full` was rebuilt.
- `demos/full`: + shop2 buttons 53-55, team2 buttons 56-64 (team2's 53-61 shifted by 3).

## Economy v3 (`feat/econ-v3`, server `econ3`, demo `economy`; feedback #35 #36 #41)
- [x] Yields (#36): `src/yields.json` -> `tools/build_yields.py` -> `purse/gen/{yields,check}`. Coal 0.1, copper 0.2, iron 0.5, gold 1, redstone 2,
  lapis 4, diamond 3, emerald 5 (nether gold 0.5, emerald block 20: my picks); stone/deepslate/cobble 0 both ways. Hundredths kept in `nx.pfrac`.
  Fortune +40%/level (item predicate on the main hand). Placing a coin block costs its Fortune III value (2.2x) -> no silk/place/fortune profit; debt as before.
- [x] Weight (#35): coins weighed at money scale S = min(max(100 + 10%/min, 100 + team avg earned / 5), 1000%); config `#w_grow #w_iref #w_smax nx.purse`.
- [x] Interest (#41): rate 1.0% + 0.1%/min up to 5.0%, cap 50 + 10/min per payout (storage nonios:config interest_*). No chat: team sidebar
  (Bank / Interest / Last payout (+"max") / Next in). Admin Economy page shows the growth terms.
- [x] Bank dialog: fixed layout (2 sliders, 4 buttons always), greyed = dark_gray label, tooltip, no action. Altar hologram icons: list root was
  "OFFERINGS" (light purple) and sprites inherit + are tinted by the colour -> plain "" root, sprites color white.
- RCON-verified: yields/fortune/placement/debt maths on a husk, interest growth + schedule loop, sidebar storage, bank dialog both states, altar text, clean log.
  Not verified in the client: sidebar look, greyed buttons, mining feel, altar icons.

## Shop v3 + gear slots + bow vs Nexus (`feat/shop-v3`, server `shop3`, demo `shop3`; #32 #34 #37)
- [x] Shop v3 (#32): categories/subcategories/pages from `src/shop.json` (build_shop.py, any size: stress build 452 items / 37 screens);
  fixed 4x6 grid (nav row, quantity row x1/x8/x64/Stack, 16 slots), "Again" repeats the last purchase, unaffordable = grey + "Need Nc more",
  partial buys when the bag is nearly full, body = purse + last result. Reopens where the player left it.
- [x] Gear slots (#34): `gear/give` / `gear/loot` used by kits, respawn, classes (build_classes.py), shop, talisman, demo. CLAUDE.md "Gear slots".
- [x] Bow vs Nexus (#37): arrows from enemy players near the core deal 20% of their damage (speed x damage x Power, x10 scale): full shot 11-12,
  Power V ~29, a diamond sword hit is ~70.
- mcdev lint: trigger check looks at all the server's packs together (a demo catalog uses the game's `nx.shop`).
- RCON-verified (no player online, test armor stand + probes): dialog SNBT parses on every screen, nav/modes/grey/again, gear categories
  of 17 items, probe copy + drop, arrow speed (2.92 b/t) and damage (Power V = 29 HP), clean log + lint.
  Not verified with a real player: hotbar placement, partial fit, the dialog look at GUI scale 2.
