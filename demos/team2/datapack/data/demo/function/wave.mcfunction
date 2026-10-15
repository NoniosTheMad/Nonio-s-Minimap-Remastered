# a hostile wave 8 blocks ahead, on the enemy team (souls too). Husks are undead: immune to the Balrog's wither curse.
function demo:enemy
summon minecraft:husk ^-2 ^ ^8 {Tags:["nx.dummy","nx.soul","demo.new"],PersistenceRequired:1b,CustomName:{text:"Raider",color:"red"}}
summon minecraft:husk ^2 ^ ^8 {Tags:["nx.dummy","nx.soul","demo.new"],PersistenceRequired:1b,CustomName:{text:"Raider",color:"red"}}
summon minecraft:vindicator ^-1 ^ ^9 {Tags:["nx.dummy","nx.soul","demo.new"],PersistenceRequired:1b,CustomName:{text:"Brute",color:"red"}}
summon minecraft:vindicator ^1 ^ ^9 {Tags:["nx.dummy","nx.soul","demo.new"],PersistenceRequired:1b,CustomName:{text:"Brute",color:"red"}}
summon minecraft:pillager ^ ^ ^11 {Tags:["nx.dummy","nx.soul","demo.new"],PersistenceRequired:1b,CustomName:{text:"Marksman",color:"red"}}
function demo:join_wave with storage demo:tmp
tellraw @s {"text":"[demo] Wave incoming (5).","color":"yellow"}
