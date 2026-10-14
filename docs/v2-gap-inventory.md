# V2 gap inventory

This document compares the systems in the V2 world (`../V2.0 - Just substitute thee world`) with what the remaster has today. It was built from the V2 command blocks, scoreboard, structures, signs and armor stands (read-only).

Status values:
- **BUILT**: the remaster has an equivalent.
- **PARTLY**: something exists but differs or is a placeholder.
- **MISSING**: nothing exists yet.

Who decides:
- **Auto**: I can build it without asking, because the V2 data is enough or it is plain data entry.
- **User**: it needs Nonios's call.

TRACKER question refs use the form "TRACKER <section> Q<n>" and point to "Questions for when user returns". They are not repeated here.

Remaster paths are relative to `datapack/data/nonios/function/` unless stated otherwise.

V1 differences: the V1 world is almost identical to V2. It has the same scoreboard and structures, and the only command-block difference is the generator fill wiring. V1 `comandos.txt` shows an older concept with 4 teams (Blue/Red/Green/Pinku), a Single/Teams mode, a 1-8 player-count menu and "show team members" links. V2 dropped all of these, and the remaster follows V2.

## 1. Match flow

| System | V2 evidence | Remaster status + where | Missing piece | Auto / User |
|---|---|---|---|---|
| Lobby, config, team join | Signs at 0,128,89-91 and 39-40,158,-53. A "How many players" tellraw sets `Info Players`. Join Black/White tellraw. Admins team in creative. | BUILT: `game/join_lobby`, `game/lobby_player`, `game/join`, `team/*` (pick, auto_pick, balance), `admin/*` | none (the V1 4-team mode is not wanted) | - |
| Start sequence | CB chain at 47-48,145-154,-49..-51 does several things. It clears inventory and effects, gives all recipes, and sets keepInventory false. It sets time 0 and spawnpoints (W -6 44 -13, B 24 44 29). It resets Coins/Bank and sets survival. | BUILT: `game/start`, `game/enter`, `kit/start`, `economy/match_start` | V2 gives all recipes (trivial) | Auto |
| Lightning toggle sign | Enable/Disable Lightning signs run setblock 41 171 -39 | PARTLY: `arena/lightning/on|off|toggle` exist (demo button only, off by default); no admin-panel switch | admin toggle | Auto (default on/off: TRACKER M4 Q4) |
| Hardcore / last life | `server.properties` hardcore=true. A dead player becomes spectator, and a clock sets `@a[team=X,m=3]` back to survival while the nexus obsidian exists. | BUILT (different mechanism): `game/death`, then `game/eliminated` once `#team nx.last`=1 (keep_inventory + respawn kit hook) | death penalty and respawn gear differ from V2 | User (open question 2 "respawn gear"; TRACKER M2/M3 core Q2) |
| Win check | `testfor @a[team=X,m=0]` fails, then titles VICTORY/DEFEAT with subtitle "The game is over" | BUILT: `game/win_check`, `game/end/*` (adds stats summary and draw) | - | - |
| Prep barriers ("Magical barriers") | Guardian armor stands at x=4 (W) and x=14 (B), z 8-10, y43. They give Wither V and glowing to enemies within r=1. Barrier stands sit around 8 43 8. There is no timer: the barriers fall only when someone buys shop item 203 (200 coins), which shows the title "Barriers Broken". | PARTLY: timed prep phase `game/prep/*` (bossbar, `contain`/`bounce`) and walls `map/walls/*` | V2 lets a team **buy** the early end of prep. The remaster uses only a timer. | User (purchasable early drop changes pacing) |
| Lower (underground) barrier | Obsidian fill 8 8 6 → 8 12 10, with levers at 8 5 6-10 (sign "unlock lower barrier") | PARTLY: `map/walls/*` drop at the end of prep. Not checked whether they reach underground. | confirm the walls span the full depth | Auto (verify) |
| Central tower | Glass pillars at 7-9,66,7-9. Standing at 8 62 8 enters the arena. | PARTLY: arena entry via `map/gen/arena_gate`, `arena/gates` | tower look depends on the map build | User (TRACKER M2/M3 core Q9 map; open question 1 main world) |
| Map reset / regeneration | none (single-use world) | BUILT: `game/reset_world`, `map/build` | - | - |
| Skull head gallery | 20-29,178-181,-45..-54: 18 named player heads (Thresh, Venom, Balrog, Frog...) placed at start | MISSING | decorative lobby gallery | Auto (pick heads; cosmetic) |
| Resource pack test sign | "Test ResourcePack" plays the custom `balrog` sound | MISSING: the resource pack has no `sounds.json` (no custom sounds) | custom Balrog sound | User (needs an audio file) |

## 2. Nexus and base defense

| System | V2 evidence | Remaster status + where | Missing piece | Auto / User |
|---|---|---|---|---|
| Nexus | Obsidian at -21,48,8 (W) and 37,48,8 (B), checked with testforblock. When broken: title "White Nexus / Destroyed", explosion sound, and chat "Nexus: (obfuscated) Our mana source has been broken. This is your last life". | BUILT and extended: `nexus/*` (barrier HP, shield, regen, hit, broken, destroyed, alert), `game/nexus_lost` | V2 "mana source" flavor line (optional) | Auto |
| Spawn zone (House) | WhiteHouse: 13 stands at -10..-6,43,-10..-8. Blackhouse: 16 at 24-28,43,26-28. Instant damage to enemies within r=1. | MISSING | anti-spawn-camp damage zone at each team spawn | Auto (V2 radius and effect known) |
| Deep zone | WhiteDeep: 33 stands at -13..1,43-47,-15..-9. BlackDeep: 15 at 17-29,43,27-32. Instant damage to enemies within r=2, plus **Wither I to own team** within r=2. | MISSING | the zone, and the meaning of the own-team wither | User (own-team wither looks like a bug or an odd rule) |
| Prep guardians | See "Magical barriers" in section 1 (Wither V + glowing on enemies at the midline) | PARTLY: replaced by `game/prep/contain`/`bounce` | - | (covered by the barrier row) |

## 3. Economy

| System | V2 evidence | Remaster status + where | Missing piece | Auto / User |
|---|---|---|---|---|
| Coin currency | Objective `Coins`, shown in the sidebar | BUILT: `nx.coins`, `purse/*` | - | - |
| Emerald to coin conversion | The `Turn` round-robin clears each emerald for +1 coin and each emerald block for +20 | BUILT (different rates): `purse/emerald` advancement, 5 per emerald and 45 per block | rates differ from V2 (1/20) | User (TRACKER M3 Economy Q1-7) |
| Coin weight slowness | 26,145-148,-39..-42. During timer 1-2500: slowness I/II/III at 40/75/100 coins. During timer 2500-6000: 100/200/300. | PARTLY: `purse/weight` gives smooth slowdown with free threshold, slope and cap | V2 **thresholds rise over match time** | User (TRACKER M3 Economy) |
| Bank | Signs: W at -6..-9,44-45,-16; B at 30,43-45,28-30. Team pool `Stored WhiteBank/BlackBank`. Deposit puts in all coins; withdraw 10/100/1000. | BUILT: `bank/*` (dialog, deposit, withdraw, near, allowed) | - | - |
| Bank interest | 35-36,171,-40..-49: about Stored/200 (0.5%), capped at 10 per cycle, remainder carried | BUILT: `bank/interest/*`, configurable `interest_rate`/`period`/`cap` | V2 defaults are 0.5% and cap 10 | User (TRACKER M3 Economy) |
| Kill rewards | 47,159-160,-53..-68: killer gets the victim's coins +10. Tier bonus: tier 1 +20, tier 2 +90, tier 3 +190. Victim's Tier is reset. | BUILT: `economy/kill/*`, `economy/kill_bonus/tier`, `purse` death drop | - | - |
| Emerald Talisman income | Special item 87 (200 coins): luck 100 head, and the tag gives +1 coin per clock tick | MISSING | passive-income head | Auto (V2 behaviour clear; the rate needs a sane conversion) |

## 4. Progression

| System | V2 evidence | Remaster status + where | Missing piece | Auto / User |
|---|---|---|---|---|
| Team offering upgrade (Kit I-III) | Offering chests at W -7 47 -11 and B 24 43 31. Book "Upgrades" by "The Observer" with armor stands "Offerings"/"Instructions". 8 iron + 8 gold + 2 diamond blocks gives Kit 1. 16/16/8 gives Kit 2. 64/64/64 gives Kit 3. | PARTLY: `nx.cls_lvl` team level exists (set to 1 at start), and the basic class (Warrior) has loot l1-l3 | **no altar or offering raises `nx.cls_lvl`** | Auto (costs known; the altar look is a placeholder) |
| Basic class picker | V2 had no pick: everyone got the team Kit I-III on respawn | PARTLY: `nx.cls_basic` + `class/on_respawn` re-apply it, but in the match nothing lets a player choose a basic class (only `class/set_id` from demo buttons); Warrior is the only basic class | picker (dialog at spawn / shop) or auto-assign the team kit to everyone like V2 | User (TRACKER M5 Q4: Warrior basic vs shop; V2-style = automatic kit) |
| Respawn kit by level | 47-63,165,-43..-45. Kit 1: chain armor and stone tools. Kit 2: iron armor, Power III bow, diamond pickaxe, shield. Kit 3: diamond armor, Sharpness III sword, Power V + Infinity bow, Efficiency V + Fortune III pickaxe, "Gardna's Shield", buckets. | PARTLY: `kit/respawn` is a stub, `kit/start` gives placeholder stone tools, and the Warrior l1-l3 loot is a placeholder | real kit contents per level | User (open question 2 respawn gear; TRACKER M5 Q4 Warrior, M2/M3 core Q2) |
| Generators | Unlock stands at W -22,47,24 and B 30,44,0 cost 75/200/500 (another chain 20/75/200). Ore blocks at -22,46,19 and 35,45,2. Structures white/black_generator_lvl1-3. | BUILT: `generator/*`, `src/generators.json` (V2 81-outcome odds, structures imported) | intervals and pot values | User (TRACKER Generators Q1-6) |
| Emerald Dream | Unlock stands at W -18.5,46,-3.5 and B 33.6,44,22.5 (1000). Places `emerald_dream_teleport`. **Per-team** areas: W -21 45 -4 ↔ -63 99 -33; B 36 43 22 ↔ 47 89 79. | BUILT (redesigned): `portal/*` (1000 unlock), `dream/*` custom dimension | shared vs per-team area | User (TRACKER Emerald Dream Q7-13) |
| Hidden loot chests | Field chests hold enchanted books, golden apples, totems, lingering potions, emerald ore/blocks and bows. Positions include -8,31,9; -7,13,7 (Tinkiwinki's Touch); -4,19,22; 14,27,-18; 1,22,-7; 7/9,8,8; 25,23,3; 16,13,17; 26,26,22; 9,51,-26; 1,44,-2; 19,42,21; 3,39,38; 8,67,8. Ore chests at -6,41,14 and 30,49,12. | MISSING | loot tables + placement in field gen | Auto for the loot tables (V2 contents known). Placement waits on the map (open question 1). |

## 5. Shop

| System | V2 evidence | Remaster status + where | Missing piece | Auto / User |
|---|---|---|---|---|
| Shop UI | "OPEN SHOP" sign (`shopDisplay`). Menus: Blocks, Ore, Food, Utility, Enchanting, Tool, Alchemy, Ammo, Kits, Special. Shop Keeper flavor line per section. | BUILT (UI): `shop/dialog`. PARTLY (content): `shop/catalog` is an 11-item placeholder plus generated class items. | categories and per-section flavor lines | Auto (port V2 lines; terse, diegetic) |
| Catalog: Blocks | 1 Dirt x4 1; 2 Cobble x2 1; 3 Log x2 1; 4 Netherrack x32 4; 5 Dark Glass x4 16; 6 Obsidian 12; 7/8 Oak/Spruce Sapling 4; 9 Soul Sand 12; 10 Sand x3 3; 11 Sugar Cane 4; 200 Brown Mushroom 4 | PARTLY (Cobble, Oak Planks placeholders) | V2 list | Auto (data entry). The final prices depend on TRACKER M2/M3 core Q7 / open question 4. |
| Catalog: Ores | 12 Coal block x2 1; 13 Iron block 4; 14 Gold block 6; 15 Diamond block 12; 16 Redstone 3; 17 Glowstone 3; 18 Gunpowder 3; 39 Lapis x3 5 | MISSING | V2 list | Auto (data entry) |
| Catalog: Food | 19 Carrot x16 1; 20 Steak x2 1; 21 Golden Carrot 1; 22 Golden Apple 40; 23 Enchanted Apple 300 | PARTLY (Bread, Steak, Golden Apple) | V2 list | Auto |
| Catalog: Utility | 24 Ender pearl 100; 25 Water 5; 26 Lava 10; 27 Cobweb x4 10; 28 Slimeball 5; 29 Milk 10; 30 End crystal 100; 31 TNT x4 320; 32 Flint & Steel 10; 33 "Farting device" fireworks x8 8; 34 Totem 500 | PARTLY (Pearl x2 30, TNT x2 50: prices far from V2) | V2 list | Auto (V2 prices as default) |
| Enchanting (enchant item in hand) | 35 x10 levels 100; 36 Book 3; 37 Bookshelf 10; 38 Enchanting table 75; then direct enchants on the held item: Fortune III 30, Efficiency II 20, Efficiency V 200, Power III 50, Flame 60, Infinity 100, Curse of Vanishing 10, Curse of Binding 10, Sharpness III 50, Fire Aspect 60, Knockback 30 | MISSING | "enchant held item" purchase type (`item_modifier` on mainhand) | Auto |
| Tools / named specials | 201 Bow 20. 41 Tinkiwinki's Touch: iron pickaxe Fortune V, 200. 42 Nonios's Weakness: diamond pickaxe Efficiency V Fortune X, 500, with chat "<NoniosTheMad> Good Choice!". 52 Satan's Blade: Sharpness 100, Smite 25, Knockback 3, 2000. Lore text recovered. | MISSING (placeholder Iron/Diamond sword, Diamond pickaxe) | the named items | Auto (V2 stats + lore). Balance needs a check: Sharpness 100 one-shots. |
| Alchemy | 54 Nether Wart 32; 55 Blaze Rod 20; 56 Rabbit Foot 5; 57 Melon 5; 58 Ghast Tear 5 (charges 20, a V2 bug); 59 Spider Eye 5; 60 Magma Cream 5; 61 Dragon Breath 25; 62 Mining Boost potion 200; 63 Faker's Elixir (glowing) 30; plus the unsold "Lightbringer" potion | MISSING | V2 list | Auto |
| Ammo | 64 Toxic Dart 40; 65 Piercing Bolt 80; 66 Healing Blast 40; 67 Lightning Strike 40; 68 Clumsy Cream 40; 69 Fragile Touch 40 (tipped arrows x8); 70 Spectral x16 20; 71 Arrow x16 5; 72 Snowball x16 5 | PARTLY (Arrows x16 8) | the tipped arrows (Lightning Strike needs a projectile hook) | Auto |
| Special | 87 Emerald Talisman 200 (see section 3). 89 Monster Skull 1800 (= Monster class). 88 Dragon Skull 3200 "[Disabled]" (the CB tests 3,200,000 and runs `say dragon`, a joke). 203 Destroy Magical barriers 200 (see section 1). | PARTLY (Monster as a class) | Talisman, barrier buy, Dragon Skull joke | Talisman and Dragon joke: Auto. Barriers: User. |
| Purchase mode | `Continuous` objective: Single purchase vs Constant purchase | MISSING | repeat buying without re-opening | User (open question 5 quantity picker) |
| Kit menu warning | Hover "Clears armour" / "Clears armour and off-hand" | PARTLY: class apply messages | - | Auto (part of the class description text) |

## 6. Classes (V2 "Kits" shop section)

| System | V2 evidence | Remaster status + where | Missing piece | Auto / User |
|---|---|---|---|---|
| Archer 50, Warrior 60, Miner 80, Tank 100, Ninja 100, Berserker 120, Reaper 200 | Kit ids 73-79. Runtime clocks: Reaper invisibility, smoke, invincible after a kill; Berserker strength, speed, regeneration with armor stripped; Ninja armor stripped and Chunin Sandals. | BUILT: `class/<id>/*`, `src/classes.json` (Warrior = basic placeholder, not a shop class) | Warrior as a V2 shop class (60) vs basic | User (TRACKER M5 Q4, Classes Q1-6) |
| Ninja death message | "Your Naruto powers vanish" on death | MISSING | one terse line in `class/on_death` | Auto |
| Monster Transformation | Kit 80 for 300. The Monster Skull special costs 1800. Devour on kill, hunger. | BUILT at 1800 | price 300 vs 1800 | User (TRACKER V2 shop classes Q1) |
| Balrog Creation 10000 | Jump boost 155, fire resistance, lava trail with Bad Luck → Cursed → Wither II, wall-climb levitation, custom sound | BUILT except the sound | `balrog` sound | User (audio asset) |
| Cracy Frog (free, 3-question chain) | Lines recovered (Cl4t-TP joke) | BUILT: `class/cracy_frog`, `class/gen/confirm` | - | - |
| Paladin 300, Death Knight 500, Titan 1500, Destroyer 2000, Guardian Angel 5000 | Listed in the V2 menu and on planned-class signs, but **never implemented** (no kit CBs) | MISSING | whole design | User (no V2 design exists) |
| Invisible players glow (`weakInv`) | Anyone with invisibility, except Reaper and Ninja, glows | MISSING | rule | User (TRACKER V2 shop classes Q11) |

## 7. Arena

| System | V2 evidence | Remaster status + where | Missing piece | Auto / User |
|---|---|---|---|---|
| Random entry gates | Enter at 8 62 8. A dispenser picks 1 of 4 slots (-38/-60/-82,105,32/54/76). `end_portal.spawn` sound plays globally. | BUILT: `arena/gates` (random slots) | - | - |
| Exit pads | -49/-71,105,43/65 send you back to 8 43 8 | BUILT: `arena/gate/leave` (exit = back to your own team's pad, TRACKER Arena V2 Q2) | - | - |
| Regrowing core block | -60,101,54 cycles cobblestone / log / hay / emerald ore / emerald block | BUILT: `arena/core` | - | - |
| Lightning Rabbit | Spawned at -67,102,57: 200 HP, speed 0.6, struck by lightning, regeneration and fire resistance | BUILT: `arena/lightning` | on/off toggle (section 1) | Auto |
| Nodes and events (surge, frog rain, golden hour, fling) | none (remaster addition) | BUILT: `arena/node/*`, `arena/event/*` | node payouts drop loot; the per-node `coins` value goes to `#nonios:arena/on_node_payout`, which is empty (no team-bank payout) | User (TRACKER Arena Q1-8 incl. Q4 payout method, Arena V2 Q1-9) |

## 8. Junk, tests, easter eggs (not ported, by intent)

These do not need porting:
- The `kill skiwaler20` CB at 3,42,-9.
- Zombie pigman anger and droplet particles at 24,42,6.
- Compass signs at y221 (`tell oli` test).
- The "found" chest test at 39,222,-49, which spawns an Emerald Dream teleport at -41,192,-1.
- 630 redstone item entities and 662 untagged armor stands.
- The dev "2do" sign ("fill chests", "modify spawners", "implement shops").
- The "REMEMBER TO SET THE WORLD TO HARDCORE" admin note.

The only possible keep is the y222 easter egg, if Nonios wants a hidden Dream portal. That is a User call and is low priority.

---

## Missing - autonomous

1. Port the full V2 shop catalog (Blocks, Ores, Food, Utility, Alchemy, Ammo) with V2 prices as defaults, replacing the 11-item placeholder.
2. Add the "enchant the held item" purchase type and the V2 enchant list.
3. Add the named specials: Tinkiwinki's Touch, Nonios's Weakness (with the chat line), Satan's Blade, Farting device, Faker's Elixir, Mining Boost, and the tipped arrows.
4. Add the per-section Shop Keeper flavor lines.
5. Build the team offering altar that raises `nx.cls_lvl` (8/8/2, 16/16/8, 64/64/64 blocks of iron/gold/diamond, from V2).
6. Add the spawn defense zones (House: instant damage to enemies at the team spawn).
7. Port the Emerald Talisman head (luck plus passive coin income).
8. Write the hidden field loot-chest loot tables from the V2 contents. Placement waits for the map.
9. Add the Ninja death line, the Dragon Skull "[Disabled]" joke, the lightning on/off admin toggle, and the all-recipes grant at start.
10. Verify that the prep walls cover underground (the V2 lower barrier).
11. Build the lobby skull head gallery (cosmetic).

## Missing - needs user

1. "Destroy Magical barriers": can a team buy the early end of prep (V2: 200 coins, no timer)?
2. Deep zone rules: V2 gives Wither I to the owning team. Is that intended?
3. Real respawn kit contents per team level (V2 Kit 1-3 are known), and how a player gets the basic class in the match (no picker today; V2 gave the team kit to everyone). See open question 2 and TRACKER M2/M3 core Q2 and M5 Q4.
4. Paladin, Death Knight, Titan, Destroyer and Guardian Angel: they are only listed in V2, so they need full designs.
5. Single vs Constant purchase mode. See open question 5.
6. Weight thresholds that rise with match time (V2 40/75/100, then 100/200/300). See TRACKER M3 Economy.
7. Emerald conversion rates (V2 1/20 vs remaster 5/45) and bank interest defaults (V2 0.5%, cap 10). See TRACKER M3 Economy.
8. A custom Balrog sound (needs an audio file).
9. Already open in TRACKER, not repeated here:
   - Invisible players glow (V2 shop classes Q11).
   - Monster price (V2 shop classes Q1).
   - Per-team vs shared Dream (Emerald Dream Q7-13).
   - Generator values (Generators Q1-6).
   - Arena (Arena Q1-8, Arena V2 Q1-9).
   - Main world / map (open question 1, M2/M3 core Q9).
   - Shop catalog prices (open question 4, M2/M3 core Q7).
