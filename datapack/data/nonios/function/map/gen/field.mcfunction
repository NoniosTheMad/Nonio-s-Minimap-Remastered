# with storage nonios:map <team>: island + trim (props: map/gen/props)
$fill $(x1) 60 $(z1) $(x2) 60 $(z2) minecraft:stone
$fill $(x1) 61 $(z1) $(x2) 62 $(z2) minecraft:dirt
$fill $(x1) $(y) $(z1) $(x2) $(y) $(z2) minecraft:grass_block
$fill $(x1) $(y) $(z1) $(x2) $(y) $(z1) $(trim)
$fill $(x1) $(y) $(z2) $(x2) $(y) $(z2) $(trim)
$fill $(x1) $(y) $(z1) $(x1) $(y) $(z2) $(trim)
$fill $(x2) $(y) $(z1) $(x2) $(y) $(z2) $(trim)
