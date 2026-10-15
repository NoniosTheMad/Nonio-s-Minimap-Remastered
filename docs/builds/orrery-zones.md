# The Orrery of Ast: interior zones

Empty, named interior volumes registered in `s.meta["zones"]` by `scenes/orrery_parts/rooms.py` (walls, floors, ceilings,
openings and windows are built; nothing is furnished). Every zone is reachable from both spawns
(`python -m tools.voxel.walk scenes/orrery.py` checks each one).

Box = interior air volume, inclusive, scene coordinates (x0 y0 z0 .. x1 y1 z1). World = scene + origin (-104, 20, -104).
Floor = top cell of the floor (feet stand at floor + 1). Type = the furnishing kind the zone is meant for.

## The Spire

| Zone | Type | Box | Floor | Mood | Must-have features |
|---|---|---|---|---|---|
| Orrery Hall | hall | 92 109 92 .. 115 128 115 | 108 | solemn, cold light from the lancets, the heart glowing up through the oculus | oculus over the Root Shaft (keep clear, r 7); star-map floor inlay; 11 lancets; south door; turret door (NNW); orrery model / central instrument around the oculus rim |
| Star Archive | library | 94 131 94 .. 113 148 113 | 130 | hushed, dusty, star charts and catalogues | tall shelves against the curved wall; mezzanine possible (18 tall); door from the stair turret |
| Gallery Room | hall | 96 151 96 .. 111 157 111 | 150 | bright, wind, the rings sweeping past the doors | 4 doors to the gallery deck (r 21.5, wraps the turret); turret arrival; stair up to the Gear Room (keep the helix clear) |
| Gear Room | lab | 97 163 97 .. 110 176 110 | 162 | mechanical, copper and oil, the axles turning under the grate floor | copper grate floor over the shaft deck (axles + central gear drum visible below); helix stair on the wall |
| Lens Room | lab | 99 179 99 .. 108 190 108 | 178 | focused, purple light, the lens grinder's workshop | doors to the upper deck (r 12.5); helix stair to the Lantern |
| Lantern | chapel | 97 193 97 .. 110 205 110 | 192 | open sky, the Focus floating overhead | open cage (8 posts, bars rail); the Focus (amethyst octahedron, glowstone core) overhead: keep clear |

## Castle wings and gate

| Zone | Type | Box | Floor | Mood | Must-have features |
|---|---|---|---|---|---|
| Library | library | 79 109 95 .. 86 119 113 | 108 | warm, wood and candlelight, purple lancet light | 5 lancets per long side; door to the court (east); inner door to the West Watch (north end) |
| Chart Room | lab | 122 109 95 .. 129 117 113 | 108 | bright, maps and brass, a table under the lancets | door to the court (west); instrument terrace on the flat roof |
| Kitchen | kitchen | 97 109 78 .. 111 114 84 | 108 | smoky, hearth light, busy | door to the court (south); stair up to the Quarters (north wall, keep clear); door to the Needle Tower (north) |
| Quarters | bedroom | 97 116 78 .. 111 121 84 | 115 | quiet, low, wooden floor, the court below the windows | stair hole with balustrade (north); windows to the court |
| Gate Room | armoury | 97 117 131 .. 111 132 137 | 116 | martial, tall, the astrolabe window glowing violet over the gate | astrolabe window (south, upper wall); two wall-walk doors (east/west); murder slots over the passage possible; gallery possible at mid height (16 tall) |

## Towers

| Zone | Type | Box | Floor | Mood | Must-have features |
|---|---|---|---|---|---|
| Dome Tower (ground) | observatory | 127 109 116 .. 135 115 123 | 108 | narrow, slit light | court door; ladder to the upper room (outer wall); slit windows |
| Dome Tower (upper) | observatory | 127 117 116 .. 135 136 123 | 116 | lookout, wind at the slits | wall-walk doors; ladder hole; slit windows |
| Bell Tower (ground) | chapel | 72 109 116 .. 80 115 123 | 108 | narrow, slit light | court door; ladder to the upper room (outer wall); slit windows |
| Bell Tower (upper) | chapel | 72 117 116 .. 80 132 123 | 116 | lookout, wind at the slits | wall-walk doors; ladder hole; slit windows |
| West Watch (ground) | armoury | 71 109 96 .. 75 115 100 | 108 | narrow, slit light | court door; ladder to the upper room (outer wall); slit windows |
| West Watch (upper) | armoury | 71 117 96 .. 75 127 100 | 116 | lookout, wind at the slits | wall-walk doors; ladder hole; slit windows |
| Armillary Tower (ground) | lab | 81 109 78 .. 86 115 82 | 108 | narrow, slit light | court door; ladder to the upper room (outer wall); slit windows |
| Armillary Tower (upper) | lab | 81 117 78 .. 86 131 82 | 116 | lookout, wind at the slits | wall-walk doors; ladder hole; slit windows |
| Needle Tower (ground) | library | 101 109 70 .. 106 115 75 | 108 | narrow, slit light | court door; ladder to the upper room (outer wall); slit windows |
| Needle Tower (upper) | library | 101 117 70 .. 106 143 75 | 116 | lookout, wind at the slits | wall-walk doors; ladder hole; slit windows |
| North Watch (ground) | armoury | 121 109 78 .. 126 115 82 | 108 | narrow, slit light | court door; ladder to the upper room (outer wall); slit windows |
| North Watch (upper) | armoury | 121 117 78 .. 126 131 82 | 116 | lookout, wind at the slits | wall-walk doors; ladder hole; slit windows |
| East Watch (ground) | bedroom | 132 109 96 .. 136 115 100 | 108 | narrow, slit light | court door; ladder to the upper room (outer wall); slit windows |
| East Watch (upper) | bedroom | 132 117 96 .. 136 125 100 | 116 | lookout, wind at the slits | wall-walk doors; ladder hole; slit windows |
| Old Observatory (ground) | ruin | 174 36 64 .. 183 41 73 | 35 | roofless, open sky through the broken wall, the fallen dome outside the door | door towards the crater; 6 lancets; helix ramp on the wall (keep clear); open to the sky |

## Inside the island (Route B) and the torn cellars

| Zone | Type | Box | Floor | Mood | Must-have features |
|---|---|---|---|---|---|
| Root Grotto | cave | 90 64 90 .. 117 78 117 | 63 | crystalline, purple glow, the heart column humming | flat floor ring round the Throat (open below: lethal fall); amethyst heart column; Root Helix arrives from below, Shaft Helix leaves upward |
| Root Shaft | cave | 97 64 97 .. 110 108 110 | 63 | vertical, ribbed, the heart glowing at the core | Shaft Helix (keep clear); open core: the deliberate fall |
| Torn Cellar 1 | cellar | 69 98 84 .. 81 104 96 | 97 | ruin, open to the sky on the outer side, wind | barrel vault; broken floor at the rim (fall risk) |
| Torn Cellar 2 | cellar | 87 99 67 .. 98 104 78 | 98 | ruin, open to the sky on the outer side, wind | barrel vault; broken floor at the rim (fall risk) |
| Torn Cellar 3 | cellar | 125 97 81 .. 137 104 93 | 96 | ruin, open to the sky on the outer side, wind | barrel vault; broken floor at the rim (fall risk) |
| Torn Cellar 4 | cellar | 131 98 107 .. 141 104 117 | 97 | ruin, open to the sky on the outer side, wind | barrel vault; broken floor at the rim (fall risk) |
| Torn Cellar 5 | cellar | 80 97 126 .. 89 104 135 | 96 | ruin, open to the sky on the outer side, wind | barrel vault; broken floor at the rim (fall risk) |
| Torn Cellar 6 | cellar | 69 98 106 .. 79 104 116 | 97 | ruin, open to the sky on the outer side, wind | barrel vault; broken floor at the rim (fall risk) |

## The crater

| Zone | Type | Box | Floor | Mood | Must-have features |
|---|---|---|---|---|---|
| Root Geode | cave | 96 17 96 .. 112 29 112 | 16 | sacred, amethyst everywhere, the conduit shards rising through the broken roof | south mouth onto the causeway; Root Helix (keep clear); oculus in the roof |
| Geode Grotto 1 | cave | 61 17 77 .. 69 26 86 | - | small, glittering, a hiding place | mouth onto the crater shore |
| Geode Grotto 2 | cave | 139 17 77 .. 146 25 85 | - | small, glittering, a hiding place | mouth onto the crater shore |
| Geode Grotto 3 | cave | 140 17 119 .. 147 24 125 | - | small, glittering, a hiding place | mouth onto the crater shore |
| Geode Grotto 4 | cave | 66 17 130 .. 71 23 136 | - | small, glittering, a hiding place | mouth onto the crater shore |

## The highland

| Zone | Type | Box | Floor | Mood | Must-have features |
|---|---|---|---|---|---|
| Old Observatory (perch) | lookout | 174 43 64 .. 183 46 73 | 42 | exposed, a sniper's half floor, the island hanging in the view | half floor (planks, 180 deg); broken wall chest-high on the crater side; telescope mount (fallen) |
