# as the landing player (tagged nx.dream_lander), at the landing spot: plant #veins regrowing veins around it
scoreboard players operation #i nx.dream = #veins nx.dream
function nonios:dream/vein/summon_loop
execute store result score #my nx.dream run data get entity @s Pos[1]
scoreboard players add #my nx.dream 6
execute store result storage nonios:dream spread.max int 1 run scoreboard players get #my nx.dream
execute store result storage nonios:dream spread.r int 1 run scoreboard players get #vein_r nx.dream
function nonios:dream/vein/spread with storage nonios:dream spread
execute as @e[type=marker,tag=nx.dream_vnew] at @s run function nonios:dream/vein/settle
