# Vharzul: zones

The rooms of `scenes/vharzul.py` are **named empty shells**: walls, floors, doors and light only, with no furniture (by brief). Each zone is recorded in the scene meta (`s.meta["zones"]`: name, kind, interior-air box, mood, doors, must-haves) so a later decorator pass can furnish it with `tools.voxel.kits.rooms`.

Boxes are inclusive interior air. Scene coordinates first; world coordinates after placement use origin (-104, 30, -100). All 9 zones are reachable on foot from `spawn_approach`. The check is a walk graph: 4-neighbour moves, step or jump up 1, drop up to 3, from the spawn, with a way-back check for traps.

| zone | kind | mood | scene box (x0 y0 z0 – x1 y1 z1) | world box | size (w×d×h) | way in |
|---|---|---|---|---|---|---|
| forge_hall | hall | forge glow | 99 59 113 – 109 72 129 | -5 89 13 – 5 102 29 | 11×17×14 | Ember Bridge door (S), passage to the heart (N) |
| heart_sanctum | chapel | lava heart | 99 59 95 – 109 67 105 | -5 89 -5 – 5 97 5 | 11×11×9 | vaulted passage from the hall's north door |
| throne_lantern | hall | open crown | 99 149 95 – 109 161 105 | -5 179 -5 – 5 191 5 | 11×11×13 | the Ember Stair surfaces at the south of the floor |
| maw_guard_w | armoury | guard post | 91 42 156 – 96 46 166 | -13 72 56 – -8 76 66 | 6×11×5 | side door off the Maw throat |
| maw_guard_e | bedroom (barracks) | barracks | 112 42 156 – 117 46 166 | 8 72 56 – 13 76 66 | 6×11×5 | side door off the Maw throat |
| spire_se | lab | alchemy | 115 59 120 – 119 64 124 | 11 89 20 – 15 94 24 | 5×5×6 | passage from the bailey |
| spire_w | armoury | arsenal | 76 59 98 – 80 64 102 | -28 89 -2 – -24 94 2 | 5×5×6 | passage from the bailey |
| spire_ne | library | archive | 115 59 75 – 119 64 79 | 11 89 -25 – 15 94 -21 | 5×5×6 | passage from the bailey |
| undercroft | cellar | storage and gaol | 99 50 114 – 109 55 128 | -5 80 14 – 5 85 28 | 11×15×6 | 9-step stair down from the hall's west aisle |

## Must-haves for the decorator (from the zone meta)
- **forge_hall**:
  - anvils and smithing tables in the bays between the pilasters;
  - the lava channel is the runner;
  - a war table at the north end.
- **heart_sanctum**:
  - the caged lava column is the altar (the cage is built);
  - the spiral stair starts here (built: the Ember Stair).
- **throne_lantern**:
  - the Ember Throne on the north dais, facing south down the Tongue axis (the dais is built);
  - six open arches with balustrades (built);
  - a crucible brazier.
- **maw_guard_w**: weapon racks; arrow slits to the stair.
- **maw_guard_e**: bunks; chests; slits to the stair.
- **spire_se**, **spire_w**, **spire_ne**: alchemy, arsenal and archive respectively.
- **undercroft**: barrels and chests in bays; two cells with bars.

## Circulation (not zones, but walkable and lit)
- **Approach**: from the island tip, the pyre road (spear posts with skulls) leads to the Tongue (three flights, two landings with pedestals) and up to the Maw.
- **Maw throat**: stepped, with chained lanterns.
- **Ember Bridge**: two spans over the lava lake, with merlon parapets topped by wall copings, up to the Forge Hall door.
- **Bailey**: the ring round the Fang, marked by a cinnabar ember path. Spire passages open off it.
- **Ember Stair**: a helix of about 15 turns from the sanctum (y 59) to the throne (y 149). It is caged from the lava heart, the slits in the shaft are barred, and ember rings in the wall light it every 12 blocks.

## Spawns and sightlines
- `spawn_approach`: (104, 18, 229) scene = (0, 48, 129) world. Attackers, on the island tip, facing the Maw.
- `spawn_defender`: (101, 59, 115) scene = (-3, 89, 15) world. Defenders, in the Forge Hall, facing the bridge door.
- The sightline map (`render` → `sightlines.png`) shows the approach axis covered from the hall door and the Maw. The outer plain is open ground with spear bundles and boulders for cover.

## Known gaps
- Wall tops (the star wall, rim crest and Maw brow) are scenery: there is no wall-walk circuit.
- The outer pier ledges of the bridge are left by ladders, which the walk graph doesn't model.
- A few 1–4 cell nooks on the lake shore can be entered but not left by walking (lava-side).
