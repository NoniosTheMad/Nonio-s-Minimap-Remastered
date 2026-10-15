# Voxel build quality, round 2: finding the ceiling

Round 1 ([`voxel-research.md`](voxel-research.md)) asked why LLM builds look like "a Minecraft house" and produced a
playbook. That playbook got us `scenes/castle.py`, which the user judged "a little boring and almost empty… it feels as
if we shipped the first thing that qualified as a castle". This round asks a different question: **what does the top
end look like, who reached it, and how**, for both AI agents and human master builders. It also measures the gap with
numbers instead of adjectives. The revised workflow is in [`voxel-playbook.md`](voxel-playbook.md).

Research date: 2026-10-15. Sources are marked [source] when read directly and [weak] when only a summary or search
snippet was available. Measurements marked [measured] were taken by us on the actual voxel data (scripts are described in §5).

---

## 0. Summary

1. **There is no public "stunning Minecraft castle by Claude".** The impressive AI 3D work in 2026 is in three.js and
   WebGL (dioramas, games, cities). It was produced by **long autonomous runs**: hours, 60+ commits, a screenshot →
   critique → fix loop and a brief that sets the bar at "premium hand-crafted work". One-shot output is not where the
   ceiling is. On MineBench and VoxelBench, Claude ranks near the top, but those are one-shot builds and look like it.
2. **What separated the best AI runs from the rest was the brief, not the model.** Shared features:
   - a showcase framing ("side by side with other models", "a floor, not a ceiling")
   - an explicit quality bar pointing at human premium work
   - a written art direction first
   - a complete piece built early, then deepened
   - each pass names "the three weakest things a viewer would notice first"
   - a list of known failure modes
   - a time budget that is actually used
3. **Self-critique is weak and external critics are weak too, unless they compare against a reference.** Claude-of-Duty
   found that 11 harsh critics, scoring blind side by side against the real target, kept the work honest. Every critic
   still picked the real Call of Duty frame every round. A note.com Blender experiment found that geometric pass
   criteria ("silhouette IoU 0.79") passed while the result "doesn't look cool". The critic needs references and a
   human-perceptual rubric.
4. **Parallel fan-out is not automatically better.** Claude-of-Duty: three rounds of 6 parallel directory owners gained
   +0.46/10 and left defects at 66. One sequential pass with a single owner per *coupled* concern gained +1.00 and cut
   defects to 26.
5. **Human master builds win on scale, composition, contrast, content count and decoration density, not on per-block
   texture.** [measured] Varuna's Ernmore Citadel (1st place, 150×150 plot) compared with our castle (128×128):
   - 7.4× the blocks, 4.9× the exposed surface, about 4× the height
   - a 2× partial-block share on facades
   - 5× the lights per facade area
   - 5-40× the decoration per exposed area

   Yet the whole-surface texture metrics are about the same (surface variation 0.40 vs 0.44). Our castle was not
   "noisy enough"; it was **small, monochrome, under-composed and empty**.
6. **The user's calibration reference, ElRichMC's EliteCraft 2 admin base, is a lesson in craft, not a style to copy.**
   It is vanilla survival with no shaders. It impresses through:
   - layer upon layer of cohesive detail
   - a designed hierarchy (three height tiers, one axis, the entrance as the densest element)
   - 4-5 depth planes on primary facades
   - "beautiful from every angle, no spot left untreated" (his words)
   - deliberate asymmetry between wings

   The full builder breakdown is [`references/elitecraft/analysis.md`](references/elitecraft/analysis.md).

---

## 1. The AI ceiling: who showed impressive 3D/voxel work, and exactly how

| Example | Prompt / workflow | Scale | Iterations | One-shot or agentic | Tools | Source |
|---|---|---|---|---|---|---|
| **Operation Tidewater**, Opus 5.5 "overnight builds" (Nipale-ai) | A 12 KB brief: showcase framing, quality bar, PLAN.md art direction, build the whole piece early, then passes ("write down the three weakest things a viewer would notice first, fix, look again, commit"), plus a failure-mode list. | 384×320×180-voxel diorama; about 40 named scene elements (README) | 65 commits in 205 min of a 4 h budget | Agentic, single agent, fully autonomous ("nobody answered questions") | three.js, Playwright screenshots via a `look` tool that reports fps and black-pixel share | [repo](https://github.com/Nipale-ai/opus-5-5-overnight-builds), [brief](https://github.com/Nipale-ai/opus-5-5-overnight-builds/blob/main/briefs/tidewater-prompt-as-sent.md) [source] |
| **Chrono City** (same set) | Same brief structure: one Toronto block through five decades | City block × 5 eras | 66 commits in 164 min | Agentic, autonomous; the first run was stopped for overheating and rerun | three.js | same repo [source] |
| **Tidewater (dgreenheck)** | "Atmospheric coastal town scene built end-to-end with Opus 5.5" | Island and ocean, WebGPU | Not documented | Agentic | three.js / WebGPU | [repo](https://github.com/dgreenheck/tidewater) [weak: README has no process] |
| **Claude-of-Duty** (Matt Shumer, Opus 5) | Single prompt: "Fan out sub-agents… /loop on each item and have a separate sub-agent check it visually… a really harsh critic… compare them side by side blind and say which one looks better… /loop until it's utterly perfect." | AAA-style FPS level, zero external assets | 4 critic rounds, 11 independent critics | Agentic, multi-agent (11 subsystems with directory ownership) | three.js, `baseline.mjs` (bit-identical shots), `imagediff.mjs`, profiler | [prompt](https://github.com/mshumer/Claude-of-Duty/blob/main/prompt.md), [README](https://github.com/mshumer/Claude-of-Duty) [source] |
| **Invisible Cities** (Quesma, Opus 5.5) | "Make a three.js visualization of all Invisible Cities… Don't ask questions, it is a one-shot task. You have 6h of work, use it until it becomes a masterpiece." | 55 city dioramas | Used 1 h 25 min; 6 parallel subagents (about 7 agent-hours); about $74 | Agentic, one prompt, parallel independent pieces | three.js, `scripts/shot.mjs` screenshots | [blog](https://quesma.com/blog/invisible-cities-one-shot/), [repo](https://github.com/stared/invisible-cities-opus-5.5) [source] |
| **MineBench** | Fixed system prompt that lists judging criteria and losing patterns; "think the hardest before writing code"; block budgets of 10k to 3M+ ("the best models routinely produce millions") | Up to millions of blocks | 1 | One-shot | The model writes a voxel program | [prompts.ts](https://github.com/Ammaar-Alam/minebench/blob/master/lib/ai/prompts.ts), [leaderboard](https://minebench.ai/leaderboard/opus) [source] |
| **VoxelBench** | Text and image-prompt tracks, blind pairwise Glicko | n/a | 1 | One-shot | n/a | [benchlm mirror](https://benchlm.ai/benchmarks/voxelbench): text track GPT-6 Astra 2767, Opus 5.5 2617; image track led by GPT-6.1 Sol ([image](https://benchlm.ai/benchmarks/voxelbench-image)) [source] |
| **Goldie Bench** | 50 one-shot demos, 0-10 rubric by the author | Small demos | 1 | One-shot | Various | [goldiebench](https://goldiebench.com/models/opus5) [weak] |
| **Promptcraft** (cgoulart35) | Plan (style, dimensions, materials) → Python generator → JSON → `.schem`; a CLAUDE.md "teaching file" | 20×20 to 40×40 builds | 1-few | Lightly agentic | Python, WorldEdit schematics | [repo](https://github.com/cgoulart35/Promptcraft) [source] |
| **Opus 5.5 × Blender** (note.com, clearether) | Modelling against reference silhouettes with numeric pass criteria | Single props and characters | Many | Agentic with a human | Blender MCP | [post](https://note.com/clearether/n/n30b928636df4?hl=en) [source] |
| **blenderai.org arena** | Same prompt for every model, blind votes | Single scenes | 1 | One-shot | Blender | [arena](https://blenderai.org/models/claude) [weak] |
| **Anthropic, Opus 5.5 launch** | Claims: "delegates to subagents far more effectively and checks its own work in creative ways"; game graphics and polish; 18 h unattended runs | n/a | n/a | Agentic | n/a | [anthropic.com](https://www.anthropic.com/claude-opus-5-5) [source] |

Curated lists that collect these: [awesome-opus-5.5-usecase](https://github.com/coolbat/awesome-opus-5.5-usecase) and
[awesome-opus-5-5-prompts](https://github.com/TripoGrowthLab/awesome-opus-5-5-prompts) [source].

### 1.1 What the best runs did that ours did not

From the Tidewater brief (verbatim fragments):

- **Framing.** "This is a showcase. It will be shown side by side with the work of other AI models… The goal is NOT
  'error-free' and NOT 'finished early'. The goal is the most impressive result you can possibly produce. Everything
  below is a floor, not a ceiling."
- **The bar is human premium work.** "Judge your work against premium, hand-crafted voxel art and high-end real-time
  renders, not against tech demos." "Scale is part of the wow… Use that headroom for detail."
- **Plan first.** "Write PLAN.md: art direction (palette, light mood, the terrain sequence…), world size… a time plan
  across the whole budget."
- **Complete early, then deepen.** "Build the complete piece early at decent quality… A complete diorama you then
  deepen beats a half-finished one."
- **A named-weakness loop.** "Each pass: … study the screenshots…, write down in NOTES.md the three weakest things a
  viewer would notice first, fix or upgrade them, …look again, commit when it is better."
- **A failure-mode list.** "Showcase pieces like this usually fail in these ways. Check for every one of them: …"
- **Use the time.** "Never stop early: as long as time remains, the piece can get better."

Our castle brief had the art direction (Loarre-on-a-spur) but none of the rest:
- no showcase framing
- no external bar
- one pass each through 8 fixed stages instead of open-ended "three weakest things" passes
- the first version that met the checklist was shipped

### 1.2 Lessons from Claude-of-Duty (the most rigorous public critic experiment)

- **The critics were blind and compared against the real thing.** Scores still rose only 3.59 → 4.14 → 4.05 → 5.05/10
  over 4 rounds, and "every critic in every round picked the real" game in the blind A/B. A blind comparison against
  a reference is what stops self-congratulation. It also shows that a 2-3 round loop is not enough to reach "pro".
- **Sequential beats parallel for coupled concerns.** "Three rounds of six agents each owning one directory moved the
  score +0.46 and left frame-ruining defects…" "One sequential pass with a single owner per coupled concern moved it
  +1.00 and cut defects 66 → 26." In a build, massing, facade, roofs and palette are coupled. Separate wings, interiors
  of different rooms and independent props are not.
- **Critics can be wrong about the cause.** "The most valuable single result came from an agent contradicting its own
  brief." Every critic reported "untextured"; the real cause was crushed albedo. Critics report *symptoms*; the owner
  diagnoses the cause.
- **Deterministic captures.** Bit-identical baseline shots plus a pixel diff make before/after comparisons trustworthy.
  Our `tools.voxel render` is already deterministic; keep a numbered history of sheets.

### 1.3 Lessons from the note.com Blender experiment

- Numeric shape criteria (silhouette IoU 0.7-0.79 against a reference) passed while the result looked like stacked
  boxes. The author's conclusion was "The shape fits, but it doesn't look cool": Claude "cannot determine if it 'looks
  cool'" from its own renders, and pass criteria must reflect how a human perceives the model.
- Implication: our metrics (§5) are **floors that catch emptiness**, not proof of beauty. The perceptual judgement
  must come from comparison against strong references and, at gates, from the user.

### 1.4 MineBench's losing patterns (still the best failure list for Minecraft-style builds)

From the system prompt ([prompts.ts](https://github.com/Ammaar-Alam/minebench/blob/master/lib/ai/prompts.ts)) [source]:
- "A large box with colored blocks painted on a surface to represent features. This is 2D pixel art, not 3D construction."
- "If a judge can look at your build and immediately see 'that's a box, that's another box stacked on it' — the surface
  quality is insufficient."
- "The subject floating in empty space with no environment, base, or context."
- Uniform detail everywhere instead of a hierarchy.

Our castle avoided painted boxes. But it floats on a void island with no context, and its detail is uniform.

---

## 2. Human master builders

### 2.1 Varuna: Ernmore Citadel [source + measured]

- **What it is.** 1st place in the Hytopia "Age of Castles" competition, on a 150×150 plot.
  - Built by Varuna (builder credited as Nikjal); renders by Sedovtop1st.
  - About 20 hours of construction over about 10 days.
  - Java 1.20.1 world on [CurseForge](https://www.curseforge.com/minecraft/worlds/ernmore-citadel-by-varuna), All Rights Reserved.
  - Write-up: [varunabuilds.com/ernmore](https://varunabuilds.com/ernmore).
  - Varuna describes it as "designed for dramatic vertical scale"
    ([blog](https://varunabuilds.com/building-medieval-towncity-in-minecraft-worldedit)).
  - We downloaded it **for analysis only** (never committed) and measured it with our anvil reader.
- **Concept.** "A medieval fortress perched atop a towering boulder."
  - The castle crowns a near-vertical rock.
  - Other elements: an observatory, aqueducts, a cathedral carved into the rock face, zig-zag stairs, a village at
    the base and waterfalls.
  - It reads as a **story stacked vertically**: village → road → gate → cathedral → keep → spires.
- **Palette.** Pale grey-white stone body, with **orange/terracotta roofs** and red flags as a warm accent.
  - Glass in grey, cyan and black.
  - Cobweb, cracked bricks and moss as weathering.
  - Wool and concrete powder are used freely as colour where stone has no matching tone.
- **Interiors.** Arcaded halls with candle chandeliers, planters and log columns.
- **Tools.** Professional teams use WorldEdit, VoxelSniper, goPaint/goBrush, Arceon and, increasingly, Axiom
  (a Blender-like in-game editor with sculpt and heightmap tools; free core, commercial licence for professional use)
  ([forum comparison](https://www.minecraftforum.net/forums/mapping-and-modding-java-edition/minecraft-mods/mods-discussion/3212582-builders-axiom-vs-world-edit-2025),
  [Axiom overview](https://www.feed-the-mods.com/axiom-mod/)) [weak]. In other words, they also build with programs
  and brushes. Our code-first approach is not the handicap.

### 2.2 ElRichMC: EliteCraft 2 Ep 14, "La base del administrador" (the user's calibration reference) [source]

- **Video.** [youtube.com/watch?v=oj-qAh5RVW4](https://www.youtube.com/watch?v=oj-qAh5RVW4), published 2021-09-03,
  40:46, about 350k views.
  - Survival SMP on Minecraft 1.17 (he mentions axolotls arriving).
  - Vanilla textures, no shaders.
  - Chapters: tour, chest room, villager area, library, riches, gold bells, maps.
  - Thumbnails and YouTube storyboard sheets are in the moodboard. High-resolution frames and the full builder
    breakdown are in [`references/elitecraft/`](references/elitecraft/) (stills are local-only).
- **Process, in his words** (Spanish auto-captions, our translation):
  - 14 months of survival building.
  - He converted the Mushroom Fields mycelium to soul soil "because I liked how it looked": **the ground was
    re-authored to match the concept**.
  - "Something I wanted to achieve with this base is that it looks beautiful from every angle; there is no spot that
    is not cared for and treated, even the bridge itself… it's elaborate everywhere." (12:44)
  - "Another thing I like is that it is asymmetric… on the left saturated colours with obsidian and crying obsidian,
    a completely different tower; on the right suddenly a triangular roof with protruding pinnacles; here those
    pinnacles are gone and there is a more spherical, dome-like shape… the other side is all spiky." (13:00)
  - Four big beacon beams: two inside and two at the entrance, carried by flanking towers. The beams are a
    **skyline device** that reads from far away.
  - The chest room is literally at the entrance ("you arrive and boom, chest room"). Function becomes interior
    texture: walls of barrels and chests behind item-frame labels.
  - He was exhausted afterwards: "the next base will be simpler, smaller". This level of density takes time. For an
    agent, the equivalent is many passes.
- **Why it impresses.** See [`analysis.md`](references/elitecraft/analysis.md) for numbers. The **theme-free** craft
  lessons:
  - **Hierarchy.** Three height tiers, with the dominant mass about 2× anything else. One axis: approach → gate
    towers → plaza → portal → keep. The wings vary.
  - **Depth.** 4-5 planes on primary facades. The portal has about 6 nested recessed rings, and its frame is 3-4× the
    opening width.
  - **Density with purpose.** About every 3×3 patch of a primary facade changes block, depth or partial block. The
    accent colour follows structure (pilasters, ribs, voussoirs) instead of being sprinkled.
  - **Thresholds.** Three before the door: bridge-head towers, plaza braziers, portal.
  - **Interiors are designed spaces.**
    - repeated rib bays with a focal end wall
    - patterned floors
    - designed ceilings (radial rib vault around a glass rose)
    - light from fixtures, not torch grids
  - **No untreated side.** Even the secondary walls are banded with pilasters.
  - **Its weaknesses are also instructive**: crude terrain and shoreline, interiors too dark for gameplay, sky-pole
    clutter.
- **What not to take from it.** The user was explicit: it is **not a style or theme target**. Our builds must not
  default to blackstone + red + soul fire or copy its composition. Theme and palette come from each scene's own
  concept. What transfers is the craft: depth layering, density, cohesion and designed hierarchy.

### 2.3 Planet Minecraft cathedrals (scale and grammar references) [source]

- **"Gothic Cathedral 350+ blocks tall, with full interior"**
  ([PMC](https://www.planetminecraft.com/project/gothic-cathedral-350-blocks-tall-with-full-interior/)).
  - "Uses almost the full build height at ~360 blocks tall", "largely based off Cologne Cathedral, Amiens, and
    Beauvais", "about 8 months of on and off building".
  - Full interior: organ, choir, passageways, bell rooms.
  - Its renders (moodboard) show the canonical Gothic grammar at Minecraft scale: twin west towers with openwork
    spires, a forest of pinnacles and flying buttresses, a dark slate roof, a formal garden setting.
  - Lesson: the builder **used the whole canvas height** and set the build in a designed landscape.
- **Other PMC references found:**
  - [English Gothic Cathedral](https://www.planetminecraft.com/project/english-gothic-cathedral/): survival, every
    block hand-placed, resources gathered legitimately.
  - [Cathedral of Ardrane](https://www.planetminecraft.com/project/cathedral-of-ardrane/) (Notux, 2012): a megabuild
    in 3 weeks, set in organic mountain terrain with dragon and angel statues.
  - [Organic Cathedral](https://www.planetminecraft.com/project/organic-cathedral---custom-terrain-with-cinematic-download/):
    620×400 blocks; the cathedral *is* the terrain.

  The recurring pattern: **landmark + context + statues/organics**. Never a building alone on a plinth.
- **Other names on the task list.**
  - Mythical Sausage: a medieval-castle YouTuber; tutorials, world downloads on Patreon, e.g.
    [Island Castle 1.17](https://www.patreon.com/posts/minecraft-island-57821773).
  - BlockWorks: a professional team; press coverage of mega-builds such as
    [PC Gamer's mega-cathedral](https://www.pcgamer.com/minecraft-mega-cathedral/).

  We found no primary process write-ups from either beyond tutorials and marketing [weak]. Their public lessons
  agree with Varuna's and are folded into §3.

### 2.4 Architecture grammar for Gothic and castle forms [source]

These are reference shape grammars to draw from when a concept calls for them, not a mandated style.

- **Elevation.** Three tiers: arcade / triforium / clerestory. Nave heights were Chartres 38 m and Beauvais 48 m
  ([Wikipedia: Gothic architecture](https://en.wikipedia.org/wiki/Gothic_architecture)).
- **Structure.**
  - quadripartite or sexpartite rib vaults (later tiercerons, liernes, fan vaults)
  - flying buttresses topped by pinnacles
  - rose windows
  - tracery types: plate → geometric → curvilinear → reticulated
  - west front: twin towers and a triple portal
- **Pointed arch rule.** From the
  [PMC Gothic tutorial](https://www.planetminecraft.com/project/gothic-tutorial-series-pointed-arches/):
  1. Pick an odd span.
  2. Draw two circles centred on the spring points, each with radius = span and odd diameter (2r+1, e.g. 21 or 45).
  3. Keep the two arcs up to their intersection.

  In code: `inside = (dist(p, springL) <= r) & (dist(p, springR) <= r)` above the spring line.
- **Procedural grammar literature.**
  - Shape grammars: Stiny & Gips 1972.
  - Split grammars: Wonka et al. 2003, "Instant Architecture".
  - CGA shape: Müller et al. 2006.

  The pattern is facade → floors → bays → tiles → elements, where each rule splits a scope and the leaves are
  modules. This maps directly onto our `stamp()` modules
  ([dusberger report](https://www.cg.tuwien.ac.at/research/publications/2010/dusberger-2010-msm/dusberger-2010-msm-report.pdf)).

---

## 3. Levers that separate competent from stunning

Ranked by how much each explains the measured gap.

| Lever | Competent (our castle) | Stunning (Ernmore / EliteCraft / Tidewater) |
|---|---|---|
| **Concept and statement** | A plausible type ("border castle on a spur") | A *specific, surprising* premise: a citadel crowning a needle of rock; a base whose wings each have their own character; a diorama with strata cut like a museum model. One sentence a viewer would repeat. |
| **Canvas use** | 17% of columns built above the yard; max 64 tall on an 84-high canvas | About 98% of the 150² plot covered at the base (rock and village included), tapering up to about 255 tall; the composition fills the frame |
| **Composition layers** | One castle on an island | 4-6 distinct sub-places (village, aqueduct, cathedral, keep, observatory, waterfalls; or a chapel wing, domed tower, gate towers, plaza, causeway), each with its own silhouette |
| **Hierarchy** | Similar-sized towers around a keep | Dominant mass about 2× the rest; 3 height tiers; one axis; the entrance is the densest element |
| **Colour contrast** | Monochrome cool grey with dark roofs | A neutral body plus one strong complementary accent that follows structure (warm roofs and flags on cool stone), plus a glow colour |
| **Facade depth** | 0.41 plane-break ratio; 20% partial blocks | 0.56 plane-break ratio; 42% partial blocks; 4-5 planes on primary faces |
| **Decoration density** | 1.9 lights, 3.2 joinery, 2.5 containers per 1,000 exposed blocks | 16.3 lights, 12.3 joinery, 6.9 containers; hundreds of pots, barrels, chiseled bookshelves |
| **Interiors** | A few rooms with carpet, table, bookshelves | Every visible room furnished to a theme; bays filled to head height; patterned floors; designed ceilings |
| **Context and ground** | A grey crag over void | A designed landscape (rock needle, waterfalls, village, gardens, re-authored ground) |
| **Process** | 8 fixed passes, self-critique, shipped at first pass | Plan → complete early → many "three weakest things" passes against an external bar; blind reference comparison; time budget used |

---

## 4. What our castle pipeline lacked (diagnosis)

1. **No concept phase.** The brief chose a historically plausible castle, not a statement. Nobody proposed three bold
   alternatives, and the user was not asked to pick one.
2. **No external bar.** The critic was the builder itself, working from a defect checklist (flat walls, stripes).
   A defect checklist cannot detect "boring" or "empty"; only comparison with a strong reference can.
3. **Canvas under-used.** The curtain was about 70×70 on a 128×128 canvas, with about 70% of all blocks spent on
   terrain filler. The height cap of 84 was chosen by us, and even that was not used.
4. **Monochrome.** Cool grey ramp, dark roofs and a 10% "accent" (weathered copper and carpet) that does not read at
   distance.
5. **Too few distinct places.** Keep, four towers, a curtain and a yard: about 8 elements. Tidewater's README lists
   about 40.
6. **Decoration 5-40× too sparse**, and almost no block-entity props:

   | Prop | Count |
   |---|---|
   | decorated pots | 1 |
   | banners | 0 |
   | flower pots | 0 |
   | chests | 3 |

   This partly reflects a **tool gap**: the studio did not export block entities (`voxel-studio.md`, Known limits).
   A platform update adding props and entities is in progress on a separate branch.
7. **Too few iterations.** One pass per stage. Claude-of-Duty needed 4 critic rounds to move from 3.6 to 5.0 out of
   10; Tidewater made 65 commits.
8. **No interior standard.** Rooms existed but were not designed spaces: no bay rhythm, no focal end, no patterned
   floor or designed ceiling.

---

## 5. Measurements

All measurements were taken on raw voxel grids. Ernmore was read from its 1.20.1 region files with a custom reader;
the castle comes from `scenes/castle.py`'s `build()`. The scripts live in the session scratchpad and are not
committed; the definitions below are enough to reimplement them.

- *Exposed* means a solid block with at least one air or water neighbour.
- *Facade* means an exposed, non-natural block with a horizontal air neighbour, counted per face (1 face = 1 m²).
- *Plane break* means a lateral neighbour of a facade face that does not continue the same plane, i.e. a corner,
  recess or protrusion. The break ratio is breaks / lateral links.
- *Partial blocks* are stairs, slabs, walls, fences, trapdoors, panes, bars, chains, lanterns, buttons, signs,
  plants, pots, heads and similar.
- Natural blocks (stone, andesite, dirt, grass, tuff, deepslate, blackstone…) are excluded from facade metrics. This
  under-counts castle masonry that uses tuff, deepslate or blackstone, so treat the castle facade numbers as
  approximate.

| Metric | Our castle | Ernmore | Ratio |
|---|---|---|---|
| Canvas / plot | 128×84×128 | 150×150 plot, about 255 tall | |
| Non-air blocks | 243,031 | 1,797,769 | 7.4× |
| Exposed blocks | 42,772 | 207,617 | 4.9× |
| Block states / base ids | 132-165 / 85 | 633 / 212 | 4.8× / 2.5× |
| Columns built above ground | 17% (2,843 of 16,384; structures above the yard) | about 98% of the plot at the base (rock and village included), tapering | |
| Height above ground p50 / p90 / max | 16 / 41 / 64 | (tapering mass up to about 255) | about 4× |
| Exposed partial-block share (all surfaces) | 0.137 | 0.173 | 1.3× |
| Surface variation (neighbouring exposed blocks differ) | 0.442 | 0.40 | about 1× |
| Top-5 states' share of exposed surface | 0.535 | 0.389 | |
| **Facade area (m²)** | 26,587 | 131,843 | 5.0× |
| **Facade plane-break ratio** | 0.41 (164 per 100 m²) | 0.56 (224 per 100 m²) | 1.4× |
| **Facade partial-block share** | 0.205 | 0.421 | 2.1× |
| **Facade top-5 states' share** | 0.67 | 0.35 | |
| **Lights within 2 blocks of a facade, per 100 m²** | 0.31 | 1.55 | 5.0× |
| Lights per 1,000 exposed | 1.9 | 16.3 | 8.6× |
| Joinery (trapdoors, fences, doors, signs…) per 1,000 exposed | 3.2 | 12.3 | 3.8× |
| Containers (chests, barrels, pots, lecterns, bookshelves…) per 1,000 exposed | 2.5 | 6.9 | 2.8× |
| Metal and rigging (chains, bars, bells, anvils…) per 1,000 exposed | 1.1 | 3.7 | 3.4× |
| Heads and skulls per 1,000 exposed | 0.05 | 0.27 | 5.4× |

Ernmore block entities [measured]:

| Block entity | Count |
|---|---|
| decorated_pot | 362 |
| barrel | 301 |
| chiseled_bookshelf | 208 |
| brewing_stand | 112 |
| bed | 96 |
| sign | 48 |
| banner | 45 |
| hopper | 31 |
| campfire | 12 |
| lectern | 11 |
| skull | 9 |

It has **zero entities**: no armor stands and no item frames. All decoration is block-based, which is cheaper on
servers and easier for us to generate. EliteCraft does use item frames as chest labels.

**Reading the table.** Whole-surface texture (variation, partial-block share) is only about 1.3× apart. The big
multipliers are scale (5-7×), lights and props (3-9×), and facade relief and partial blocks (1.4-2×). The top-5 facade
share (0.67 vs 0.35) shows that our facades are dominated by a few blocks. That is the monochrome problem in numbers.
The playbook's targets are set from these.

---

## 6. Interiors and decoration (furniture kits)

What the references do, generalised and theme-free:

- **Every room has a job, and the job furnishes it.** Storage halls are walls of barrels and chests (EliteCraft);
  libraries have chiseled bookshelves and lecterns; workshops have brewing stands, cauldrons and grindstones;
  bedrooms have beds, chests and banners. Function becomes texture.
- **Bays, rhythm and a focal end.** Long rooms repeat a structural bay every 3-6 blocks (column, rib or beam) and end in
  a feature: a window rose, an altar, a hearth, a portal, a throne.
- **Designed floors and ceilings.** At least two floor materials in a pattern (checker, runner, medallion, inlaid
  border) and a ceiling with structure (beams, ribs, coffers, a vault, a skylight). Ceilings are at least 3 high in
  rooms and 5+ in halls.
- **Light from fixtures.**
  - lanterns on 1-3 chains
  - candles in clusters of 1-4 on tables and sills
  - chandeliers (chain + fence + candles or lanterns)
  - hidden light under carpets or behind leaves
  - emissive strips under stained glass

  No torch grids. Gameplay floors stay at light level ≥ 7.
- **Clutter in clusters, not sprinkles.** Groups of 3-7 small props at points of use (table + pots + candles + a
  lectern + a banner behind) with empty floor between them.
- **Furniture vocabulary** (vanilla, block-only):
  - stair chairs with sign or trapdoor arms
  - fence or wall + pressure-plate tables
  - trapdoor cabinets and drawers
  - barrel or chest counters
  - bed + carpet + banner bedrooms
  - cauldron basins
  - brewing-stand candelabras
  - flower pots and decorated pots on every horizontal surface
  - chains + lanterns
  - anvil and grindstone in workshops
  - chiseled bookshelves for libraries

  Avoid armor stands and item frames unless needed: they are entities, server-heavy, and Ernmore does without them.

  Sources: Ernmore measurements, EliteCraft analysis, and builder tips
  ([sportskeeda depth tips](https://www.sportskeeda.com/minecraft/4-best-ways-add-depth-minecraft-build),
  [exitlag interiors](https://www.exitlag.com/blog/minecraft-interior-design/),
  [namehero](https://www.namehero.com/gaming-blog/top-minecraft-interior-design-ideas/)) [weak: SEO-grade, but they agree].

---

## 7. Multi-agent evidence, and a proposal

| Pattern | Evidence | Use for builds |
|---|---|---|
| Parallel independent pieces | Invisible Cities: 6 subagents on 55 independent dioramas, finished in 1 h 25 min | Independent wings, interiors of different rooms, props and furniture kits, terrain vs. building (with an agreed interface) |
| Parallel owners on coupled concerns | Claude-of-Duty: +0.46 over 3 rounds, defects rising | **Avoid** for massing, facades, roofs and palette of one building |
| Sequential single owner per coupled concern | Claude-of-Duty: +1.00 in one pass, defects 66 → 26 | One "architect" owns the shell (massing → silhouette → facade → roof → palette) |
| Independent harsh critics, blind A/B against the real thing | Claude-of-Duty: 11 critics, 4 rounds | Several critic agents, each given *our* sheet and a *reference* sheet unlabelled ("which is the pro build?"), plus a scored rubric |
| Long autonomous single-agent loop | Tidewater: 65 commits in 205 min | The owner's inner loop between critic rounds |

The proposal is in the playbook (§3, pipeline): concept agent(s) → user picks → sequential architect →
parallel decorators (interiors and props by zone) → independent critic panel (blind, rubric-scored) → architect fixes
the top defects → repeat at least 4 rounds or until the critic panel stops picking the reference every time.

---

## 8. Sources not reachable or not useful

- elitecraft.fandom.com returned 402 or empty pages.
- voxelbench.ai blocks automated fetches (benchlm mirror used).
- Planet Minecraft blocks plain fetches (curl with a browser UA works for og: metadata and images).
- Tidewater (dgreenheck) and Invisible Cities READMEs describe the result, not the process.
- No Claude-made Minecraft castle or cathedral of note was found. A [Tom's Guide piece](https://www.tomsguide.com/ai/claude-was-given-access-to-minecraft-and-it-built-a-mansion-with-domes)
  covers an older agent building "a mansion with domes" in-game; it is impressive for an embodied agent, not as
  architecture.
