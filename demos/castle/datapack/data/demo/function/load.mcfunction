# demo castle: the castle is placed from code (python -m tools.voxel place scenes/castle.py --server castle).
# This pack only fixes the light and adds teleport buttons (G > Castle).
scoreboard objectives add demo.cs trigger
gamerule spawn_mobs false
gamerule advance_time false
weather clear
time set 9000
