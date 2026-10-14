# as the landing player (tagged nx.dream_lander), at the landing spot: try to plant #ruins ruins (loot inside)
# 12..#ruin_r blocks away, on ground, never within 48 blocks of another ruin (markers tagged nx.dream_ruin)
scoreboard players operation #i nx.dream = #ruins nx.dream
function nonios:dream/ruin/summon_loop
execute store result score #my nx.dream run data get entity @s Pos[1]
scoreboard players add #my nx.dream 10
execute store result storage nonios:dream spread.max int 1 run scoreboard players get #my nx.dream
execute store result storage nonios:dream spread.r int 1 run scoreboard players get #ruin_r nx.dream
function nonios:dream/ruin/spread with storage nonios:dream spread
execute as @e[type=marker,tag=nx.dream_rnew] at @s run function nonios:dream/ruin/settle
