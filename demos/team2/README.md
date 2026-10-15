# team2
Demo for `feat/team-v2`: copy of `demos/full` (trigger `demo.team2`, dialog `demo:team2`, G > "Demo: Team altar")
plus buttons 53-61 for the new team systems. No game-pack code here.

Game pack (namespace `nonios`):
- `altar/*` + `map/gen/altar`: team offering altar (V2 "Offerings"). Right-click it in prep/battle to hand over iron/gold/diamond
  blocks from your inventory (only what the next step still needs). A paid step raises `#<team> nx.cls_lvl` (basic classes use it on
  the next respawn). Costs: `storage nonios:config altar_steps` (V2 8/8/2, 16/16/8, 64/64/64; index = level - 1; teams start at 1).
  Position: `map/config` `<team>.altar`. Reset by `game/reset_world` and `map/build`.
- `guard/*`: spawn defense (V2 House/Deep): enemies within `<team>.guard.r` (4) of the spawn take Instant Damage II every 10 ticks
  in prep + battle. Own team never hit. `config spawn_guard` 0b = off.
- `talisman/*`: Emerald Talisman (V2 special 87). `talisman/give`; worn on the head: Luck +100, `talisman_coins` (1) every
  `talisman_period` (3) seconds in prep + battle. Binding curse. Model `nonios:emerald_talisman` (V2 emerald texture).
  Shop entry for the rebuilt shop: `src/specials.json` (with the Dragon Skull joke, `special/dragon_skull`).
- Admin panel: "Lightning Rabbit: ON/OFF" (`nx.admin` 18). `game/enter`: `recipe give @s *` (V2 start chain).
- Prep walls underground: barrier plane now also y -64..-1; `game/prep/contain` bounces anyone past the wall row at any depth
  (`<team>.out` moved one row in: white z >= 86, black z <= 114).

Buttons 53 offering blocks (next step) / 54 partial offering / 55 TP altar / 56 TP enemy spawn / 57 talisman / 58 Dragon Skull /
59 team status / 60 spawn defense on/off / 61 +3,200,000 coins. 15 "Time x10" also speeds the talisman income.
