# arena

Arena systems (DESIGN 2.10) on top of the game code in `datapack/data/nonios/function/arena/`.
G -> "Demo: Arena": switch my team, spawn enemy dummy (nearest node), remove dummies, random event, Emerald Surge,
Supply Drop, Golden Hour now, toggle lightning, speed x10 / x1, Purse Thief, status, reset (`trigger demo.arena set N`).

Layout: 41x41 floor at y=63, low wall. Nodes (5x5 zone, 3 high) on plain stone pads: West (-11,64,-3) haste,
North (0,64,-13) interest, East (11,64,-3) regrow. Centre generator (emerald fountain) at (0,64,-3).
The demo overrides nodes, arena box, centre and cgen from `#nonios:arena/config` (`demo:arena_config`).

## How it works (game code, feat/arena-runes #126-#130)
- **Runes (#126):** each node shows an Elder Futhark rune drawn in dust particles, billboarded per viewer within
  `config.rune.view` blocks, `lift` above the zone. The rune comes from the bonus (`src/runes.json` -> `tools/build_runes.py`
  -> `arena/rune/gen/*`): Fehu = interest, Sowilo = haste, Jera = regrow, Othala = no bonus; spares Raidho = swift
  (Speed I in the arena), Algiz = ward (Resistance I in the arena), unused by default. A node may set `rune` explicitly.
  Colour = owner (amber neutral, white, purple for Black); while being captured the strokes paint in, in stroke order,
  with an end-rod pen tip and a throb; red unpainted strokes = contested. Captured: flare + sparks; lost: puff.
  A 4-particle marcher outlines the square zone on the ground. No hologram, no beacon.
  Budget per node and viewer: idle ~n/3 particles per tick (n = 18-29 points), capturing ~n/2 + 1, ring 4.
- **Bossbar:** max = capture x 10 and slides between the 10-tick capture checks, so it fills smoothly. Its title is
  the legend: "<rune> <name>  held by <team>  <bonus>".
- **Payout:** a held node only gives its rune bonus (no loot, no coins). Hook `#nonios:arena/on_node_payout`,
  `storage nonios:arena payout = {team,node,name,bonus}`.
- **Golden Hour (#127):** for `golden_time` every coin earned in the centre is x `golden_mult`: centre generator
  emeralds, kill rewards (base + bounty + streak/tier bonuses) for kills inside `config.bounds`
  (`#nonios:economy/kill_mult` -> `arena/event/golden_kill`, shown as "+N golden"), and the interest node.
- **Purse split (#128/#129):** a kill inside the arena hands the killer `centre_killer_share` % (storage nonios:config,
  default 50) of the victim's purse; the rest drops on the spot as coin bags (the no-killer death path).
  `purse_drop_scope`: "centre" (default) or "everywhere". Golden Hour never multiplies purses (no minting).
- **Centre generator (#130):** an emerald fountain (`src/generators.json` centre). Every `interval_ticks` it throws
  1 + banks / bank_per_roll emeralds (max `max_rolls`, x golden_mult in Golden Hour) onto the floor, while fewer than
  `item_cap` emeralds lie within 4 blocks. Emeralds become coins on pickup. Its spinning emerald core grows with level.
- **Events, lightning, hooks:** as before: `config.events` list, `lightning/on|off|toggle`, `#nonios:arena/config`,
  `#nonios:arena/on_capture` (`cap = {team,node,name}`).

## From the original (V2.0, recovered from command blocks / signs in the region files)
- **Arena:** a central area around (-60, 101..105, 54), about 44x44. Players entered from the Field portal (8 62 8) at one of
  four random spots 22 blocks from the centre (a dispenser fired one of four coloured blocks to pick it). Four corner pads
  at (-49/-71, 105, 43/65) sent them back to the Field (8 43 8).
- **Central generator:** the block at (-60, 101, 54) regrew when mined: cobblestone 4/9, log 2/9, hay 1/9, ore roll 2/9
  (emerald ore, or an emerald block on the last ore outcome). Open to anyone, no capture.
- **Lightning:** signs "Enable / Disable Lightning" in the admin room (next to "Test ResourcePack" and "Configuration").
  Enable summoned a rabbit tagged `Lightning` in the arena: 200 HP, knockback resistance 1, speed 0.6, burning, silent,
  Regeneration X, fire resistance. A clock ran `execute @e[tag=Lightning] ~ ~ ~ summon lightning_bolt ~ ~3 ~`.
  Disable killed it.
- **No timed events** existed in V2; Emerald Surge / Frogs / Golden Hour are new.

## 26.3 gotcha found here
Loot tables use the new format: `"modifier"` (object or list, each with `"type"`) instead of `"functions"` (`"function"`),
and `"condition"` (one object with `"type"`; combine with `minecraft:all_of`) instead of `"conditions"`. The old keys are
**silently ignored** (no load error): every entry drops with count 1 and every chance passes.
