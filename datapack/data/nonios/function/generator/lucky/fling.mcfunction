# one emerald with a random sideways/upward push; repeats #ln times
summon minecraft:item ~ ~0.6 ~ {Item:{id:"minecraft:emerald",count:1},Tags:["nx.gen_fling"],PickupDelay:10s}
execute store result storage nonios:gen fling.x double 0.01 run random value -25..25
execute store result storage nonios:gen fling.z double 0.01 run random value -25..25
execute store result storage nonios:gen fling.y double 0.01 run random value 25..45
execute as @e[type=item,tag=nx.gen_fling,distance=..2] run function nonios:generator/lucky/push with storage nonios:gen fling
scoreboard players remove #ln nx.gen 1
execute if score #ln nx.gen matches 1.. run function nonios:generator/lucky/fling
