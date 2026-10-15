# as/at a Sanctuary marker: a golden ring 0.8 blocks wider each tick, 10 ticks
scoreboard players add @s nx.cls_aw 1
execute if score @s nx.cls_aw matches 11.. run return run kill @s
execute store result storage nonios:tmp aw.r double 0.8 run scoreboard players get @s nx.cls_aw
scoreboard players set #a nx.cls_tmp 0
execute rotated 0 0 run function nonios:class/angel/ring with storage nonios:tmp aw
