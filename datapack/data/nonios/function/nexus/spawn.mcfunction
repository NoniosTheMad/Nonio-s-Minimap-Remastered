# function nonios:nexus/spawn {team:"white",x:0,y:64,z:-8}
$setblock $(x) $(y) $(z) minecraft:obsidian
$kill @e[tag=nx.$(team)]
$summon minecraft:marker $(x) $(y) $(z) {Tags:["nx.core","nx.$(team)"]}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~-0.1 ~0.5 run summon minecraft:interaction ~ ~ ~ {Tags:["nx.shield","nx.$(team)"],width:1.3f,height:1.25f,response:1b}
$summon minecraft:block_display $(x) $(y) $(z) {Tags:["nx.shield_fx","nx.$(team)"],block_state:{Name:"minecraft:light_blue_stained_glass"},brightness:{sky:15,block:15},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[-0.15f,-0.15f,-0.15f],scale:[1.3f,1.3f,1.3f]}}
$execute as @e[type=interaction,tag=nx.shield,tag=nx.$(team)] run function nonios:nexus/reset_hp
$bossbar set nonios:barrier_$(team) visible true
