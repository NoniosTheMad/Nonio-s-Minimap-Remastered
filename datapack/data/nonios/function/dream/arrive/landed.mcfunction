# as the player, at their landing spot
tag @s remove nx.dream_arriving
scoreboard players set @s nx.dch 0
effect clear @s minecraft:blindness
effect give @s minecraft:jump_boost infinite 1 true
title @s times 5 40 20
title @s subtitle {"text":"you are dreaming","color":"gray","italic":true}
title @s title {"text":"The Emerald Dream","color":"green"}
playsound minecraft:block.amethyst_block.resonate player @a ~ ~ ~ 1 1
playsound minecraft:entity.allay.ambient_with_item player @a ~ ~ ~ 1 1.2
particle minecraft:happy_villager ~ ~1 ~ 1.5 1 1.5 0 60
particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 25
scoreboard players set @s nx.dgok 0
scoreboard players operation @s nx.dchg = #wing_max nx.dream
scoreboard players set @s nx.dboost 0
data modify storage nonios:dream reason set value "arrived"
function #nonios:dream/on_enter
