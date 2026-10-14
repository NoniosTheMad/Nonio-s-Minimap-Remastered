# TRACKER · Nonios's Map Remastered

## Objective
Remaster the Nonios's Map game (Java 26.3 vanilla) with datapack, resource pack, and `/posteffect` shaders. Two teams, own fields, contested arena, destroy enemy Nexus to win. No mods.

## Milestones
| Stage | Status | Meaning |
|-------|--------|---------|
| M0 | ✓ Done | Dev framework (mcdev.py, persistent servers, feedback, packing) |
| M1 | ✓ Done | Spikes: `/posteffect` shaders, Nexus barrier, shop dialog, coin purse (awaiting user tests) |
| M2 | ★ Your test | Playable core: teams, phases, respawn, win screen, reset (built, merged to main) |
| M3 | ★ Your test | Economy: bank dialog, interest, kill rewards (built, merged to main) |
| M4 | ✓ Done | Progression: generators, Emerald Dream, arena (merged to main 28e83b7); demo server m4 ★ |
| M5 | ✓ Done | Classes: Reaper (200 coins) and Cracy Frog (free) merged to main (5850661); demo server m5 ★; V2 classes roster in progress |
| M6 | → Now | Map & polish: new build, sounds, textures, balance, playtests |

## Current focus
M6 map & polish: Smoke test of main passes (server "full" deployed, be19d2d end bossbar fix). V2 gap inventory documented (docs/v2-gap-inventory.md, 3ef3cfe). Dev-tool fixes (#26 Servers menu labels/tooltip, #27 void spawn + respawn_radius=0, ec18b7c) — **user must restart mcdev daemon**. V2 shop catalog merged (31f59f2, 84 items, V2 prices, enchant-in-hand, named items, shopkeeper lines, server shop2 ★). Team v2 merged (4994386, altar, spawn defense, Emerald Talisman, Lightning Rabbit, recipes, underground walls, server team2 ★). Shaders round 4 merged (306f9f0, Acid reset fixed, Planet + Tiny Planet, Angel rebuilt, Fluorescent + Neon, Monster heartbeat + madness, #22-25 resolved). Testing M2 + M3 + M4 + M5 + arena2 + classes2 + shop2 + team2.

## Waiting on user
1. **M5 classes (★):** server `m5` (Reaper 200 coins + Cracy Frog free). Join: G → Demo or G → Shop. Pick a class on respawn, test during match. Check: Reaper invisibility (4 s after kill), Cracy Frog confirm chain (3 questions), kill tier rewards, class selection persistence, death/respawn. Six class design questions below.
2. **M4 progression (★):** server `m4` (generators + arena + Emerald Dream). Join: G → Demo or explore. Test: build generators (sneak-click to upgrade Lv1→Lv2→Lv3; upgrades cost 200/500 coins from purse), capture arena nodes (3 active in battle; watch contested freeze, payouts, events), unlock Emerald Dream (1000-coin team portal on pad, shared dimension). Check: generator placement, upgrade discovery, arena events, Dream exits (sneak 5s), field costs, admin panel (dream_cost TBD).
3. **M2 playable core (★):** server `m2` (solo test w/ dummies). Join: G → Demo: M2 playable core (first-time chooser). Steps: pick team → start match → kill the dummies → destroy enemy Nexus. Check: all phases (prep/battle/end), respawn, spectator on last life, stats, placeholder map reset on return to lobby.
4. **M3 economy (★):** server `econ`. G → Demo or go to team base vault. Test: deposit/withdraw coins with sliders, check interest (+2%/60 s, capped 50, overflow carried), kill rewards (+10 base, +10×streak from 3+ kills max 150, +20/+90/+190 tier bonus), admin economy page. Check: own team's vault only, teammates can see/withdraw all, interest during prep.
5. **Shaders v2 (★):** server `shaders`. Refresh pack (G → Refresh resource pack), then G → Demo: custom shaders. Check: god-ray direction, thermal colours, Cosmic v3 (lightray rebuild), Acid (world warp), Monster darkness.
6. **Nexus barrier (★):** server `nexus`. Read cracks 10–20 blocks (vanilla textures). Check hit actionbar text.

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
- M3 economy (feat/economy, merged to main f584840): bank dialog at vault on team pad (deposit/withdraw sliders + all buttons), interest 2%/60 s capped 50 (overflow carried as V2), kill rewards (+10 base, +10×streak from 3+ max 150, +20/+90/+190 tier bonus), admin economy page. Server econ ★. Awaiting user test.
- Classes (6d87e5a, feat/classes, server classes ★): Data-driven via src/classes.json + build_classes.py. Reaper (200 coins, invisibility 4 s after kill, HP −10 armour +6) + Cracy Frog (free, V2 lore/kit recovered, confirmation chain word-for-word, frog vision permanent). Shop kits lost on death, basic at team level. Not merged yet; wired into match after M4 integration.
- M4 progression (28e83b7, feat/m4-integration → main): Generators (one per field, 3 levels, team-wide upgrades 200/500 coins from purse, anyone can collect pot, emerald outcomes → coin pot), Arena (3 nodes in battle phase, 10 s solo capture, contested frozen, payouts every 30 s, weighted events), Emerald Dream (shared dimension, 1000-coin team portal unlock on pad, 10 regrowing veins per visit). Demo server m4 ★. Ready for user test. Eight design questions queued.
- M5 classes (5850661, feat/m5-classes → main): Reaper (200 coins, 4 s post-kill invisibility, −10 HP +6 armour, in shop) + Cracy Frog (free, V2 lore/kit recovered, confirmation chain, frog vision permanent, in shop). Death/respawn hooks wired; kill tier set by class; classes reset at match start. Coin-minting fix (emerald pickup = 5 coins, placing while broke creates debt, emerald ores/blocks drop nothing). Demo server m5 ★. Ready for user test. Six design questions queued.

## In flight
- V2 classes roster (feat/classes-v2, server classes2): Archer, Miner, Tank, Ninja, Berserker (confirm), Monster, Balrog (maybe). Data-driven via src/classes.json + build_classes.py (same framework as M5).
- Arena v2 features (feat/arena-v2, server arena2): Random-entry portals (V2 return) + regrowing central block (capture mechanic from V2).
- Shaders v3: Cosmic (rebuild around light, feedback #19/#21), Acid (real world warp effect), both awaiting user test.
- Daemon feature: Screenshots (F2) now queued automatically to feedback log.

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
**Classes** (built 6d87e5a; from coordinator notes, with suggested defaults):
1. **Reaper invisibility:** [suggested: 4 s after each kill; V2 was permanent]. Duration of post-kill invisibility buff.
2. **Keep the "Scyce" typo:** [suggested: keep]. Archaic spelling in lore, keep for authenticity?
3. **Reaper HP + armour:** [suggested: HP −10, armour +6; V2 was −14/+15]. Trade glass cannon for tankier?
4. **Frog vision permanent:** [suggested: yes]. While in frog form, keep vision effect always on?
5. **Cracy Frog free:** [suggested: yes, behind 3 questions]. Free class after passing the lore confirmation chain?
6. **Custom textures:** [suggested: later]. Custom skins for Reaper + Frog to be added post-launch?

**V2 shop classes** (feat/classes-v2, server `classes2`; built with these defaults):
1. **Monster price:** [built: 1800]. V2 sold the whole Monster kit for 300 and the head alone ("Monster Skull") for 1800. Which?
2. **Balrog power:** [built: 300 HP, armour 20/20, whip +14 dmg, no x3 attack]. V2 also tripled all damage. Too much or too little for 10000?
3. **Balrog curse:** [built: enemies only, Wither II until death/milk]. V2 cursed everyone (team-mates too) with Wither III.
4. **Potions -> reusable flasks:** [built: Ironskin 15 s / 60 s cd, Pulverizer 8 s / 45 s cd, Genjutsu 5 s / 20 s cd]. V2 gave 1-3 one-shot potions. Keep flasks?
5. **Berserker armour:** [built: axe in hand zeroes armour via attributes, armour comes back when you switch]. V2 deleted all armour for good.
6. **Ninja armour:** [built: other armour pops back into the inventory; sandals invisible; +40% speed]. V2 deleted it and doubled speed.
7. **Archer extras:** [built: quiver refills to 16 (1 per 3 s), arrow hits make the target glow 6 s]. New, not in V2. Keep?
8. **Kit supplies:** [built: tools/blocks/food given once as normal items, not re-given]. OK?
9. **Monster numbers:** [built: +30% speed (V2 +100%), claws at sword speed, 15% bigger]. OK?
10. **Monster head skin:** [built: EnzziGaming skin by name, resolved online]. Keep that skin or pick another?
11. **Invisible players glow:** [not ported]. V2 made every invisible non-Ninja/Reaper glow. Bring back?

**M3 Economy** (merged f584840; from coordinator notes, with suggested defaults):
1. **Interest rate:** [suggested: 2%/60 s; V2 was 0.5%]. How fast should vault interest accrue?
2. **Any teammate can withdraw all:** [suggested: yes, announced]. Teammates can access and fully withdraw from shared vault?
3. **Interest during prep phase:** [suggested: yes]. Should interest accrue while team is preparing, not just during battle?
4. **Bounty formula:** [suggested: +10×streak from 3+ kills, max 150]. How should kill streak multiply the bounty reward?
5. **Base reward for no-team victims:** What does a killer earn if their victim had no team (neutral/solo)?
6. **Tier bonus set by classes:** [suggested: yes]. Do class tiers set the bonus tier (+20/+90/+190)? Or override?
7. **Enemy can't see your bank:** [suggested: yes]. Should opposing team see vault deposits/balance or only their own?

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
11. **Emerald block farm cost:** Placing one costs 100 coins to prevent infinite farms. Accept? [suggested: yes]. (Superseded by M5 #1: emerald blocks are never held now.)

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

**M4 Progression** (merged 28e83b7; from coordinator notes, with current implementation):
1. **Generator pot collection:** [current: anyone can collect any generator's coins; only owning team upgrades]. Enemy raid incentive or restrict to owner?
2. **Upgrade + portal payment:** [current: from purse only, not bank]. Bank-vs-purse for big purchases (portal 1000, upgrades 200/500)?
3. **Pad entry after payment:** [current: direct entry, no dialog]. After paying portal cost, team enters Dream directly or show confirmation?
4. **Arena lightning toggle:** [current: off by default]. Should Lightning Rabbit event start with battle or stay off?
5. **Dream vein reset:** [current: veins not reset between matches]. Reset veins on each Dream visit or keep per-match state?
6. **Admin panel dream_cost:** [noted: not yet in admin UI]. Should dream_cost (emerald block value) be admin-tunable?
7. **Generator upgrade discovery:** [current: sneak-click to upgrade, no in-game hint]. Is sneak-upgrade action discoverable enough without tutorial?
8. **Generator + pad placement:** [noted: placeholder]. Final placement on actual map to be decided in M6.

**M5 Classes in the match** (feat/m5-classes, server m5; built with these defaults):
1. **Emeralds = coins (anti-mint fix):** [default: emerald / emerald block items become purse coins on pickup, 5 / 45 like generator outcomes; emerald ore and emerald blocks drop nothing when mined (the mined stat pays 25 / 100); placing any coin block while broke books the rest as debt, repaid first from mining]. Closes the M4 exploit (place an emerald block with 0 coins, mine it for 100). OK, or should arena emerald blocks pay 100 like Dream blocks?
2. **Shop roster:** [default: only implemented classes listed: Reaper 200, Cracy Frog free (via the three questions). Archer 50, Warrior 60, Miner 80, Tank 100, Ninja 100, Berserker 120, Monster 1800, Balrog 10000 hidden until built; prices/tiers kept in src/classes.json _v2_roster]. Show the rest greyed out instead?
3. **Kill tier per class:** [default: V2 values — Tank/Ninja/Berserker 1, Reaper/Monster 2, Balrog 3, Cracy Frog 0; basic class = team level − 1 (V2 kit II = 1, III = 2)]. Killing a Reaper pays +90 on top of the kill reward.
4. **Warrior:** [default: stays the placeholder *basic* class (team kit, back on respawn), not sold]. V2 sold Warrior as a 60-coin shop kit (iron + shield). Basic, shop, or both?
5. **Class on match reset:** [default: everyone loses their class (and basic pick) at match start and in the lobby; team class levels back to 1].
6. **Buying a shop class while having one:** [default: allowed, the old one is replaced (no refund); buying the same class again is refused].

**Arena V2: portals + central block** (feat/arena-v2, server arena2; built with these defaults):
1. **Where the gates are:** [default: one 3x3 gate pad per team field (placeholder, next to the Dream pad); anyone may use either pad]. V2 had a single portal on top of the shared central tower. One shared pad, or one per team?
2. **Exit destination:** [default: the exit sends you back to your own team's pad (`out`); V2 sent everyone to the tower base]. OK?
3. **Rotation:** [default: V2 values: one random slot of 4 every 128 ticks (6.4 s), repeats allowed; only the active slot's exit works and shows particles]. Keep, or never repeat the same slot twice in a row?
4. **Entry sound global:** [default: yes, like V2 (end_portal.spawn for every player)]. It gives away arena entries map-wide. Keep, or local only?
5. **Active phases:** [default: gates and core only in battle; V2's core regrew in every phase]. Core in prep too?
6. **Core odds + regrow delay:** [default: V2 odds 36/18/9/16/2 of 81 (cobble/log/hay/emerald ore/emerald block); regrows on the next 0.5 s check (V2: same tick)]. Add a delay (config `core_regrow`, ticks)?
7. **Core economy:** [default: unchanged mining payouts (ore 25, block 100) ⇒ ~7.4 coins per break; an efficiency-V pickaxe could farm ~300-400 coins/min vs generators ~72/min at Lv3]. Lower the core's payouts, add a regrow delay, or keep it as the arena's prize?
8. **Extras not in V2:** [default: emerald-block regrow chime, regrow particles, red/grey "ARENA" pad labels]. Keep?
9. **Final layout:** [noted: 4 placeholder slots (corner landings → nearby exits) and pad positions; real arena geometry in M6].

**V2 Gap Inventory** (from docs/v2-gap-inventory.md, new user-decision questions):
1. **Early end to prep:** V2's "Destroy Magical barriers" ritual (200 coins). Bring back, or remove the prep exit?
2. **Respawn kit by team level:** What does each team level's basic class kit hold? How does a player pick a basic class in the match?
3. **New class designs:** Paladin, Death Knight, Titan, Destroyer, Guardian Angel. Specs and prices?
4. **Repeat-buy mode:** V2's shop had a mode that kept buying the same item repeatedly; the remaster buys one item per click. Bring repeat-buy back?
5. **Coin weight growth:** Weight slowness that increases over the match (V2 trend: more coins = more ponderous). Linear, quadratic, or soft cap?
6. **Emerald rates:** V2 paid 1 coin per emerald and 20 per emerald block; the remaster pays 5 and 45. Keep or rebalance?
7. **V2 interest rate:** V2 = 0.5% per 60 s, cap 10 coins. Now 2%/60 s capped 50. Revert or keep?
8. **Arena node payouts:** Arena nodes' coins don't feed the bank (only loot drops to ground). Keep or send to bank?

**V2 shop catalog** (feat/shop-v2, server `shop2`; built with these defaults, prices in `src/shop.json`):
1. **Page layout:** [default: first page = section menu; pages Blocks, Ores, Food, Utility, Enchanting, Tools, Alchemy, Ammo, Classes, each with V2's Shop Keeper line and a Back button; the dialog stays on the page after a purchase]. V2's "Special" page is left out (its items are on Tools/Classes or not built yet: Talisman, barriers, Dragon Skull). OK?
2. **Duplicates:** [default: like V2, an item can sit on several pages (Golden Apple in Food + Utility, Sand/Soul Sand/Redstone... in Blocks/Ores + Alchemy, Lapis in Ores + Enchanting)]. Keep, or one page each?
3. **Prices:** [default: V2's live prices, e.g. TNT x4 320, Ender Pearl 100, Totem 500, Diamond Block 12, Satan's Blade 2000]. The remaster's emerald rate is 5/45 vs V2 1/20, so V2 prices are relatively cheaper now. Scale them?
4. **Ghast Tear:** [default: 5 (the price V2 showed); V2 actually charged 20]. OK?
5. **Button labels:** [default: V2's names with spelling fixed: Oak Sapling, Bookshelf, Cobweb, Lapis Lazuli, Rabbit's Foot]. The named items keep V2's names and lore exactly ("Farting device", `"Faker's Elixir"` with the quotes, "Mining boost", "Toxic dart", "He rushes this everytime..."). OK?
6. **Enchant in hand:** [default: vanilla /enchant rules like V2: the item must accept it, no conflicts, and an item that already has that enchantment is refused (Efficiency II then V = refused); refused = no coins taken]. Tooltip says "Enchants the item in your hand." (V2: "Put the item in hand to enchant"). V2's Fortune III also handed out a Fortune III book (looks like a leftover CB); not copied. OK?
7. **Satan's Blade:** [default: V2 stats exactly: Fire Aspect 100, Fire Protection 25, Knockback 3, Curse of Vanishing, unbreakable, +12 attack damage, +20 max health, +4 toughness, +1 knockback resistance, -0.025 speed while held; enchantments hidden]. The gap inventory said "Sharpness 100, Smite 25": wrong, V2's numeric ids were 20 = Fire Aspect and 1 = Fire Protection. As in V2, its modifiers replace the sword's own, so it swings with no cooldown. Keep, or add the normal attack speed?
8. **Tinkiwinki's Touch / Nonios's Weakness:** [default: V2 exactly: Fortune V (+10 luck) / Efficiency V + Fortune X (+100 luck), unbreakable; their modifiers replace the pickaxe's own attack damage, like V2]. Nonios's Weakness sends the buyer "<NoniosTheMad> Good Choice!" (V2). OK?
9. **Tipped arrows:** [default: V2 effects as written (Lightning Strike = Speed IV on the target, Healing Blast = Instant Health, Piercing Bolt = Instant Damage...). Vanilla still divides tipped-arrow durations by 8, as in V2]. The gap inventory's "Lightning Strike needs a projectile hook" is not built: V2's was only a Speed arrow. Real lightning?
10. **XP x10 levels (100):** [default: kept on the Enchanting page]. OK?

**Team V2: altar, spawn defense, talisman** (feat/team-v2, server `team2`; built with these defaults):
1. **Altar costs:** [built: team level = V2 kit number, teams start at Kit I, so the altar asks 16 iron/16 gold/8 diamond blocks for Kit II and 64/64/64 for Kit III]. V2's 8/8/2 step (Kit I) is unused unless teams start at level 0. Config `altar_steps`.
2. **When the new kit applies:** [built: on each player's next respawn, as V2 "a kit each life"]. Or re-kit the whole team immediately?
3. **Altar style:** [built: right-click a respawn-anchor altar, own team only, takes only what is still needed, partial payments kept until the match ends]. V2 used a chest that needed the exact amounts. OK?
4. **Spawn defense:** [built: enemies within 4 blocks of the spawn pad get Instant Damage II every 0.5 s, in prep and battle; switch `spawn_guard`]. V2's deeper zone (r=2) also gave the own team Wither. Not ported. Bring that back?
5. **Emerald Talisman income:** [built: +1 coin every 3 s while worn on the head, prep and battle; Luck +100; Curse of Binding]. V2's exact clock rate is unknown. The head model is untested in game (paper with an item_model).
6. **Talisman + Dragon Skull in the shop:** [built: listed in `src/specials.json` only, not sold yet, waiting for the shop-v2 rebuild]. Dragon Skull keeps V2's joke: "[Disabled]" unless you have 3,200,000 coins, then it says "dragon".
7. **Lightning Rabbit:** [built: admin switch (Admin > Lightning Rabbit), off by default]. On by default?
8. **Underground prep walls:** [built: barriers in the void layers (y -64..-1) + the prep containment now bounces anyone past the wall row at any depth]. Tunnels through solid ground are stopped by the bounce, not by blocks. OK?
9. **All recipes at match start:** [built: every player gets every recipe on entering the match]. OK?

## Backlog ideas (deferred, not commitments — shader work paused after M1 v2 + feedback #14, resumes after M2; M5 classes may pull specific shaders earlier)
- **Shader: healer-class vision:** angel-class post effect showing all players' total HP (infrared-like). Hearts >20 glow "as if to burst" (log-scaled).
- **Shader: RTX-like effects:** ref https://www.youtube.com/watch?v=AdTxrggo8e8 (advanced ray tracing style shaders for high-end clients).
- **Shader: real landscape, cosmic, monster class effect:** feedback #14 additions to v2 (deferred post-M2).

## Log (recent ~30 lines)
| Date | Event |
|------|-------|
| 10-14 | **Shop v2 merged** (31f59f2, feat/shop-v2 → main, server shop2 ★): 84-item catalog at V2 prices, 8 pages (Blocks/Ores/Food/Utility/Enchanting/Tools/Alchemy/Ammo), enchant-in-hand, named items with V2 lore, Shop Keeper lines, stay-open dialog. Ten design questions queued (catalog layout, duplicates, prices scaling, Ghast Tear, button labels, enchant rules, Satan's Blade, Tinkiwinki's Touch, tipped arrows, XP levels). |
| 10-14 | **Team v2 merged** (4994386, feat/team-v2 → main, server team2 ★): Offering altar (team class level upgrades, respawn-anchor interface), spawn defense (enemies get Instant Damage II in 4-block zone), Emerald Talisman (head armor, +1 coin/3 s), Lightning Rabbit admin toggle, underground prep walls (void barriers), all recipes on match start. Nine design questions queued (altar timing, spawn zone depth, talisman income/model, dragon skull gating, Wither back, underground wall bounce, recipe auto-grant). |
| 10-14 | **Shaders round 4 complete** (306f9f0, feat/shaders → main): Acid fixed (reset fully functional world warp), Planet + Tiny Planet shaders added, Angel rebuilt with new healer vision, Fluorescent + Neon dual effects, Monster with heartbeat + madness overlays. Issues #22-25 resolved. Ready for user test. |
| 10-14 | **M5 classes merged** (5850661, feat/m5-classes → main): Reaper (200 coins, 4 s post-kill invisibility) + Cracy Frog (free, 3-question confirm chain) in shop; death/respawn hooks wired; kill tier set by class; classes reset at match start. Coin exploit fixed (emerald pickup 5 coins, placing while broke = debt, ores/blocks drop nothing). Demo server m5 ★. Six design questions queued. |
| 10-14 | **Shaders progress:** Cosmic v3 rebuilt around light (feedback #19, #21 resolved); Acid reborn as real world warp effect. Both awaiting user playtest. |
| 10-14 | **Daemon feature:** Screenshots (F2) now auto-queued to feedback log (.mcdev/screenshots/<N>.png). Acked "📷 noted (#N)", entry written after 60s with image path + chat context. |
| 10-14 | **V2 shop classes merged** (6db932a, feat/classes-v2 → main, server classes2 ★): Archer, Miner, Tank, Ninja, Berserker, Monster, Balrog (all built, same data-driven framework as M5). Eleven design questions queued (Monster price/skull split, Balrog power/curse, potions→flasks, Berserker/Ninja armour, Archer extras, kit supplies, Monster numbers/head skin, invisible glow). |
| 10-14 | **Arena v2 features merged** (939989e, feat/arena-v2 → main, server arena2 ★): Random-entry gates (one 3x3 pad per team field, slot every 6.4s), regrowing central block (V2 odds 36/18/9/16/2 of 81). Core economy risk ~300-400 coins/min (efficiency-V mine) vs ~72/min Lv3 generator. Nine design questions queued (gate location, exit dest, rotation repeat, sound global, core in prep, regrow delay, economy risk, extras, layout). |
| 10-14 | **Shaders round 4 started:** #22 Angel (healer vision), #23 Fluorescent/Neon, #24 Monster heartbeat+madness, #25 Acid continuity+new Planet shader. |
| 10-14 | **Smoke test passes** (be19d2d, server "full" on main): all modules turn on/off at right phase, end bossbar bug fixed, every button works. V2 gap inventory documented (docs/v2-gap-inventory.md, 3ef3cfe). |
| 10-14 | **Dev-tool fixes done** (ec18b7c): #26 Servers menu (short labels, tooltip on all rows), #27 void spawn (player over void → spawn, respawn_radius=0). **User must restart mcdev daemon** (old process running old code). |
| 10-14 | **Shop v2 started** (feat/shop-v2, server shop2): Full ~80-item V2 catalog, enchant-in-hand, named items, shopkeeper lines. |
| 10-14 | **Team v2 started** (feat/team-v2, server team2): Team offering altar (class level upgrade), spawn defense, Emerald Talisman, Lightning Rabbit admin switch, all recipes at game start, underground prep walls. |
| 10-14 | **M4 progression merged** (28e83b7, feat/m4-integration → main): Generators (one per field, 3 levels, upgrades 200/500 coins from purse, anyone collects pot), Arena (3 nodes active in battle, 10 s solo capture, contested frozen, payouts 30 s), Emerald Dream (shared, 1000-coin team portal on pad, 10 veins per visit ±3000). Demo server m4 ★. Eight design questions queued (pot collection, payment source, pad entry, lightning toggle, vein reset, admin panel, upgrade discovery, placement). |
| 10-14 | **M5 classes into match started** (feat/m5-classes, server m5): Wiring Reaper + Cracy Frog from framework into match logic. Fixing emerald-block coin exploit. |
| 10-14 | **Shaders feedback #18** (forwarded): Separate Layers and Presets sections in UI, move "No Effect" resets out of effect rows. |
| 10-14 | **M4 integration in progress** (feat/m4-integration): Merging generators + Emerald Dream + arena into main. Loot table format fix done (08e04dd, 26.3 compatible modifiers). Portal unlock cost 1000 coins, arena nodes in match mode. User testing M2 + M3 in parallel. |
| 10-14 | **M3 economy merged** (f584840, feat/economy → main): Bank dialog at vault on team pad (deposit/withdraw sliders + all buttons, own vault only). Interest 2%/60 s capped 50 (overflow V2-style). Kill rewards: +10 base, +10×streak (3+ max 150), +20/+90/+190 tier bonus. Admin economy page. Seven design questions for user. Server econ ★. |
| 10-14 | **M4 integration started** (feat/m4-integration): Merge generators + Emerald Dream + arena into main. Loot table format fix in progress (26.3 incompatible functions→modifiers). Eight Arena design questions for user (capture time/contested/payouts/drops vs bank/lightning/events/forceload/portals). |
| 10-14 | **Arena spike done** (f765a48, feat/arena, server arena ★): capture nodes (10 s solo, 3+ faster; contested frozen), payouts every 30 s via hook (suggested loot drops), weighted events (Emerald Surge, Cracy Frog jackpot, Golden Hour; first at 3 min then every 5), Lightning Rabbit toggle (V2 return, 100 HP). Eight design questions for user. |
| 10-14 | **M3 economy started** (feat/economy): bank dialog, interest, kill rewards. M2 merged to main, built, awaiting user test. Parallel: Classes, M4 integration. |
| 10-14 | **M2 playable core merged** (051fbcc, feat/m2-core → main): barrier + shop + purse + teams (white/black) + phases (lobby/prep/battle/end) + admin panel (/function nonios:admin) + keep_inventory ON + respawn + last life→spectator + win check + stats + placeholder map with reset. Server m2 ★. Awaiting user test. 11 design questions. |
| 10-14 | **Emerald Dream spike done** (6729ef0, feat/emerald-dream, server dream ★): custom dimension with floating islands, random arrivals ±3000, 10 regrowing veins, 5 s sneak-exit, saved return point. V2 lore recovered (Shop Keeper, Emerald Talisman, Crazy Frog chain). Seven design questions for user (shared/void/jump/regrow/value/range/mobs). |
| 10-14 | **Classes started** (feat/classes): class framework + Reaper + Cracy Frog end-to-end. M5 milestone now in progress; spikes ongoing (M2 core, Arena). |
| 10-14 | **Generators spike done** (855e046, feat/generators, server gens ★): V2 level structure reuse via `/place template`, emerald outcomes → coin pot (right-click collect), rolls scale team size, data-driven via src/generators.json, loot from V2's 81-outcome dispenser. Six design questions for user (coins/drops/raids/costs/fortune/protection). |
| 10-14 | **Classes framework done** (6d87e5a, feat/classes, server classes ★): Data-driven via src/classes.json + build_classes.py. Reaper (200 coins, 4 s invisibility after kill, −10 HP +6 armour) + Cracy Frog (free, V2 lore/kit recovered word-for-word, confirmation chain, frog vision permanent). Shop kits lost on death, basic at team level. Six design questions for user (Reaper invisibility/HP/custom texture, Scyce typo, Frog vision, Cracy Frog free). Not merged yet; wired into match after M4 integration. |
| 10-14 | **User feedback #15** (attacker barrier message): Attacker barrier text now just "⛨ Nexus Barrier" (no tutorial lines). User loved the cracks. Rule added to CLAUDE.md: "In-game text stays terse and diegetic: no instructions/tutorial lines in the game pack; those go in try.txt / demo dialogs." |
| 10-14 | **Server archive started** (mcdev archive): G → Servers → Archive; archiving nexus/shop/purse/fx. User requested server archive functionality. |
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

