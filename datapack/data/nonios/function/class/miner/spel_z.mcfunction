execute if block ~ ~ ~ #nonios:class/spelunk if score #n nx.cls_tmp matches ..63 run function nonios:class/miner/spel_ore
scoreboard players add #sz nx.cls_tmp 1
execute if score #sz nx.cls_tmp matches ..16 positioned ~ ~ ~1 run function nonios:class/miner/spel_z
