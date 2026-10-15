# orrery

Concept B, "The Orrery of Ast": a floating torn summit with a castle and the copper armillary Spire over a crater
arena, from `scenes/orrery.py` (voxel studio, `docs/voxel-studio.md`; art direction `scenes/orrery.md`, zones
`docs/builds/orrery-zones.md`). Placed from code, then protected:

    python -m tools.voxel place scenes/orrery.py --server orrery --pristine           # meta origin (-104, 20, -104)
    python -m tools.voxel protect scenes/orrery.py --backup 2000 -64 0 --install orrery --setup

The pack keeps noon light and no mobs, and adds a G dialog (`demo.or` trigger: 1-11 teleports, 12 day, 13 night,
14 creative, 15 survival, 16 spectator). Spawns: white (0 52 92), black (0 50 -92).
