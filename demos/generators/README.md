# generators

Resource generators (DESIGN 2.9) on top of the game code in `datapack/data/nonios/function/generator/`.
G -> "Demo: Generators": upgrade / downgrade / buy upgrade (nearest), reset all, time x10 / x1, +100 coins, empty purse,
simulate 20 players per team, drop now, status, rebuild. All buttons are `trigger demo.gen set N`.

Layout: floor at y=63, three generators at x=-6/0/6, z=-6 (white Lv1, black Lv2, white Lv3). Players join in adventure mode.

## How it works (game code)
- **Entities per generator:** `marker` (tags `nx.gen`, `nx.gen.<team>`; `data:{team,lvl,name,col,glow}`), `item_display` core
  (`nx.gen_core`, turned 45/90/135 degrees per second by an absolute `tp` (yaw kept in range) with `teleport_duration:20`), `text_display` hologram (`nx.gen_holo`),
  `interaction` (`nx.gen_click`, right-click = collect). Parts are found with `distance=..2.5` from the marker, so keep generators >= 3 blocks apart.
- **Loop:** `nonios:generator/loop` reschedules itself every 20 ticks. Per generator: timer -= 20 x `#speed`; when due, `drop`
  rolls `1 + (team players - 1) / 4` times (`@a[team=white|black]`; `#sim` overrides) and resets the timer. Nothing runs per tick.
- **Rolls:** `generator/roll/<team>_lvl<N>` (generated) = `random value 1..81`: the emerald outcomes add `#e1`/`#e9` coins to the pot,
  everything else is `loot spawn` from `nonios:generator/<team>_lvl<N>`. Pot capped per level (50/150/500).
- **Item cap:** if 16+ item stacks lie within 2 blocks the drop waits ("full").
- **Collect:** advancement `nonios:generator/click` (player_interacted_with_entity) -> the clicked interaction (checked with `on target`)
  -> its marker: items within 2 blocks teleport to the player, the pot goes into `nx.coins`.
- **Levels:** `upgrade` / `downgrade` / `set_level {lvl}` / `reset` -> `apply`: interval + cap from config, `place template
  nonios:generator/<team>_lvl<N>` (base two blocks below the marker), core item, glow at Lv3, sound + particles.
- **Data:** `src/generators.json` -> `python tools/build_generators.py` -> loot tables, roll functions, `generator/config`.
  `--structures` re-imports the V2 structures (black copied as is, white cropped from 5x5 to its 3x3 core; both DataVersion 1343,
  upgraded by the game's DataFixer on load).

## From the original (V2.0, recovered from the region files)
The V2 generator was a block on a sea lantern that regenerated instantly when mined: two 9-slot dispensers fired a random
item each (1 of 81 outcomes), item detection picked the next block. Type dispenser: cobblestone 4, log 2, lapis 2 (-> ore roll), apple 1.
Ore dispenser: coal 3, iron 3, gold 2, diamond 1. Per level (white / black where they differ):

| outcome (x/81) | Lv1 | Lv2 | Lv3 |
|---|---|---|---|
| 36 | stone / cobblestone | stone / cobblestone | emerald ore |
| 18 | log | sandstone / netherrack | diamond ore |
| 9 | hay block | emerald ore | emerald block |
| 6 | coal ore | gold ore | iron block |
| 6 | iron ore | diamond ore | gold block |
| 4 | emerald ore | iron block | diamond block |
| 2 | iron block | loot chest | loot chest |

Upgrade signs charged 75 (build Lv1), 200 (Lv2), 500 (Lv3) coins; 1000 bought the Emerald Dream portal. Structures `white_generator_lvl1..3`
(5x5 incl. grass) and `black_generator_lvl1..3` (3x3): bedrock base + sea lantern, Lv2 adds 4 corner glass panes, Lv3 a full glass ring.
