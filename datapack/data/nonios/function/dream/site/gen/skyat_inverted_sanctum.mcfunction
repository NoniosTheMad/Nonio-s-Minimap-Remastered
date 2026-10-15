# sky site inverted_sanctum: its box (62x91x62) must be mostly open air (21/27 samples; islands inside its silhouette get carved)
execute unless loaded ~-31 ~ ~-31 run return run scoreboard players set #res nx.dream 3
execute unless loaded ~-31 ~ ~31 run return run scoreboard players set #res nx.dream 3
execute unless loaded ~31 ~ ~-31 run return run scoreboard players set #res nx.dream 3
execute unless loaded ~31 ~ ~31 run return run scoreboard players set #res nx.dream 3
scoreboard players set #air nx.dream 0
execute if block ~-31 ~-72 ~-31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-31 ~-27 ~-31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-31 ~18 ~-31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-31 ~-72 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-31 ~-27 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-31 ~18 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-31 ~-72 ~31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-31 ~-27 ~31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~-31 ~18 ~31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-72 ~-31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-27 ~-31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~18 ~-31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-72 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-27 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~18 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-72 ~31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~-27 ~31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~0 ~18 ~31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~31 ~-72 ~-31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~31 ~-27 ~-31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~31 ~18 ~-31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~31 ~-72 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~31 ~-27 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~31 ~18 ~0 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~31 ~-72 ~31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~31 ~-27 ~31 #minecraft:air run scoreboard players add #air nx.dream 1
execute if block ~31 ~18 ~31 #minecraft:air run scoreboard players add #air nx.dream 1
execute unless score #air nx.dream matches 21.. run return run scoreboard players set #res nx.dream 2
tp @s ~ ~ ~
execute at @s run function nonios:dream/site/gen/place_inverted_sanctum
scoreboard players set #res nx.dream 1
