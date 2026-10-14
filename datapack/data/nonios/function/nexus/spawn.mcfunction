# function nonios:nexus/spawn {team:"white",x:0,y:64,z:-8}
$setblock $(x) $(y) $(z) minecraft:obsidian
$kill @e[tag=nx.$(team)]
$summon minecraft:marker $(x) $(y) $(z) {Tags:["nx.core","nx.$(team)"]}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~-0.1 ~0.5 run summon minecraft:interaction ~ ~ ~ {Tags:["nx.shield","nx.$(team)"],width:1.3f,height:1.25f,response:1b}
# shell = forcefield-textured cube (resourcepack nonios:nexus_shield), tinted per team via dyed_color.
# Spawns collapsed (scale 0); fx/reform grows it 2 ticks later so the client interpolates.
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~0.5 ~0.5 run summon minecraft:item_display ~ ~ ~ {Tags:["nx.shield_fx","nx.reform","nx.$(team)"],item:{id:"minecraft:glass",count:1,components:{"minecraft:item_model":"nonios:nexus_shield"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0f,0f,0f]}}
$execute as @e[type=interaction,tag=nx.shield,tag=nx.$(team)] store result score @s nx.col run data get storage nonios:nexus team.$(team).col[0]
$execute as @e[type=item_display,tag=nx.shield_fx,tag=nx.$(team)] store result entity @s item.components."minecraft:dyed_color" int 1 run data get storage nonios:nexus team.$(team).col[0]
$execute as @e[type=interaction,tag=nx.shield,tag=nx.$(team)] run function nonios:nexus/reset_hp
$bossbar set nonios:barrier_$(team) visible true
schedule function nonios:nexus/fx/reform 2t append
