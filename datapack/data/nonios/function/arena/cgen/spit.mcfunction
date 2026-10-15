# at the centre generator: throw one emerald out of the core in a random direction, #left times
execute if score #left nx.arena matches ..0 run return 0
summon minecraft:item ~ ~1.1 ~ {Tags:["nx.cg_em","nx.cg_new"],PickupDelay:10s,Item:{id:"minecraft:emerald",count:1},Motion:[0d,0.38d,0d]}
execute as @e[type=item,tag=nx.cg_new,distance=..2] run function nonios:arena/cgen/fling
scoreboard players remove #left nx.arena 1
function nonios:arena/cgen/spit
