# demo vharzul: the build is placed from code (python -m tools.voxel place scenes/vharzul.py --server vharzul --pristine).
# This pack fixes the light and weather, stops mobs, and adds teleport buttons (G > Vharzul).
scoreboard objectives add demo.vz trigger
gamerule spawn_mobs false
gamerule advance_time false
weather clear
time set 6000
