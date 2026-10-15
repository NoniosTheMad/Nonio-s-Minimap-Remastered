# The Orrery of Ast: art direction

**Story in one line:** an astronomer-mage tore the summit off a mountain and hung it over the crater it left. On the summit stand a ring-walled castle and the Spire, and three armillary rings turn round the Spire on axles.

## The three reads, in order
1. **Silhouette (1 km):** a floating cone with the Spire needle on top and three tilted rings crossing the needle. The crater below repeats the island's outline as a hole. The Spire is the only vertical, and the rings are the only curves in the sky.
2. **Massing (200 m):**
   - the ring wall with 7 needle towers and the Astrolabe Gate;
   - the three mooring chains tying the island to the ground;
   - the Floating Stair from the crater to the gate;
   - the Fallen Arc and Old Observatory on the highland, which echo the rings and the Spire at ground level, in ruin.
3. **Detail (eye level):**
   - string courses every 5 blocks;
   - copper ribs on the cones;
   - graduated ring trusses, with ticks, rungs and glyph plates;
   - the astrolabe window over the gate;
   - lanterns hung under the belly.

## Palette roles (`scenes/orrery_parts/common.py`)

| Role | Material | Where |
|---|---|---|
| Ground rock | `ROCK`: deepslate, then tuff, then tuff/andesite/calcite as y rises | crater, highland |
| Underside | `UNDERSIDE`: dark deepslate at the tip, tuff/dripstone higher up; calcite seams every 9 | the belly |
| Masonry | `MASONRY`: deepslate bricks at the base, then tuff bricks, then polished tuff | wall, towers, wings |
| Spire | `SPIRE_BODY`: darkest at the foot, calcite and quartz at the lantern | the Spire (lightens with height) |
| Trim | `TRIM`: calcite / smooth quartz | crowns, linings, ticks, seams; structured, never mottled |
| Feature | amethyst + purple glass | the heart, the Focus, lancets, the astrolabe; the magic colour, used sparingly |
| Metal | waxed copper only, in all four ages | rings, cones, chains, lamps |

Waxed copper must stay unchanged in the map, so every copper block is `waxed_`. Ages tell parts apart: ring 1 is oxidized + fresh, ring 2 is weathered + exposed, ring 3 is exposed + oxidized. Fresh copper marks the newest repairs and the instruments: the rete, alidade and chiseled hubs.

## Light
- **Day:** warm stone against a cool copper-green.
- **Night:** the build should read as a star field.
  - Copper bulbs sit in vertical strings on the courses. The gate face is kept dark so the astrolabe window wins.
  - 64 lanterns hang under the belly, and court standards stand at 8 points.
  - The violet heart glows up the Root Shaft.
- No torches. Light comes from copper bulbs, copper lanterns, froglights inside the amethyst, and glowstone in the Focus.

## Rules
- No vines and no spreading or decaying blocks: `stability.fix_soil` runs last. Hanging dripstone must be held from above (`finish.loose_dripstone`).
- Every drop is either a lethal edge or has a way back. `tools/voxel/walk.py` must report 0 hard and 0 soft traps.
- Interiors stay empty: `s.meta["zones"]` and `docs/builds/orrery-zones.md` hand them to the furnishing pass.
- Text in game is diegetic and terse.
