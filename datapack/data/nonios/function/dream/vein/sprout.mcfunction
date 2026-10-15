execute unless block ~ ~ ~ #nonios:dream_spread_into run return 0
execute positioned ~ ~1 ~ if entity @e[type=marker,tag=nx.dream_vein,distance=..0.6] run return 0
summon minecraft:marker ~ ~1 ~ {Tags:["nx.dream","nx.dream_vein","nx.dv3","nx.dream_vsprout"]}
execute as @e[type=marker,tag=nx.dream_vsprout] at @s run function nonios:dream/vein/sprouted
