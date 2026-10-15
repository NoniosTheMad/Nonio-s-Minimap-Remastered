# voxel

Showcase of the voxel studio (`tools/voxel/`, docs: `docs/voxel-studio.md`). The island is not part of this pack:
it is placed from code over RCON:

    python -m tools.voxel place scenes/ruined_tower.py --server voxel     # meta origin (-40, 40, -40)

The pack only sets a fixed afternoon light, no mobs, and a G dialog with teleports and gamemode buttons
(`demo.vx` trigger: 1-4 teleports, 5 creative, 6 survival, 7 spectator).
After placing, the world is snapshotted to `world.pristine` so "Reset this server" restores the island.
