# with <team>.wall {team,z,tint}: barrier plane x -64..64, y 0..59 and 64..140 (the island layers 60..63 stay solid ground)
$fill -64 64 $(z) 64 140 $(z) minecraft:barrier replace minecraft:air
$fill -64 0 $(z) 64 59 $(z) minecraft:barrier replace minecraft:air
$kill @e[type=item_display,tag=nx.wall,tag=nx.$(team)]
$execute positioned 0 65 $(z) run function nonios:map/walls/row {team:"$(team)",tint:$(tint)}
$execute positioned 0 69 $(z) run function nonios:map/walls/row {team:"$(team)",tint:$(tint)}
$execute positioned 0 73 $(z) run function nonios:map/walls/row {team:"$(team)",tint:$(tint)}
$execute positioned 0 77 $(z) run function nonios:map/walls/row {team:"$(team)",tint:$(tint)}
$execute positioned 0 81 $(z) run function nonios:map/walls/row {team:"$(team)",tint:$(tint)}
