# Voxel build playbook (paste into the brief of any session that designs terrain, arenas or buildings)

Evidence and links: [`voxel-research.md`](voxel-research.md). Target: Minecraft Java 26.3 vanilla, no mods.

## 0. The one-paragraph brief

You are designing a Minecraft PvP arena as **code**, not as hand-placed blocks. Write a Python script that fills a NumPy voxel
array, render it, look at the renders, critique them against the checklist below, fix, re-render. Only convert to blocks
when the renders pass. Your untutored default is "a plank box with a stair roof on flat grass" (distributional convergence):
that is the failure this playbook exists to prevent. Commit to a specific named aesthetic, get the gameplay layout and the
silhouette right before any detail, and never leave a flat wall, flat ground or a single-block surface.

## 1. Workflow (one pass at a time, render after each)

| # | Pass | Output | Gate (must be true before the next pass) |
|---|---|---|---|
| 1 | **Brief** | 3 lines: aesthetic name, mood, 3-5 references (real places / pro builds), scale, palette families | Not "medieval castle": something like "collapsed basalt caldera, weathered-copper shrine, ash and moss" |
| 2 | **Gameplay blockout** | Plain blocks: spawns, Nexus approach, lanes, chokepoints, high ground, cover, centre node | Measured: travel times equal per team; no point covers all chokes; sightline map OK |
| 3 | **Massing** | 3-4 primary masses + the landmark, at different heights | Top + side renders read as distinct shapes; landmark visible from both spawns |
| 4 | **Silhouette** | Skyline and edge shapes | Side renders against the sky are not rectangles; no "box on box" |
| 5 | **Terrain / organic** | Heightfield + SDF rocks, erosion, overhangs, transitions into structures | No terraces (Y-band steps), no flat plains > 8x8, no hard seams |
| 6 | **Depth** | Frames, pulled pillars, recesses, ledges, overhangs, sub-block layer | Every wall > 5 wide has ≥ 2 depth levels; eye-level render shows shadow pockets |
| 7 | **Palette / gradient** | Value-ordered gradients, clustered noise, team colours | No large single-block surface; dark low → light high; 60/30/10 |
| 8 | **Light** | Visible lanterns/froglights + hidden light | No block light 0 on walkable surfaces (or spawns disabled); reads at dusk |
| 9 | **Decoration / ecology** | Foliage, rubble, banners, props, path wear | Detail concentrated at focal points, not sprinkled evenly |
| 10 | **Convert + verify** | Structure `.nbt`, `/place template`, in-game screenshot | Matches the renders; play-test the routes |

Rules for the loop: change one thing per iteration; state the expected visual change before re-rendering; keep the scene
script modular (one function per element, parameters at the top) so edits stay local; keep every render in
`renders/<pass>_<n>_<view>.png` and compare with the previous one.

## 2. Render set and critique prompt

Every iteration renders: **iso** from 4 corners, **top** orthographic, **eye level** (1.6 blocks up) from each spawn and from the
centre, and for arenas a **sightline map** (top view, cells coloured by how many key points can see them). Eye-level views
expose flat walls and bare cliffs that top-down hides.

Critique prompt (send with the renders, plus references if any):
```
You are a pro Minecraft builder and a competitive level designer judging this render set.
List concrete defects, most severe first, each with the element, the view, and a fix in terms of the
scene script's parameters. Check: silhouette (box-on-box?), flat walls/ground, single-block surfaces,
palette value order and monoculture, scale (doors 2-3 high, storeys 4-5), floating parts, seams,
terraces, readability of lanes/chokes/landmark, team colour coding, symmetry fairness.
Do not praise. Max 10 items. Then say which single change will improve it most.
```

## 3. Do / Don't

**Do**
- Write a program: `box`, `line`, `cylinder`, `ellipsoid`, `sdf_fill`, `heightfield`, `noise`, `scatter`, `gradient`, `mirror`.
- Plan proportions, silhouette and materials before code ("think hardest before writing code").
- Primary mass → secondary (1/3-1/2 size) → tertiary detail. Focal point ≥ 25% taller/wider than its surroundings.
- Odd widths (5, 7, 9, 11...) for anything with a centre (gates, ridges, the Nexus housing).
- Three depth layers on walls: frame (pillars/beams pulled out 1), infill, sub-block (stairs, slabs, walls, fences, trapdoors, buttons, panes, chains).
- On long walls push/pull a column every 3-4 blocks; roofs overhang 1-2 blocks.
- Terrain from heightfields + 3D noise + erosion; slope decides material (rock on steep faces, soil on gentle, path wear on routes).
- Drive material choice with *low-frequency* noise so patches cluster; replace ~25-35% of a surface with gradient neighbours.
- Ground everything: bases flare into terrain, rubble at the foot of walls, roots/vines where structure meets rock.
- Rotate one team half 180° for fairness; vary only cosmetic details per side (seeded).
- Use stairs/slabs for 0.5-block steps on walkable slopes so players don't have to jump every block.

**Don't**
- Don't place blocks one by one in a list, and don't build directly in-world as the design step.
- No flat walls, flat ground, perfect cylinders/spheres left raw, or "painted" features (colour standing in for geometry).
- No Y-band stacking (ziggurat terraces) for terrain; no salt-and-pepper random block noise.
- No floating objects, no unlit caves, no dead-end pockets in the arena that trap players without a reason.
- Don't detail before the silhouette and the gameplay blockout pass; detail can't save a wrong silhouette.
- Don't use more than ~4-5 blocks per material family or more than 2-3 families in one area.
- Don't let the defaults in: oak planks + cobblestone + glass panes + stair roof on grass. If it appears, justify it or replace it.

## 4. Arena design rules (Nexus PvP)

- **Layout**: 3 lanes from each base to the centre, 1 chokepoint per lane; no single position sees all chokes; teams reach the
  centre at the same time (± 1 s; equal path lengths measured in the script).
- **Symmetry**: 180° rotation of one half (point symmetry). Landmark on the axis (centre generator); each half has its own
  secondary landmark in team colour.
- **Sightlines**: mix of short (≤ 12 blocks, melee) and long (30+, bows) with cover breaking every long line; long lines cost
  exposure to use. Bows dominate open ground, so the centre needs full cover pieces 2-3 high.
- **Cover**: err on too little; full cover (≥ 2 high) to advance, half cover (1 high / slab walls) at fight spots. Players can place
  blocks, so designed cover must be protected (arena restore) or it becomes a pillar-up meta.
- **Verticality**: 2-3 height levels; high ground costs time or an exposed route. Climb with stairs/slabs/ladders/scaffolding,
  1-block step-ups max, 2 blocks headroom, sprint-jump gaps ≤ 3 (4 is max, too punishing). Falls > 3 hurt; void edges need intent.
- **Readability**: team colours on the team's half (red/blue concrete, terracotta, wool, banners, stained glass) in accents,
  not whole surfaces; neutral palette in the centre; the landmark visible from every spawn; distinct material themes per lane
  so call-outs are possible ("copper lane", "moss lane").
- **Mobs/light**: light every walkable surface above 0 or keep `spawn_mobs` off.

## 5. Palette tables (average texture colour from the 26.3 client jar, L = luminance 0-255, "tex" = texture contrast)

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

**Team red**: red_nether_bricks 20 · crimson_nylium 52 · red_concrete 56 · red_wool 64 · red_terracotta 77 · red_glazed_terracotta 85
**Team blue**: blue_concrete 53 · blue_wool 63 · blue_terracotta 65 · cyan_terracotta 90 · warped_wart_block 99 · light_blue_concrete 119

**Ready-made gradients** (bottom → top, or shadow → light):
- Ruined fortress: blackstone → cobbled_deepslate → tuff → stone_bricks / mossy_stone_bricks (cluster) → andesite → smooth_stone trim
- Volcanic: obsidian (accents) → blackstone → basalt → polished_basalt → tuff → magma_block / shroomlight for hidden glow
- Canyon: packed_mud → terracotta → granite → cut_red_sandstone → sandstone → smooth_sandstone (top bands, broken by noise, not stripes)
- Overgrown: mud → rooted_dirt → moss_block → grass, with mossy_cobblestone / mossy_stone_bricks where stone meets soil
- Copper temple: weathered/oxidized copper roofs, exposed copper trim, tuff_bricks walls, calcite inlay

Rule of thumb: neighbours in a gradient should differ by ~10-25 L; jumps > 40 read as stripes. Mix "busy" textures (high tex)
with calm ones (low tex) so surfaces don't buzz.

## 6. Code skeleton and conversion

```python
import numpy as np
P = ["minecraft:air", "minecraft:blackstone", "minecraft:tuff", "minecraft:stone_bricks"]  # index 0 in grid = untouched
grid = np.zeros((W, H, D), np.uint16)   # x, y, z; value k>0 -> P[k-1]
# ... massing(grid); terrain(grid); depth(grid); palette(grid); light(grid); decorate(grid) ...
```
Write a vanilla structure (verified layout of 26.3 files): `DataVersion` **5023**, `size [x,y,z]`, `palette` entries
`{id:"minecraft:oak_stairs", properties:{facing:"east",half:"bottom"}}` (26.x uses lowercase `id`/`properties`),
`blocks` list of `{pos:[x,y,z], state:i}`, `entities: []`; gzip; save as `data/nonios/structure/<name>.nbt` and place with
`/place template nonios:<name> x y z` (no 48³ limit, unlike structure blocks). Omitted voxels leave the world as is; use
`minecraft:air` explicitly to carve. A tested `nbtlib` writer is in `voxel-research.md` (appendix A); port it to `tools/voxel/`.
Directional blocks (stairs, logs, walls, panes, fences) need correct states: compute `facing`/`shape`/connections from
neighbours in a final "states" pass instead of guessing.

## 7. Quality checklist (the critic's rubric; all must pass)

- [ ] Named aesthetic and references stated; palette ≤ 3 families × ≤ 5 blocks each.
- [ ] Gameplay: 3 lanes, a choke per lane, equal travel times, no all-seeing spot, long sightlines broken by cover.
- [ ] Landmark readable from every spawn; team halves identifiable at a glance (accents, not floods of colour).
- [ ] Silhouette: side renders show varied skyline; ≥ 3 masses at different heights; no box-on-box.
- [ ] No flat wall wider than 5, no flat ground larger than 8x8, no single-block surface larger than ~16 blocks.
- [ ] Gradients run dark low → light high, clustered, ≤ 25 L per step; no stripes, no salt-and-pepper.
- [ ] Terrain: no terraces, no seams, overhangs or undercuts somewhere, erosion visible, structures grounded.
- [ ] Sub-block detail (stairs/slabs/walls/trapdoors/fences) on edges, frames and openings.
- [ ] Scale sane: 2-block headroom on routes, doors 2-3 high, storeys 4-5, step-ups ≤ 1, gaps ≤ 3.
- [ ] Lit: no walkable light-0 surface (or mob spawning off).
- [ ] Eye-level renders from each spawn look like a place, not a diagram.
- [ ] Block states valid in 26.3 (load the structure once; check the server log).
