# while the clamp holds (nx.cls_bcap ticks left): #mx back to the unclamped max; hurt meanwhile = the clamp follows down
execute store result score #c nx.cls_tmp run attribute @s minecraft:max_health modifier value get nonios:berserk_cap 100
scoreboard players operation #mx nx.cls_tmp -= #c nx.cls_tmp
scoreboard players remove @s nx.cls_bcap 1
execute if score @s nx.cls_bcap matches ..0 run return run attribute @s minecraft:max_health modifier remove nonios:berserk_cap
execute if score #hp nx.cls_tmp < @s nx.cls_bhp run function nonios:class/berserker/recap
