# as + at the core marker. Only an empty (air) core regrows; a block placed in it blocks it (as in V2).
execute unless block ~ ~ ~ #minecraft:air run return run tag @s remove nx.c_wait
execute unless entity @s[tag=nx.c_wait] run scoreboard players operation @s nx.ar_t = #c_regrow nx.arena
tag @s add nx.c_wait
scoreboard players operation @s nx.ar_t -= #dt nx.arena
execute if score @s nx.ar_t matches ..0 run function nonios:arena/core/regrow
