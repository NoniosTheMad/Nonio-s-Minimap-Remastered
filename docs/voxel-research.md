# Voxel / Minecraft build quality with LLMs: research notes

Research for the Nonios's Map remaster (2026-10-14). Goal: future sessions design arenas and landscapes as 3D voxel
scenes in code, render them, critique the renders, iterate, then convert to Minecraft 26.3 blocks.
The distilled, paste-ready brief is [`voxel-playbook.md`](voxel-playbook.md). This file holds the evidence and links.

Confidence tags: **[verified]** = checked locally in this repo/machine; **[source]** = stated by the linked page;
**[weak]** = page content was thin, stale or partly unreachable.

---

## 1. Why LLM builds look like "a Minecraft house"

- Anthropic's own diagnosis for frontend design applies 1:1 to builds: **distributional convergence**. Without direction
  the model samples the high-probability centre of its training data (for UIs: Inter font, purple gradient, rounded cards;
  for Minecraft: a 7x7 oak-plank box, cobblestone base, glass-pane windows, a stair roof). The fix that worked for them:
  name the convergent defaults explicitly, give concrete alternatives, pitch guidance at a middle "altitude" (concepts
  that map to code, not exact hex values and not vague taste), commit to a bold named aesthetic, and package it as a
  reusable brief/skill. [source]
  [Improving frontend design through Skills (claude.com)](https://claude.com/blog/improving-frontend-design-through-skills)
- MineBench's system prompt lists the losing patterns it saw across thousands of votes [source]
  ([prompts.ts](https://github.com/Ammaar-Alam/minebench/blob/master/lib/ai/prompts.ts)):
  - "A large box with colored blocks painted on a surface to represent features. This is 2D pixel art, not 3D construction."
  - "If a judge can look at your build and immediately see 'that's a box, that's another box stacked on it' — the surface quality is insufficient."
  - "The subject floating in empty space with no environment, base, or context."
  - "The losing builds are always the ones where the model started coding with a rough idea and filled in details as an afterthought."
  - "The models that win MineBench are not the ones that write the most code — they are the ones that THINK the hardest before writing any code."
  - Build order: "(1) Primary structure, (2) Secondary elements, (3) Tertiary details. Never skip to step 3 on a weak step 1."
  - "Concentrate detail on focal areas (silhouette edges, faces, joints, openings)." "Use material variation to break up large surfaces."
  - "Judges zoom in. They rotate the camera."
- VoxelCodeBench (Unreal voxel API, code generation): "producing executable code is far easier than producing spatially
  correct outputs, with geometric construction and multi-object composition proving particularly challenging." [source]
  [arXiv 2604.02580](https://arxiv.org/abs/2604.02580). Implication: code that runs is not evidence the build is right; only a render is.
- Claude cannot see the world it builds in. Every serious Claude build agent found (below) adds an offline render step for exactly this reason.

## 2. Benchmarks and leaderboards

| Benchmark | Output the model produces | Ranking | Notes |
|---|---|---|---|
| **MC-Bench** (Adi Singh, 2025) | JavaScript build script: `async function buildCreation(startX,startY,startZ)` using helpers `safeSetBlock()` / `safeFill()`, run by a Mineflayer bot on a real server in Docker | Human pairwise votes, blind | Claude 3.7 Sonnet #1 (86% win rate), 3.5 Sonnet #2 in Mar 2025. "Technically a programming benchmark." Domain `mcbench.ai` no longer resolves (Oct 2026). [source] [TechCrunch](https://techcrunch.com/2025/03/20/a-high-schooler-built-a-website-that-lets-you-challenge-ai-models-to-a-minecraft-build-off), [github.com/mc-bench](https://github.com/mc-bench), [orchestrator](https://github.com/mc-bench/orchestrator), [simple-minecraft-server-builder](https://github.com/mc-bench/simple-minecraft-server-builder), [prompt generator](https://github.com/adonis-singh/MC-Bench-Prompts) |
| **MineBench** (Ammaar Alam) | Either raw JSON block coordinates, or **tool mode**: JS run by `voxel.exec` with only `block(x,y,z,t)`, `box(...)`, `line(...)`, seeded `rng()`, `Math` | Bradley-Terry over blind votes | Tool mode exists because JSON hits token limits; procedural code is what makes large builds possible. Prompt quoted in section 1. [source] [repo](https://github.com/Ammaar-Alam/minebench), [site](https://minebench.ai/) (homepage numbers looked stale) [weak] |
| **VoxelBench** | Voxel structures from text (and an image-prompt track) | Glicko-2, blind pairwise | Text track, 2026-10-12: GPT-6 Astra 2767, **Claude Opus 5.5 2617**, GPT-6.1 Sol 2554, GPT-6 Sol 2446, Claude Opus 5 2187, ... [source] [benchlm mirror](https://benchlm.ai/benchmarks/voxelbench), [voxelbench.ai](https://voxelbench.ai/leaderboard) (site blocks AI fetchers) |
| **VoxelCodeBench** | Code against an Unreal voxel API; symbolic / geometric / artistic tasks | Automatic | Runs ≠ correct; composition is the hard part. [source] [arXiv](https://arxiv.org/abs/2604.02580) |
| **GDMC** (Generative Design in Minecraft, since 2018) | Python settlement generators adapting to real terrain | Human judges: adaptability, functionality, narrative, aesthetics | Long-running academic PCG competition; WFC buildings, terrain-adaptive placement. [source] [GDMC 2023](https://gendesignmc.wikidot.com/wiki:2023-settlement-generation-competition), [paper](https://arxiv.org/pdf/1803.09853), [WFC example](https://github.com/ScholliYT/MGAIA-Minecraft-GDMC) |

**What separates top entries** (synthesis of the prompts and the judged criteria):
1. *Code, not block lists.* All competitive setups give the model a small procedural API (block/box/line/fill + RNG) and let
   it write loops, functions and math. Block lists cap out at a few hundred blocks; code scales to 10^5-10^6.
2. *Planning before code*: proportions, silhouette and a material plan decided first.
3. *Hierarchy*: primary mass → secondary → tertiary detail, detail concentrated at edges/openings/focal points.
4. *Real 3D depth* instead of painted surfaces; *material variation* on every large surface.
5. *A ground/scene context*: base, terrain, surroundings, not a floating object.
6. Judged from multiple angles and close up, so all faces must hold up.

## 3. Claude-specific demos and agent setups

- **minecraft-java-fabric-claude-plugin** (chapmanjw) — the most complete Claude build agent found. [source]
  [repo](https://github.com/chapmanjw/minecraft-java-fabric-claude-plugin)
  - A gated pipeline of skills: survey → research → plan → shape → ecology → blueprint → build → integrate → inspect → register → reflect.
    Skills include `terrain-shape`, `terrain-landmark`, `terrain-ecology`, `terrain-cave`, `design-building`, `design-monument`, `exec-inspect`, `exec-reflect`.
  - **Render-before-place**: "author a model you can see and verify it against the references before placing a single block."
    Parametric NumPy model → render three orthogonal PNG views → compare to references → change one parameter at a time →
    re-render → decompose to fills → place in one batch → scan-render the placed result to confirm.
    Rationale: Claude can't see the world, and "a wrong silhouette can't be detailed away".
  - "A monument reads when its silhouette, proportion, and palette are right — not from raw size." "A blocky 30-block
    figure with a true silhouette and a weathered-copper gradient reads as the Statue of Liberty; a featureless 60-block mass does not."
  - Quality contract: *silhouette assertions* (sample surface points, check height variance) and *block_mix_ratios* rows
    per named gradient "to prevent monoculture".
  - Terrain is a **recipe (sampler graph)**, not a voxel grid: heightfield → thermal then hydraulic erosion → rivers →
    climate/biome masks → seam blend → materialize as columns. Rules: "Never stack Y-band fills" (anti-ziggurat gate rejects
    terracing); slope-driven materials ("rock on steep faces, snow above the snowline, beach near water, mix everywhere");
    "Erosion is the realism multiplier"; judge with slope and **eye-level** renders, because they "expose the bare-wall failure top-down hides".
  - Toolkit: NumPy + Pillow, SciPy for terrain, OpenSimplex noise. Fills pre-tiled to ≤32,768 blocks (the `/fill` limit).
- **minecraft-builder-claude-mcp-server** (joshdevous): Claude writes JSON/Python → `.schem` via `mcschematic` → WorldEdit
  `//schem load` + `//paste`. Advice for 300+ blocks: write to a file rather than inline. Simple, but no render loop. [source]
  [repo](https://github.com/joshdevous/minecraft-builder-claude-mcp-server)
- **deepslate-mcp** (Philogag): MCP server that renders `.nbt` / `.schem` / `.litematic` to PNG with vanilla assets extracted
  from Mojang's `client.jar` (isometric / top / front / side / custom), plus `render_blocks` (build from code and render).
  Node ≥20, headless WebGL (Mesa/Xvfb on Linux). Ships an agent skill for procedural structures in Python. [source]
  [repo](https://github.com/Philogag/deepslate-mcp), upstream [misode/deepslate](https://github.com/misode/deepslate)
- **Mindcraft** (kolbytn / Emergent Garden videos): Claude 3.x agents building in-world through Mineflayer commands; Claude 3.5
  Sonnet built a mansion with domes. In-world bot building is slow and unseen; useful as a curiosity, not a quality method.
  [Tom's Guide](https://www.tomsguide.com/ai/claude-was-given-access-to-minecraft-and-it-built-a-mansion-with-domes) [weak],
  [AI Builds Stuff in Minecraft](https://www.youtube.com/watch?v=Xd5PLYl4Q5Q)
- **Three.js voxel scenes**: prompt libraries of Claude Opus 5.5 / Fable 5 Three.js scenes (voxel mascot loops, voxel Japanese
  garden with pagoda, castle above clouds, procedural worlds). The strong prompts read like creative briefs: vision line,
  art direction (palette, mood, lighting), camera, technical constraints, then a validation checklist. [source]
  [Tripo 3D prompts: Opus 5.5](https://www.tripo3d.ai/3d-prompts/models/claude-opus-5-5),
  [awesome-3d-prompts](https://github.com/TripoGrowthLab/awesome-3d-prompts) [weak: individual prompt pages blocked fetches]
- **Research on render-critique loops** (Blender code agents):
  - **LL3M** (2025): Claude 3.7 Sonnet as the coding agent writing Blender Python; a critic VLM renders *multiple views* and
    lists discrepancies; a verification agent checks each fix landed; code kept modular so edits are local
    ("make it taller", "steampunk style"). [source] [LL3M](https://www.alphaxiv.org/abs/2508.08228)
  - **SceneCraft**: dual loop, multimodal LLM critiques renders of its own Blender script and accumulates a library of reusable
    "spatial skills". [source] (via LL3M summary)
  - **SceneAssistant** ([arXiv 2603.12238](https://arxiv.org/pdf/2603.12238)), **SceneWeaver** (self-reflective agent,
    [arXiv 2509.20414](https://arxiv.org/pdf/2509.20414)): same pattern, visual feedback as the main quality lever.
  - Common lesson: one-shot code is mediocre; *render → critique against an explicit checklist → targeted parameter edits*
    is what moves quality, and the critique must use several views (orthographic + perspective + close-up).

## 4. Techniques

### 4.1 "Write a program that builds it"
Model the scene as code that fills a NumPy voxel array (`uint16` block ids + a palette list), never as hand-placed coordinates.
Primitives worth having (MineBench's set plus what pro builders do by hand):
`box`, `hollow_box`, `line` (3D Bresenham), `cylinder`, `sphere/ellipsoid`, `cone`, `arch`, `extrude(polygon)`,
`sdf_fill(f)` (fill where a signed distance function ≤ 0: smooth unions/subtractions give organic rock and sculpted forms),
`heightfield(h)` (column fill), `noise2/3` (OpenSimplex), `scatter(mask, density, rng)`, `gradient(mask, palette_by_height_or_value)`,
`mirror/rotate180` (for team symmetry), `stamp(template)`.

- **SDFs** for organic masses: rocks = union of noise-displaced ellipsoids; arches = torus minus box; cliffs = heightfield + 3D noise
  to allow overhangs. Smooth-min (`smin`) blends masses so they don't read as "visible primitives".
- **Noise**: fBm OpenSimplex for terrain height; ridged noise for crests; low-frequency noise to drive *material* variation
  (which block in the gradient) so patches cluster instead of salt-and-pepper.
- **Erosion**: thermal (talus) + hydraulic on the heightfield before materializing. Biggest single realism win for terrain.
- **L-systems / space colonization**: custom trees, roots, vines; branches as 3D lines, leaves as noise-thinned spheres.
- **Wave Function Collapse**: tile-based building/wall modules that fit together (GDMC entries use it); overkill for one arena,
  useful for repeated modules (ramparts, walkway segments).
- **Mirror symmetry**: generate one team half, then rotate 180° (point symmetry) so both teams get identical routes;
  break perfect symmetry only in cosmetic detail (seeded per side) and in team colour.

### 4.2 Multi-pass workflow (consensus of all sources)
1. **Brief / reference**: name the aesthetic (e.g. "basalt caldera with weathered copper shrine"), list 3-5 references, set scale.
2. **Gameplay blockout** (for arenas): lanes, chokepoints, spawn timing, cover, heights in plain blocks. Measure distances.
3. **Massing**: 3-4 primary masses at varied heights; landmark first.
4. **Silhouette check** in render (sky-line, side views). Fix before any detail.
5. **Terrain & organic shaping**: heightfield/SDF, erosion, overhangs, transitions into structures.
6. **Depth pass**: frames, pillars pulled out 1, recesses, ledges, overhangs, stair/slab/wall/trapdoor micro-depth.
7. **Palette & gradient pass**: value-ordered gradients (dark/mossy low, light high), clustered noise, 60/30/10 ratios.
8. **Lighting pass**: hidden and visible light sources (no mob spawns at light 0; readable at night).
9. **Decoration & ecology**: foliage, rubble, banners, team colour accents, small props.
10. **Render-critique loop** after each pass, against the checklist; only then convert to blocks and test in-game.

### 4.3 References and moodboards
Claude can read images: give it reference screenshots (pro builds, real places) and the renders of its own output side by side,
and ask for a numbered discrepancy list. The fabric plugin and LL3M both compare against references explicitly.

## 5. Minecraft builder craft knowledge

- **Palette size and ratio**: 3-5 blocks per material family; 50-60% primary, 30% secondary, 10-20% accent.
  [Switchblade Gaming](https://www.switchbladegaming.com/minecraft/building-tips/), [Craftdex](https://craftdex.net/articles/the-architecture-of-builds)
- **Gradients**: value (lightness) matters most; texture density and material "feel" second. Darkest/mossiest low, under
  ledges and beside cracks; transition blocks in *clusters*, not horizontal stripes; replace ~25-35% of a surface with
  neighbours in the gradient. Reliable stone ramp: stone → andesite → tuff → cobblestone → deepslate → polished deepslate → blackstone.
  [minecraftgradient.blog wall gradients](https://minecraftgradient.blog/minecraft-wall-gradient/),
  [deepslate→stone](https://minecraftgradient.blog/deepslate-to-stone-gradient/), [blockblend stone](https://blockblend.app/guides/stone-gradient-guide)
- **Depth ("no flat walls")**: three depth layers: structural frame (pillars/beams pulled out 1 block), wall infill, and a
  sub-block layer (stairs, slabs, walls, fences, trapdoors, buttons, panes). Walls wider than ~5 blocks need at least one
  depth change; on long walls push/pull a column every 3-4 blocks. "You are building pockets for shadows."
  [Minecraft Forum: depth](https://www.minecraftforum.net/forums/minecraft-java-edition/creative-mode/369294-depth-in-building-a-simple-way-to-improve-all),
  [Craftdex](https://craftdex.net/articles/the-architecture-of-builds), [Sportskeeda](https://www.sportskeeda.com/minecraft/4-best-ways-add-depth-minecraft-build)
- **Massing and silhouette**: 3-4 cuboids at different heights; secondary masses 1/3-1/2 of the primary; focal point ≥25% taller
  or wider than its surroundings; the black-shape-against-sunset test. [Craftdex](https://craftdex.net/articles/the-architecture-of-builds)
- **Odd widths** (5-7-9): a centre block for doors, ridges, focal points; odd-width roofs end in one clean peak.
  [Roof guidelines wiki](https://minecraft.fandom.com/wiki/Tutorials/Roof_construction_guidelines), [Odd blocks video](https://www.youtube.com/watch?v=ODO56wjGpKs)
- **Overhangs**: roofs 1-2 blocks past the wall; the shadow line defines the building's edge.
  [4netplayers roofs](https://www.4netplayers.com/en/blog/minecraft/minecraft-roofs-building-tips-tricks-roofdesign/)
- **Terraforming tools translated to code**:
  - WorldEdit: sphere brush to block out hills, smooth brush (`//brush smooth <r> <iterations>`) for large areas,
    erosion modes (default/lift/fill/melt/smooth), `//gmask` to restrict what is affected.
    [WorldEdit BE brushes](https://worldedit-be-docs.readthedocs.io/en/stable/usage/brushes/), [Manacube terraforming](https://manacube.com/threads/terraforming-with-worldedit-for-beginners.18061/)
  - VoxelSniper: "Melt, fill and blend ball will take care of about 95%" of terraforming. Workflow: ball brush size 15-20 to block
    out, 8-12 for ridges and valleys, erosion *melt* on cliff faces and peaks, *fill* to soften, *blend ball* to transition
    stone → gravel → dirt → grass. [Westeroscraft VoxelSniper basics](https://westeroscraft.fandom.com/wiki/VoxelSniper_Basics),
    [FAVS commands](https://intellectualsites.gitbook.io/fastasyncvoxelsniper/default-commands/commands), [Astroworld guide](https://guide.astroworldmc.com/how-to-use-voxelsniper-minecraft)
  - Code equivalents: *smooth* = 3D box/Gaussian blur of the solid mask then threshold at 0.5; *melt* = remove solid voxels with
    ≥ N air neighbours (erodes exposed edges); *fill* = add air voxels with ≥ N solid neighbours (closes pits); *lift* = dilate
    upward; *blend ball* = per-voxel majority/mode filter over the material ids (inside a mask); *gmask* = boolean mask array.
    These are cellular-automaton passes on NumPy arrays (`scipy.ndimage.convolve`, `uniform_filter`, `generic_filter`).

## 6. Arena / PvP level design

From [The Level Design Book: map balance](https://book.leveldesignbook.com/process/combat/balance),
[Pascal Luban, Rules of map design](https://www.gamedeveloper.com/design/multiplayer-level-design-in-depth-part-2-the-rules-of-map-design),
[World of Level Design: chokepoints](https://www.worldofleveldesign.com/categories/csgo-tutorials/csgo-principles-choke-point-level-design.php),
[layouts](https://www.worldofleveldesign.com/categories/csgo-tutorials/csgo-how-to-design-gameplay-map-layouts.php),
[ongamedesign FPS maps](https://www.ongamedesign.net/designing-fps-multiplayer-maps-part-1/):

- **Symmetry**: two-team competitive maps are usually mirrored or rotated 180°; asymmetry is "really hard to get right".
  Rotation (point symmetry) avoids the left/right-handed bias of a plain mirror.
- **Lanes and chokepoints**: ~3 lanes, one chokepoint per lane (3-4 total); "It should be impossible to cover all chokepoints
  from a single point." Teams should reach the contested choke at about the same time, defenders slightly earlier.
- **Sightlines**: mix long and short; every long sightline has a risk/reward; corners shape LOS breaks. No single vantage sees everything.
- **Cover**: soft (blocks sight) vs hard (blocks projectiles), half vs full. "For PvP, err on too little cover." Break up large open
  spaces with full cover so players can advance without being exposed for too long.
- **Verticality**: increases choices and "gameplay per square metre"; height advantage must cost something (exposed route, time).
- **Readability / navigation**: players must answer "Where am I? Where should I go? How do I get there?" Landmarks are large,
  unique and visible from most of the map, and come first in the blockout. Colour-code areas.
- **Events and secrets**: optional risky routes, dynamic elements; optional, never mandatory for fairness.

Minecraft-specific constraints (long-standing vanilla mechanics, not re-tested in 26.3; re-check if a number is critical):
player hitbox 0.6 × 1.8 (needs 2 blocks headroom); jump height ~1.25 (1 block step-ups, 1.5 needs stairs/slabs);
sprint-jump gap up to 4 blocks flat; fall damage starts above 3 blocks; arrows arc (long sightlines favour bows);
players place and break blocks (cover is dynamic, so designed cover should be protected/regrowing like the arena's
`clone masked` restore); ender pearls bypass chokepoints; mobs spawn only at block light 0 (light everything or disable spawns).

## 7. Tooling (Python and renderers), status October 2026

| Tool | What | Status / fit for 26.3 |
|---|---|---|
| **nbtlib** 2.0.4 | Read/write NBT; enough to write vanilla structure `.nbt` | Installed here. Old (2021) but format-agnostic. **[verified]** wrote a structure in the 26.3 layout and read it back. |
| Vanilla structure `.nbt` | `DataVersion`, `size`, `palette`, `blocks[{pos,state}]`, `entities` | **[verified]** in the 26.3 server jar: `DataVersion` **5023**, palette entries use lowercase **`id`** and **`properties`** (older versions: `Name`/`Properties`). Place with `/place template <ns>:<name> x y z` from `data/<ns>/structure/` (singular); no 48³ limit for `/place` (structure blocks are limited to 48³). |
| **amulet-core** 1.9.50 (2026-10-08) | Read/write whole worlds (region files) | Maintained; py ≥3.11. Use only if editing `.mca` directly; for this project prefer structures + `/place`. Version coverage for 26.3 not confirmed. [source] [repo](https://github.com/Amulet-Team/Amulet-Core) |
| **amulet-nbt** 2.1.8 | Fast NBT (C++) | No wheel for Python 3.13 on Windows → source build needs MSVC. **[verified]** (install failed here). |
| **mcschematic** 11.4.4 | Sponge `.schem` for WorldEdit | Latest version enum `JE_25W10A` (early 2025); no 26.x enum, DFU upgrades older data versions. Stores the full bounding box incl. air. **[verified]** [repo](https://github.com/Sloimayyy/mcschematic) |
| **litemapy** 0.11.0b0 | `.litematic` read/write, `Region.to_structure_nbt(mc_version)` | Beta, depends on nbtlib; useful to hand Nonios a Litematica preview. **[verified]** installs. [docs](https://litemapy.readthedocs.io/en/latest/) |
| **deepslate** / **deepslate-mcp** | WebGL renderer with real vanilla textures/models from `client.jar` | Best real-texture renderer. Node ≥20 + headless GL. Windows support of headless `gl` not confirmed. [source] |
| **structura-render** 0.8.3 | Python: `.nbt/.schem/.litematic` → PNG (perspective, orthographic, 6-view projections), SVG sections; textures from `STRUCTURA_MINECRAFT_ASSETS` (jar) | Targets 1.21.1 assets. **[verified]** does not install on Windows/Python 3.13 (needs amulet-nbt 2.x → compiler). Would need Python 3.11/3.12 or WSL. [repo](https://github.com/kirimba1024/structura-render) |
| **Chunky** | Path-traced world renders, headless (`-render`, `-snapshot`) | Beauty shots of the real world after placement, slow; not for the inner loop. [docs](https://chunky-dev.github.io/docs/reference/user_interface/chunky_launcher/headless/) |
| **moderngl** 5.13 + numpy + Pillow | Build our own renderer | All installed here. Client jar at `C:\Users\danir\curseforge\minecraft\Install\versions\26.3\26.3.jar` has 1405 block textures, 2884 block models, 1289 blockstates **[verified]**. |

**Average texture colours from the 26.3 jar** **[verified]** (luminance L 0-255; useful for value-ordered gradients and a
fast flat-colour renderer). See the playbook palette tables; computed by averaging each texture's opaque pixels.

## 8. Recommendations for this project

1. Keep design in **Python + NumPy** in `tools/voxel/` (a scene = a script that fills a `uint16` array plus a block-state palette).
2. Build a **small in-repo renderer** first (numpy face extraction → moderngl offscreen, textures or average colours from the
   26.3 client jar, sun + ambient occlusion). Views: iso from 4 corners, top orthographic, 2 eye-level shots from each team spawn,
   one sightline map (top view coloured by visibility from key points). This is the self-critique loop; it must run in seconds.
3. Export to **vanilla structure `.nbt`** (DataVersion 5023, `id`/`properties`), tile ≤48 per side only if needed, paste with
   `/place template` from the datapack (no mods). Explicit `minecraft:air` where carving; omitted voxels keep the world.
   Optional `.litematic` via litemapy for Nonios to inspect in Litematica.
4. After placement, confirm in-game with a screenshot (F2 feedback pipeline) or a Chunky beauty shot.
5. Treat the playbook's checklist as the critic's rubric; iterate one pass at a time, never detail before the silhouette and gameplay blockout are approved.


## Appendix A. Structure writer (tested with nbtlib 2.0.4; layout matches the 26.3 server jar's own structures)

```python
import numpy as np, nbtlib
from nbtlib.tag import Compound, List, Int, String
def write_structure(path, grid, palette, data_version=5023):
    """grid: int array [x,y,z]; 0 = leave untouched (omitted), k>0 -> palette[k-1] like 'minecraft:stone_stairs[facing=east]'."""
    pal, idx = [], {}
    def state(s):
        if s not in idx:
            name, _, props = s.partition('[')
            c = Compound({'id': String(name)})
            if props:
                c['properties'] = Compound({k: String(v) for k, v in (p.split('=') for p in props.rstrip(']').split(','))})
            idx[s] = len(pal); pal.append(c)
        return idx[s]
    blocks = [Compound({'pos': List[Int]([Int(x), Int(y), Int(z)]), 'state': Int(state(palette[grid[x,y,z]-1]))})
              for x, y, z in zip(*np.nonzero(grid))]
    root = Compound({'DataVersion': Int(data_version), 'size': List[Int]([Int(n) for n in grid.shape]),
                     'palette': List[Compound](pal), 'blocks': List[Compound](blocks), 'entities': List[Compound]([])})
    nbtlib.File(root).save(path, gzipped=True)
```

Usage: `write_structure('arena.nbt', grid, ['minecraft:air', 'minecraft:tuff', 'minecraft:oak_stairs[facing=east,half=bottom]'])`.
Not yet placed in-game: first use should `/place template` it on a test server and check the log.
