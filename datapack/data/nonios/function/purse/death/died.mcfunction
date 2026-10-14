# as a player whose deathCount went up (next tick, body still at the death spot).
# Coins still here = no player/holder took them -> drop a coin bag (void deaths: the bag falls into the void = lost).
scoreboard players set @s nx.died 0
scoreboard players set @s nx.plast -1
execute if score @s coins matches 1.. at @s run function nonios:purse/death/drop
