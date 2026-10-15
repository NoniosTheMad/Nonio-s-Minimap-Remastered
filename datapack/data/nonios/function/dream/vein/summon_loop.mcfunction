execute if score #i nx.dream matches ..0 run return 0
summon minecraft:marker ~ ~ ~ {Tags:["nx.dream_vein","nx.dream_vnew"]}
scoreboard players remove #i nx.dream 1
function nonios:dream/vein/summon_loop
