# as the Berserker with Rage: after 3 s out of combat it drains, 1 every other tick (10 s from full)
scoreboard players operation #d nx.cls_tmp = #now nx.cls_tmp
scoreboard players operation #d nx.cls_tmp -= @s nx.cls_brt
execute if score #d nx.cls_tmp matches ..59 run return 0
scoreboard players operation #p nx.cls_tmp = #now nx.cls_tmp
scoreboard players operation #p nx.cls_tmp %= #2 nx.cls_tmp
execute if score #p nx.cls_tmp matches 0 run scoreboard players remove @s nx.cls_brg 1
