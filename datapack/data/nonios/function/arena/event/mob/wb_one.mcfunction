# at the spawn point: one raider (every 3rd a pillager), repeated #left times
scoreboard players operation #k nx.arena = #left nx.arena
scoreboard players operation #k nx.arena %= #3 nx.arena
execute unless score #k nx.arena matches 0 run summon minecraft:vindicator ~ ~ ~ {Tags:["nx.ev_mob","nx.ev_raider","nx.ev_new"],PersistenceRequired:1b,DeathLootTable:"nonios:arena/raider",equipment:{mainhand:{id:"minecraft:iron_axe",count:1}},drop_chances:{mainhand:0.0f},attributes:[{id:"minecraft:follow_range",base:40d}]}
execute if score #k nx.arena matches 0 run summon minecraft:pillager ~ ~ ~ {Tags:["nx.ev_mob","nx.ev_raider","nx.ev_new"],PersistenceRequired:1b,DeathLootTable:"nonios:arena/raider",equipment:{mainhand:{id:"minecraft:crossbow",count:1}},drop_chances:{mainhand:0.0f},attributes:[{id:"minecraft:follow_range",base:40d}]}
scoreboard players remove #left nx.arena 1
execute if score #left nx.arena matches 1.. run function nonios:arena/event/mob/wb_one
