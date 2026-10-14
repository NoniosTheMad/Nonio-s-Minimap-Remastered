# TRACKER · Nonios's Map Remastered

## Objective
Remaster the Nonios's Map game (Java 26.3 vanilla) with datapack, resource pack, and `/posteffect` shaders. Two teams, own fields, contested arena, destroy enemy Nexus to win. No mods.

## Milestones
| Stage | Status | Meaning |
|-------|--------|---------|
| M0 | ✓ Done | Dev framework (mcdev.py, persistent servers, feedback, packing) |
| M1 | ✓ Done | Spikes: `/posteffect` shaders, Nexus barrier, shop dialog, coin purse (awaiting user tests) |
| M2 | ★ Your test | Playable core: teams, phases, respawn, win screen, reset (built, merged to main) |
| M3 | → Now | Economy: bank dialog, interest, kill rewards (in progress) |
| M4 | — | Progression: altar upgrades, generators, arena events, Emerald Dream |
| M5 | — | Classes: Reaper and Cracy Frog end-to-end, then roster |
| M6 | — | Map & polish: new build, sounds, textures, balance, playtests |

## Current focus
M3 economy (in progress). M4 integration: merge generators + Emerald Dream + arena into main (loot table format fix in progress). Testing M2 + arena. Parallel: Classes end-to-end.

## Waiting on user
1. **M2 playable core (★):** server `m2` (solo test w/ dummies). Join: G → Demo: M2 playable core (first-time chooser). Steps: pick team → start match → kill the dummies → destroy enemy Nexus. Check: all phases (prep/battle/end), respawn, spectator on last life, stats, placeholder map reset on return to lobby.
2. **Arena (★):** server `arena`. G → Demo. Capture nodes (10 s alone, faster with 3+ team-mates). Watch contested freeze, payouts, weighted events (Emerald Surge, Cracy Frog jackpot, Golden Hour), Lightning Rabbit toggle. Check node captures, bossbar inside node, payouts every 30 s.
3. **Shaders v2 (★):** server `shaders`. Refresh pack (G → Refresh resource pack), then G → Demo: custom shaders. Check: god-ray direction, thermal colours, Cosmic at Midnight, Monster darkness.
4. **Nexus barrier (★):** server `nexus`. Read cracks 10–20 blocks (vanilla textures). Check hit actionbar text.
5. **Shop dialog (★):** server `shop`. Try buying. Check NPC, catalog, trigger buttons, not-enough-coins message.

## Promised
- Shader spikes v2 (combinable layers, 4 looks: Cinematic/Thermal/Cosmic/Monster, presets, time-of-day, materials gallery, landscape) — done (c65d643)
- Nexus barrier v3 (vanilla destroy_stage cracks, 20% regen/min, no HP numbers, defenders-only bossbar) — done (658e2d2)
- Shop dialog spike (data-driven catalog, trigger buttons, NPC, not-enough-coins) — done (f8fa3f8)
- Coin purse spike (mining → coins, weight slowdown, killer takes purse, bank stub, anti-silk-touch) — done (3f09c2c)
- In-game inbox (G → Inbox, chat notifications, chat = feedback grouped, persistent "recent" replay) — done (f6fdfb8)
- Text-box feedback dialog (topic + multiline, log4j2 route, ✔ noted) — done (f9d3229)
- Roadmap kept current (docs/roadmap.html) — synced with this file
- Quiet session (only checkpoints) — established
- Generators spike (V2.0 level structure reuse via `/place template`, coin pot, data-driven via src/generators.json, loot table from V2's 81-outcome dispenser odds) — done (855e046)
- Emerald Dream spike (custom dimension with floating islands, random arrivals ±3000, 10 regrowing veins, 5 s sneak-exit, saved return point, V2 lore recovered) — done (6729ef0)
- M2 playable core (feat/m2-core, merged to main 051fbcc): barrier + shop + purse + teams (white/black) + phases (lobby/prep/battle/end) + admin panel + keep_inventory ON + respawn + last life→spectator + win check + stats + placeholder map with reset. Server m2 ★. Awaiting user test.
- Arena spike (f765a48, feat/arena, server arena ★): capture nodes (10 s alone, 3+ team-mates faster; contested frozen), payouts via hook (every 30 s), weighted events (Emerald Surge, Cracy Frog jackpot, Golden Hour, first at 3 min), Lightning Rabbit toggle (V2 return). Awaiting user test.

## In flight
- M3 economy (feat/economy): Bank dialog, interest, kill rewards. In progress.
- Classes (feat/classes): Class framework + Reaper + Cracy Frog end-to-end implementation.
- M4 integration (feat/m4-integration): Merge generators + Emerald Dream + arena into main. Loot table format fix in progress (26.3 incompatible functions→modifiers).

## Decisions
| Date | Decision |
|------|----------|
| 2026-10-14 | Version: **26.3 vanilla** (client + server, no mods). Java 25 portable JRE. |
| 2026-10-14 | Dev framework: `mcdev.py` (hub/main/test persistent; ephemeral demo servers; daemon; `/transfer` nav; feedback Book & Quill + storage devnav:req; `/posteffect` + resource pack). |
| 2026-10-14 | **Nexus** = Barrier (HP bossbar, 20% regen/min default) + Obsidian (final target). Sneaking past barrier = instakill prevention. |
| 2026-10-14 | **Scale:** up to **20 per team**; typical **2v2–5v5**. No per-player command blocks. |
| 2026-10-14 | **Classes:** two tiers — *basic* (selectable, upgraded team-wide) + *shop* (one-time, custom, lost on death). |
| 2026-10-14 | **Coins** = scoreboard purse. No item juggling. On death: everything to killer + kill reward. Bank is safe. Carrying = slowness. |
| 2026-10-14 | **Emerald Dream** = custom dimension. Exit by sneaking X seconds (risky channel). Regenerated/random spawn each visit. |
| 2026-10-14 | **Map:** brand-new build (not V2 terrain). Tooling-driven. Legacy humour & lore kept. |
| 2026-10-14 | **Feedback queue:** not interrupts. Batch at checkpoints; act; `mcdev feedback --ack`. No live monitors. |
| 2026-10-14 | **Roadmap (docs/roadmap.html):** user's single overview. Published; kept in sync. Frame messages: Done / Waiting on you / Next. |
| 2026-10-14 | **Dialog op-command confirmation:** Op-level commands in `run_command` buttons prompt the player. Always use `/trigger` for non-op actions (permission 0, no prompt). |
| 2026-10-14 | **Status source (lead + user):** TRACKER.md is the single high-level overview. PROGRESS.md → technical notes only (after inbox agent finishes). |
| 2026-10-14 | **User pronouns:** they/them in all docs. |
| 2026-10-14 | **Nexus bossbar:** defenders-only (attackers get no bossbar). Actionbar HP on hit stays (all players). |
| 2026-10-14 | **Shaders: side track.** After v2 + feedback #14, further shader ideas deferred after M2. Classes (M5) may pull specific shaders earlier. Critical path: M1 shop + purse → M2 playable core. |
| 2026-10-14 | **Shop: stays open after buy.** Dialog remains open (user can buy multiple items, close manually). |
| 2026-10-14 | **Shop: NPC at team base only.** Shopkeeper at team spawn/base; safe zone NPC trigger. |
| 2026-10-14 | **Shop: refuses when inventory full.** No drop/split; player gets "inventory full" message; purchase blocked. |
| 2026-10-14 | **Coins: building blocks earn nothing.** Only ore + custom blocks count toward mining rewards. Anti-silk-touch applied. |
| 2026-10-14 | **Coins: first 20 weightless.** Carrying 1–20 coins = no slowness. 21+ applies 0.1%/coin (capped 40%). |
| 2026-10-14 | **Coins: mob/environment deaths drop purse.** Killed by mob/fall/environment = coin-bag on ground for anyone to pick up. Killer gets kill reward separately. |
| 2026-10-14 | **Bank: team-wide.** Single vault per team (not per-player); all team members deposit/withdraw from same pool. Recoverable on death (coins to killer, bank intact). |
| 2026-10-14 | **Actionbar: barrier hit beats coin counter.** On nexus hit, barrier HP text shows on actionbar (coin counter yields). Coin counter resumes when not hitting. |
| 2026-10-14 | **Coin objective & teams:** coin objective = `nx.coins` (scoreboard). Teams: `white` and `black` everywhere (universal naming across branches). |

## Open questions
1. **Main world:** fresh flat or import V2 terrain? Decide before M6 build.
2. **Respawn gear vs keepInventory:** draft idea (user 2026-10-14): keep inventory, but bank + reward to killer. Reconcile with class kits in M2 playable core.
3. **`/posteffect` persistence:** does shader effect survive death, relog, transfer? Critical for class/shop effects in M3+.
4. **Shop catalog:** real catalog (per team/phase?) vs. test data? Decide before M3 economy build.
5. **Quantity picker:** support buying multiple items per dialog (2x Diamond Sword) or single-item only?

## Questions for when user returns
**Arena** (spike done f765a48; from coordinator notes, with suggested defaults):
1. **Capture time:** [suggested: 10 s alone; faster with 3+ team-mates]. How long to capture a node solo vs. with team-mates?
2. **Contested behaviour:** [suggested: freeze]. When both teams are in a node, what happens — frozen, no progress, or other?
3. **Payout interval:** [suggested: every 30 s]. How often are coins/resources awarded for held nodes?
4. **Payout method:** [suggested: loot drops]. Payouts as loot drops (on ground) or to team bank?
5. **Lightning Rabbit:** [suggested: yes, 100 HP]. Bring back V2 Lightning Rabbit mob? Should it have a health cap?
6. **Events schedule:** [suggested: first at 3 min, then every 5 min]. When do weighted events start, then repeat?
7. **Node forceloading:** [suggested: yes]. Should nodes stay loaded even when no players are near? For chunk loading purposes?
8. **Portal + central block:** [suggested: yes, later]. Bring back V2 random-entry arena portals + regrowing central block. When?

**M2/M3 core** (from M2 merge, with built/suggested defaults):
1. **Bank withdrawal mechanic:** How do players withdraw coins? [built: M3 now; dialog pending].
2. **Keep inventory + respawn kit hook:** keep_inventory ON; classes may add custom kits. Hook wired? [to do].
3. **Battle skip = draw:** If a team skips a phase during battle, match ends as draw. Accept? [suggested: yes].
4. **Admin panel access:** Op runs `/function nonios:admin` once. Wires the admin UI. [built].
5. **Late joiners:** Players joining mid-match spectate until they pick a team. Accept? [suggested: yes].
6. **Black team colour:** dark_purple or light_purple for black team? [pick one].
7. **Placeholder shop catalog:** What items + pricing for now? [test data built].
8. **Full inventory edge case:** Refuses purchases even when a matching stack has room? [suggested: yes, strict].
9. **Map regeneration:** Fresh copy pulled at each return to lobby. Accept? [suggested: yes].
10. **Prep phase lockdown:** Barrier plane + 1 Hz pushback keeps teams in base during prep. Physics OK? [built].
11. **Emerald block farm cost:** Placing one costs 100 coins to prevent infinite farms. Accept? [suggested: yes].

**Generators** (spike done 855e046; from coordinator notes, with suggested defaults):
1. **Coins per emerald outcome:** [suggested: 5; block-level 45; Lv3 ≈72 coins/min]. Scales with team size; rolls from V2's 81-outcome dispenser odds.
2. **Drop intervals:** [suggested: 10/8/6 s per level; pot caps 50/150/500]. How often rolls occur; pot size limit per team.
3. **Can enemies collect your pot?** [suggested: yes]. Raid incentive; holders can defend or split coins before enemy raid.
4. **Upgrade costs:** [suggested: V2 values — 200→Lv2, 500→Lv3; later via Team Altar]. How teams level generators; Altar not yet built.
5. **Drops as mined items without fortune:** [suggested: yes]. Generator outcomes count as mined; no fortune multiplier applied.
6. **Generator structure protection + chunk loading:** [noted: not handled yet]. How to prevent/allow breaking structures; which chunks keep them loaded during map reset.

**Emerald Dream** (spike done 6729ef0; from coordinator notes, with suggested defaults):
7. **Dream shared or per-team?** [suggested: shared by both teams, unlike V2]. Same dimension or separate instances?
8. **Void fall = death?** [suggested: yes]. Does falling out of floating islands kill you?
9. **Jump Boost in the Dream?** [suggested: on]. Should players get Jump Boost III in the Dream?
10. **Channel time, regrow, veins count:** [fixed: 5 s sneak to exit, 30 s regrow, 10 per arrival]. Adjustable or keep as-is?
11. **Emerald block value:** [suggested: 100 coins per emerald]. Scales dream farming value relative to generators.
12. **Arrival range:** [suggested: ±3000 blocks]. Smaller for guaranteed team meetings, or larger for separation?
13. **Dream mob danger:** [suggested: endermen + allays]. What creatures make the dream risky vs. just a farm?

(More questions will accumulate from M2 core, Classes, and Arena research.)

## Backlog ideas (deferred, not commitments — shader work paused after M1 v2 + feedback #14, resumes after M2; M5 classes may pull specific shaders earlier)
- **Shader: healer-class vision:** angel-class post effect showing all players' total HP (infrared-like). Hearts >20 glow "as if to burst" (log-scaled).
- **Shader: RTX-like effects:** ref https://www.youtube.com/watch?v=AdTxrggo8e8 (advanced ray tracing style shaders for high-end clients).
- **Shader: real landscape, cosmic, monster class effect:** feedback #14 additions to v2 (deferred post-M2).

## Log (recent ~30 lines)
| Date | Event |
|------|-------|
| 10-14 | **M4 integration started** (feat/m4-integration): Merge generators + Emerald Dream + arena into main. Loot table format fix in progress (26.3 incompatible functions→modifiers). Eight Arena design questions for user (capture time/contested/payouts/drops vs bank/lightning/events/forceload/portals). |
| 10-14 | **Arena spike done** (f765a48, feat/arena, server arena ★): capture nodes (10 s solo, 3+ faster; contested frozen), payouts every 30 s via hook (suggested loot drops), weighted events (Emerald Surge, Cracy Frog jackpot, Golden Hour; first at 3 min then every 5), Lightning Rabbit toggle (V2 return, 100 HP). Eight design questions for user. |
| 10-14 | **M3 economy started** (feat/economy): bank dialog, interest, kill rewards. M2 merged to main, built, awaiting user test. Parallel: Classes, M4 integration. |
| 10-14 | **M2 playable core merged** (051fbcc, feat/m2-core → main): barrier + shop + purse + teams (white/black) + phases (lobby/prep/battle/end) + admin panel (/function nonios:admin) + keep_inventory ON + respawn + last life→spectator + win check + stats + placeholder map with reset. Server m2 ★. Awaiting user test. 11 design questions. |
| 10-14 | **Emerald Dream spike done** (6729ef0, feat/emerald-dream, server dream ★): custom dimension with floating islands, random arrivals ±3000, 10 regrowing veins, 5 s sneak-exit, saved return point. V2 lore recovered (Shop Keeper, Emerald Talisman, Crazy Frog chain). Seven design questions for user (shared/void/jump/regrow/value/range/mobs). |
| 10-14 | **Classes started** (feat/classes): class framework + Reaper + Cracy Frog end-to-end. M5 milestone now in progress; spikes ongoing (M2 core, Arena). |
| 10-14 | **Generators spike done** (855e046, feat/generators, server gens ★): V2 level structure reuse via `/place template`, emerald outcomes → coin pot (right-click collect), rolls scale team size, data-driven via src/generators.json, loot from V2's 81-outcome dispenser. Six design questions for user (coins/drops/raids/costs/fortune/protection). |
| 10-14 | **Coin objective + teams decided:** `nx.coins` scoreboard, teams `white`/`black` universal across branches. |
| 10-14 | **M2 core started** (feat/m2-core): merging M1 spikes into main; teams/phases/respawn/win logic; placeholder map. Parallel: Generators (feat/generators, resource structures) and Emerald Dream (feat/emerald-dream, dimension spike). |
| 10-14 | **All M1 shop + purse design questions approved** (user via coordinator): Shop stays open, NPC at base, refuses when full. Coins: blocks earn nothing, first 20 weightless, mob deaths drop purse. Bank: team-wide. Actionbar: barrier > coin counter. Added to Decisions table. |
| 10-14 | **M1 spikes complete.** All built and awaiting user tests (shaders, nexus, shop, purse, text-box feedback). **MERGE NOTE:** shop, nexus-barrier, and purse all modify tick.json/load.json (conflicts on merge to main). Proposed next: user tests, then plan M2 playable core. |
| 10-14 | Coin purse spike done (3f09c2c, feat/coin-purse, server purse ★): per-block mining values (anti-silk-touch), weight 0.1%/coin (capped 40%), killer takes purse, coin-bag drop for non-player deaths, bank stub. User tests. |
| 10-14 | Shop dialog spike done (f8fa3f8, feat/shop-dialog, server shop ★): data-driven catalog, trigger buttons, NPC shopkeeper, not-enough-coins message, G → Shop. User tests. |
| 10-14 | Shop dialog spike (feat/shop-dialog) and Coin purse spike (feat/coin-purse) started in parallel. Critical path M1. |
| 10-14 | Shaders: side track decision. After v2 + feedback #14, deferred after M2 (M5 classes may pull specific shaders earlier). Feedback #14: split acid (wave/rainbow), stackable, drop Reaper (no-depth), landscape/cosmic/monster added. |
| 10-14 | Barrier v3 done (658e2d2): vanilla destroy_stage crack textures, HP numbers removed from hit messages, dialog shows regen 20%/min. User tests crack readability 10–20 blocks, hit actionbar. |
| 10-14 | Idle sleep + wake-on-select done (589fd46): non-hub servers sleep 10 min empty; G → Servers shows dimmed "(asleep, ~10s)"; click to wake. |
| 10-14 | Console windows fixed: all child processes windowless (no popups). |
| 10-14 | Shaders v2 started: time-of-day buttons, materials gallery, cinematic (RTX-feel), thermal (angel-vision prototype), +1. User #12. |
| 10-14 | Text-box feedback dialog done (f9d3229, log4j2 route): topic + multiline (4000 chars), Send → "✔ noted (#N)". User tests with quotes/accents. |
| 10-14 | Nexus barrier regen: changed from ~5% to **20% per minute** default (user #11). |
| 10-14 | Nexus barrier v2 done (279d8ce): 4 crack stages (75/50/25%), red tint + shrink, flicker when low, shards on hit, defenders-only bossbar, actionbar HP. User tests readability 10–20 blocks. |
| 10-14 | In-game inbox done (f6fdfb8): G → Inbox, chat notifications, chat = feedback (grouped), persistent "recent" thread replay on join, mcdev notify/feedback --resolve, instructions in G → "What to try here". |
| 10-14 | Nexus barrier visuals done (4fe02ed): forcefield texture (team-tinted), hit flash/pulse, crack stages (50%/25%), shatter on break, rate-limited actionbar. Awaiting user texture check. |
| 10-14 | Feedback = Book & Quill (G menu → Feedback): any length, signed, context (branch@commit, pos, server log, client chat) captured. |
| 10-14 | G menu: ★ marks servers waiting for review; "Reset this server" (ephemeral/test) wipes world, restarts, sends back. |
| 10-14 | Demo trigger bug (reset @a after enable) fixed; check_server linter on start checks for it. |
| 10-14 | M0 complete: hub :25565 (lobby, void) + main :25566 (the map) both running; user validated join, G menu, travel, refresh pack. |
| 10-14 | `spike/shaders` deployed: posteffect-probe spike done; custom shaders (Reaper depth+luma, Acid hue/UV) live, awaiting user test. |
| 10-14 | `feat/nexus-barrier`: Spawn/regen (~5%/min) verified via RCON; hit detection (interaction on attacker) coded, awaiting user test/visuals. |
| 10-14 | Framework work on main: in-game inbox plumbed (devnav:fb storage); chat (feedback book) integrated; instructions moved to G → "What to try here". |
| 10-14 | Dev protocol agreed: one main channel (lead owns design/merges); spikes in worktrees; feedback queue; quiet monitoring (only new feedback + crashes); batch at checkpoints. |

