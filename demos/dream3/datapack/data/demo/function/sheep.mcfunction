execute unless dimension nonios:emerald_dream run return run tellraw @s {"text":"[demo] enter the Dream first","color":"gray"}
summon minecraft:sheep ~2 ~ ~ {Tags:["nx.dfauna","demo.sheep"]}
execute as @e[type=sheep,tag=demo.sheep] run function nonios:dream/fauna/gleam
tag @e[tag=demo.sheep] remove demo.sheep
tellraw @s {"text":"[demo] a gleaming sheep (6-10 emeralds, 35% Dream Key)","color":"yellow"}
