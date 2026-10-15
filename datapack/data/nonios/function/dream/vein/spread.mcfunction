# at the mined vein block: one random neighbour (6 sides) that is plain host rock becomes a new vein
execute store result score #c nx.dream if entity @e[type=marker,tag=nx.dream_vein,distance=..6]
execute if score #c nx.dream >= #deposit_cap nx.dream run return 0
execute store result score #d nx.dream run random value 0..5
execute if score #d nx.dream matches 0 positioned ~1 ~ ~ run return run function nonios:dream/vein/sprout
execute if score #d nx.dream matches 1 positioned ~-1 ~ ~ run return run function nonios:dream/vein/sprout
execute if score #d nx.dream matches 2 positioned ~ ~ ~1 run return run function nonios:dream/vein/sprout
execute if score #d nx.dream matches 3 positioned ~ ~ ~-1 run return run function nonios:dream/vein/sprout
execute if score #d nx.dream matches 4 positioned ~ ~1 ~ run return run function nonios:dream/vein/sprout
execute if score #d nx.dream matches 5 positioned ~ ~-1 ~ run return run function nonios:dream/vein/sprout
