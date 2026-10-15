# Why the EliteCraft admin base works: a builder's breakdown
Reference: ElRichMC, EliteCraft 2 Ep 14, "La base del administrador" (https://www.youtube.com/watch?v=oj-qAh5RVW4). Frames: see README.md (local-only stills).

## 0. Vanilla or not?
- Textures: vanilla default (1.17-era; screenshot message dated 2021-09-01). No resource pack.
- Shaders: none. Flat vanilla smooth lighting, no shadows or bloom, vanilla water; night shots are genuinely dark.
- Plugins: buff HUD, chat ranks and custom item names only. Every block is placeable in vanilla 26.3.
- FOV is about 100 and the camera is a handheld survival view, so judge proportions from the straight-on shots (3940, 0156).

## 1. Concept and silhouette
- One theme pushed everywhere: a "Nether cathedral" in black, red and soul-cyan.
- 3 height tiers stepping back: a dominant slab keep (about 2x anything else), mid wings and towers, low gate towers in front (3940, 1236, 3116).
- Every roofline is crowned with spikes at a 1–2 block pitch.
- Symmetric main axis: sea → causeway → gate towers → plaza → portal → keep → skull mosaic. The wings vary (domed tower on the left, red chapel on the right).
- Designed plan (3528): bastioned outline, round corner towers, radial plaza, long bridge.

## 2. Palette and gradients
| Role | Blocks | Share |
|---|---|---|
| Base | polished blackstone bricks, blackstone, deepslate bricks/tiles, cracked variants | ~55% |
| Accent | red nether bricks, nether wart block | ~20% |
| Trim | light grey stone family (polished andesite / stone bricks / smooth stone / calcite-tone) | ~15% |
| Pattern tiles | chiseled blocks with concentric-square faces (pavement medallions) | ~3% |
| Glow | soul fire, soul lanterns, cyan accents, shroomlight, lava under red stained glass | ~4% |
| Feature | purple nether portal / amethyst (shrine only) | ~1% |
| Ground | coarse/rooted dirt with crimson specks, water | — |

Rules: 3+1 colours; the base is a noisy mix of 3–4 blocks; the accent follows structure; the light trim marks the outermost depth edges and pinnacles.

## 3. Depth layering
- Main facade (0156): 4–5 planes: wall; lancet recesses (−1); pilasters (+1); buttress or pinnacle shafts (+2); portal frame and mosaic (+2/+3); stairs, braziers and lamps in front.
- Portal (0220): about 6 concentric recessed arch rings (−1 each), alternating dark/light; red flame voussoirs radiate 3–5 blocks outward. Opening about 7 wide; composition about 25 wide (frame is 3–4x the opening).
- Tower drums: 4–8 grey pinnacle shafts attached, standing 1–2 blocks proud and rising above the eave.
- No flat wall over about 5x5 on a primary facade.

## 4. Detail density
- On primary facades, about every 3x3 patch has a change (block, depth, or a partial block).
- Secondary walls are banded, with pilasters every 4–6 blocks.
- Stairs make the voussoirs and eaves; walls make the pinnacles and lamp posts; slabs make steps and relief; chains and lanterns make hanging lights. The mosaics are full-block pixel art.

## 5. Roofs, towers, spires
- Flared pagoda roofs on the gate towers: 2–3 stair-ring tiers kicking out at the eave, red with dark bands, a soul-lantern ring under the top.
- Steep (about 1:1 or more) red gabled chapel roof with spiky dormers.
- Shrine: a stepped triangular gable with spikes on every step (fractal outline), filled with purple portal.
- Keep: flat top with a crown of corner spires; height comes from mass.
- Patterned roof surfaces (diagonal red stripes, 2104).

## 6. Entrances
- The entrance is the most detailed element: nested arches, about 8 approach steps with a red runner, lanterns on the jambs, a flame crown.
- 3 thresholds before the door: bridge-head gate towers, plaza braziers, portal.

## 7. Interiors
- Long naves with a repeated rib frame every 4–5 blocks and a focal end (rose mosaic or portal) (0420, 1352).
- Storage (barrels, chests) fills the bays to head height: function becomes texture.
- Patterned floors everywhere: irregular grey/white/blackstone checker; lava under red glass; red carpet runners; two-tone wood checker in the library.
- Designed ceilings: radial rib vault around a glass rose (0508).
- Lighting is in fixtures (lava strips, shroomlight sconces, lanterns on chains). Interiors are dark with pools of light.

## 8. Scale
- Keep about 60+ tall, chapel ridge about 30, gate towers 20–25 (ratio about 1 : 0.5 : 0.35).
- Gate opening about 7x10–12; causeway about 7 wide by 40 long; halls 15–20 wide and 15+ tall.

## 9. Terrain
- Nether-tinted ground (coarse/rooted dirt with crimson specks) matches the palette; stepped plinths; raised plaza with a stepped water edge.
- Weakness: crude flat dirt slopes and an abrupt shoreline. Beat this.

## 10. Weaknesses not to copy
Crude terrain with no ground gradient and few plants; simpler side walls; very dark interiors (bad for gameplay readability); sky-pole clutter.

## Critic rubric checks
1. ≤ 4 colour families per structure; the feature colour is ≤ 2% of visible blocks.
2. The dominant family uses ≥ 3 block types; no single block covers > 60% of a facade.
3. Primary facades have ≥ 4 depth planes; secondary ≥ 2.
4. No single-plane, single-block patch > 5x5 on primary facades (8x8 secondary).
5. Partial blocks (stairs, slabs, walls, fences, trapdoors, chains, lanterns) are ≥ 15% of primary facade surface blocks.
6. ≥ 80% of accent blocks lie on aligned structural runs (pilasters, edges, ribs, bands).
7. On landmarks, the roofline height changes at least every 3 blocks along 20 blocks; no flat roofline longer than 8.
8. Landmark complexes have ≥ 3 height tiers; the tallest is ≥ 1.7x the second.
9. The main portal frame is ≥ 3x the opening width, has ≥ 3 nested recess rings, and is the highest-density element.
10. Approach, entrance and dominant mass share one axis; the wings vary (no exact clones except the flanking pair).
11. Long rooms repeat a bay every 3–6 blocks; end walls have a focal feature.
12. Interiors over 50 m² have a patterned floor (≥ 2 materials) and a designed ceiling.
13. Light comes from designed fixtures; no bare torch or glowstone grids; gameplay floors at light level ≥ 7.
14. ≥ 2 ground materials blend between the plinth and natural ground; no straight 1-block shoreline.

## Generator rules
- palette: {base:[3–4], accent:[1–2], trim:[1–2], feature:[1], glow:[...]}; base sampled with weighted noise (50/25/15/10).
- facade: plane → recessed openings (−1) → pilasters every 4–6 (+1, accent) → corner and bay-edge pinnacle shafts (+2, trim) → spike-row cap at a 1–2 block pitch.
- portal(w): n = max(3, w/2) nested pointed arches at −1 each, alternating trim/base; outward accent voussoirs extending 0.3w–0.5w; stair approach with a centre runner; paired jamb lanterns.
- tower(r): drum plus 4–8 trim shafts rising 3–6 above the eave; flared stair-ring pagoda roof (2–3 tiers, +1 kick per eave) or stepped spire; a glow ring at the eave.
- skyline post-pass: a spike or crenel every 1–2 roof-edge blocks on landmarks.
- hall: rib bays every 4–6 (accent rib, base infill); functional blocks fill the bays to head height; patterned floor with an emissive centre strip under stained glass; ribbed or radial ceiling; end-wall rose or portal.
- lighting: lanterns on chains of 1–3 links at bay centres, rib sconces, emissive floor strips; no exposed torches on primary surfaces.
- ground: 2–3 step plinth → paved plaza with medallion tiles every 6–8 → a 3–5 block blend band → an irregular, vegetated shoreline.
