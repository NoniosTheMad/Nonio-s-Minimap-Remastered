# with <team>.bank {team,x,y,z,facing}: 3x3 gold pad with a vault in the middle and 8 gold pressure plates around it.
# Stepping onto a plate deposits the whole purse (bank/pad, own team only). Right-clicking the vault
# (interaction nx.bank_npc -> advancement nonios:bank/click) opens the withdraw dialog.
# Marker nx.bank_zone + nx.<team> = where bank/near measures config bank_range from (own team only).
$execute positioned $(x) $(y) $(z) run fill ~-1 ~ ~-1 ~1 ~ ~1 minecraft:gold_block
$execute positioned $(x) $(y) $(z) run fill ~-1 ~1 ~-1 ~1 ~1 ~1 minecraft:light_weighted_pressure_plate
# solid but invisible core under the vault display (the slightly larger interaction box still catches the click)
$execute positioned $(x) $(y) $(z) run setblock ~ ~1 ~ minecraft:barrier
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~1 ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["nx.bank_zone","nx.$(team)"]}
$execute positioned $(x) $(y) $(z) align xyz positioned ~ ~1 ~ run summon minecraft:block_display ~ ~ ~ {Tags:["nx.bank_fx","nx.$(team)"],block_state:{id:"minecraft:vault",properties:{facing:"$(facing)",vault_state:"active"}},brightness:{sky:15,block:15}}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~1 ~0.5 run summon minecraft:interaction ~ ~-0.02 ~ {Tags:["nx.bank_npc","nx.$(team)"],width:1.1f,height:1.1f,response:1b}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~3.2 ~0.5 run summon minecraft:text_display ~ ~ ~ {billboard:"center",text:{text:"TEAM BANK",color:"gold",bold:true}}
