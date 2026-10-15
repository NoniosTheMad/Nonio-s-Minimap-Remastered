# with <team>.wall {team,z,tint}: barrier plane x -64..64, y -64..59 and 64..140 (the island layers 60..63 stay solid ground).
# Underground (dug through the island layers / built below them) the barrier blocks only fill air: game/prep/contain
# bounces anyone past the wall row at any depth, so a tunnel through solid ground never gets further than the wall.
$fill -64 64 $(z) 64 140 $(z) minecraft:barrier replace minecraft:air
$fill -64 0 $(z) 64 59 $(z) minecraft:barrier replace minecraft:air
$fill -64 -64 $(z) 64 -1 $(z) minecraft:barrier replace minecraft:air
$kill @e[type=item_display,tag=nx.wall,tag=nx.$(team)]
$execute positioned 0 65 $(z) run function nonios:map/walls/row {team:"$(team)",tint:$(tint)}
$execute positioned 0 69 $(z) run function nonios:map/walls/row {team:"$(team)",tint:$(tint)}
$execute positioned 0 73 $(z) run function nonios:map/walls/row {team:"$(team)",tint:$(tint)}
$execute positioned 0 77 $(z) run function nonios:map/walls/row {team:"$(team)",tint:$(tint)}
$execute positioned 0 81 $(z) run function nonios:map/walls/row {team:"$(team)",tint:$(tint)}
