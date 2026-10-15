# every tick (nonios:tick): single blocks that were just mined, upgrade dialog clicks
execute as @e[type=marker,tag=nx.gen_one] at @s unless block ~ ~ ~ #nonios:generator/single run function nonios:generator/one/mined
# instant regrowth (#109): an empty spot gets its next block in the same tick (both styles); upgrades only change the pool
execute as @e[type=marker,tag=nx.gen] at @s if block ~ ~ ~ #minecraft:air run function nonios:generator/grow
function nonios:generator/ui/tick
