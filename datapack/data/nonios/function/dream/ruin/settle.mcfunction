# as a new ruin marker standing on the top block of its column: keep it only on open ground away from the lander,
# other ruins and veins, with ground under all four corners of an 11x11 square (no ruin hanging over the void)
execute unless block ~ ~-1 ~ #nonios:dream_vein_host run return run kill @s
execute if entity @e[tag=nx.dream_lander,distance=..12] run return run kill @s
execute if entity @e[type=marker,tag=nx.dream_ruin,distance=..48] run return run kill @s
execute if entity @e[type=marker,tag=nx.dream_vein,distance=..4] run return run kill @s
execute if block ~5 ~-1 ~5 #minecraft:air if block ~5 ~-2 ~5 #minecraft:air if block ~5 ~-3 ~5 #minecraft:air run return run kill @s
execute if block ~-5 ~-1 ~5 #minecraft:air if block ~-5 ~-2 ~5 #minecraft:air if block ~-5 ~-3 ~5 #minecraft:air run return run kill @s
execute if block ~5 ~-1 ~-5 #minecraft:air if block ~5 ~-2 ~-5 #minecraft:air if block ~5 ~-3 ~-5 #minecraft:air run return run kill @s
execute if block ~-5 ~-1 ~-5 #minecraft:air if block ~-5 ~-2 ~-5 #minecraft:air if block ~-5 ~-3 ~-5 #minecraft:air run return run kill @s
tag @s remove nx.dream_rnew
tag @s add nx.dream_ruin
execute align xyz run tp @s ~0.5 ~ ~0.5
execute at @s run function nonios:dream/ruin/place
