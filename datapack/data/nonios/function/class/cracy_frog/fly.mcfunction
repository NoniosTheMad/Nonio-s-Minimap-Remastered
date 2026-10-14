# broom held in use (nx.cls_fly is refreshed every tick by the using_item advancement)
scoreboard players remove @s nx.cls_fly 1
# released: stop lifting right away
execute if score @s nx.cls_fly matches 0 run return run effect clear @s minecraft:levitation
execute unless score @s nx.cls_fuel matches 1.. run return run function nonios:class/cracy_frog/out_of_fuel
scoreboard players remove @s nx.cls_fuel 1
# lift follows the pitch: look up = climb, look level = gentle climb, look down = glide (slow falling)
execute if entity @s[x_rotation=-90..-25] run effect give @s minecraft:levitation 1 4 true
execute if entity @s[x_rotation=-25..15] run effect give @s minecraft:levitation 1 0 true
execute if entity @s[x_rotation=15..90] run effect clear @s minecraft:levitation
effect give @s minecraft:slow_falling 2 0 true
# forward push every 6 ticks: the frog_broom enchantment applies the impulse while nx.cls_kick >= 1
execute store result score #k nx.cls_tmp run time query gametime
scoreboard players operation #k nx.cls_tmp %= #6 nx.cls_tmp
execute if score #k nx.cls_tmp matches 0 run scoreboard players set @s nx.cls_kick 1
particle minecraft:happy_villager ~ ~0.2 ~ 0.3 0.1 0.3 0 1
execute if predicate nonios:class/coin run particle minecraft:witch ~ ~0.4 ~ 0.3 0.1 0.3 0 1
title @s actionbar [{"text":"🧹 ","color":"light_purple"},{"score":{"name":"@s","objective":"nx.cls_fuel"},"color":"light_purple"},{"text":"/60  look up to climb, down to glide","color":"gray"}]
