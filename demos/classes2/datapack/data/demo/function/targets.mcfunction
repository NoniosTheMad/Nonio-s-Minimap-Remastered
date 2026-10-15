# three still enemy husks 5 blocks ahead (2 apart). Count as souls (Reaper / Monster devour).
function demo:enemy
summon minecraft:husk ^-2 ^ ^5 {NoAI:1b,Tags:["nx.dummy","nx.soul","demo.new"],PersistenceRequired:1b,CustomNameVisible:1b,CustomName:{text:"Target",color:"red"}}
summon minecraft:husk ^ ^ ^5 {NoAI:1b,Tags:["nx.dummy","nx.soul","demo.new"],PersistenceRequired:1b,CustomNameVisible:1b,CustomName:{text:"Target",color:"red"}}
summon minecraft:husk ^2 ^ ^5 {NoAI:1b,Tags:["nx.dummy","nx.soul","demo.new"],PersistenceRequired:1b,CustomNameVisible:1b,CustomName:{text:"Target",color:"red"}}
function demo:join_new with storage demo:tmp
tellraw @s {"text":"[demo] 3 targets on the enemy team.","color":"yellow"}
# and a wounded ally behind you (Angel beam / Sanctuary)
summon minecraft:villager ^ ^ ^-4 {NoAI:1b,Health:6f,Tags:["nx.ang_patient","demo.pat"],PersistenceRequired:1b,CustomNameVisible:1b,CustomName:{text:"Wounded",color:"green"}}
execute if entity @s[team=white] run team join white @e[type=villager,tag=demo.pat]
execute if entity @s[team=black] run team join black @e[type=villager,tag=demo.pat]
tag @e[type=villager,tag=demo.pat] remove demo.pat
