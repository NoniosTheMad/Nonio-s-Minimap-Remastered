# a faint green seed while it regrows; busier in the last 3 s
particle minecraft:composter ~ ~-0.5 ~ 0.2 0.2 0.2 0 1
scoreboard players operation #left nx.dream = @s nx.dvt
scoreboard players operation #left nx.dream -= #now nx.dream
execute if score #left nx.dream matches ..60 run particle minecraft:happy_villager ~ ~-0.5 ~ 0.3 0.3 0.3 0 2
