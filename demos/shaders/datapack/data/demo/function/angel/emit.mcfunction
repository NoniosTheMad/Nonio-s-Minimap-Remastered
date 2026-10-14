# a light mote drifting up, a little gold dust, and a sparkle on flowers
particle minecraft:end_rod ~ ~0.05 ~ 0 1 0 0.035 0 force @s
particle minecraft:dust{color:[1.0,0.86,0.55],scale:0.7} ~ ~0.15 ~ 0.35 0.05 0.35 0 1 force @s
execute if block ~ ~ ~ #minecraft:small_flowers run particle minecraft:wax_off ~ ~0.45 ~ 0.15 0.15 0.15 0 2 force @s
