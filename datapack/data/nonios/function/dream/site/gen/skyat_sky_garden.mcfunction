# sky site sky_garden: its box (42x78x42) must be mostly open air (21/27 samples; islands inside its silhouette get carved)
execute unless loaded ~-21 ~ ~-21 run return run scoreboard players set #res nx.dream 3
execute unless loaded ~-21 ~ ~21 run return run scoreboard players set #res nx.dream 3
execute unless loaded ~21 ~ ~-21 run return run scoreboard players set #res nx.dream 3
execute unless loaded ~21 ~ ~21 run return run scoreboard players set #res nx.dream 3
scoreboard players set #air nx.dream 0
execute if block ~-21 ~-41 ~-21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-21 ~-2 ~-21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-21 ~36 ~-21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-21 ~-41 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-21 ~-2 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-21 ~36 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-21 ~-41 ~21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-21 ~-2 ~21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-21 ~36 ~21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-41 ~-21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-2 ~-21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~36 ~-21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-41 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-2 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~36 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-41 ~21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-2 ~21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~36 ~21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~21 ~-41 ~-21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~21 ~-2 ~-21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~21 ~36 ~-21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~21 ~-41 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~21 ~-2 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~21 ~36 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~21 ~-41 ~21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~21 ~-2 ~21 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~21 ~36 ~21 #minecraft:air run scoreboard players add #air nx.dream 1
execute unless score #air nx.dream matches 21.. run return run scoreboard players set #res nx.dream 2
tp @s ~ ~ ~
execute at @s run function nonios:dream/site/gen/place_sky_garden
scoreboard players set #res nx.dream 1
