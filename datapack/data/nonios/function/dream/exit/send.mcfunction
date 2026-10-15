# as the player (anywhere in the dream): send them back where they came from, else #nonios:dream/fallback_return
tag @s remove nx.dream_hold
tag @s remove nx.dream_arriving
scoreboard players set @s nx.dch 0
execute at @s run particle minecraft:happy_villager ~ ~1 ~ 0.5 1 0.5 0 40
execute at @s run playsound minecraft:block.beacon.deactivate player @a ~ ~ ~ 1 1.4
effect clear @s minecraft:jump_boost
function nonios:dream/wings/strip
function nonios:dream/pixie/dismiss
effect give @s minecraft:blindness 1 0 true
effect give @s minecraft:slow_falling 3 0 true
function #nonios:dream/on_exit
function nonios:dream/pid
execute store result storage nonios:dream tmp.id int 1 run scoreboard players get @s nx.pid
data remove storage nonios:dream back
function nonios:dream/exit/recall with storage nonios:dream tmp
execute if data storage nonios:dream back.dim run function nonios:dream/exit/tp_back with storage nonios:dream back
execute unless data storage nonios:dream back.dim run function #nonios:dream/fallback_return
function nonios:dream/exit/forget with storage nonios:dream tmp
tag @s remove nx.in_dream
title @s times 5 30 15
title @s subtitle {"text":"...was it all a dream?","color":"gray","italic":true}
title @s title {"text":"You wake up","color":"green"}
execute at @s run playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6
