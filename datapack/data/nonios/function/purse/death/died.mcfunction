# as a player who died and has respawned (called by nonios:death).
# Coins still here = no player/holder took them (mob, fall, void...) -> they drop as a coin bag where the player died
# (LastDeathLocation: with immediate_respawn the player is already back at spawn). Void deaths: the bag falls = lost.
scoreboard players set @s nx.plast -1
execute unless score @s nx.coins matches 1.. run return 0
execute store result storage nonios:purse at.x int 1 run data get entity @s LastDeathLocation.pos[0]
execute store result storage nonios:purse at.y int 1 run data get entity @s LastDeathLocation.pos[1]
execute store result storage nonios:purse at.z int 1 run data get entity @s LastDeathLocation.pos[2]
function nonios:purse/death/drop_at with storage nonios:purse at
