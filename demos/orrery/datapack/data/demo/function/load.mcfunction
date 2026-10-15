# demo orrery: the Orrery of Ast is placed from code (python -m tools.voxel place scenes/orrery.py --server orrery --pristine).
# This pack fixes the weather, stops mobs and adds teleport + light buttons (G > The Orrery).
scoreboard objectives add demo.or trigger
gamerule spawn_mobs false
gamerule advance_time false
weather clear
time set 6000
