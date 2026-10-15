# Feedback audit (#60)

Audit of every user request up to #62. Sources: in-game feedback #1-#62 (`mcdev feedback --all`, screenshots 26/28/29/52/62),
`.mcdev/inbox.json` (Claude's resolve notes) and the user's terminal messages (`T@hh:mm`, UTC from the transcript; in-game #ids are local time = UTC+2).
Checked against `main` @ 383793b, plus the unmerged branches `feat/gen-dream` (5 commits) and `spike/shaders` (9 commits).
Every other `feat/*` branch is fully merged into main.

Statuses: **DONE** (on main) · **DONE-UNMERGED** (branch) · **PARTIAL** · **NOT DONE** · **WRONG** · **NEEDS-USER-CHECK** (code exists; only an in-game look can confirm) · **SUPERSEDED** (a later instruction replaces it).
Fix size: S = under 1 h, one area · M = a few hours or several files · L = a new system or a redesign.

## 1. Open items: NOT DONE / PARTIAL / WRONG

| # | Area | Request (user's words) | Latest src | Status | What's missing | Size |
|---|------|------------------------|-----------|--------|----------------|------|
| 1 | Shaders | "The thermal shader looks horrible" (screenshot 62: flat red/orange blobs around lights on a purple world) | #61 (supersedes the new Thermal of #54) | NOT DONE | Round-5 Thermal (spike/shaders 41a2c10, 23:50) is what the user rejected at 23:53. It needs a redo. | M |
| 2 | Shaders | "cinematic shader idea is a great initiative, but it feels very broken. Redo from scratch." | #61 | NOT DONE | Cinematic is unchanged since shaders v2 (c65d643). | M |
| 3 | Shaders | All shader work: shader layers/presets, Thermal/Alien, Cosmic, Angel, Neon/Fluorescent, Monster, Planet, Acid (#12-#25, #54-#59) | — | WRONG (tracking) | **None of it is on main.** `spike/shaders` is 9 commits ahead and unmerged. Main has only `reaper`, `acid` and `rainbow` (the first spike). TRACKER says "Shaders round 4 merged (306f9f0)", which is false. Acid's world warp lives only in the demo's resource-pack overlay (`demos/shaders/resourcepack/.../shaders/core`), not in the game pack. | M (merge plus a plan for which effects go in the game pack) |
| 4 | Classes / shaders | "I need an effect for the monster class too" | #14 (#24 "Love the monster effect") | PARTIAL | The Monster look exists only on spike/shaders. The Monster class in `src/classes.json` has `vision: []`. The heartbeat sound and the HP-driven madness aren't wired to the class. | M |
| 5 | Barrier | "attack cooldown doesn't seem to apply to barrier damage. I almost one-shot it… by spamming clicks" | #49 | DONE-UNMERGED (feat/gen-dream dc9bbf3) | Main's `nexus/hit` still does full `attack_damage x10` per click. The `nexus/charge` scaling is only on the branch. | S (merge) |
| 6 | Barrier | "barrier still doesn't seem to be harmed by arrows/projectiles (at 20% damage)" | #47 (refines #37) | DONE-UNMERGED (feat/gen-dream 3bb7c78) + NEEDS-USER-CHECK | Main has the shop-v3 version (arrows near the core). #47 was tested on shop2, which predates that. The branch rewrites hits to be geometric (arrows, tridents, rockets, wind charges, fireballs). | S (merge, then test) |
| 7 | Barrier / match | "field barriers should not disappear with time… controlling the center could put pressure… After min20, barriers could lose durability… By min 30, they'd break… 10%/min" | #48 | DONE-UNMERGED (feat/gen-dream dc9bbf3), **interpretation risk** | It was built on the **Nexus** barrier (centre-hold drain, minute-20 decay). "Field barriers" that "disappear with time" more likely means the **prep walls**: DESIGN.md calls them "Barriers Broken", V2 had "Destroy Magical barriers", and the walls currently drop on a 5-minute timer. If so, it is WRONG. **Ask the user** which barrier they meant before merging. | S to ask, M if it has to move |
| 8 | Generators | "a single mineable block (so tool doesn't have to be swapped) with a custom loot table. Not for chances of traps" | #47 (supersedes the #39 lucky-block proposal) | DONE-UNMERGED (feat/gen-dream 6168fa0) | Main still carries the lucky block with traps (off by default). On the branch, single-block mode is `"on": false`, so V2 multi-blocks stay the default. Confirm the default with the user. | S |
| 9 | Emerald Dream | "Emerald dream should be much 'richer'" | #47 | DONE-UNMERGED (feat/gen-dream 2594965) + NEEDS-USER-CHECK | Ores, veins, crystals, lamps, life and ruins with loot are on the branch only (server `gdream`). | S (merge) |
| 10 | Emerald Dream / shaders | "can't wait until we decide what shader fits well with it" | #47 | NOT DONE | No Dream shader has been proposed yet. This is a future decision (once shaders are merged). | M |
| 11 | Dev / mcdev | "remove the reload shaders/resource packs options from the menu… if they were [needed], I expect the reload to happen automatically" | #33 | PARTIAL | The resource-pack button is gone and packs auto-reload (PackWatch). **"Reload datapacks" is still a G-menu button** (`tools/mcdev.py:579`), and datapack changes don't auto-reload. The literal request was resource packs, but the stated intent (reloads happen by themselves) also covers datapacks. Either drop the button and have `PackWatch` `/reload` on datapack changes, or ask the user. | S |
| 12 | Dev / mcdev | "archive the obsolete demos for me so i don't have to spend time reviewing them" (m4, shop, shop2) | #51 (overrides #31 "only archive what I've reviewed" for these) | PARTIAL | shop and shop2 are archived. **m4 is still listed ★** ("m4 next once you're off it"). Other superseded ★ demos are also still listed: m2, econ, arena, gens, classes, m5, arena2, team2, econ3, shop3, bank4. Claude offered "archive all" but nothing has been confirmed. | S |
| 13 | Process | "make the messages to wake you… periodically… as part of the framework built around" | #46 (refines #45) | PARTIAL | This is a session cron (15 min, dies with the session or after 7 days). It isn't part of mcdev/the daemon, and a new session has no wake-up. | M |
| 14 | UI rules | "try not to add task feedback as in-game content" (rule: terse, diegetic) | #15 | PARTIAL | The game pack still has tutorial lines. `game/start.mcfunction:39`: "Shop: the villager at your base. Bank: the vault on the gold pad (right-click). Coins: mine ores." `shop/denied`: "Talk to your team's shopkeeper (the villager at your base)…". `dream/arrive/landed`: subtitle "sneak to wake up". `game/skip`: "press Start". | S |
| 15 | UI rules | "menus… Generator, emerald dream, etc. Have the buttons way at the bottom while the text way at the top" and "buttons should always exist, but be greyed out if not available" | #44, #41 | PARTIAL | Generator, bank and shop follow the rules. **Emerald Dream unlock** (`portal/offer_show`): "Open" stays active when the purse is short, and the refusal is only an actionbar (should be greyed with a "Need N coins" tooltip). **Admin** and **Admin > Economy** have 4-6 line bodies with long italic notes, and "Rebuild map" (lobby only) isn't greyed outside the lobby. The **full** demo dialog has 66 buttons. | S-M |
| 16 | Process / demos | "the 'shop 2' demo… should be re-made to properly compile the massive batch of feedback/changes… I just want to see the changes" | #47 | PARTIAL | `full` (main) is the all-in-one demo, but `demos/full/try.txt` is stale. It says "10 pages, the last is Special", which is shop v2; shop v3 uses categories, x1/x8/x64/Stack and Again. It says nothing about mineable field generators, the centre generator, node bonuses, protection, ore yields/Fortune or events. The gen-dream items (#47-#49) aren't on main. | S |
| 17 | Gear | "All demos should inherit this [gear slots] if they plan to give items" | #34 | PARTIAL (minor) | `demos/economy/.../ores.mcfunction` (5 pickaxes) and `demos/coin-purse/.../gear.mcfunction` still use a plain `give`. Game code and the other demos use `gear/give`. | S |
| 18 | Shaders | RTX-like shaders ("Something like https://www.youtube.com/watch?v=AdTxrggo8e8") | #9 | NOT DONE (backlog by agreed triage) | Never started. Kept in TRACKER backlog. | L |
| 19 | Classes | Angel/healer class ("Class to be implemented") | #9, #22 | NOT DONE (backlog) | The Angel look exists on spike/shaders. There is no Angel class in `src/classes.json`. | L |
| 20 | Map / tools | Voxel studio: "design the 3D scene in Voxel… a system to convert that into a minecraft construction" | T@21:46 | PARTIAL (in flight) | `feat/voxel-studio` has only an untracked `tools/voxel/` (no commits). `feat/voxel-research` has only uncommitted docs. Server `voxel` is up. | L |

### Needs a user decision before the related fix lands
- #7 / #48: which barrier did "field barriers" mean (Nexus or prep walls)?
- #8 / #47: should single-block generators be the default?
- #11 / #33: should "Reload datapacks" go too?
- #12 / #51: "archive all" superseded demos?
- #34 point 4 ("my last comment is a mistake. The two texts do not match. Keep both"): today no text shows on join (title only) and try.txt sits behind the demo-dialog button. If "keep both" meant keeping the on-join instructions as well, this is WRONG. Marked NEEDS-USER-CHECK.

## 2. DONE-UNMERGED, by branch

**feat/gen-dream** (server `gdream` = Dream, `gd3` = arena3 demo; 5 commits ahead, includes a main merge at 23:10)
- #47 Projectiles hit the barrier geometrically (3bb7c78)
- #47 Single-block generator mode with a loot table; the lucky block is removed (6168fa0). Default off.
- #49 Melee attack charge on barrier hits (dc9bbf3)
- #48 Centre-pressure drain and minute-20 decay, on the **Nexus** barrier (dc9bbf3). See open item 7.
- #47 Richer Emerald Dream: ores, veins, crystals, lamps, life, particles, ruins with loot (2594965)
- Demos arena3 (buttons 11, 23-27) and full (67-71) updated

**spike/shaders** (server `shaders`; 9 commits ahead, never merged)
- #12 time-of-day buttons, materials gallery, more looks · #14 Acid split (Acid / Rainbow / Wobble), layers + categories, landscape (seed 2), Cosmic, Monster, Reaper (no depth) removed
- #17 toggle-off fix · #18 category resets are a REMOVE row, presets on their own page · #19/#21/#55 Cosmic (round 5: leaf halo back, nebula sky)
- #22/#57 Angel (round 5: gold bloom, god rays, motes from real blocks) · #23 Neon/Fluorescent · #24/#58/#59 Monster (heartbeat, eased tunnel, drifting distortion, eyes replaced)
- #25 Acid continuity; chat (shaders) Acid as a real world warp (demo overlay only) · #25/#56 Planet (round 5 rewrite) · #54 Alien = old Thermal
- All round-5 items (#54-#59) are NEEDS-USER-CHECK. Round 5 committed at 23:50, and the only reaction so far is #61 (Thermal rejected, Cinematic broken).

**demo/posteffect-probe**: 3 commits ahead. The old vanilla-effects probe (#38 answered); intentionally left unmerged.

## 3. Full ledger

Order: area, then #id. "Where" = main unless stated. T@hh:mm = terminal message (UTC).

### Dev framework / mcdev menus
| Src | Request | Status | Where / note |
|-----|---------|--------|--------------|
| #1 | Back button in the feedback dialog | SUPERSEDED by #33 (text box removed) | — |
| #2 | "Unknown scoreboard objective 'devnav.act'" | DONE | trigger lint in `check_server` |
| T@15:30 | Feedback >256 chars / with apostrophes fails | SUPERSEDED (Book & Quill, then #33) | — |
| T@15:30 | Feedback attaches context (server/branch) | DONE | daemon context block |
| T@15:30 | "Highlighted servers" awaiting review | DONE | ★ in G → Servers |
| T@15:30 | Know what to do on each demo | DONE → refined by #34 | try.txt button |
| T@16:57 | "Any way you could spot these kind of issues in the demos before I try them?" | DONE | `check_server` lint |
| T@16:46 | Inbox in chat; instructions as a G button; chat = feedback | DONE | f6fdfb8 |
| T@15:54/16:00 | Chat persists across restarts; easier feedback | DONE | thread.json replay; book |
| T@16:15 | No popping console windows | DONE | windowless children |
| #4 | Reset a demo to its initial state | DONE | "Reset this server" (world.pristine) |
| #5, #6, #7, #16 | Pipeline tests / "can you read?" | DONE (answered) | — |
| #12 | Servers shut down after 10 min idle | DONE | idle sleep |
| #15 | Server archive for old tests | DONE | G → Servers → Archive |
| T@21:34 | "Don't see the archive in my server menu" | DONE | screenshot 29 shows "Archive (4)" |
| #26 | Servers menu labels/tooltips | DONE | ec18b7c |
| #27 / #28 | Demos spawn you into the void | DONE | `devnav:spawn_set`, `ground_check` |
| #29 | Tall Servers tooltip (screenshot) | DONE | `tip_lines` ≤ 6×34 |
| #30 → #36 → #50, T@21:34 | Clicking an asleep server queues the join | DONE | `execute as <uuid>` fix; #50 resolve says confirmed after the daemon restart at 23:37 |
| #31 | Don't archive unreviewed servers | DONE | nexus/purse/fx back to sleeping; memory rule. Overridden for named demos by #51 |
| #51 | Archive obsolete demos (m4, shop, shop2) | PARTIAL | open item 12 |
| #33a | Remove "Feedback (book)" option; Feedback gives the book | DONE | 383793b: button "Feedback" gives the book, text box removed |
| #33b | Remove reload shader/resource-pack options; reload automatically | PARTIAL | open item 11 |
| #34a | Demo instructions under the demo's own dialog | DONE | `write_demo_dialogs` |
| #34c | Instructions visible by default should be hidden | SUPERSEDED by #34d | — |
| #34d | "my last comment is a mistake… Keep both" | NEEDS-USER-CHECK | see the decision list |
| #38 | "list mine" in fx? Only vanilla effects? | DONE (answered) | fx = old probe; custom shaders on `shaders` |
| #47 | Remake the shop2 demo to show all changes | PARTIAL | open item 16 |

### Shop
| Src | Request | Status | Where / note |
|-----|---------|--------|--------------|
| #32 | Overhaul: hundreds of items, bulk/continuous buying | DONE | shop v3: categories, pages of 16, x1/x8/x64/Stack, Again, partial buys |
| #47 | Back button in a consistent place regardless of item count | DONE | fixed 4×6 grid, row 1 Prev/Back/Next/Again |
| M1 decisions | Stays open after buy; NPC at base | DONE | — |
| M1 decision | "refuses when inventory full" | SUPERSEDED by shop v3 partial buys (#32 bulk) | — |

### Bank / economy
| Src | Request | Status | Where / note |
|-----|---------|--------|--------------|
| T@15:17 #4 | Die = give away everything; carrying coins slows you | DONE | purse |
| #35 | Slowness more tolerant as the game progresses | DONE + NEEDS-USER-CHECK | `purse/scale*`, `#w_grow` |
| #36 | Yields: stone 0, coal 0.1, copper 0.2, iron 0.5, redstone 2, lapis 4, gold 1, diamond 3, emerald 5, Fortune +40%/lvl | DONE | `src/yields.json` v2 (+ my picks: nether gold 0.5, emerald block 20) |
| #41a | Bank deposit/withdraw buttons always exist, greyed when unavailable | DONE (as redesigned in #47) | bank v4 preset buttons greyed |
| #41b | Interest grows over time | SUPERSEDED by #47 | — |
| #41d | Interest not in chat; visible to the team on the right side | DONE | team sidebar (`economy/hud`) |
| #47a | Interest every second, 1% → 10% at min 30, cap 20/s | DONE | `interest_start 100 / end 1000 / ramp 1800 / cap_s 20` |
| #47b | Withdraw quick options | DONE | 10/50/100/200/500/1000/Half/All |
| #47c | Deposit = all, on contact with the gold platform | DONE + NEEDS-USER-CHECK | `bank/pad` (plate detection while walking is untested) |
| #47d | Feedback for the enemy team on deposit ("finish line") | DONE | actionbar + bell |

### Classes
| Src | Request | Status | Where / note |
|-----|---------|--------|--------------|
| T@14:18 | Reaper B/W outlines; Crazy Frog acid-like vision | DONE | `nonios:reaper`; frog = acid + rainbow (= old Acid, per #14) |
| T@15:17 #3 | Basic classes on respawn (team upgrade via offering); shop classes one-time, binding | DONE | classes framework, altar |
| #14e | Monster class effect | PARTIAL | open item 4 |
| #9 / #22 | Angel healer class | NOT DONE (backlog) | open item 19 |

### Arena / events
| Src | Request | Status | Where / note |
|-----|---------|--------|--------------|
| #40 | Capture = sub-objective with minor team bonuses | DONE | node bonuses (West Haste, Centre +0.5%, East regrow x1.5) |
| #40 | Arena main generator gives items and (especially) coins | DONE | centre generator (`arena/cgen`) |
| #41e | Frog event out of that demo; separate events demo; gameplay events + a troll | DONE | demo `events`; `config.trolls 0b` |
| #41f | Don't overkill the frog joke | DONE | troll off by default |
| #42 | Events come with a timer/warning (raid bar) | DONE | `event_warn` 600 t bossbar |
| #43 | Centre natural blocks unminable; building allowed | DONE + NEEDS-USER-CHECK | `arena/protect` |

### Generators
| Src | Request | Status | Where / note |
|-----|---------|--------|--------------|
| #39a | Field generators: old mineable blocks | DONE | `generator/grow/*` |
| #39b | Middle generator pot-style, scales with the banks | DONE | centre gen Lv by bank total |
| #39c | Lucky-block proposal | SUPERSEDED by #47 | — |
| #47 | Single mineable block with a custom loot table, no traps | DONE-UNMERGED (gen-dream) | open item 8 |

### Nexus / barrier
| Src | Request | Status | Where / note |
|-----|---------|--------|--------------|
| T@15:17 #1 | Bossbar barrier over the obsidian, slow regen | DONE | — |
| T@15:30 | Visual effects so it feels like a barrier | DONE | forcefield shell |
| #10a | Cracks more visible | SUPERSEDED by #13 → approved in #15 | — |
| #10b | Bossbar only for the barrier's team | DONE | `shield_tick` |
| #11 | Default regen 20%/min | DONE | `nexus/regen` |
| #13a | Cracks less cartoonish | DONE (approved #15 "So minecrafty!") | vanilla destroy_stage |
| #13b | Remove the exact-HP text on hits (both teams) | DONE | `hit` shows "⛨ Nexus Barrier" only |
| #15 | Attacker text should just name the barrier | DONE | same |
| #37 | Bow damages the barrier at 20% | SUPERSEDED by #47 | — |
| #47 | Still not harmed by arrows | DONE-UNMERGED + check | open item 6 |
| #48 | Centre pressure, decay from min 20, broken by min 30 | DONE-UNMERGED, interpretation risk | open item 7 |
| #49 | Attack cooldown applies to barrier damage | DONE-UNMERGED | open item 5 |

### Team / altar
| Src | Request | Status | Where / note |
|-----|---------|--------|--------------|
| #41c | Offering icons wrong colour | DONE + NEEDS-USER-CHECK | econ-v3: plain root, white sprites |
| T@15:17 #2 | Up to 20/team, typical 2v2-5v5, no per-player ceiling | DONE | scaling in generators |

### Emerald Dream
| Src | Request | Status | Where / note |
|-----|---------|--------|--------------|
| T@15:17 #5 | Dimension, random location, exit by sneaking X s | DONE | — |
| #47 | Much richer | DONE-UNMERGED (gen-dream) | open item 9 |
| #47 | A shader that fits the Dream | NOT DONE | open item 10 |

### Shaders (all on spike/shaders unless stated)
| Src | Request | Status | Note |
|-----|---------|--------|------|
| #9 | RTX-like shaders | NOT DONE (backlog) | open item 18 |
| #9 → #22 → #57 | Angel: HP infrared on entities only; majestic, ethereal; particles from the environment; no whitish filter | DONE-UNMERGED + NEEDS-USER-CHECK (round 5) | #9/#22 superseded by #57 |
| #12 | Daytime option, materials, more shaders | DONE-UNMERGED | — |
| #14 | Acid without rainbow; old Acid = wave+rainbow renamed; categories to combine | DONE-UNMERGED | Wobble/Rainbow; layers |
| #14 | Decent landscape | DONE-UNMERGED | seed 2 |
| #14 → #19 → #21 → #55 | Cosmic: magical light, keep the moon-behind-leaves aura, better sky | DONE-UNMERGED + NEEDS-USER-CHECK (round 5) | earlier ones superseded by #55 |
| #14 | Reaper (no depth) removed | DONE-UNMERGED | — |
| #17 | A shader didn't deactivate | DONE-UNMERGED | 768f9f2 |
| #18 | Presets clearly separated from layers | DONE-UNMERGED | — |
| #22 | Keep Thermal | SUPERSEDED by #54 (renamed Alien) | — |
| #23 | Neon → Fluorescent; new desaturated Neon with coloured outlines | DONE-UNMERGED | — |
| #24 → #58 → #59 | Monster: synced heartbeat, madness at low HP; progressive tunnel; heartbeat on damage; slow-drifting distortion; replace the eyes; "enough madness effects already" | DONE-UNMERGED + NEEDS-USER-CHECK | #59 supersedes #58's "add more madness effects" |
| #25 | Acid continuity (sudden reset) | DONE-UNMERGED | — |
| chat (shaders, ~19:40) | Acid = classic MC acid (world bends, hides the sky) | DONE-UNMERGED | demo overlay only |
| #25 → #56 | Planet (fake curvature); clouds glitch | DONE-UNMERGED + NEEDS-USER-CHECK (round 5) | — |
| #54 | Thermal → "Alien"; new real Thermal | Alien DONE-UNMERGED; new Thermal SUPERSEDED by #61 | — |
| #61 | Thermal looks horrible | NOT DONE | open item 1 |
| #61 | Cinematic: redo from scratch | NOT DONE | open item 2 |
| — | Shaders on main | WRONG (TRACKER claim) | open item 3 |

### UI rules
| Src | Request | Status | Note |
|-----|---------|--------|------|
| #15 | In-game text terse, no task/tutorial content | PARTIAL | open item 14 |
| #41a / #44 | Compact dialogs; fixed buttons; greyed = unavailable | PARTIAL | open item 15 (Dream unlock, admin) |
| #34b | Gear slots: weapon 1, bow 2, pickaxe 3, bucket 4, tool 5, demos included | DONE (game) / PARTIAL (2 demos) | open item 17 |
| #44 | Low GUI scale | NEEDS-USER-CHECK | rule in CLAUDE.md; generator/bank/shop comply |

### Process
| Src | Request | Status | Note |
|-----|---------|--------|------|
| T@14:56, T@15:44 | One main channel; quiet session; roadmap; tracker agent | DONE | CLAUDE.md protocol |
| T@15:53 | Push back on process | DONE | memory rule |
| T@16:41 | Work the backlog autonomously while away; accumulate questions | DONE | TRACKER questions |
| T@17:42 | Screenshots go into the inbox | DONE | daemon `screenshots` |
| #45 → #46 | Messages wake Claude periodically, batched, as part of the framework | PARTIAL | open item 13 |
| T@21:46 | Voxel scene → MC builder platform and research | PARTIAL (in flight) | open item 20 |
| #60 | Collect and verify all feedback | DONE | this file |
