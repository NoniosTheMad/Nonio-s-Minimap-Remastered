scoreboard players set @s nx.dch 0
tag @s add nx.dream_hold
title @s actionbar {"text":"The dream holds you! (hit - let go of sneak and try again)","color":"red"}
playsound minecraft:block.amethyst_block.break player @a ~ ~ ~ 1 0.6
particle minecraft:angry_villager ~ ~1.8 ~ 0.3 0.2 0.3 0 3
