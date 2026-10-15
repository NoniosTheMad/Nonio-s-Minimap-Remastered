# ore scan, x columns (17 x 13 x 17 cells around the Miner, at most 64 ores)
scoreboard players set #sy nx.cls_tmp 0
function nonios:class/miner/spel_y
scoreboard players add #sx nx.cls_tmp 1
execute if score #sx nx.cls_tmp matches ..16 positioned ~1 ~ ~ run function nonios:class/miner/spel_x
