# sky site nightmare_spire: its box (68x90x68) must be mostly open air (21/27 samples; islands inside its silhouette get carved)
execute unless loaded ~-34 ~ ~-34 run return run scoreboard players set #res nx.dream 3
execute unless loaded ~-34 ~ ~34 run return run scoreboard players set #res nx.dream 3
execute unless loaded ~34 ~ ~-34 run return run scoreboard players set #res nx.dream 3
execute unless loaded ~34 ~ ~34 run return run scoreboard players set #res nx.dream 3
scoreboard players set #air nx.dream 0
execute if block ~-34 ~-25 ~-34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-34 ~20 ~-34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-34 ~64 ~-34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-34 ~-25 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-34 ~20 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-34 ~64 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-34 ~-25 ~34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-34 ~20 ~34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-34 ~64 ~34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-25 ~-34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~20 ~-34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~64 ~-34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-25 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~20 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~64 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-25 ~34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~20 ~34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~64 ~34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~34 ~-25 ~-34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~34 ~20 ~-34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~34 ~64 ~-34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~34 ~-25 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~34 ~20 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~34 ~64 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~34 ~-25 ~34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~34 ~20 ~34 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~34 ~64 ~34 #minecraft:air run scoreboard players add #air nx.dream 1
execute unless score #air nx.dream matches 21.. run return run scoreboard players set #res nx.dream 2
tp @s ~ ~ ~
execute at @s run function nonios:dream/site/gen/place_nightmare_spire
scoreboard players set #res nx.dream 1
