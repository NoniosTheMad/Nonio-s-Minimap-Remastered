# as/at every Balrog, each tick. It cannot jump (jump_strength 0, step_height +1): walking into a wall climbs it.
execute if predicate nonios:class/input_forward rotated ~ 0 positioned ^ ^0.5 ^1 unless block ~ ~ ~ #minecraft:replaceable run return run function nonios:class/balrog/climb
execute if entity @s[tag=nx.bal_climb] run function nonios:class/balrog/unclimb
# a smoking trail every 10 ticks (class/tick runs the markers: they curse enemies who walk through)
execute if score #t nx.cls_tmp matches 5 run function nonios:class/balrog/trail_drop
execute if score #t nx.cls_tmp matches 15 run function nonios:class/balrog/trail_drop
