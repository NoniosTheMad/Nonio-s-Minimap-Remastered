# m5-classes
M5 integration: the class framework (feat/classes: Reaper, Cracy Frog, Warrior placeholder) wired into the full match on main
(M2 core, economy, generators, arena, Emerald Dream). Superset of m4-match (buttons 1-26 are the same, 27-34 are classes).
Demo dummies/captors carry `nx.soul` so the Reaper harvests them.

Wiring (game pack):
- `nonios:load` / `nonios:tick` call `class/load` / `class/tick` with every other module.
- Deaths: `game/death` calls `class/on_death` first, on every death (shop class lost, basic items/vision removed);
  `#nonios:kit/respawn` = `kit/respawn` + `class/on_respawn` (basic class back at the team level `#white/#black nx.cls_lvl`).
- `nx.tier` (victim tier for the kill bonus, read by `economy/kill_bonus/tier` at the moment of death) is owned by classes:
  set by `class/gen/<id>/apply` (`src/classes.json` `kill_tier`; basic = team level - 1, V2 kits II/III), 0 in `class/strip`.
- Shop: `shop/catalog` appends `class/gen/shop_items` (classes with a `shop` block in src/classes.json). A class entry
  (`class` field) goes through `shop/buy_class`: already that class = refused, price from the purse, then `class/set_id`.
  `confirm` classes (Cracy Frog, free) open their dialog chain instead (`class/gen/confirm`), the shop dialog stays closed.
  The bare `trigger nx.cls_ask set 1` only opens the chain next to your shopkeeper. Unimplemented V2 classes are not listed
  (prices/tiers kept in `src/classes.json` `_v2_roster`).
- Match reset: `class/reset` (no class, no basic class) in `game/enter` (new match) and `game/lobby_player`; `game/start` sets
  both team class levels back to 1.
- Coins can't be minted from coin blocks any more:
  - placing a coin block while broke books the rest as debt (`nx.pdebt`), repaid first from mining income (`purse/mine/placed`, `repay`);
  - emerald / emerald block items become coins on pickup (`advancement purse/emerald` -> `purse/emerald`, 5 / 45 like generator outcomes);
  - emerald ore, deepslate emerald ore and emerald blocks drop nothing when mined (`data/minecraft/loot_table/blocks`), the mined stat pays.
