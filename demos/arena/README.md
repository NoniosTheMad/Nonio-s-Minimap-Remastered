# arena

Arena systems (DESIGN 2.10) on top of the game code in `datapack/data/nonios/function/arena/`.
G -> "Demo: Arena": switch my team, spawn enemy dummy (nearest node), remove dummies, random event, each event,
toggle lightning, speed x10 / x1, payouts drop / bank, status, reset. All buttons are `trigger demo.arena set N`.

Layout: 41x41 floor at y=63 around spawn, low wall. Nodes (5x5 zone, 3 high): West (-11,64,-3), North (0,64,-13),
East (11,64,-3). Under each centre: indicator glass on a beacon on 3x3 iron, so the beam shows the owner.
The demo overrides the node list, arena box and centre from `#nonios:arena/config` (`demo:arena_config`),
the same way the real map will plug in.

## How it works (game code)
- **Config:** `nonios:arena/config` writes everything to `storage nonios:arena config` (capture speed, payout,
  loot, nodes, arena box, events, lightning). It runs on every load, followed by the `#nonios:arena/config` tag for overrides.
  `function nonios:arena/setup` rebuilds the nodes from it; `start` / `stop` / `reset` control the loop.
- **Loop:** `nonios:arena/loop` reschedules itself every 10 ticks. Nothing runs per tick. Per node and loop: four
  box-bounded entity counts (`@a[x,dx,team=..]` + non-player `nx.captor` entities), one `bossbar set players`, score maths.
  Holograms and particles update once a second. Timers (payout, events, lightning) advance by 10 x `#speed nx.arena`.
- **Capture:** progress `nx.ar_cap` from -100 (Black) to +100 (White). Only one team inside: +-5 per check per capturer,
  counting up to 3 capturers (10 s alone, 3.3 s with 3+). Both inside: contested, frozen. Empty: drifts 2 per check back to
  the owner's full value, or toward 0. A held node drained to 0 turns neutral, then the other team can take it.
  Players count only on team white/black and not in spectator; mobs count with tag `nx.captor` and a team.
- **Bossbar** `nonios:arena/<id>`, shown only to players inside: colour = progress sign (white / purple), red when contested;
  the name says the state. **Hologram** above the node: name in owner colour, state + %, next payout.
  **Indicator** block (config `blocks`, default yellow / white / purple / red stained glass) at the centre floor block.
- **Payout:** a held node pays every 600 ticks. `storage nonios:arena payout = {team,node,name,loot,rolls,coins}`, then
  `#nonios:arena/on_node_payout` runs as + at the node. If no handler sets `#handled nx.arena 1`, `loot` spawns at the node
  `rolls` times. Rolls = 1 + (team size - 1) / 4 (20 players: 5), x2 during Golden Hour. Drops wait while 24+ item stacks
  lie within 3 blocks. The demo's "bank" mode is such a handler (`demo:bank_hook`).
- **Events:** `config.events` is a list of `{id,name,color,sub,at,sound,weight,fn}`; the timer (first after 3 min, then
  every 5 min) picks one by weight, picks a random node if `at:1b`, shows title + subtitle + sound + chat line, runs `fn`
  as + at that node. Adding an event = one `append` line in the config + its function.
  - *Emerald Surge* (weight 3): 8 waves of emeralds flung out of the node.
  - *It's Raining Frogs* (weight 2): 10 frogs with slow falling and emeralds inside (`DeathLootTable`), plus the glowing
    **Cracy Frog** (emerald blocks, golden carrots, 25% enchanted golden apple, "Cracy Frog's Lucky Spit"). Leftovers vanish after 60 s.
  - *Golden Hour* (weight 1, global): held nodes pay double for 60 s.
- **Lightning** (`lightning/on|off|toggle`, remembered across reloads): the V2 Lightning Rabbit. A glowing, burning,
  fast rabbit (100 HP, Regeneration V, fire resistance) spawns at the arena centre with a bolt and calls a bolt on itself
  every 60 ticks. If it leaves the arena box it is teleported back. Kill it for emeralds and a "Charred Rabbit's Foot";
  it comes back 30 s later.
- **Hooks:** `#nonios:arena/config`, `#nonios:arena/on_node_payout`, `#nonios:arena/on_capture`
  (`storage nonios:arena cap = {team,node,name}`, team "" when neutralised).

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
