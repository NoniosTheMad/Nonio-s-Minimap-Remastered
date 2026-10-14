# with <team>.altar {team,Team,x,y,z}: offering altar. 3x3 blackstone pad (crying obsidian centre) under a respawn anchor
# (block_display over a barrier core: unbreakable), interaction nx.altar_npc (right-click -> altar/click), marker nx.altar,
# hologram nx.altar_txt (altar/refresh writes it).
$execute positioned $(x) $(y) $(z) run fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 minecraft:polished_blackstone_bricks
$execute positioned $(x) $(y) $(z) run setblock ~ ~-1 ~ minecraft:crying_obsidian
$execute positioned $(x) $(y) $(z) run setblock ~ ~ ~ minecraft:barrier
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~ ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["nx.altar","nx.$(team)"]}
$execute positioned $(x) $(y) $(z) align xyz run summon minecraft:block_display ~ ~ ~ {Tags:["nx.altar_fx","nx.$(team)"],block_state:{id:"minecraft:respawn_anchor",properties:{charges:"1"}},brightness:{sky:15,block:15}}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~ ~0.5 run summon minecraft:interaction ~ ~-0.02 ~ {Tags:["nx.altar_npc","nx.$(team)"],width:1.1f,height:1.1f,response:1b}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~2.1 ~0.5 run summon minecraft:text_display ~ ~ ~ {Tags:["nx.altar_txt","nx.$(team)"],billboard:"center",alignment:"center",text:{text:"OFFERINGS",color:"light_purple",bold:true}}
