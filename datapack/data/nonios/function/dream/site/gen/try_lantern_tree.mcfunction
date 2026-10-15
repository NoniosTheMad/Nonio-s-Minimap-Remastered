# as the site marker at (x, 250, z): drop onto the island surface (spreadplayers fails over the void)
execute unless loaded ~-9 ~ ~-9 run return run scoreboard players set #res nx.dream 3
execute unless loaded ~-9 ~ ~9 run return run scoreboard players set #res nx.dream 3
execute unless loaded ~9 ~ ~-9 run return run scoreboard players set #res nx.dream 3
execute unless loaded ~9 ~ ~9 run return run scoreboard players set #res nx.dream 3
execute store success score #ok nx.dream run spreadplayers ~ ~ 0 1 under 250 false @s
execute unless score #ok nx.dream matches 1 run return run scoreboard players set #res nx.dream 2
execute at @s run function nonios:dream/site/gen/ground_lantern_tree
