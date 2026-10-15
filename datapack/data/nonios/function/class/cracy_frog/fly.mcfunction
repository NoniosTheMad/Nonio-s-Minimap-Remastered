# as/at a frog on its broom, each tick (nx.cls_fly 1). Sneak dismounts (vanilla), fuel runs out = thrown off.
execute unless function nonios:class/cracy_frog/riding run return run function nonios:class/cracy_frog/unmount
scoreboard players remove @s nx.cls_fuel 1
execute unless score @s nx.cls_fuel matches 1.. run return run function nonios:class/cracy_frog/out_of_fuel
# one seat: anyone else who climbs on is shaken off
tag @s add nx.cls_me
execute on vehicle on passengers if entity @s[type=player,tag=!nx.cls_me] run ride @s dismount
tag @s remove nx.cls_me
scoreboard players operation #me nx.cls_tmp = @s nx.pid
execute rotated ~ 0 as @e[type=item_display,tag=nx.frog_broomfx] if score @s nx.pid = #me nx.cls_tmp run tp @s ~ ~0.15 ~ ~ ~
particle minecraft:happy_villager ~ ~0.1 ~ 0.3 0.1 0.3 0 1
execute if predicate nonios:class/coin run particle minecraft:witch ~ ~0.2 ~ 0.3 0.1 0.3 0 1
title @s actionbar [{"text":"🧹 ","color":"light_purple"},{"score":{"name":"@s","objective":"nx.cls_fuel"},"color":"light_purple"},{"text":"/160","color":"gray"}]
