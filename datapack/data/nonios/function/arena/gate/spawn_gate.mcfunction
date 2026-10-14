# macro (one gate: team, x y z = pad centre block, out): marker at foot level on the pad + label above it
$forceload add $(x) $(z)
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~1 ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["nx.agate","nx.ag_new","nx.$(team)"]}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~3 ~0.5 run summon minecraft:text_display ~ ~ ~ {Tags:["nx.agate_label"],billboard:"center",alignment:"center",text:{text:"ARENA",color:"dark_gray",bold:true}}
data modify entity @e[type=marker,tag=nx.ag_new,limit=1] data set from storage nonios:arena tmp.gl[0]
tag @e[type=marker,tag=nx.ag_new] remove nx.ag_new
scoreboard players add #gates nx.arena 1
