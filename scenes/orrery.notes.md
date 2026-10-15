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
