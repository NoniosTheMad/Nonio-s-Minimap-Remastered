# 20 s without finding ground: land on the emerald raft at 0 0 (forceloaded)
execute in nonios:emerald_dream run fill -2 239 -2 2 239 2 minecraft:emerald_block
execute in nonios:emerald_dream run fill -1 239 -1 1 239 1 minecraft:moss_block
execute in nonios:emerald_dream run tp @s 0.5 240 0.5
execute in nonios:emerald_dream positioned 0.5 240 0.5 run function nonios:dream/arrive/landed
