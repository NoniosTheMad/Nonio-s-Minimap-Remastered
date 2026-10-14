# arena3
Arena v3 (feedback #39 #40 #42 #43, branch feat/arena-v3). The game pack does the work; this demo only adds test buttons
(G > "Demo: Arena v3") and builds the placeholder map on first load.

## What changed
- **Field generators (#39)** `nonios:generator/*`: V2 style again. One block grows on top of the sea lantern
  (`generator/grow/<team>_lvl<N>`, V2 81-outcome tables from `src/generators.json`); players mine it, coins only through the
  purse (emerald ore / block yields, `src/yields.json`). When the spot is empty the regrow timer runs (`levels.regrow_ticks`
  300 / 200 / 140), x (1 + (team players - 1) / 4), x1.5 with a "regrow" node. No pot, no hologram. An interaction over the
  3x3 base opens the upgrade dialog (compact, one fixed button, greyed out when unaffordable / max) and shields the base.
- **Lucky block (proposal, off)** `generator/lucky/*`: `lucky.on` in `src/generators.json` (default false), runtime switch
  `function nonios:generator/lucky/toggle` (`#lucky nx.gen`). 1 in `one_in` regrowths = `lucky.block`; mined -> coins 8/20
  (4-10 flung emeralds), item 7/20 (`loot generator/lucky_item`), trap 5/20 (silverfish / cobweb + poison / levitation).
- **Centre generator (#39/#40)** `nonios:arena/cgen/*`: pot style (spinning core, hologram, click = collect pot + drops), at
  `arena_cfg.cgen`. Runs with the arena. B = both team banks: level 1 / 2 / 3 at B >= 0 / 1000 / 3000 (pot cap 100 / 300 / 800,
  better table with items), rolls per drop = min(5, 1 + B / 1000), one drop every 10 s, Golden Hour x3 speed.
- **Capture nodes (#40)**: per node `bonus` (none | haste | interest | regrow). No loot by default. Haste I inside your field;
  bank + 0.5% (max 10, x Golden Hour) every 30 s; field generator regrows x1.5. Hologram + bossbar show the bonus.
- **Events (#42)**: every event is announced `event_warn` (600) ticks ahead: bossbar `nonios:arena/event` with countdown,
  raid horn, short title; timed events then count down on the same bar. New: Supply Drop, Bounty Hunt (+50 per kill in the
  arena), Low Gravity. Golden Hour now speeds up the centre generator. Frog rain is a troll event (`config.trolls`, off).
- **Protection (#43)** `nonios:arena/protect/*`: `arena_cfg.protect` box (y 60..67) copied to y -40 at setup; every tick
  `execute unless blocks ... masked` -> `clone ... masked` back, 0-tick-old item drops killed, mining stats of
  `protect_types` cancelled (before purse/tick). Air in the snapshot = buildable; core + node indicators are holes.

## Buttons
| # | Button | Does |
|---|--------|------|
| 1 | Start + battle now | team if needed, start, skip preparation |
| 2 | Start match | normal start |
| 3 / 4 | Skip phase / Stop match | `game/skip`, `game/stop` |
| 5 | Switch team | white <-> black |
| 6 | Pickaxe + axe | efficiency V tools, cobblestone, food |
| 7 | Time x10 | `#speed` for arena + generators |
| 8 | Tp: my generator | in front of your field generator |
| 9 | Grow now | nearest generator rolls a new block |
| 10 | Generator Lv+1 | free upgrade (Lv 3 -> 1) |
| 11 | Lucky block | proposal on/off |
| 12 | Tp: centre generator | |
| 13 / 14 | Banks +1000 / Banks 0 | +500 to each bank / empty both |
| 15 | Centre gen: drop now | |
| 16 | Tp: arena | |
| 17 | Own all nodes | every node to your team |
| 18 | Protection on/off | `#prot nx.arena` |
| 19 | Random event | announced with countdown |
| 20 | Status | arena + generators |
| 21 / 22 | Rebuild map / Admin panel | |
