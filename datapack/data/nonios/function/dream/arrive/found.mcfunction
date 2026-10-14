# ground at ~ ~ ~: needs two free blocks above it
execute unless block ~ ~1 ~ #nonios:dream_passable run return run function nonios:dream/arrive/reroll
execute unless block ~ ~2 ~ #nonios:dream_passable run return run function nonios:dream/arrive/reroll
tp @s ~ ~1 ~
execute at @s run function nonios:dream/arrive/landed
