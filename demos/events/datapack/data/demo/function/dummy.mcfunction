# an enemy-team husk 3 blocks in front of you (kill it during Bounty Hunt, inside the arena) + a sword
data modify storage demo:tmp enemy set value "black"
execute if entity @s[team=black] run data modify storage demo:tmp enemy set value "white"
summon minecraft:husk ^ ^ ^3 {NoAI:1b,Tags:["nx.dummy","nx.soul","demo.new"],PersistenceRequired:1b,CustomNameVisible:1b,CustomName:{text:"Dummy",color:"red"}}
function demo:join_new with storage demo:tmp
give @s minecraft:diamond_sword
tellraw @s {"text":"[demo] Enemy dummy spawned.","color":"yellow"}
