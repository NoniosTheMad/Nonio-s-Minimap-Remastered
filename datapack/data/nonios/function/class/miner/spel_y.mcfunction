scoreboard players set #sz nx.cls_tmp 0
function nonios:class/miner/spel_z
scoreboard players add #sy nx.cls_tmp 1
execute if score #sy nx.cls_tmp matches ..12 positioned ~ ~1 ~ run function nonios:class/miner/spel_y
