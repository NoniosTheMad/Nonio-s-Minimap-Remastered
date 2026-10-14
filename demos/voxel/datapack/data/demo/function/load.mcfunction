# demo voxel: the scene itself is placed from code (python -m tools.voxel place scenes/ruined_tower.py --server voxel).
# This pack only fixes the light and adds teleport buttons (G > Voxel: ruined tower).
scoreboard objectives add demo.vx trigger
gamerule spawn_mobs false
gamerule advance_time false
weather clear
time set 9000
