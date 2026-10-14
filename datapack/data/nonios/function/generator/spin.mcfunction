# as + at a generator marker: turn the core 45/90/135 degrees per second by level. The client interpolates the yaw over
# teleport_duration (20 ticks); spin_core keeps the stored yaw within 0..359 so it never grows without bound.
scoreboard players operation #spin nx.gen = @s nx.gen_lvl
scoreboard players operation #spin nx.gen *= #45 nx.gen
execute as @e[type=item_display,tag=nx.gen_core,distance=..2.5,limit=1] run function nonios:generator/spin_core
