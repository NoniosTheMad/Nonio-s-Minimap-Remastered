# advancement nonios:class/monster_kill: someone killed a player (or a mob tagged nx.soul)
advancement revoke @s only nonios:class/monster_kill
execute unless items entity @s armor.head *[minecraft:custom_data~{nx_item:"monster_head"}] run return 0
effect give @s minecraft:regeneration 3 3 true
effect give @s minecraft:strength 5 1 true
effect give @s minecraft:speed 5 1 true
effect give @s minecraft:saturation 1 3 true
execute at @s run particle minecraft:dust{color:[0.6,0.0,0.0],scale:2.0} ~ ~1 ~ 0.6 0.8 0.6 0 40
execute at @s run playsound minecraft:entity.wither.death player @a[distance=..48] ~ ~ ~ 0.5 1.4
title @s actionbar {"text":"Devoured.","color":"dark_red","bold":true}
