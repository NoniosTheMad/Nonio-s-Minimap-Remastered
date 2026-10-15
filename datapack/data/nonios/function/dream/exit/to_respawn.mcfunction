data modify storage nonios:dream back set value {}
data modify storage nonios:dream back.dim set from entity @s respawn.dimension
execute store result storage nonios:dream back.x int 1 run data get entity @s respawn.pos[0]
execute store result storage nonios:dream back.y int 1 run data get entity @s respawn.pos[1]
execute store result storage nonios:dream back.z int 1 run data get entity @s respawn.pos[2]
data modify storage nonios:dream back.yaw set value 0f
data modify storage nonios:dream back.pitch set value 0f
execute unless data storage nonios:dream back.dim run data modify storage nonios:dream back.dim set value "minecraft:overworld"
function nonios:dream/exit/tp_back with storage nonios:dream back
