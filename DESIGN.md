# Nonios's Map — Remaster Design & Technical Plan

Status: draft v0.1 (2026-10-14). Reference: V2.0 world (Minecraft 1.12.2).
Rule of the remaster: **keep the objective, rethink everything else.**

---

## 0. Platform decision

| Item | Choice | Why |
|---|---|---|
| Game version | **Java 26.3** (released 2026-09-15), pinned | It adds `/posteffect`, which turns on a resource-pack shader for specific players. Per-class shaders depend on it. |
| Data pack format | 121.0 | 26.3 |
| Resource pack format | 97.1 | 26.3 |
| Server | Vanilla server jar (no plugins/mods) | Players join with an unmodified client. The resource pack is pushed by the server (`require-resource-pack=true`). |
| Java | SE 25 | Required by 26.3 |

**Version risk:** 26.4 snapshots make Vulkan the default renderer. The shader pipeline has changed in almost every drop (reversed depth buffer in 26.2, ShaderC compilation and `#include` in 26.3). Pin 26.3, keep all GLSL in one folder, and treat a version bump as a separate task.

---

## 1. Core loop (unchanged objective)

1. Two teams (White / Black). Each owns a **Field**: a base area where it builds, gathers and progresses with normal survival play.
2. Between them is the **Arena**, where both teams contest resources.
3. Each team has a **Nexus** (obsidian). **Destroying the enemy Nexus is the end-game trigger.**
4. After its Nexus falls, a team has no respawns left. When its last player dies, the other team wins.

Suggested match phases (to be confirmed):

| Phase | What happens |
|---|---|
| Lobby | Admin configures the match; players pick a team and class |
| Preparation | Fields are sealed off by a barrier. Teams gather, build and upgrade. |
| Battle | Barrier drops ("Barriers Broken"). The Arena opens. |
| Sudden death (optional) | After X minutes Nexuses weaken or the Arena shrinks, so matches don't stall |
| End | VICTORY / DEFEAT titles, stats screen, reset |

---

## 2. System map

Each system lists what it must do, how the original built it, and the new approach.

### 2.1 Match lifecycle & lobby
- **Must:** configure the match, let players join teams and pick classes, start, detect the end, show results and reset.
- **Original:** admin clicks chat `tellraw` links that set scoreboard flags, polled by command-block clocks. The player count was entered by hand.
- **New:**
  - The game state is one value (`#state game` = lobby/prep/battle/end). One `tick` function branches on it, so only the current phase's logic runs.
  - The admin opens a **dialog** (native modal UI, available since 1.21.6) with sliders and toggles for prep time, starting coins, lightning, sudden death and similar settings. Values are applied with `dynamic/run_command`, and the settings live in `data storage nonios:config`.
  - Players pick their team and class through a dialog too, using `/trigger`, which works for non-op players.
  - Player count is computed automatically instead of being typed in.

### 2.2 World layout & map reset
- **Must:** Field ×2, Arena, Lobby, and possibly an Emerald Dream area. The map must reset cleanly between matches.
- **New:**
  - All zone coordinates live in one config function, so the map can be rebuilt without editing logic.
  - Zones are detected with `execute if entity @s[x=..,dx=..]` volumes or predicates. Marker entities are only used where something needs a moving anchor.
  - **Reset:** for v1, keep a pristine copy of the world and restart the server per match. This is the simplest option and has no size limits. Later, a structure-template reset could rebuild in place (templates can be large if they are generated externally).
  - **Emerald Dream** can be a **custom dimension** (`dimension` + `dimension_type` in the data pack). That separates it cleanly and allows its own sky, fog and light. Travel uses `execute in nonios:emerald_dream run tp`.

### 2.3 Nexus & end condition
- **Must:** the end-game trigger.
- **Original:** `testforblock` on the obsidian position, then titles and a "last life" message.
- **New:**
  - Each tick, run `execute unless block <pos> minecraft:obsidian` on each Nexus. Two checks per tick cost almost nothing.
  - The breaker is identified with a `minecraft.mined:minecraft.obsidian` score. If a teammate breaks their own Nexus, the block is restored.
  - **Design option (needs a decision):** Nexus **HP**. Each break removes 1 HP and the block regrows; at 0 the Nexus is destroyed. This makes sieges a real phase instead of one lucky break. A per-team **bossbar** shows HP and works as the main HUD element.
  - When a Nexus is destroyed: title, sound and shader pulse for everyone, and that team's `lives` mode switches to "last life".
  - Win check: when a team has no `gamemode=survival` players left (an event check on each death, not a constant poll), the other team wins. Then the stats screen is shown and the match resets.

### 2.4 Death, respawn & lives
- **New:** set game rules `immediate_respawn` and `keep_inventory false` (rule names are snake_case since 1.21.11). Death is detected with a `deathCount` score. Each team gets its own spawnpoint.
  - Before the Nexus falls: respawn in the Field with the team's **respawn kit** (see 2.8).
  - After the Nexus falls: switch to spectator. Spectators get the `nonios:ghost` post effect (desaturated).
  - Class powers are lost on death, as in the original. Whether the class itself is kept is a design question.

### 2.5 Economy (currency)
- **Original:** emeralds were converted to `Coins` (emerald = 1, emerald block = 20) through a round-robin "turn" system, because 1.12 selectors couldn't handle it in one pass. Carrying coins caused slowness.
- **New:**
  - **Coins are a scoreboard currency.** Raw emeralds are the physical resource.
  - Conversion is one command per player: `execute store result score @s coins_in run clear @s emerald` (clear returns the count), triggered by an `inventory_changed` advancement, so it only runs when the inventory changes. The turn system disappears.
  - The **coin weight penalty** is kept but made smooth: a `movement_speed` attribute modifier whose amount is computed from coins carried (a macro function passes the value). The threshold can scale with match time, as before.
  - **HUD:** actionbar coin counter with a custom font glyph for the coin icon.

### 2.6 Bank
- **Original:** deposit and withdraw signs for 10, 100 or 1000 coins. Shared team bank with periodic interest.
- **New:** a bank **dialog**, opened by an interaction entity at the bank. It uses a `number_range` slider ("Deposit [——●——] 340") plus deposit and withdraw buttons, with `dynamic/run_command` sending `/trigger bank set <n>`. Interest runs on `schedule function` (for example every 60 s).
  - Why bank: coins carried are dropped to the killer on death; banked coins are safe. This keeps the original risk/reward.

### 2.7 Kill rewards
- **Original:** the killer took the victim's coins, plus 10 coins and a tier bonus (+20/+90/+190).
- **New:** a `player_killed_entity` advancement runs a reward function with the killer as `@s`. The victim is found through their `deathCount` change in the same tick. Bounty grows with the victim's tier or class, and with their killstreak (new). Event-driven, no polling.

### 2.8 Team progression (the Field)
- **Must:** "build and progress natively" within your own Field.
- **Original:** the team kit upgrades were chest offerings (8/8/2, 16/16/8, 64/64/64 iron/gold/diamond blocks). They gave better respawn armor, weapons and tools.
- **New:** a **Team Altar** with an upgrade tree, opened as a dialog that shows `item` bodies for each cost. Materials are paid from the player's inventory with `clear` (it returns the count), so no chest scanning. Suggested branches:
  - **Respawn kit** tiers I–III (as in the original)
  - **Generators** level 1–3 (see 2.9)
  - **Nexus** fortification: armor/HP, a regeneration aura, and a defender's mark on enemies who come near (the original Guardian/House/Deep zones)
  - **Team buffs:** Haste and other cheap passives
  - **Emerald Dream** access (unlock 1000 coins, as in the original)
- The visual for each upgrade is a structure template placed with `/place template` (the original already had `white_generator_lvl1..3` structures).

### 2.9 Resource generators
- **Original:** every tick, two droppers were replaced and fired to roll 1 of 81 outcomes, and the dropped items were detected and turned into a score. It was very laggy.
- **New:**
  - Each generator is a **marker entity** with a `level` score and a timer.
  - A `schedule function` loop (no per-tick cost) runs `loot spawn <pos> loot nonios:generator/<team>_lvl<N>`. **Loot tables** provide weighted entries, `random_chance` conditions and count ranges, so drop probabilities are real data instead of dropper hacks.
  - Visuals: an `item_display` spinning core and a `text_display` hologram ("Lv 2 · next drop 4s"). Both are display entities with no hitbox and no ticking AI.
  - Upgrades swap the loot table, the interval and the structure.

### 2.10 Arena (contested resources)
- **Original:** a central area and the Emerald Dream portals.
- **New (proposal):**
  - **Contested nodes:** high-tier generators in the Arena that drop only to whoever holds the zone (capture by standing in it, with a progress bossbar).
  - **Timed events:** for example "Emerald Surge" every 5 min (a burst of loot at a random node, announced with a title and sound).
  - **Regenerating ore veins** (as in Emerald Dream): marker entities pick a block from a weighted list with `random value` and the block regrows after N seconds.
  - Lightning strikes are a config toggle (as in the original).

### 2.11 Shop
- **Original:** about 200 command blocks on a clock, each polling `WhiteShop=<id>`, then a cost check, a give and a reset.
- **New:**
  - The shop is a **dialog** (`multi_action`) per category: Blocks, Ores, Food, Tools, Utility, Enchanting, Ammo, Special, Kits. Each button shows its price, and the dialog `item` body can show the item icon.
  - Each button runs `/trigger shop set <id>`. One tick check (`execute as @a[scores={shop=1..}]`) calls a **single macro function** `shop:buy`. It reads `price` from `storage nonios:catalog`, checks coins, subtracts, gives the item with `loot give @s loot nonios:shop/<id>` (so items can carry any components), plays a sound and re-enables the trigger.
  - The whole catalog lives in **one data file** (see §4). Dialogs, loot tables and the storage catalog are **generated** from it. Adding an item means adding one line.
  - The Shop Keeper is a **mannequin** (player-like NPC entity, 1.21.9+) with a custom skin and an **interaction** entity hitbox that opens the dialog. The keeper's personality comes back in the dialog text (the Cracy Frog confirmation chain is a nice easter egg to keep).

### 2.12 Classes / kits — the main upgrade
- **Original:** helmet-tag checks on a clock, `effect` re-applied every tick, a few NBT items. Limited, and every class cost about 10 command blocks.
- **New:** a **class framework**. Each class is a data entry with these slots:

| Slot | Mechanism (26.3 vanilla) |
|---|---|
| Equipment & custom items | Item components (`item_model`, `attribute_modifiers`, `equippable`, `weapon`, `tool`, `damage_resistant`, `death_protection`, `glider`, `use_cooldown`, attack/interact animation…) and a resource pack model per item |
| Passive | **Custom enchantments** on class items, using the `tick` effect (runs every tick while equipped), `attributes`, `damage_immunity` and `damage_protection`. Applied by the engine without a polling clock. |
| On-hit mechanics | Enchantment `post_attack` → `run_function`, `apply_mob_effect`, `damage_entity`, `explode`, `apply_impulse` (lifesteal, cleave, knock-up, mark…) |
| Active ability (right-click) | Item with `consumable` + a `using_item` advancement → ability function. `use_cooldown` shows the vanilla cooldown sweep on the hotbar. |
| Movement abilities | `apply_impulse` (dash, leap), player `input` predicates (double jump, sneak combos) |
| Vision / feel | **`/posteffect add @s nonios:<class>`**: a per-player full-screen shader. Re-applied on respawn, removed on death or class change. |
| Audio / particles | Custom `sounds.json` entries (the Balrog roar is back), particles at the player |
| Model / look | Custom armor textures (`equippable.asset_id`) and item models; no more player-head workarounds |

Class roster from the original, with first-pass concepts (all open for redesign):

| Class | Concept | Shader idea |
|---|---|---|
| **Reaper** | Scythe: lifesteal on hit, short invisibility after a kill, souls stack into a burst | **Black-and-white + edge outlines** (Sobel on depth): "sees all" |
| **Cracy Frog** | Magic Broom flight (levitation pulses), huge jumps, chaos/knockback items | **Acid**: hue cycling, UV wobble, chromatic split |
| **Balrog** | Fire whip (ignite + pull), lava immunity, wither aura, levitation leap | Heat haze, red/orange grade, ember vignette |
| **Monster** | Devour: kills grant regeneration, strength and speed; claws weapon | Pulsing red vignette while Devour is active |
| **Berserker** | Battle axe; strips armor for strength and speed; rage at low HP | Screen shake / red edges when raging |
| **Ninja** | Fragile but very fast, wall-run / dash, smoke bomb | Speed lines at sprint |
| **Emerald Talisman** | Economy class: passive coin income, better generator luck | Subtle green sparkle overlay |
| Paladin, Death Knight, Destroyer, Titan, Archer, Miner, Tank, Warrior | Retained as names from the V2 signs. Need concepts. | — |

### 2.13 Shaders (resource pack)
- Post effects go in `assets/nonios/post_effect/*.json` (passes, render targets, uniforms) with GLSL in `assets/nonios/shaders/post/`.
- `/posteffect add|remove|clear <players> <id>` (permission 2, which functions have) applies them per player, and several can stack.
- **Unknowns to test first (spike):** does a post effect survive death, respawn and relog? How is time passed in (for animation)? How are depth and main color sampled under the 26.3 compile pipeline?
- Cheap fallback with no post effect: `equippable.camera_overlay` (a full-screen texture overlay drawn while wearing an item, like the pumpkin blur).

### 2.14 HUD & UI
- **Bossbars:** Nexus HP for each team, capture progress, phase timer.
- **Actionbar:** coins and ability cooldown text with custom font glyphs (icons drawn from the resource pack font).
- **Sidebar:** team scores with `numberformat` styling.
- **Dialogs:** shop, bank, altar, class picker, admin config.
- **Titles:** phase changes, Nexus destroyed, victory.

### 2.15 Admin & debug
- `function nonios:admin/...` entry points (start, stop, skip phase, give coins, set class).
- A debug toggle prints state to ops only.
- Lightning, resource-pack test and config live in the admin dialog.

---

## 3. Engineering principles

- **No world-bound logic:** no command blocks and no redstone. Everything lives in the data pack.
- **Event-driven first:** advancements (`using_item`, `player_killed_entity`, `inventory_changed`, `player_hurt_entity`), enchantment effects and `schedule`. Per-tick work is limited to a few cheap checks gated by `#state`.
- **Data-driven content:** shop items, classes, generators and upgrades are defined in source data and generated into the pack.
- **Selectors:** tag the players and entities involved; avoid bare `@e` scans. Use markers and display entities instead of armor stands.
- **Namespacing:** everything under `nonios:`. Scoreboards are prefixed `nx.` to avoid clashes.

---

## 4. Tooling & project layout

```
Remaster/
  DESIGN.md
  src/                    # source of truth (human-edited)
    shop.yaml             # catalog: id, category, price, item components
    classes.yaml          # class definitions
    generators.yaml       # loot weights per level
  build.py                # generates dialogs, loot tables, storage init, item defs
  datapack/               # data/nonios/{function,advancement,loot_table,dialog,enchantment,predicate,dimension,...}
  resourcepack/           # assets/nonios/{items,models,textures,post_effect,shaders,sounds,font}
  server/                 # local 26.3 test server (git-ignored world)
```

- **Generator:** a small Python script (Python 3.13 is already installed) turns the YAML into JSON and mcfunction files. Beet/Bolt is an alternative if we outgrow the script.
- **Editor:** VS Code + Spyglass (datapack language server) to validate commands against 26.3.
- **Testing:** local 26.3 server and `/reload`. Data-driven **GameTest** test instances (`/test`) for regression checks of the economy and shop. Shaders are checked by eye in the client.
- **Version control:** git repository in `Remaster/`.

---

## 5. Milestones

| # | Goal | Done when |
|---|---|---|
| M0 | Toolchain | 26.3 server runs; empty data pack + resource pack load; build script works |
| M1 | **Spikes** | `/posteffect` with a grayscale and an acid shader on one player; a shop dialog that buys one item; a loot-table generator |
| M2 | Playable core | Teams, phases, Nexus, respawn/lives, win screen, reset |
| M3 | Economy | Coins, conversion, weight penalty, bank, kill rewards, full shop |
| M4 | Progression & Arena | Altar upgrades, generators, Arena nodes and events, Emerald Dream |
| M5 | Classes | Framework + Reaper and Cracy Frog end-to-end (items, abilities, shaders), then the rest |
| M6 | Map & polish | Final build, sounds, textures, balance, playtests |

---

## 6. Design decisions (user, 2026-10-14) — these override earlier sections where they conflict

1. **Nexus = Barrier + Obsidian.** The obsidian block is the final target (mine it to win/eliminate). It is protected by a
   **Barrier** with HP shown as a team **bossbar** (visible to the defending team — warns of infiltration). While the barrier
   is up the obsidian can't be mined. Barrier regenerates **~20% per minute** unless fully destroyed (then stays down).
   Purpose: sneaking in with few players is not an instant win.
2. **Scale:** no hard player cap (no per-player command blocks). Design target up to **20 per team**; typical games **2v2–5v5**.
   Field size / generators must scale with team size.
3. **Classes, two tiers:**
   - *Basic classes*: selectable, given/applied on respawn; upgraded team-wide (the old "offering" upgrades).
   - *Shop classes*: the "juice". One-time use, heavily customised mechanics, strengths + weaknesses; often lock armour
     (curse of binding) and require their custom tool. Lost on death.
4. **Coins:** keep the risk economy — carrying coins slows you; dying gives **everything carried to the killer**; bank is the safe.
   Drop the "emeralds cleared from inventory" proxy. Proposal (Claude): coins are a scoreboard purse fed directly
   (ore mined → `minecraft.mined` stat → coins; generators collected by right-clicking them; arena events) — no item juggling.
   - *Tentative (to detail later)*: keepInventory on (gear kept), but on death the purse goes to the killer + kill reward;
     respawn equipment reduced/removed accordingly. Must be reconciled with basic-class respawn kits (point 3).
5. **Emerald Dream = custom dimension**, regenerated each time (or random arrival point). Exit by **sneaking for X seconds**
   (risky channel). Room for lots of extra juice.
6. **Map:** brand-new build (with tooling), not the V2 terrain.
7. **Keep legacy humour & lore** (Shop Keeper lines, Nonios's Weakness, Satan's Blade, Cracy Frog…) — sells the "remaster".

---

Sources consulted (2026-10-14): [Java Edition 26.3](https://minecraft.wiki/w/Java_Edition_26.3), [/posteffect](https://minecraft.wiki/w/Commands/posteffect), [Shader](https://minecraft.wiki/w/Shader), [Dialog](https://minecraft.wiki/w/Dialog), [Mannequin](https://minecraft.wiki/w/Mannequin), [Enchantment definition](https://minecraft.wiki/w/Enchantment_definition), [Game rule](https://minecraft.wiki/w/Game_rule), [Datapack Wiki: right-click via consumable](https://datapack.wiki/guide/right-click/consumable_component), [26.4 Snapshot 1: Vulkan default](https://www.minecraft.net/en-us/article/minecraft-26-4-snapshot-1).
