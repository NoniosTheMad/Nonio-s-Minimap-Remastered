# Send @s into the Emerald Dream at a random safe spot and remember where they came from. Ungated (see try_enter).
execute unless entity @s[type=player] run return fail
execute if entity @s[tag=nx.dream_arriving] run return fail
execute at @s if dimension nonios:emerald_dream run return run tellraw @s {"text":"You are already dreaming.","color":"green","italic":true}
function nonios:dream/pid
data modify storage nonios:dream tmp set value {}
data modify storage nonios:dream tmp.dim set from entity @s Dimension
data modify storage nonios:dream tmp.x set from entity @s Pos[0]
data modify storage nonios:dream tmp.y set from entity @s Pos[1]
data modify storage nonios:dream tmp.z set from entity @s Pos[2]
data modify storage nonios:dream tmp.yaw set from entity @s Rotation[0]
data modify storage nonios:dream tmp.pitch set from entity @s Rotation[1]
execute store result storage nonios:dream tmp.id int 1 run scoreboard players get @s nx.pid
function nonios:dream/save_return with storage nonios:dream tmp
playsound minecraft:block.beacon.activate player @a ~ ~ ~ 0.8 1.6
particle minecraft:happy_villager ~ ~1 ~ 0.4 0.8 0.4 0 30
tag @s add nx.in_dream
tag @s add nx.dream_arriving
scoreboard players set @s nx.dtry 0
scoreboard players set @s nx.drol 0
scoreboard players set @s nx.dch 0
effect give @s minecraft:blindness 3 0 true
title @s times 10 50 20
title @s subtitle {"text":"you drift off...","color":"gray","italic":true}
title @s title {"text":"The Emerald Dream","color":"green"}
function nonios:dream/arrive/roll
