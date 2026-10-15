# every arena loop (10 ticks) while the gates are open: rotation timer, portal particles at the pads and the active exit
scoreboard players operation #g_t nx.arena -= #dt nx.arena
execute if score #g_t nx.arena matches ..0 run function nonios:arena/gate/rotate
execute as @e[type=marker,tag=nx.agate] at @s run particle minecraft:portal ~ ~0.6 ~ 0.2 0.5 0.2 0 12
execute as @e[type=marker,tag=nx.aslot_on] at @s run particle minecraft:portal ~ ~1 ~ 0.1 0.5 0.1 0 20
