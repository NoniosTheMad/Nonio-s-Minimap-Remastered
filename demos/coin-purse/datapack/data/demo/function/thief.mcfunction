# summon the Purse Thief: a husk tagged nx.purse_holder, so the game code hands it your purse if it kills you
kill @e[type=husk,tag=demo.thief]
kill @e[type=marker,tag=demo.thief_pos]
scoreboard players set #thief demo.c 0
summon minecraft:husk 0.5 64 -12.5 {Tags:["nx.purse_holder","demo.thief"],CustomName:{text:"Purse Thief",color:"red"},CustomNameVisible:1b,PersistenceRequired:1b,equipment:{mainhand:{id:"minecraft:iron_sword",count:1}},drop_chances:{mainhand:0.0f}}
summon minecraft:marker 0.5 64 -12.5 {Tags:["demo.thief_pos"]}
tellraw @a {"text":"[demo] Purse Thief spawned north of spawn. Let it kill you with coins in your purse.","color":"yellow"}
