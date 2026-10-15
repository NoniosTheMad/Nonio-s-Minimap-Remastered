# macro (slot exit: x y z = the block the feet go in)
$forceload add $(x) $(z)
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~ ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["nx.aslot","nx.as_new"]}
data modify entity @e[type=marker,tag=nx.as_new,limit=1] data set from storage nonios:arena tmp.sl[0]
scoreboard players add #slots nx.arena 1
scoreboard players operation @e[type=marker,tag=nx.as_new] nx.ar_slot = #slots nx.arena
tag @e[type=marker,tag=nx.as_new] remove nx.as_new
