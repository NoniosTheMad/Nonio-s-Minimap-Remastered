execute as @e[type=marker,tag=nx.surge] at @s run function nonios:arena/event/surge_one
execute if entity @e[type=marker,tag=nx.surge] run schedule function nonios:arena/event/surge_wave 6t replace
