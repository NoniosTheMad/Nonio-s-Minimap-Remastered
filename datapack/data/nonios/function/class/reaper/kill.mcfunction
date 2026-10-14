# advancement nonios:class/reaper_kill: someone killed a player (or a mob tagged nx.soul, e.g. demo dummies)
advancement revoke @s only nonios:class/reaper_kill
execute unless items entity @s armor.head *[minecraft:custom_data~{nx_item:"reaper_head"}] run return 0
scoreboard players add @s nx.cls_souls 1
execute if score @s nx.cls_souls matches 6.. run scoreboard players set @s nx.cls_souls 5
effect give @s minecraft:invisibility 4 0 true
execute at @s run playsound minecraft:entity.wither.spawn player @a[distance=..32] ~ ~ ~ 0.5 1.6
execute at @s run particle minecraft:soul ~ ~1 ~ 0.5 0.8 0.5 0.05 25
title @s actionbar [{"text":"☠ soul harvested ","color":"dark_purple"},{"score":{"name":"@s","objective":"nx.cls_souls"},"color":"light_purple"},{"text":"/5","color":"dark_gray"},{"text":"  (4s invisible)","color":"gray"}]
