# The Orrery of Ast: pass log

Each pass names the three weakest things a viewer notices first, then fixes their causes.
Sheets: `.mcdev/voxel/out/orrery/history/<round>_<iter>_sheet.png`.

## Pass 1: blockout of the whole composition, plus walkability
The whole composition is blocked out: crater and lake, floating island, ring wall with 7 towers and a gatehouse, Spire, 3 rings, the Floating Stair, the Root Helix and Shaft Helix, and the zones.
- Walk model (`tools/voxel/walk.py`): 0 hard and 0 soft traps. Every zone is reachable from both spawns and has a way back.
- Rings re-chosen by a clearance search (axles only), and the turret, galleries and Gear Room re-plumbed.

Weakest three after pass 1 (fixed in pass 2 onward):
1. The rings read as three identical dark-teal tubes. There is no metalwork, no graduation and no different oxidation per ring.
2. From every eye view below the island, the underside is one dark, uniform cone. The amethyst drips are thin, and there are no roots, chains or foundations.
3. Castle facades are dark and flat, with almost no partial blocks or lights. The stats show partial-block share 0.04 and 0.18 lights per 100 m2.

## Pass 2: rings, underside, facades
Fixes for pass 1's weakest three:
1. Rings → open truss.
   - Two cut-copper rails, chiseled rungs at every degree tick (5°/5°/10°), and proud teeth every third tick.
   - Calcite tick marks on the outer face, and glyph plates with amethyst inlay and paired bulbs.
   - Each ring has its own body age plus an accent age: oxidized+fresh, weathered+exposed, exposed+oxidized.
   - Bands are thinner (hw 3.0/2.6/2.6, ht 1.2/1.1/1.0). The sky shows between the rungs.
2. Underside.
   - Lighter strata palette (tuff/dripstone), with bright double calcite seams every 9 blocks.
   - 12+ bleached pale-oak root trunks that split and end in pale moss. They are kept under the overhang, so they catch no falling player.
   - Three giant mooring chains (`moorings.py`, links 5 wide with alternating planes) run from hawses deep under the belly to capstan anchors on the crater slope. They pass the rim more than 23 blocks below it, so they are a fall, not a trap.
   - The torn cellars are now real sections: walls stop at the rim instead of hanging off it as brick boxes.
3. Facades.
   - Stair skin (`common.skin`) on every crown, eave, wing roof, gate pagoda and the Spire taper.
   - Needle and banded cones get copper ribs (8 and 6) over age bands.
   - The random calcite mottling is gone from MASONRY and SPIRE_BODY; the light stone is now only in structured trims.
- Walk: 0 hard and 0 soft traps.

Weakest three after pass 2:
1. The eye views from the crater floor and spawns are still dominated by the dark belly. The castle reads as a small crown on a tall dark column.
2. The gate approach: the top of the floating stair cuts a trench into the forecourt (eye_cam_gate), so the arrival at the gate is a hole, not a threshold.
3. The court and gallery views are dark and cramped. Few lights (0.29 per 100 m2 near facades), and the court has no focal light.

## Pass 3: the far highland
Fixes for pass 2's weakest three plus the quiet highland:
- Highland (new `highland.py`): the Fallen Arc (NW, broken sector of an older ring, R 24, faces the crater, two horns
  with rubble and a sunk glyph plate), the Old Observatory (NE: plinth, roofless tower, ramp to a sniper perch, fallen
  dome half sunk in the slope, fallen telescope), two oak groves with understorey, the pilgrims' road with lantern pylons,
  spawn plazas, amethyst shards over the heath.
- Gate approach: cam_gate re-aimed at the portal (the trench was fine, the camera was not).
- Fallen dome: its hollow shell on a slope made a 128-cell hard trap; filled with earth. Walk: 0 hard, 0 soft.
- Zones: Old Observatory (ground, perch). Cameras: cam_arc, cam_observatory.

Weakest three after pass 3:
1. The belly still dominates crater and spawn views (big, dark, uniform).
2. Lighting: court, gallery and walls are dark (0.35 lights/100 m2 near facades).
3. Facade palette is flat (top-5 share 0.49, partial blocks 0.08): trims and gradients needed.

## Pass 4: light, courses, the belly at night (sheet rendered at dusk)
- String courses: every 5th row of flat masonry becomes an upside-down stair of its own stone facing into the wall
  (drip groove, flush top: no new ledges); outer corners of round walls get outer-corner stairs (`common.relief`).
- Star lamps: lit copper bulbs set in the courses, chosen by column, so they stack in vertical strings on towers
  (20% of course cells above the deck, 8% below).
- Court: 8 lamp standards round the compass rose (copper cage + lantern), a lantern on every 4th merlon.
- Belly: 64 copper lanterns on chains of 2-11 links (thickest at the rim, clear of the stair and mooring chains);
  crystal stalactites get pearlescent froglight facets. At night the underside reads as a field of lamps.
- cam_court re-aimed into the court. Walk: 0 traps. Stats: top-5 0.49 -> 0.44 (PASS), metal 3.0 (PASS),
  facade lights 0.35 -> 0.91, partial 0.08 -> 0.14.

Weakest three after pass 4:
1. The gatehouse is not yet the densest element: a flat wall with a portal and random lamps.
2. Daylight belly is still one dark mass (lamps only help at night).
3. Rings: full-block truss (0 partial blocks), and the Spire heart is hidden from most views.

## Pass 5: the Astrolabe Gate
- The gate face was a flat wall: its rose window and hood moulding never existed (both tested the face plane on
  voxel centres and matched no cell). Rebuilt as `castle.gate_face`: a 14-block astrolabe over the portal (calcite
  mater, 12 oxidized-copper hour ticks proud of it, a fresh-copper rete of star lines, an exposed ecliptic ring,
  a chiseled alidade, an amethyst boss with a lit bulb) over violet glass that is also the Gate Room's window.
- Gate body raised to FLOOR + 26, Gate Room 16 tall. Two stepped buttresses (3 setbacks, stair caps, copper
  pinnacles with rods); on each first setback a waxed copper golem statue (pose "star") and a lantern.
- Star lamps masked off the gate face (it has its own composed lights). Walk: 0 traps.

Weakest three after pass 5:
1. Rings are full-block trusses: no partial blocks, the rails read flat close up.
2. The Spire heart (amethyst) is invisible from the court and the highland.
3. Daylight belly: still one dark mass from the crater.

## Pass 6: cable trusses, dripping amethyst
- Ring rungs between the rails are copper chains (axis = the ring's width axis, where it is within ~35 deg of a
  block axis): the rings become a cable truss with sky through it; rung ends at the rails stay chiseled.
- Belly: 96 stalactites (was 70), a third of them amethyst with pearlescent froglight facets (was a fifth): the
  dripping amethyst now covers the whole underside and breaks the dark mass in daylight too.
- Walk: 0 traps. Partial 0.14 -> 0.17, facade lights 0.92.

Weakest three after pass 6:
1. The Spire's middle (between the deck and the gallery) is a dark masonry cone; its heart is not shown.
2. Crater as a play space: the lake shore and causeway lack landmarks between spawn and the island.
3. Facade partial share (0.17) still low on the Spire body.
