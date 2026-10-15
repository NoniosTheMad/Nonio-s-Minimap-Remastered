# once a second, in the Dream (positioned anywhere in it)
# a site's loot chest has been opened (its LootTable is gone): its beacon beam goes out
execute as @e[type=marker,tag=nx.dream_loot,distance=0..] at @s unless data block ~ ~ ~ LootTable run function nonios:dream/site/looted
# beacons are scenery here: a mined one drops nothing
execute as @e[type=item,distance=0..] if items entity @s contents minecraft:beacon run kill @s
