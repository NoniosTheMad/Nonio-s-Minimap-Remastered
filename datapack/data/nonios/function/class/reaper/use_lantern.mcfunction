# Grave Lantern (goat horn, 5 s cooldown): spend a soul, bind the first enemy along the aim (8 blocks, walls stop it) for 2 s.
# A miss keeps the soul.
execute unless score @s nx.cls_souls matches 1.. run return run function nonios:class/reaper/no_souls
tag @s add nx.cls_me
execute if entity @s[team=white] run tag @e[type=player,team=white] add nx.cls_ally
execute if entity @s[team=black] run tag @e[type=player,team=black] add nx.cls_ally
scoreboard players set #r nx.cls_tmp 0
execute anchored eyes positioned ^ ^ ^0.5 run function nonios:class/reaper/bind_ray
execute as @e[tag=nx.reaper_bindhit,limit=1] at @s run function nonios:class/reaper/bind
execute if entity @e[tag=nx.reaper_bindhit,limit=1] run scoreboard players remove @s nx.cls_souls 1
execute if entity @e[tag=nx.reaper_bindhit,limit=1] run function nonios:class/reaper/bind_line
execute if entity @e[tag=nx.reaper_bindhit,limit=1] run title @s actionbar [{"text":"☠ ","color":"dark_purple"},{"score":{"name":"@s","objective":"nx.cls_souls"},"color":"light_purple"},{"text":"/5","color":"dark_gray"}]
execute unless entity @e[tag=nx.reaper_bindhit,limit=1] anchored eyes run particle minecraft:soul ^ ^ ^1 0.1 0.1 0.1 0.02 4
tag @e[tag=nx.reaper_bindhit] remove nx.reaper_bindhit
tag @e[tag=nx.cls_ally] remove nx.cls_ally
tag @s remove nx.cls_me
