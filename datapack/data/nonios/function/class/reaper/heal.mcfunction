# #137: spend a soul, heal 2 hearts. Banked kills are the Reaper's only real healing.
execute unless score @s nx.cls_souls matches 1.. run return run function nonios:class/reaper/no_souls
scoreboard players remove @s nx.cls_souls 1
effect give @s minecraft:instant_health 1 0 true
particle minecraft:soul ~ ~1 ~ 0.3 0.5 0.3 0.04 12
particle minecraft:damage_indicator ~ ~1.2 ~ 0.3 0.3 0.3 0.1 3
playsound minecraft:particle.soul_escape player @a ~ ~ ~ 1.2 0.7
title @s actionbar [{"text":"☠ ","color":"dark_purple"},{"score":{"name":"@s","objective":"nx.cls_souls"},"color":"light_purple"},{"text":"/5","color":"dark_gray"}]
