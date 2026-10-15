# Archer, once a second: the quiver gives an arrow back every 3 s while you carry fewer than 8
scoreboard players add @s nx.cls_quiv 1
execute if score @s nx.cls_quiv matches ..2 run return 0
scoreboard players set @s nx.cls_quiv 0
execute store result score #a nx.cls_tmp run clear @s minecraft:arrow 0
execute if score #a nx.cls_tmp matches 8.. run return 0
give @s minecraft:arrow 1
