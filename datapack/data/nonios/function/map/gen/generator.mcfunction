# with <team>.gen {team,lvl,x,y,z}: the field's resource generator (3x3 structure + marker on top of its sea lantern)
$execute positioned $(x) $(y) $(z) run function nonios:generator/spawn {team:"$(team)",lvl:$(lvl)}
