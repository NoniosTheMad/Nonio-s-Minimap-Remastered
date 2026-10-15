# as + at a node marker: its Grave Lord + husks, scattered over the node's zone
summon minecraft:husk ~ ~ ~ {Tags:["nx.ev_mob","nx.ev_grave","nx.ev_new"],PersistenceRequired:1b,CustomName:{text:"Grave Lord",color:"dark_green"},DeathLootTable:"nonios:arena/grave_lord",equipment:{head:{id:"minecraft:chainmail_helmet",count:1},mainhand:{id:"minecraft:stone_sword",count:1}},drop_chances:{head:0.0f,mainhand:0.0f},attributes:[{id:"minecraft:scale",base:1.35d},{id:"minecraft:max_health",base:40d}],Health:40f}
execute store result score #left nx.arena run data get storage nonios:arena config.graves.per_node
scoreboard players remove #left nx.arena 1
execute if score #left nx.arena matches 1.. run function nonios:arena/event/mob/gr_one
data modify storage nonios:arena mob set value {r:3}
data modify storage nonios:arena mob.x set from entity @s data.x
data modify storage nonios:arena mob.y set from entity @s data.y
data modify storage nonios:arena mob.z set from entity @s data.z
function nonios:arena/event/mob/spread
