execute if score #i nx.dream matches ..0 run return 0
summon minecraft:marker ~ ~ ~ {Tags:["nx.dream_rnew"]}
scoreboard players remove #i nx.dream 1
function nonios:dream/ruin/summon_loop
