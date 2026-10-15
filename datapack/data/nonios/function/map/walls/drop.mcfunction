$fill -64 64 $(z) 64 140 $(z) minecraft:air replace minecraft:barrier
$fill -64 0 $(z) 64 59 $(z) minecraft:air replace minecraft:barrier
$fill -64 -64 $(z) 64 -1 $(z) minecraft:air replace minecraft:barrier
$execute as @e[type=item_display,tag=nx.wall,tag=nx.$(team)] at @s run particle minecraft:electric_spark ~ ~ ~ 1.5 1.5 0.1 0.2 12 force
$kill @e[type=item_display,tag=nx.wall,tag=nx.$(team)]
$execute positioned 0 70 $(z) run particle minecraft:explosion_emitter ~ ~ ~.5 8 4 0 0 6 force
