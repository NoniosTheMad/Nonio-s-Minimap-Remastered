# Voxel build playbook, v2 (paste into the brief of any session that designs terrain, arenas or buildings)

Evidence and links:
- [`voxel-research.md`](voxel-research.md) (round 1: why LLM builds look generic; techniques)
- [`voxel-research-2.md`](voxel-research-2.md) (round 2: the quality ceiling, measured gap, multi-agent evidence)
- calibration reference: [`references/elitecraft/analysis.md`](references/elitecraft/analysis.md)
- tool: [`voxel-studio.md`](voxel-studio.md)

Target: Minecraft Java 26.3 vanilla, no mods.

Why v2 exists: v1 produced a castle the user called "boring and almost empty… the first thing that qualified as a
castle". v1 guarded against *defects* (flat walls, stripes). It had no *bar*: no concept phase, no external reference,
no numeric density targets, no independent critic and one pass per stage. v2 adds all of these.

---

## 0. The brief (paste this)

> This is a **showcase**. It will be judged side by side, blind, against premium hand-made Minecraft builds (Varuna's
> Ernmore Citadel, ElRichMC's EliteCraft admin base, Planet Minecraft's best). The goal is not "error-free" and not
> "finished early"; it is the most impressive build you can make on this canvas. Everything below is a **floor, not a
> ceiling**.
>
> You design as **code** (a `tools.voxel` scene), render, look, critique, fix and re-render. Your untutored default is
> "a plausible example of the type": a castle that qualifies as a castle. That is the failure this playbook exists to
> prevent.
>
> Start with three bold concepts and let the user pick one. Write an art-direction sheet. Build the **complete
> composition early** at low detail, then deepen it in passes. Each pass names the **three weakest things a viewer
> would notice first** and fixes them. An independent critic panel scores you against references; you stop when the
> bar is met, not when the checklist is.

---

## 1. The bar: calibration references

The critic compares our renders against these. They calibrate **craft, not style**.

| Reference | Calibrates | Where |
|---|---|---|
| **ElRichMC, EliteCraft 2 admin base** (user's pick, "a wonder") | Layer upon layer of cohesive detail; 4-5 facade depth planes; designed hierarchy (3 tiers, one axis, entrance as the densest element); designed interiors; "beautiful from every angle, no spot untreated"; deliberate asymmetry between wings | [`references/elitecraft/`](references/elitecraft/) README (frame index) + `analysis.md`; stills are local-only |
| **Varuna, Ernmore Citadel** (1st place, 150×150) | Canvas use (fills the plot, about 255 tall); vertical storytelling (village → gate → cathedral → keep); warm accent on a cool body; decoration density (measured, §5) | [`references/voxel/`](references/voxel/) README |
| **PMC Gothic cathedral, 360 tall** | Using the full height; a grammar executed at scale (twin towers, pinnacle forest, flying buttresses); a designed landscape setting | [`references/voxel/`](references/voxel/) README |
| **Opus 5.5 Tidewater diorama** | What an autonomous agent reaches with a showcase brief and 65 commits: about 40 distinct scene elements, context on every side | [`references/voxel/`](references/voxel/) README |

**Theme rule (from the user).** None of these is a style or theme target. Do not default to EliteCraft's blackstone,
red and soul fire, Ernmore's white and orange, or Gothic. Do not copy their compositions. Each scene's theme, palette
and forms come from **its own concept** (§2). The rubric (§4) checks craft properties that hold in any theme.

---

## 2. Concept phase: three bold options (mandatory, before any detailed code)

The concept agent(s) produce **three concepts that differ in premise, not just in palette**. At least one must be the
option that feels risky. Each concept is one page:

1. **Statement**: one sentence a player would repeat to a friend. Example quality:
   - "A citadel welded onto a falling meteor, half of it still burning."
   - "A cathedral grown from a single colossal tree."
   - "A fortress carved into the ribcage of a fossil leviathan."

   A type with an adjective ("a weathered border castle") is **not** a statement.
2. **Why it is not generic**: three bullets, each naming the default it breaks.
3. **Composition**: top-down plan and side elevation as a 5-minute massing blockout, rendered (`--only iso,top`).
   - Show the height tiers, the main axis and the 4-6 sub-places.
4. **Palette roles**: base / accent / trim / feature / glow / ground (§6 table), with the **warm-cool or value contrast**
   named.
5. **Story layers**: what sits at the bottom, middle and top; what the approach reveals in order.
6. **References**: 3-5 images, each tagged with *what to take* from it ("take the stepped massing from X, the
   roof-colour contrast from Y").
7. **Risk**: what could make it fail and the fallback.

**Gate.** The user picks one (or merges two). When the user is away, the director picks the strongest and records the
other two as open questions (see the autonomous-backlog rule). The picked concept becomes the art-direction sheet.

---

## 3. Pipeline (multi-agent)

Evidence (research-2 §7):
- **Parallel** works for independent pieces (Invisible Cities: 6 agents on 55 dioramas).
- **Sequential single ownership** wins for coupled concerns (Claude-of-Duty: +1.00 vs +0.46; defects 66 → 26).
- **Independent, blind, reference-anchored critics** keep the loop honest.

| Phase | Who | Parallel? | Output | Gate |
|---|---|---|---|---|
| P0 Concept | 3 concept agents, one concept each | Yes | 3 concept pages + blockout sheets | User picks |
| P1 Art direction | Director (main session) | n/a | `scenes/<name>.md` art-direction sheet (§3.1) | Sheet complete |
| P2 Full blockout | **Architect** (single owner) | No | The whole composition at massing level: every sub-place, all tiers, landscape, approach | Canvas and composition targets (§5.1) met; user glance |
| P3 Shell passes | Architect | No | Silhouette → facade depth → roofs → palette → light fixtures, cumulative (`<NAME>_PASS` env like the castle) | Facade targets (§5.2) on primary faces |
| P4 Zones | **Zone decorators**: interiors by room group, landscape and ground, props/kits library | Yes, one zone each | `scenes/<name>/zone_*.py` stamped into the shell; each writes only inside its zone box | Interior standards (§7) per zone |
| P5 Critic rounds | **Critic panel**: 3-5 fresh agents that never build | Yes | Rubric scores, blind pairwise picks, top defects (§4) | Ship gate (§4.4) |
| P5b Fix | Architect, plus zone owners for zone defects | Owners in parallel only across independent zones | Diagnosed causes (critics report symptoms), fixes, re-render | Back to P5; **minimum 4 rounds** |
| P6 Place and walk | Director | n/a | `place --pristine`, `diff` (0 changes), in-game stills via `tools/mcfilm.py still`, demo dialog | User walks it |

Rules:
- **The architect's inner loop between critic rounds** is the Tidewater loop. Render, then write the three weakest
  things a viewer would notice first in `scenes/<name>.notes.md`. Fix them, re-render, commit. Do at least 3 inner
  iterations per round.
- **Zones need contracts.** Each zone has a box, an entrance list, a palette (from the sheet) and a light budget. The
  shell owner freezes the zone boxes before P4. Decorators never edit the shell; they file requests with the
  architect.
- **Budget time, then use it.** Set the budget up front (e.g. 4-8 agent-hours for a showcase build). Do not stop
  early while the critics are still picking the reference every time.
- **Keep every sheet.** Store them as `.mcdev/voxel/out/<name>/history/<round>_<iter>_sheet.png` so the critic can see
  progress and regressions.

### 3.1 Art-direction sheet (template, `scenes/<name>.md`)

```
Statement:      <one sentence>
Not generic because:  1) ... 2) ... 3) ...
References:     <file or URL> - take <aspect>          (3-5 lines)
Canvas:         W x H x D; landmark height; footprint use target
Tiers:          T1 <element> y=..  T2 ..  T3 ..        (tallest >= 1.7x second)
Axis / approach: <entry> -> <threshold 1> -> <threshold 2> -> <focal>
Sub-places (4-6): <name: purpose, silhouette idea>
Element list (>= 25 named things a viewer can point at)
Palette roles:  base[3-4] / accent[1-2] / trim[1-2] / feature[1] / glow[..] / ground[2-3]  + shares
Contrast:       <warm vs cool | light vs dark | saturated vs neutral>, where it goes
Detail map:     A-zones (densest: entrance, crown, focal end), B, C (quiet rest areas)
Light mood:     time of day, fixture families, night read
Interiors:      room list with job, bay size, focal end, floor and ceiling pattern
Known failure modes for this concept: ...
```

---

## 4. The critic

### 4.1 The panel

- Each critic is a fresh agent with **no stake in the build** and a different lens:
  - composition and silhouette
  - facade craft
  - interiors and decoration
  - context and light
  - one generalist "player arriving for the first time"
- Each critic receives:
  - our render set: sheet, hero 3/4 from the approach, entrance close-up, 2-3 interior eye shots, and an in-game
    still if placed
  - the art-direction sheet
  - **reference images** from the calibration set, in comparable views

### 4.2 Blind pairwise test

The critic receives two images labelled only A and B: one ours, one a calibration reference at a similar view, with
the order randomised. It answers "which is the professional build, and why, in 3 concrete observations". Record the
pick rate.

The test is informational, not the gate. Claude-of-Duty's critics never stopped picking the real game, yet the scores
rose. The observations ("B's entrance has five nested frames; A's has one") become fix items.

### 4.3 Rubric (score each 0-10, theme-agnostic)

Anchors:
- 3 = a competent first pass (castle v1 is about 3)
- 5 = a good Planet Minecraft upload
- 7 = a featured build
- 8-9 = EliteCraft or Ernmore level
- 10 = beyond the references

Each score must cite a view and a concrete feature.

| # | Category (weight) | What a high score requires |
|---|---|---|
| R1 | **Statement** (×2) | The concept reads in the first second; a viewer could name it in one sentence; it is not "a typical X" |
| R2 | **Composition and hierarchy** (×2) | ≥ 3 height tiers, the tallest ≥ 1.7× the second; one clear axis from approach to focal mass; 4-6 sub-places with distinct silhouettes; wings vary (no clones except deliberate pairs); the canvas is used (§5.1) |
| R3 | **Silhouette and skyline** (×1.5) | Against the sky, every landmark roofline is punctuated: height changes at least every 3 blocks over 20, no flat run > 8 unless the concept demands it; distinct shapes per sub-place; a far-read device (spire, beam, crown, flag, glow) |
| R4 | **Depth and facade craft** (×2) | Primary facades ≥ 4 depth planes, secondary ≥ 2; no single-plane single-block patch > 5×5 primary (8×8 secondary); about every 3×3 primary patch changes block, depth or partial block; the entrance frame is ≥ 3× the opening, has ≥ 3 nested layers and is the densest element |
| R5 | **Density with hierarchy** (×1.5) | Detail concentrates at A-zones (entrance, crowns, focal ends) and rest areas stay calmer; secondary faces are still treated (bands, pilasters every 4-6); no "untreated side" from any angle |
| R6 | **Material and colour cohesion** (×1.5) | ≤ 4 colour families per structure; the dominant family uses ≥ 3 blocks, mixed by noise; the accent follows structure (≥ 80% of accent blocks lie on pilasters, ribs, edges, bands or roofs); a named contrast (warm/cool or value) that reads at distance; the feature colour ≤ 2-5% |
| R7 | **Interiors** (×1.5) | Every visible room has a job and is furnished by it; bays every 3-6 with a focal end; rooms over 50 m² have a patterned floor (≥ 2 materials) and a designed ceiling; prop clusters of 3-7 |
| R8 | **Context and ground** (×1) | The build sits in a designed landscape: approach, thresholds, plinths blending into ≥ 2 ground materials, vegetation, water edges that are not straight 1-block lines, no void or floating plinth unless it is the concept |
| R9 | **Light** (×1) | Light from designed fixtures (no torch grids, no bare glowstone patterns); it reads at dusk and night; gameplay floors ≥ 7 |
| R10 | **Finish** (×1) | No seams, floating blocks or broken states; signs of use (weathering, wear paths, clutter) where the story wants them |

Output format (each critic):

```
SCORES  R1 x/10 ... R10 x/10   weighted /10
BLIND   pick: A|B  (ours was ?)  observations: 1) 2) 3)
TOP 3 DEFECTS (most visible first): element - view - symptom - suggested fix
ONE CHANGE that would raise the score most
```

No praise. Symptoms over causes; the owner diagnoses.

### 4.4 Ship gate

All of these must hold:
- the **median weighted score is ≥ 7.0** and no category's median is below 5
- the quantitative floors in §5 are met
- at least 4 critic rounds have run
- the user has signed off on the concept (P0), the blockout (P2) and the final walk (P6)

If after 6 rounds the median is still under 6, stop and escalate to the user with the critics' top observations.
Do not quietly lower the bar.

---

## 5. Quantitative floors

These catch emptiness; they do not prove beauty (research-2 §1.3). The numbers come from measured Ernmore vs castle v1
data in research-2 §5. A `python -m tools.voxel stats SCENE` command computing them is the recommended next tool step;
until it exists, use the definitions in research-2 §5.

### 5.1 Canvas and composition

| Metric | Floor | Castle v1 | Ernmore |
|---|---|---|---|
| Built footprint, landscape included, as a share of canvas columns | ≥ 60% (unless empty space is the concept) | 17% (structures only) | about 98% at the base (rock included) |
| Landmark height vs canvas footprint width | ≥ 0.8× (canvas H set by the concept, not a default 84) | 64 / 128 | about 255 / 150 |
| Height tiers | ≥ 3; tallest ≥ 1.7× second | 2 | 4+ |
| Distinct sub-places | 4-6 | 1-2 | 6+ |
| Named elements a viewer can point at | ≥ 25 | about 8 | 40+ |

### 5.2 Facades (per 100 m² of facade; 1 exposed side face = 1 m²)

| Metric | Floor on primary facades | Castle v1 | Ernmore |
|---|---|---|---|
| Plane breaks (corners, recesses, protrusions) per 100 m² | ≥ 200 (break ratio ≥ 0.5) | 164 (0.41) | 224 (0.56) |
| Partial-block share of facade blocks | ≥ 30% | 20% | 42% |
| Top-5 states' share of facade | ≤ 45% | 67% | 35% |
| Light fixtures within 2 blocks of a facade, per 100 m² | ≥ 1.2 | 0.31 | 1.55 |
| Depth planes | ≥ 4 primary, ≥ 2 secondary | 2-3 | 4-5 |

### 5.3 Decoration density (per 1,000 exposed blocks of built area)

| Category | Floor | Castle v1 | Ernmore |
|---|---|---|---|
| Light fixtures | ≥ 10 | 1.9 | 16.3 |
| Joinery (trapdoors, fences, doors, signs, buttons, ladders) | ≥ 9 | 3.2 | 12.3 |
| Containers and furniture (barrels, chests, pots, lecterns, bookshelves, brewing stands, cauldrons) | ≥ 6 | 2.5 | 6.9 |
| Metal and rigging (chains, bars, bells, anvils, lightning rods) | ≥ 3 | 1.1 | 3.7 |
| Heads, skulls and other statuary accents | ≥ 0.25 | 0.05 | 0.27 |
| Block-entity props (pots, barrels, chiseled bookshelves, banners, signs, beds, lecterns, campfires) | ≥ 1 per 8 m² of interior floor; ≥ 5 prop types per furnished room | about 0 | 1,235 total |

---

## 6. Craft rules (theme-agnostic generator rules)

Adapted from the EliteCraft builder's breakdown and the Ernmore measurements. Shapes and materials come from the
concept; the *structure* of the rules is what transfers.

- **Palette roles.** Fill these from the concept: base [3-4 blocks, noise-mixed about 50/25/15/10], accent [1-2],
  trim [1-2], feature [1, ≤ 2-5%], glow [fixtures], ground [2-3].
  - The accent follows structure.
  - The trim marks the outermost depth edges and the crowns.
  - Name a contrast (warm/cool or light/dark) and make sure it reads in the far iso render.
- **Facade stack.** Plane → recessed openings (−1) → pilasters or ribs every 4-6 (+1, accent) → corner and bay-edge
  shafts or buttresses (+2, trim) → a crown or cap row that punctuates the skyline every 1-3 blocks.
- **Entrance(w).** A frame ≥ 3w wide; n = max(3, w/2) nested recessed rings at −1 each, alternating materials; an
  outward flourish 0.3w-0.5w; a stepped approach with a centre runner; paired fixtures on the jambs; 2-3 thresholds
  before it (bridge-head, plaza, portal).
- **Towers(r).** A drum or prism with 4-8 attached shafts rising 3-6 above the eave; a roof that changes the outline
  (flare, step, spire, dome, crown) and differs between towers unless they are a deliberate pair; a light ring or
  fixture at the eave.
- **Skyline post-pass.** On landmark rooflines, add a punctuation element (finial, crenel, spike, dormer, chimney,
  flag) every 1-3 blocks.
- **Halls.** Bays every 4-6; functional blocks fill the bays to head height; a patterned floor with a runner or inlay;
  a ribbed, beamed or coffered ceiling; a focal end wall.
- **Ground.** A 2-3 step plinth → a paved approach with inlay every 6-8 → a 3-5 block blend band → natural ground with
  vegetation; irregular shorelines.
  - Re-author the ground to the concept. ElRichMC turned mycelium into soul soil because it suited the build.
- **Every angle.** Render all 4 isos and the top view. Any face that looks like "the back" gets the facade stack at
  secondary level.
- **Asymmetry with intent.** Keep the axis symmetric and vary the wings: a different roof form, tower type or
  material emphasis per wing.

- **Stability (a gate, not a style).** Every built map region is protected (`protect`), and each block that changes
  by itself costs a restore forever. `stats` shows a stability FAIL, and `protect --install` refuses the build until it
  passes. Check these:
  - Grass: never put `grass_block` under a full block face (a full block, bottom slab or bottom stairs). It dies to dirt.
  - Dirt: never leave lit `dirt` touching grass. It turns to grass. Use `coarse_dirt` or `rooted_dirt` there.
    `stability.fix_soil(scene)` does both as a last pass.
  - Vines spread on every random tick. Use them only where spread is acceptable (outside the protected box) or capped,
    i.e. every face around them is covered. Prefer glow lichen, moss carpet or hanging roots for growth that stays put.
  - Other blocks that change by themselves:
    - grow: mushrooms (spread in low light), saplings, kelp, bamboo, sugar cane, cactus, cave/twisting/weeping vines
      (unless at max age), chorus flowers;
    - decay or turn: leaves without `persistent=true`, unwaxed copper (use `waxed_*`), farmland, budding amethyst, fire.
- **Interaction loot.** Blocks that hand out an item when used (flower pots, chiseled bookshelves, lecterns, jukeboxes,
  campfires, composters, cauldrons, suspicious sand, beehives, decorated pots, berry bushes, pumpkins, rooted dirt,
  cakes) are locked by `protect`: they can't be used. Containers restore empty, so their loot is handed out once.
  Place them as decoration with that in mind.

Optional grammars when the concept calls for them (from research-2 §2.4):
- Gothic: arcade/triforium/clerestory; rib vaults; flying buttresses with pinnacles; rose; twin-tower front with a
  triple portal.
- Pointed arches from two circles of odd diameter centred on the spring points, cut at their intersection.
- Split grammar (facade → floors → bays → tiles → modules) implemented with `stamp()` modules.

---

## 7. Interior and decoration standards

- **Every visible room has a job** and is furnished by it:
  - storage: barrels and chests in bays
  - library: chiseled bookshelves, lecterns, candles
  - workshop: anvil, grindstone, smithing table, cauldron
  - chapel or hall: benches, focal altar or hearth, banners
  - quarters: bed, chest, carpet, banner, pots
  - kitchen: smoker, barrels, campfire, hanging lanterns
- **Bays, focal end.** Repeat a structural bay every 3-6 blocks; end long rooms on a feature.
- **Floors and ceilings.**
  - Rooms over 50 m² get a pattern of ≥ 2 materials (checker, border, runner, medallion) and a structured ceiling
    (beams, ribs, coffers, vault, skylight).
  - Ceilings are ≥ 3 high in rooms and ≥ 5 in halls.
- **Prop clusters.** 3-7 props at points of use, with calm floor between clusters. Every horizontal surface in an
  A-zone gets something (pot, candle cluster, lantern, book).
- **Light from fixtures.** Use lanterns on 1-3 chains, candle clusters, chandeliers (chain + fence + candles), hidden
  light under carpet or behind leaves, and emissive strips under glass. Gameplay floors stay at ≥ 7.
- **Furniture kits.** Build them as code modules in `scenes/kits/` so every scene reuses them. Furniture vocabulary:
  - stair chairs with trapdoor or sign arms
  - fence or wall + pressure-plate or carpet tables
  - trapdoor cabinets
  - barrel counters
  - bed alcoves
  - brewing-stand candelabras
  - decorated-pot shelves
  - chain + lantern chandeliers
  - banner walls
- **Entities.** Prefer blocks. Ernmore has zero entities. Use armor stands, item frames and paintings only where they
  carry meaning (labels, trophies), never as filler.
- **Tool gap.** Block entities (banner patterns, pot sherds, sign text, book contents) need structure export with
  NBT. Until the platform update that adds props and entities lands, place them in a post-placement function and
  record them in the scene. Do not skip them.

---

## 8. Do / Don't

**Do**
- Write a program, not a block list. Plan proportions, silhouette and materials before code ("think hardest before
  writing code").
- Build the **whole** composition early at low detail, then deepen.
- Primary mass → secondary (1/3-1/2 size) → tertiary. The focal point is ≥ 25% taller or wider than its surroundings.
- Use odd widths for anything with a centre (gates, ridges, the Nexus housing).
- Give walls three depth layers: frame (pulled out 1), infill, sub-block (stairs, slabs, walls, fences, trapdoors,
  buttons, panes, chains).
- Overhang roofs by 1-2 blocks.
- Make terrain from heightfields + 3D noise + erosion; slope decides material.
- Drive material choice with low-frequency noise so patches cluster.
- Ground everything: flared bases, rubble, roots, vines where structure meets rock.
- Name the contrast and the far-read device in the art-direction sheet.
- Keep a numbered render history and a notes file with the three weakest things per iteration.

**Don't**
- Don't ship the first version that passes a checklist. Passing the checklist is the *start* of the critic rounds.
- Don't default to a plausible example of the type. If the statement could describe 1,000 builds, it is not a
  statement.
- Don't copy a reference's theme, palette or composition. Take named aspects only.
- Don't leave a monochrome palette. A cool ramp with a 10% accent that does not read at distance is monochrome.
- Don't float the build in a void or on a token island unless the concept is about that.
- Don't run parallel agents on coupled parts of one shell.
- Don't let the builder grade itself as the gate. Its own "three weakest things" loop is for iteration; the gate is
  the panel.
- No flat walls, flat ground, raw primitives, painted features, Y-band terraces, salt-and-pepper noise, unlit
  walkable areas or torch grids.
- Don't let the defaults in: oak planks + cobblestone + glass panes + stair roof on grass.

---

## 9. Arena design rules (Nexus PvP)

- **Layout.** 3 lanes from each base to the centre, 1 chokepoint per lane. No single position sees all chokes. Teams
  reach the centre at the same time (± 1 s; equal path lengths measured in the script).
- **Symmetry.** 180° rotation of one half (point symmetry). The landmark sits on the axis (centre generator). Each half
  has its own secondary landmark in team colour (teams are `white` and `black`).
- **Sightlines.** Mix short lines (≤ 12 blocks, melee) with long ones (30+, bows); cover breaks every long line, and
  using a long line costs exposure. Bows dominate open ground, so the centre needs full cover pieces 2-3 high.
- **Cover.** Err on too little: full cover (≥ 2 high) to advance, half cover (1 high or slab walls) at fight spots.
  Players can place blocks, so designed cover must be protected (arena restore) or the meta becomes pillaring up.
- **Verticality.** 2-3 height levels; high ground costs time or an exposed route.
  - Climb with stairs, slabs, ladders or scaffolding.
  - 1-block step-ups max; 2 blocks headroom.
  - Sprint-jump gaps ≤ 3 (4 is the maximum and too punishing).
  - Falls over 3 hurt; void edges need intent.
- **Readability.**
  - Team colours on the team's half (white/black concrete, terracotta, wool, banners, stained glass) as accents,
    not whole surfaces.
  - A neutral palette in the centre.
  - The landmark is visible from every spawn.
  - Distinct material themes per lane so call-outs work ("copper lane", "moss lane").
- **Mobs and light.** Light every walkable surface above 0, or keep `spawn_mobs` off.
- The showcase bar (§4) applies to arenas too. R1-R6 and R8-R9 hold; R7 applies to any enterable structure.

---

## 10. Palette tables (average texture colour from the 26.3 client jar; L = luminance 0-255, "tex" = texture contrast)

**Cool stone ramp (dark → light)**: blackstone 37 · polished_blackstone_bricks 44 · deepslate_tiles 54 · deepslate_bricks 70 ·
polished_deepslate 72 · cobbled_deepslate 77 · deepslate 80 · tuff_bricks 101 · polished_tuff 102 · tuff 108 · mossy_cobblestone 115 ·
cracked_stone_bricks 117 · mossy_stone_bricks 118 · stone_bricks 121 · stone 125 · cobblestone 127 (busy, tex 29) · gravel 128 ·
polished_andesite 134 · andesite 136 · smooth_stone 158 · diorite 188 (busy, tex 34) · calcite 223

**Warm stone**: terracotta 104 · bricks 107 · mud_bricks 109 · granite 111 · packed_mud 112 · dripstone_block 112 · polished_granite 115 ·
cut_red_sandstone 115 · sandstone 202 · cut_sandstone 205

**Wood (dark → light)**: spruce_log 40 · dark_oak_planks 46 · dark_oak_log 48 · stripped_dark_oak_log 58 · crimson_planks 61 ·
mangrove_planks 67 · oak_log 87 · spruce_planks 88 · warped_planks 91 · stripped_spruce_log 92 · acacia_planks 104 · jungle_planks 122 ·
oak_planks 133 · bamboo_planks 170 · birch_planks 175 · cherry_planks 188 · pale_oak_planks 219

**Ground**: mud 58 · podzol 66 · coarse_dirt 90 · grass (plains tint) ~99 · moss_block 100 · dirt 102 · rooted_dirt 110 · dirt_path 123 ·
clay 166 · sand 206 · snow 253

**Accents**: obsidian 12 · crying_obsidian 18 · red_nether_bricks 20 · nether_bricks 26 · gilded_blackstone 45 · basalt 73 ·
dark_prismarine 82 · polished_basalt 88 · copper 123 → exposed 131 → weathered 140 → oxidized 143 (orange → teal) · purpur 138 ·
prismarine_bricks 155 · end_stone_bricks 218 · quartz 230

**Strong roof and colour accents** (the colour Ernmore gets from wool and concrete): orange/red/cyan wool, concrete and
concrete powder; glazed terracotta for inlays and medallions; stained glass in 2-3 tones for windows. Use them for the
named contrast, following structure (roofs, bands, banners), never sprinkled.

**Teams are `white` and `black`** (shared names across branches; see CLAUDE.md).

**Team white**: white_terracotta 183 · white_glazed_terracotta 206 · white_concrete 211 · pale_oak_planks 219 · calcite 223 · bone_block 225 · quartz_bricks 229 · white_wool 235

**Team black**: black_concrete 10 · obsidian 12 · coal_block 15 · black_wool 21 · black_terracotta 25 · polished_blackstone 50 · gray_concrete 57

Team caveats:
- The Nexus is obsidian (L 12), so black-team accents must not sit next to it or it stops reading as the target.
  Frame it with a light or coloured trim instead.
- Avoid calcite/snow/quartz-heavy and blackstone-heavy *neutral* palettes, or the neutral centre reads as one team's
  territory.
- A mid-value neutral (tuff, stone, copper, moss: L 90-140) keeps both team accents visible.

**Example gradients** (bottom → top, or shadow → light). These are starting points; the concept decides.
- Ruined fortress: blackstone → cobbled_deepslate → tuff → stone_bricks / mossy_stone_bricks (clustered) → andesite → smooth_stone trim
- Volcanic: obsidian (accents) → blackstone → basalt → polished_basalt → tuff → magma_block / shroomlight for hidden glow
- Canyon: packed_mud → terracotta → granite → cut_red_sandstone → sandstone → smooth_sandstone (top bands broken by noise, not stripes)
- Overgrown: mud → rooted_dirt → moss_block → grass, with mossy_cobblestone / mossy_stone_bricks where stone meets soil
- Copper temple: weathered/oxidized copper roofs, exposed copper trim, tuff_bricks walls, calcite inlay

Rules of thumb:
- Neighbours in a gradient differ by about 10-25 L; jumps over 40 read as stripes.
- Mix busy textures with calm ones.
- The named contrast is the exception: it is a deliberate jump, placed on structure.

---

## 11. Tooling notes

- Author scenes with `tools.voxel` (see [`voxel-studio.md`](voxel-studio.md)): `Scene`, SDF `shapes`,
  `Mix`/`Gradient`/`Noise` palettes, `stamp()` modules, auto-connect, and `render`, `place`, `diff`.
- Structures are DataVersion 5023 with `{id, properties}` palette entries.
- Mojang assets are extracted locally to `.mcdev/` and never committed.
- Camera markers (`cam_*`) drive eye-level renders. Every scene sets at least:
  - `cam_hero`: 3/4 view from the approach
  - `cam_entrance`: close-up
  - `cam_interior_*`: one per major room
  - `cam_far`: skyline read

  These are the views the critic compares with the references.
- Use in-game stills (`tools/mcfilm.py still`, see [`mcfilm.md`](mcfilm.md)) for the final critic round. Real
  lighting and night reads only show in game.
- Reference images: `docs/references/voxel/` and `docs/references/elitecraft/` are **local-only** (third-party
  images, gitignored in this public repo). Their READMEs list the sources and how to re-fetch them.

---

## 12. Checklist (the floor; the gate is §4.4)

- [ ] P0: three concepts with statements; the user picked one.
- [ ] Art-direction sheet complete: statement, references with "take X from Y", tiers, axis, 4-6 sub-places, ≥ 25 elements, palette roles, named contrast, detail map, room list.
- [ ] Whole composition blocked out before detail; canvas targets met (§5.1).
- [ ] Facade floors met on primary faces (§5.2); every iso view shows a treated side.
- [ ] Decoration floors met (§5.3); every visible room furnished by its job (§7).
- [ ] Landscape and approach designed; no void or token plinth unless that is the concept.
- [ ] Light from fixtures; dusk/night read checked; gameplay floors ≥ 7.
- [ ] ≥ 4 critic rounds; median weighted ≥ 7.0, no category < 5; blind pick rate recorded.
- [ ] Gameplay (arenas): lanes, chokes, equal travel, no all-seeing spot, cover on long lines.
- [ ] `stats` stability PASS (no unstable soil, nothing spreading or decaying).
- [ ] Placed with 0-diff, in-game stills taken, user walked it.
