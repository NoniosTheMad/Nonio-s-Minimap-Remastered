# as/at every Balrog, each tick. It cannot jump (jump_strength 0, step_height 1.6): walking into a wall taller than a
# step climbs it. Starts on a wall face at chest height, keeps going while the face is there at feet or knee height,
# so it rises until its feet clear the top and the forward input carries it onto the ledge (no stall below the lip).
execute if entity @s[tag=nx.bal_climb] run return run function nonios:class/balrog/climbing
execute if predicate nonios:class/input_forward rotated ~ 0 positioned ^ ^1.7 ^0.9 unless block ~ ~ ~ #minecraft:replaceable run function nonios:class/balrog/climb
# a smoking trail every 10 ticks (class/tick runs the markers: they curse enemies who walk through)
execute if score #t nx.cls_tmp matches 5 run function nonios:class/balrog/trail_drop
execute if score #t nx.cls_tmp matches 15 run function nonios:class/balrog/trail_drop
