# with <team>.dream {team,Team,x,y,z}: Emerald Dream portal pad (styled after the V2 exit platform). x y z = centre floor block.
# Stepping on the frame = portal/step. Marker nx.dream_pad + nx.<team> marks whose pad it is.
$execute positioned $(x) $(y) $(z) run fill ~-2 ~ ~-2 ~2 ~ ~2 minecraft:end_stone_bricks
$execute positioned $(x) $(y) $(z) run setblock ~ ~ ~ minecraft:end_portal_frame[eye=true]
$execute positioned $(x) $(y) $(z) run fill ~-2 ~1 ~-2 ~-2 ~1 ~-2 minecraft:purpur_pillar
$execute positioned $(x) $(y) $(z) run fill ~2 ~1 ~-2 ~2 ~1 ~-2 minecraft:purpur_pillar
$execute positioned $(x) $(y) $(z) run fill ~-2 ~1 ~2 ~-2 ~1 ~2 minecraft:purpur_pillar
$execute positioned $(x) $(y) $(z) run fill ~2 ~1 ~2 ~2 ~1 ~2 minecraft:purpur_pillar
$execute positioned $(x) $(y) $(z) run setblock ~-2 ~2 ~-2 minecraft:end_rod
$execute positioned $(x) $(y) $(z) run setblock ~2 ~2 ~-2 minecraft:end_rod
$execute positioned $(x) $(y) $(z) run setblock ~-2 ~2 ~2 minecraft:end_rod
$execute positioned $(x) $(y) $(z) run setblock ~2 ~2 ~2 minecraft:end_rod
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~1 ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["nx.dream_pad","nx.$(team)"]}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~3 ~0.5 run summon minecraft:text_display ~ ~ ~ {Tags:["nx.dream_label","nx.$(team)"],billboard:"center",alignment:"center",text:{text:"EMERALD DREAM",color:"dark_green",bold:true}}
