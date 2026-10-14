# every tick (nonios:tick): single blocks that were just mined, upgrade dialog clicks
execute as @e[type=marker,tag=nx.gen_one] at @s unless block ~ ~ ~ #nonios:generator/single run function nonios:generator/one/mined
function nonios:generator/ui/tick
