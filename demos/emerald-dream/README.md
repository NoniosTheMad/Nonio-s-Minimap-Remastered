# emerald-dream
M4 feature: the Emerald Dream as a custom dimension `nonios:emerald_dream`.
G -> "Demo: Emerald Dream": enter, force exit, regrow veins, channel 2/5/10/15 s, vein regrow 10/30 s, hurt me (test cancel), settings, gear, reset coins.
The end-portal-frame pad east of spawn (styled after the original exit platform) enters too.

Game code: `datapack/data/nonios/` -> `dimension/`, `dimension_type/`, `worldgen/` (noise_settings, material_rule, density_function/dream, biome, feature, placed_feature),
`function/dream/`, tags `function/dream/*` (hooks), `block/dream_*`, predicates `dream/*`.
- **World**: floating islands (vanilla floating_islands router), grass/dirt tops, moss undersides, stone with calcite-wrapped emerald ore veins
  (material rule `ore_vein`, raw emerald blocks 3%) plus a second amethyst vein with deepslate emerald ore (#47). Features: emerald ore + clusters,
  gold, lapis, diamond, calcite pockets, geodes, glow lichen, crystal spires (amethyst + green glass + froglight), amethyst buds, glow lamps in the
  grass, azaleas, glow-berry vines, spore blossoms, oaks, flowers, wildflowers, firefly bushes. Emerald sky/fog/foliage; sparkles, spores, fireflies
  and glow particles; allays, rabbits, parrots, frogs, bats, rare endermen. Fixed time, no beds/anchors.
- **Ruins (#47)**: on landing, up to `#ruins` (2) small ruins (shrine / well / arch, `structure/dream/ruin_*`, built by `tools/build_dream.py`) are placed
  on flat ground within `#ruin_r` (48), 48+ apart, with chests on loot table `nonios:dream/ruin` (emeralds, shards, pearls, XP; rarely a diamond,
  golden apple, enchanted book or totem). Placed at runtime with `place template` because the servers run `generate-structures=false`.
- **Enter** `function nonios:dream/enter` (as player, ungated) or `nonios:dream/try_enter` (runs hook `#nonios:dream/gate` first: a gate function sets
  `#deny nx.dream 1` to refuse). Saves dim/pos/rotation in storage `nonios:dream ret.p<nx.pid>`, holds the player at y 250 over a random column
  in +/-`#range` until the chunk loads, scans down for ground with 2 free blocks (else nudges +/-40, re-rolls after 12 misses, 20 s fallback = raft at 0 0).
- **Veins**: on landing, `#veins` markers (`nx.dream_vein`) are spread within `#vein_r` and set a weighted ore under them (55% emerald, 15% deepslate emerald,
  8% diamond, 9% gold, 8% lapis, 5% emerald block). Mined -> regrows after `#regrow_ticks` (never into a player or a placed block). Veins nobody has been near
  for `#ttl` are forgotten. `function nonios:dream/reset_veins` regrows all loaded ones.
- **Exit**: hold sneak `#channel_ticks` (default 100). Bar in the actionbar, chimes audible to others. Damage (`damage_taken`/`damage_absorbed` stats) or
  releasing cancels; after a hit you must release sneak first. Returns to the saved spot, else hook `#nonios:dream/fallback_return` (default: respawn point, else overworld 0 0 surface).
  `function nonios:dream/force_exit` wakes instantly. Dying there just forgets the saved spot.
- Hooks: `#nonios:dream/gate`, `#nonios:dream/on_enter`, `#nonios:dream/on_exit` (storage `nonios:dream reason`: arrived/woke/forced/lost), `#nonios:dream/fallback_return`.
- Config: fake players in `nx.dream` (set in `dream/load` only when missing): `#channel_ticks #regrow_ticks #range #veins #vein_r #ruins #ruin_r #ttl #land_min_y` (veins 16 within 11 since #47).
Demo only: portal pad, sidebar (coins come from the game pack purse, which pays mined ores).
