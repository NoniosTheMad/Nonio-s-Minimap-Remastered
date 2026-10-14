# as the player, at their landing spot
tag @s remove nx.dream_arriving
scoreboard players set @s nx.dch 0
effect clear @s minecraft:blindness
effect give @s minecraft:jump_boost infinite 0 true
title @s times 5 40 20
title @s subtitle {"text":"sneak to wake up","color":"gray","italic":true}
title @s title {"text":"The Emerald Dream","color":"green"}
playsound minecraft:block.amethyst_block.resonate player @a ~ ~ ~ 1 1
playsound minecraft:entity.allay.ambient_with_item player @a ~ ~ ~ 1 1.2
particle minecraft:happy_villager ~ ~1 ~ 1.5 1 1.5 0 60
particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 25
tag @s add nx.dream_lander
function nonios:dream/vein/site
function nonios:dream/ruin/site
tag @s remove nx.dream_lander
data modify storage nonios:dream reason set value "arrived"
function #nonios:dream/on_enter
