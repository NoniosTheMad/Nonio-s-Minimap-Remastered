# macro (config.core): marker inside the core block, then a fresh roll
$forceload add $(x) $(z)
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~0.5 ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["nx.acore"]}
scoreboard players set #core nx.arena 1
scoreboard players set #c_grown nx.arena 0
execute as @e[type=marker,tag=nx.acore] at @s run function nonios:arena/core/place
