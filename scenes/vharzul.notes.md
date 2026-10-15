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
