# no ground in this column (void, water...): try a nearby column; after 12 misses, a fresh random point
scoreboard players add @s nx.drol 1
execute if score @s nx.drol matches 12.. run scoreboard players set @s nx.drol 0
execute if score @s nx.drol matches 0 run return run function nonios:dream/arrive/roll
execute store result storage nonios:dream roll.dx int 1 run random value -40..40
execute store result storage nonios:dream roll.dz int 1 run random value -40..40
function nonios:dream/arrive/nudge with storage nonios:dream roll
