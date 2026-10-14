# with <team>.nexus {team,x,y,z}: the obsidian itself is placed by nexus/spawn at match start
$execute positioned $(x) $(y) $(z) run fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 minecraft:polished_blackstone_bricks
$execute positioned $(x) $(y) $(z) run setblock ~ ~ ~ minecraft:air
$execute positioned $(x) $(y) $(z) run summon minecraft:text_display ~ ~2.2 ~ {billboard:"center",text:{text:"NEXUS",color:"dark_purple",bold:true}}
