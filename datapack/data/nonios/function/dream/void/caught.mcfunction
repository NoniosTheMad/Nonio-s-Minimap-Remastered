effect give @s minecraft:slow_falling 4 0 true
effect give @s minecraft:blindness 1 0 true
title @s times 5 30 15
title @s title ""
title @s subtitle {"text":"the dream catches you","color":"gray","italic":true}
execute at @s run playsound minecraft:block.amethyst_block.resonate player @a ~ ~ ~ 1 0.8
execute at @s run particle minecraft:happy_villager ~ ~1 ~ 0.6 1 0.6 0 30
