# with <team>.agate {team,x,y,z,out}: arena gate pad (3x3, centre = the gate). Marker + label come from arena/setup (gate/spawn_gate).
$execute positioned $(x) $(y) $(z) run fill ~-1 ~ ~-1 ~1 ~ ~1 minecraft:polished_blackstone_bricks
$execute positioned $(x) $(y) $(z) run setblock ~ ~ ~ minecraft:crying_obsidian
$execute positioned $(x) $(y) $(z) run setblock ~-1 ~1 ~-1 minecraft:polished_blackstone_wall
$execute positioned $(x) $(y) $(z) run setblock ~-1 ~2 ~-1 minecraft:soul_lantern
$execute positioned $(x) $(y) $(z) run setblock ~1 ~1 ~-1 minecraft:polished_blackstone_wall
$execute positioned $(x) $(y) $(z) run setblock ~1 ~2 ~-1 minecraft:soul_lantern
$execute positioned $(x) $(y) $(z) run setblock ~-1 ~1 ~1 minecraft:polished_blackstone_wall
$execute positioned $(x) $(y) $(z) run setblock ~-1 ~2 ~1 minecraft:soul_lantern
$execute positioned $(x) $(y) $(z) run setblock ~1 ~1 ~1 minecraft:polished_blackstone_wall
$execute positioned $(x) $(y) $(z) run setblock ~1 ~2 ~1 minecraft:soul_lantern
