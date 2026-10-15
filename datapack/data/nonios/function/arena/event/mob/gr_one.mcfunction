summon minecraft:husk ~ ~ ~ {Tags:["nx.ev_mob","nx.ev_grave","nx.ev_new"],PersistenceRequired:1b,DeathLootTable:"nonios:arena/grave"}
scoreboard players remove #left nx.arena 1
execute if score #left nx.arena matches 1.. run function nonios:arena/event/mob/gr_one
