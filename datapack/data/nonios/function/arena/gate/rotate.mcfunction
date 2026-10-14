# Pick the active slot at random (uniform, may stay the same: V2 rolled a dispenser). Restarts the rotation timer.
tag @e[type=marker,tag=nx.aslot_on] remove nx.aslot_on
scoreboard players operation #g_t nx.arena = #g_every nx.arena
scoreboard players set #slot nx.arena 0
execute unless score #slots nx.arena matches 1.. run return 0
scoreboard players set #r nx.arena 1
data modify storage nonios:arena tmp.roll set value {}
execute store result storage nonios:arena tmp.roll.max int 1 run scoreboard players get #slots nx.arena
execute if score #slots nx.arena matches 2.. run function nonios:arena/event/roll with storage nonios:arena tmp.roll
scoreboard players operation #slot nx.arena = #r nx.arena
execute as @e[type=marker,tag=nx.aslot] if score @s nx.ar_slot = #slot nx.arena run tag @s add nx.aslot_on
