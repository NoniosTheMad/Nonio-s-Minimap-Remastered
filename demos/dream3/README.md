# dream3: Emerald Dream v3
Feedback #79-#83 on top of emerald-dream/gen-dream. G -> "Demo: Emerald Dream v3" (2 columns, fixed slots):
enter / wake, build a minor / major / grand / nightmare site where you stand, Dream Key, gear, gleaming sheep,
hurt me, regrow veins, yields, reset coins, site log.

## What changed in the game pack (`datapack/data/nonios/function/dream/`)
- **Sites** (`site/`, templates from `scenes/dream/*.py` via `tools/build_dream.py`): one possible site per 192x192 cell at a hashed
  point (world `#seed`); decided when a dreamer comes within 112 blocks, flagged with a barrier at y 0. Tier odds 30 none / 45 minor /
  18 major / 6 grand / 1 nightmare (once per world). Grand/major that don't fit fall back a tier. Ground sites drop onto an island
  (`spreadplayers`), sky sites take a mostly-empty box at y 120-200 and carve islands inside their own silhouette.
  - minor: wayshrine, moonwell, lantern_tree (1 chest, 3 deposits) - major: crystal_grotto (ground), sky_garden (sky) (1 chest + beam)
  - grand: inverted_sanctum (vault opened with a Dream Key + beam) - nightmare: nightmare_spire
  - Beacon beams mark unlooted loot; looting turns the beam off (tinted glass). A shaft is punched through islands above each beacon.
- **Deposits** (`vein/`, #80): ores only regrow at site deposits; a mined vein has `#spread_pct` (25%) to sprout into a neighbouring
  stone/dirt block, up to `#deposit_cap` (10) veins within 6 blocks.
- **Dream ores pay coins only** (#82): diamond/gold/lapis/redstone ore loot tables drop nothing in `nonios:emerald_dream`
  (emerald ore/blocks drop nothing everywhere already). Coins come from the purse (`src/yields.json`) in every dimension.
- **Dream Wings** (`wings/`): bare chest -> vanishing elytra; any chestplate gets the glider component while in the Dream.
  Jump while gliding = boost (enchantment `nonios:dream_wings`: apply_impulse 0.12/tick for 12 ticks, up to 34 b/s);
  3 charges, 1 per 3 s. Everything is stripped on waking / dying / every 10 ticks outside (inventory, armor, cursor, ender chest).
- **Void catch** (`void/`): below y 6 you go back to the last solid ground you stood on, with slow falling (the "fell out of the world").
- **Pixie** (`pixie/`, #80): an allay + interaction (`nx.shop_npc`, `nx.any`) hovering at your shoulder, through walls; right-click = the shop v3 dialog.
- **Animals** (`fauna/`): rabbits/frogs/parrots/sheep/foxes drop 1-2 emeralds; 10% gleam (glowing, bigger): 6-10 emeralds, 35% Dream Key. Babies drop nothing.
- **Nightmare** (`nightmare/`, #81): guard posts wake within 20 blocks (vindicators, evokers, wither skeletons, breezes, a ravager, 2 wardens;
  buffed, no loot); mining fatigue IV around the keep. The altar gives "Exodia" once per team (`#nonios:dream/exodia_grant`, stub = a nether star).
- Jump Boost II (#81), no endermen (#81), sheep + foxes added, wake channel 10 s (#83).

## Yields (coins; emerald = 5, emerald block = 45 when picked up)
| Source | Per event | Rough rate |
| --- | --- | --- |
| Mining a deposit | avg 5.2 per break (x2.2 with Fortune III) | ~100/min on a full 10-vein deposit (30 s regrow) |
| Animal | 1-2 emeralds (5-10) | bonus while flying |
| Gleaming animal (10%) | 6-10 emeralds (~40) + 35% key | |
| Minor chest | 3-7 emeralds, 25% block, extras (~35) | one-shot per site |
| Major chest | 10-18 emeralds + 1-2 blocks (~150) + 50% key | one-shot |
| Grand vault | 5-9 blocks + 10-20 emeralds (~400) + rare item | once per player per vault, needs a key |

Main world (econ3): the same ores pay the same coins there **and** drop their items; in the Dream they pay coins only.
