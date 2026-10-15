# Vharzul: pass notes

Each pass: render (day + ember), the three weakest things a viewer notices first, and what fixed their cause.
Sheets: `.mcdev/voxel/out/vharzul/history/p<N>_sheet.png`. `VHARZUL_PASS=<n>` rebuilds the state after pass n.

## P1: blockout (whole composition)
Built: teardrop island (south tongue carries the approach), ash plain with cooled lava tongues, crater + lava lake, breach gorge
+ edge fall, basalt-organ plug, star wall, Fang (twisted star prism, hollow shaft, lava heart, throne lantern bulb), 3 obsidian
horns, 3 spires, Forge Hall with cinnabar roof, Ember Bridge, Maw gatehouse with crossed bone tusks, processional stair, barbican,
pyre road, outer-ring sub-places (Field of Spears SE, Teeth obelisks N, Wyrm skeleton W, Slag Works NW, sulfur fumaroles NE),
room boxes (meta zones). Palette families set: lighter ash ground, mid-grey masonry, obsidian focal, sulfur/bone trims, cinnabar roof.

Weakest three (P1 sheet):
1. The approach: the barbican is a blank 16-high box that fills the spawn view; the Maw is a dark lump whose only feature is the
   bone arch of the tusks (the tusks out-shout the gate; the gate has no frame).
2. The fort still reads black: star wall, rim wall and spires are flat dark masses with no depth planes and no trim in view;
   only the hall roof and the horn bands give colour. In daylight it is a silhouette, not architecture.
3. The outer ring sub-places don't read: the Wyrm ribs are lumps, the obelisks are tiny, the slag works vanish at iso distance.
Also: horn gold bands read as wasp stripes (cut to one band each in P1); cam_bailey is inside a wall.

## P2: facades, depth layers, the Maw
Fixes for P1's list:
1. Approach -> the Maw is now a demon face and the densest element: mouth arch with three nested archivolts stepping back
   (sulfur -> polished basalt -> dark bricks), bone teeth on the intrados, raised portcullis, a machicolated brow on corbels,
   two slanted lava "eyes" behind bars, battered cheek piers with sulfur caps, and two diamond-section jaw towers that twist
   outward (the Fang's family) with collars; the tusks now flank and curl instead of meeting, so the jaws + tusks frame the
   Fang from the road. The barbican became the Pylons: two horned bastions with a low breastwork and an open gap, so the
   spawn view is pylons -> tusks -> Maw -> jaws -> Fang on one axis (three nested frames).
2. Black fort -> depth stack on the star wall (battered basalt plinth, 12 stepped buttresses, sulfur string course, corbel
   + machicolation band, sulfur cornice, merlons with polished basalt caps, arrow slits), the rim wall (battered skirt,
   buttresses every 11 blocks, sulfur string course, caps), the Fang's six twisting arrises in polished basalt, Forge Hall
   buttress piers + arched door with archivolts + barred gable window. Body palette lightened with tuff bricks.
3. Outer ring: deferred to P6 (terrain pass), it needs the ground work.

Weakest three (P2 sheet):
1. Skyline: spires, rim fangs and star points are the same grey jagged cones; horns are smooth tubes without ribs; the
   Fang collars are thin; only the hall has a roof. No hierarchy of crowns.
2. Palette by absolute y: every outwork low on the island (pylons, Maw base, rim skirt) falls in the darkest blackstone band,
   so the approach is black where the viewer stands. Trims are all the same flat sulfur.
3. Outer ring still unreadable (ribs = lumps, NE fumaroles = yellow blobs at eye level, cam_ash_ne buried in a spike).

## P3: rooflines, spikes, collars, skyline
Fixes for P2's list:
1. Skyline hierarchy: three spires with three silhouettes: the Alembic (SE: round tower, cinnabar dome, three flues, sulfur
   needle, gold tip), the Blade (W: twisted square tower, machicolation, tile pyramid, four bone corner thorns), the Bell
   (NE: hexagonal, open belfry with six arches, twisted cinnabar needle, gold finial). Fang collars got six curved thorns
   each (basalt to bone, 24 total, spaced so the Fang reads as a thorned stem), the throne lantern a sulfur cornice and
   six obsidian/gold crown thorns. Horns got 13 growth ridges each (shadow texture) and three bone thorns on the outer
   curve. The Maw jaws were pulled 4 blocks forward (they were hidden behind the brow from the stair; checked with a
   stair-foot camera) and got bone needle tips; Forge Hall got ridge thorns and buttress pinnacles with cinnabar caps.
2./3. Palette and outer ring: P4 and P6.

Weakest three (P3 sheet):
1. The horns are two huge black blobs in the hero view: obsidian with obsidian ridges, no colour or value change until the
   tips. The Fang body is still a plain black column between collars.
2. The approach is still black at eye level: the WALL gradient is by absolute y, so pylons, cheek piers, stair and the
   Maw's lower body all use the darkest stop; the stair is a featureless dark ramp.
3. Rim fangs and the field of spears are one repeated grey cone; they make noise rather than places.

## P4: palette gradients, texture mixing, light copings
Fixes for P3's list:
1. Horns: three crisp cinnabar growth rings each (slab-cut so they are 2 blocks wide, not blotches; a first try with
   ridge-replacement turned the horns into red/black camouflage and was thrown away), the gold band re-cut the same way.
   The red ties the horns to the hall roof, the Alembic dome and the Bell needle. Fang kept black on purpose (the focal
   dark), its arrises carry the light.
2. Walls are now one masonry family and `weather()` grades them by height above their OWN foot (column run), not by
   world y: dark plinth (0-3) -> deepslate body -> tuff-mixed upper body in noise patches -> cracked variants. Every
   sky-facing masonry edge gets a pale polished-tuff coping, so steps, merlons, buttress tops and jaw shoulders read as
   lines in daylight. The pylons, Maw and walls are now mid-grey with light edges instead of black.
3. Ember render checked: lava ring + falls + Maw eyes carry it; fixtures still missing (P7).

Weakest three (P4 sheet):
1. The processional stair is a 25-block dark ramp with no landings, parapets, lamps or statues; the road is a flat strip.
2. Outer ring: NE fumaroles are yellow boxes at eye level, rim fangs and spears are one repeated cone, the ash plain is
   flat noise, the island edge is a straight cut.
3. Night read: no fixtures at all; the throne lantern is dark; rooms are black.

## P5: bridges, stairs, approaches
Fixed (P4 weakest #1, the stair was a dark ramp):
- **The Tongue** (`processional2`): a 5-block threshold landing under the archivolts, then flights of 7, 7 and 6 with 3-deep landings. Every step is a real stair block (`lay_steps`: a stair where the next column down is exactly one lower), so the whole run is walkable without jumping. Pale polished-tuff flanks, a cinnabar runner pouring out of the Maw down the centre, tuff-wall parapets, and parapet gaps at each landing onto pedestals with a sulfur cap and a bone thorn.
- **Pyre road** (`road2`): pale tread with dark kerbs, basalt spear posts with bone tips every 5 blocks. The Pylons moved to stair foot + 9 so they stay on the island tip, and the spawn stays on the ground.
- **Ember Bridge** (`bridge2`): two pointed spans on piers over the lava, from the throat (GATE_I) up to the Forge Hall door (DECK). Stepped deck with stairs and a runner, merlon parapets, and a sulfur string course. New marker `cam_bridge`.
- `throat_steps`: the Maw's rising throat is stairs, not a slope.
- Build-order bug: `spires()` also ran at PASS 3. Fixed.

Weakest three now:
1. Outer ring: fumaroles read as yellow boxes, the rim spikes are repetitive cones, the ash plain is flat, and the island edge is a plain extrusion (cam_ash_ne, cam_breach).
2. No fixtures and no night read: the interiors are black, there are no lamps on the Tongue or the bridge, and the throne lantern is dark.
3. The cinnabar runner is a flat, single-texture field and the steps are monotone. It needs edge trim and lamp posts on the landings (P7).

## P6: terrain transitions, the outer ring
Fixed (P5 weakest #1, the outer ring):
- **Causeway edge** (`causeway`): the island edge is a crown of hexagonal basalt columns that echo the plug's organ pipes. Tops step up 2 to 6 blocks at the brink as a ragged palisade, and the inner cells rise 0 to 1, so there are no pits. Below the brink, organ pipes of uneven length hang down (15% are "great pipes" +18), and some have magma tips that glow at night. Dark joints run only in the upper band, ash fades onto the inner caps, and the road tip is kept level. The cliff now reads as a curtain of columns instead of an extruded wall.
- **Sulfur Terraces** (`sulfur_terraces`, replaces the 9 fumarole boxes): three travertine mounds of one-block terraces (walkable) with wobbly sulfur rims, calcite floors, a lava eye with a `potent_sulfur[continuous]` vent, and sulfur spikes.
- **Spear bundles** (`spear_clusters`, replaces 130 identical cones): 22 splayed bundles of 3 to 6 curved shards from a common basalt root. Each has a tall leader with a polished or bone tip, and there are 45 scoria boulders on the ash. Dense in the SE.
- Cameras fixed: cam_ash_ne is no longer inside a spike, cam_breach now looks down the gorge from the lake, and cam_bailey looks along the bailey canyon.

Weakest three now:
1. No fixtures and no night read (P7): black rooms, no lamps on the Tongue, bridge or bailey, a dark throne lantern, and an unlit Maw throat.
2. The bailey is a canyon 5 to 8 wide between the Fang, the horn roots and a 14-high star wall. It is dramatic but dark and has no hero courtyard. It needs light, and an opened, legible route around the ring.
3. Zones are unchecked: reachability, windows, and the spawn and defender markers.
