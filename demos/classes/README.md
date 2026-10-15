# classes

Class framework (DESIGN 2.12, 6.3) with the first two shop classes, Reaper and Cracy Frog, plus a placeholder basic class
(Warrior = the V2 "automatic kits") to exercise the respawn path. G -> "Demo: Classes"; all buttons are `trigger demo.cls set N`.
The demo is survival with keep_inventory + immediate respawn, a walled 40x40 yard, and plays M2's part for deaths (`demo.died`).

## Data-driven
`src/classes.json` -> `python tools/build_classes.py` writes (all regenerated, never edit):
- `loot_table/class/<class>/[l<N>/]<item>.json`: one item each. Adds `custom_data {nx_cls, nx_item, nx_cls_item}`, curse of vanishing
  (class items never drop), binding on shop-class armour, unbreakable, name/lore + a "lost on death" footer.
- `enchantment/class/<key>.json`: the class passives (dynamic registry: restart the server after changes).
- `advancement/class/use/<class>_<item>.json`: right-click on items with a `consumable` component. Short consume time =
  `consume_item` (fires when the use completes; the item is used up and re-given next tick, and that completed use is what
  applies `use_cooldown`). consume_seconds >= 60 = `using_item` (every tick while held, e.g. the broom).
- `function/class/gen/**`: per class `apply`, `equip[_l<N>]`, `strip`, `vision[_off]`, `check` + `need_<item>` (shop kits stay complete),
  dispatchers on `nx.class` (`apply` uses `nx.cls_req`), `purge` (class items of a class you don't have vanish), `is_shop`, `lost`, `catalog`
  (storage `nonios:class catalog`: id, num, tier, price, name, blurb for the shop UI).

## API (as/at the player)
- `nonios:class/set {num:N}` / `nonios:class/set_id {id:"reaper"}`: become that class (strips the current one; old armour comes back).
- `nonios:class/remove`: no class, forgets the basic class.
- `nonios:class/on_death` (hook for M2's death handling) then `nonios:class/on_respawn` (hook for `#nonios:kit/respawn`).
- Team level for basic classes: `#white` / `#black` / `#solo nx.cls_lvl` (1-3).
- Cracy Frog purchase = `trigger nx.cls_ask set 1` (V2 confirmation chain, dialogs `nonios:class/frog_ask_1..3`).

## Classes
| class | V2 | remaster |
|---|---|---|
| Reaper (shop, 200) | Possessed Pumpkin (-14 max HP, +15 armour, binding), Reaper's Scyce (iron hoe, +10 dmg, fire aspect 10), permanent invisibility + speed II with the scythe, 3 s resistance V and the wither sound on a kill | pumpkin (-10 HP, +6 armour, proj. prot IV), invisible shroud, Scyce: 9 dmg, slow, +0.75 reach, +20% speed and 50% knockback resistance in hand, fire aspect I, 2-heart lifesteal per swing; hit = Slowness I 3 s; kill = soul (max 5) + 4 s invisibility (head and scythe models hidden) + 8 s Resistance V (no refresh while active) + wither sound; scythe glints when charged, right-click = souls burst (2+2/soul + wither, 6 blocks, allies spared, 8 s cd), never consumed (two-state consumable, "No souls" when empty); flight: gravity P-controller, Space rises / Shift sinks / hover, rising only within 10 blocks of ground, no fall damage; vision `nonios:reaper` |
| Cracy Frog (shop, FREE behind 3 "are you sure?") | frog head (+10% speed, thorns), Frog Skin leather, Frog Spring boots (feather falling), Magic Broom (levitation V while holding it high up) | same look; Frog Legs boots enchantment (+0.42 jump strength, +12 safe fall); Magic Broom = hold right-click: levitation by pitch + forward `apply_impulse` every 6 ticks, 3 s fuel refilled on the ground; Frog Tongue: random chaos on hit, RIBBIT wind bursts on right-click (6 s cd); vision rainbow + acid |
| Warrior (basic, placeholder) | team "automatic kits" I/II/III | chainmail / iron + shield / diamond + Gardna's Shield, re-applied on respawn |

Shaders `nonios:reaper`, `nonios:rainbow`, `nonios:acid` are copied from spike/shaders with identical paths.
