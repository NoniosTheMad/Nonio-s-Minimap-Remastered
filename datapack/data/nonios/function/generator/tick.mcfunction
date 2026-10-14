# every tick (nonios:tick): lucky blocks that were just mined, upgrade dialog clicks
execute as @e[type=marker,tag=nx.gen_lucky] at @s if block ~ ~ ~ #minecraft:air run function nonios:generator/lucky/burst
function nonios:generator/ui/tick
