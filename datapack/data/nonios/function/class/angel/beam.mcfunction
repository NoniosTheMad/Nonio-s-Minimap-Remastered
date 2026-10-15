# as/at the Angel, locked on (angel/lock): mend or empower the ally, draw the light, show its health
execute as @e[tag=nx.ang_t] if score @s nx.cls_atg = #me nx.cls_tmp run tag @s add nx.ang_cur
# sneaking = Valor (Strength I + Speed I), else Mending: Regeneration IV (about 3 health a second), given again only
# once it ran out (re-giving it every tick would reset its heal timer)
execute if predicate nonios:class/input_sneak run effect give @e[tag=nx.ang_cur] minecraft:strength 1 0 true
execute if predicate nonios:class/input_sneak run effect give @e[tag=nx.ang_cur] minecraft:speed 1 0 true
execute unless predicate nonios:class/input_sneak as @e[tag=nx.ang_cur] unless predicate nonios:class/angel/mending run effect give @s minecraft:regeneration 1 3 true
# the light flows from the staff to the ally's chest
execute as @e[tag=nx.ang_cur,limit=1] run function nonios:class/angel/aim
execute if predicate nonios:class/input_sneak anchored eyes positioned ^-0.35 ^-0.3 ^0.7 run function nonios:class/angel/flow_valor with storage nonios:tmp ang
execute unless predicate nonios:class/input_sneak anchored eyes positioned ^-0.35 ^-0.3 ^0.7 run function nonios:class/angel/flow with storage nonios:tmp ang
# its health, for the Angel only
execute store result score #th nx.cls_tmp run data get entity @e[tag=nx.ang_cur,limit=1] Health
execute store result score #tm nx.cls_tmp run attribute @e[tag=nx.ang_cur,limit=1] minecraft:max_health get
title @s actionbar [{"text":"❤ ","color":"red"},{"score":{"name":"#th","objective":"nx.cls_tmp"},"color":"gold"},{"text":" / ","color":"gray"},{"score":{"name":"#tm","objective":"nx.cls_tmp"},"color":"gray"}]
tag @e[tag=nx.ang_cur] remove nx.ang_cur
