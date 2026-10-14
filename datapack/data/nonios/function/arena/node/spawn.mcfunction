# macro: storage nonios:arena n (one resolved node). The chunk must be loaded (forceload is added for later).
$forceload add $(x) $(z)
$summon minecraft:marker $(x) $(y) $(z) {Tags:["nx.node","nx.node_new"]}
$execute positioned $(x) $(y) $(z) as @e[type=marker,tag=nx.node_new,distance=..1,limit=1] at @s run function nonios:arena/node/init
