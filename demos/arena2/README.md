# arena2
V2's arena portals and regrowing central block, rebuilt for 26.3 on top of the match (main 5850661+).
The game pack does all the work; this demo only adds test buttons (G > "Demo: Arena gates + core") and builds the map on first load.

## What V2 did (recovered from the V2 world's command blocks)
- **Arena portals** (machine at -64..-57 88..91 51..60): the arena floated at (-60, 101..112, 54). Its single entrance was the top of the
  central tower (portal particles at 8 63 8, standing on 8 62 8). Four repeating chains, one per *slot*; only the chain with a redstone
  block under it ran. Each slot = a landing point on the arena rim (N/E/S/W, 22 blocks from the centre, facing it) + an exit portal
  (portal particles, floor 11 blocks diagonally from the centre) that sent you to the tower base (8 43 8).
  A 16-item hopper clock (128 ticks = 6.4 s) re-rolled the active slot: a dispenser with 4 different items fired one at random and
  `testfor` placed the redstone block under that chain (uniform 1/4, may repeat). Entry played `block.end_portal.spawn` to every player.
- **Central block** (-60 101 54, bottom of the arena's central pit): an always-on repeating block refilled it the tick it was air with the
  current roll. Rolls (redstone clock ~0.3 s): dispenser #1 cobblestone x4 / log x2 / lapis ore x2 (= "ore") / apple x1 (= hay);
  for "ore", dispenser #2 coal x3 / iron x3 / gold x2 / diamond x1 -> emerald ore unless diamond -> emerald block.
  Odds per regrowth: cobblestone 36/81, oak log 18/81, hay 9/81, emerald ore 16/81, emerald block 2/81. Always on (all phases).

## What the remaster does
- `nonios:arena/gate/*` (arena module): config `gates` (entry pads), `slots` ({land, exit}), `gate {every, sound}`.
  Markers: `nx.agate` (+ `nx.<team>`) at foot level on each pad, `nx.aslot` at each exit (`nx.ar_slot` = 1..), `nx.aslot_on` = active.
  `gate/tick` (from `nonios:tick`) is one score check while shut; open (`#gon`): pad -> active landing (+ entry sound to all),
  active exit -> your team's pad `out` (no team: first pad). Rotation + particles run in the 10-tick arena loop (`#speed` applies).
- `nonios:arena/core/*`: config `core {x,y,z}`, `core_blocks [{id,w}]` (V2 odds), `core_regrow` (ticks, 0 = next 10-tick check).
  Only air regrows (a block placed in it blocks it, as in V2). Emerald ore / block pay through the purse's mined stats (25 / 100).
- Phases: both run only while the arena runs (battle in the match): `arena/start|stop` -> `gate/state` (pad labels red/grey).
  `arena/reset` (from `game/reset_world` and `to_lobby`) -> fresh slot, counters, core re-rolled, drops near it removed.
  `arena/setup` (map build) rebuilds the markers. Without config (arena demo, no map) both stay inert.
- Map: `map/config` per field `agate {team,x,y,z,out}` (pad built by `map/gen/arena_gate`), `arena_cfg.slots` (4 corners -> 4 exits),
  `arena_cfg.core` = 0 65 100 (top of the Centre Node's ore pile; the static emerald ore there is gone). `map/arena_config` copies them.

## Buttons
Start + battle now, Start, Skip phase, Stop, Switch team, Pickaxe + axe, Time x10, Prep 20 s,
TP my gate / active exit, Re-roll gate slot, Gate status, TP core, Break the core, Core 810 rolls, Core status,
TP arena, Full arena status, Rebuild map, Admin panel.
