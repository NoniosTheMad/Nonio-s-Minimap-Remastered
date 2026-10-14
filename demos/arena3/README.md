# arena3
Arena v3 (feedback #39 #40 #42 #43, branch feat/arena-v3; #47-49 on feat/gen-dream). The game pack does the work; this demo only adds test buttons
(G > "Demo: Arena v3") and builds the placeholder map on first load.

## What changed
- **Field generators (#39)** `nonios:generator/*`: V2 style again. One block grows on top of the sea lantern
  (`generator/grow/<team>_lvl<N>`, V2 81-outcome tables from `src/generators.json`); players mine it, coins only through the
  purse (emerald ore / block yields, `src/yields.json`). When the spot is empty the regrow timer runs (`levels.regrow_ticks`
  300 / 200 / 140), x (1 + (team players - 1) / 4), x1.5 with a "regrow" node. No pot, no hologram. An interaction over the
  3x3 base opens the upgrade dialog (compact, one fixed button, greyed out when unaffordable / max) and shields the base.
- **Single-block mode (#47, replaces the lucky block)** `generator/one/*`, `generator/mode/toggle`: `single.on` in
  `src/generators.json` (default false), runtime `#single nx.gen`. Every regrowth is `single.block` (gilded blackstone);
  mined, it rolls the same V2 81-outcome table as a loot table (`loot_table/generator/one/<team>_lvl<N>`) and pays the
  purse yield of the V2 block it stands for. No traps.
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
- **Barrier (#47-49)** `nonios:nexus/*`: enemy players' projectiles hit the shell geometrically (`nexus/proj`: arrows,
  tridents, fireworks with stars, wind charges, fireballs; 20% of their player damage). Melee scales with the attack charge
  (`nexus/charge`: x(0.2 + 0.8 c^2), c = time since your last Barrier hit / your weapon cooldown): spam-clicking ~20%/click.
  `nexus/press/*` once a second in the battle: the team holding the centre node (`press.node`, "centre") drains the enemy
  Barrier at `#press_pm` (120 = 12%/min of max HP) x r^2, r = hold s / `#press_ramp` (300) capped at 1; losing the node resets.
  From battle minute `#decay_min` (20) each Barrier's ceiling (`nx.hp_cap`) drops `#decay_pm` (100 = 10%/min): an untouched
  Barrier breaks at minute 30. Config in `nexus/load` (`nx.const`, set only when missing).

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
| 11 | Single-block generators | mode on/off |
| 12 | Tp: centre generator | |
| 13 / 14 | Banks +1000 / Banks 0 | +500 to each bank / empty both |
| 15 | Centre gen: drop now | |
| 16 | Tp: arena | |
| 17 | Own all nodes | every node to your team |
| 18 | Protection on/off | `#prot nx.arena` |
| 19 | Random event | announced with countdown |
| 20 | Status | arena + generators |
| 21 / 22 | Rebuild map / Admin panel | |
| 23 | Ranged kit | Power V bow, crossbow, loyalty trident, rockets with stars, wind charges |
| 24 | Tp: enemy Nexus | 6 blocks in front of it |
| 25 | Centre hold sim | cycles none / white / black holds the centre |
| 26 | Hold +4 min | skips the current hold towards full pressure |
| 27 | Minute-20 decay | jumps the barrier clock to the decay start |
