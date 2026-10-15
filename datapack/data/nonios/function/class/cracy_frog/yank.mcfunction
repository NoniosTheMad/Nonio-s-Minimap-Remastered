# as/at the tongue's victim: thrown up and toward the frog by a wind burst just under and behind it.
# Wind bursts cancel vanilla fall damage above the launch point, so players are tracked (yanked_tick) and hurt on landing.
execute if entity @s[type=player] unless predicate nonios:class/on_ground if block ~ ~-1 ~ #minecraft:air if block ~ ~-2 ~ #minecraft:air run return run function nonios:class/cracy_frog/hook_down
# two bursts on the ground (one close = lift, one further back = pull). The burst must go off on top of the floor (inside a block it has no exposure, so no push); in the air it rises into the victim
execute facing entity @e[tag=nx.cls_me,limit=1] feet rotated ~ 0 positioned ^ ^ ^-0.45 unless block ~ ~-0.3 ~ #minecraft:replaceable run summon minecraft:wind_charge ~ ~0.15 ~ {Motion:[0.0,-1.0,0.0]}
execute facing entity @e[tag=nx.cls_me,limit=1] feet rotated ~ 0 positioned ^ ^ ^-1.1 unless block ~ ~-0.3 ~ #minecraft:replaceable run summon minecraft:wind_charge ~ ~0.15 ~ {Motion:[0.0,-1.0,0.0]}
execute facing entity @e[tag=nx.cls_me,limit=1] feet rotated ~ 0 positioned ^ ^ ^-0.45 if block ~ ~-0.3 ~ #minecraft:replaceable run summon minecraft:wind_charge ~ ~-0.6 ~ {Motion:[0.0,1.0,0.0],Tags:["nx.frog_wc"]}
playsound minecraft:entity.frog.eat player @a ~ ~ ~ 2 0.6
playsound minecraft:entity.slime.jump player @a ~ ~ ~ 1.5 0.8
particle minecraft:item_slime ~ ~1 ~ 0.4 0.6 0.4 0.1 20
title @s[type=player] actionbar {"text":"#Useful","color":"green","italic":true}
execute if entity @s[type=player] run function nonios:class/cracy_frog/yank_track
