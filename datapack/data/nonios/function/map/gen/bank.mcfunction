# with <team>.bank {team,x,y,z,facing}: 5x5 gold floor (raw gold rim, gold blocks inside) with a vault in the middle.
# The floor marks the bank zone: entering it (walk, jump, fly) deposits the whole purse (bank/zone, own team only, no blocks
# involved). Right-clicking the vault
# (interaction nx.bank_npc -> advancement nonios:bank/click) opens the withdraw dialog.
# Marker nx.bank_zone + nx.<team> = where bank/near measures config bank_range from (own team only).
$execute positioned $(x) $(y) $(z) run fill ~-2 ~ ~-2 ~2 ~ ~2 minecraft:raw_gold_block
$execute positioned $(x) $(y) $(z) run fill ~-1 ~ ~-1 ~1 ~ ~1 minecraft:gold_block
# open air over the zone (also removes the bank v4 pressure plates from older worlds)
$execute positioned $(x) $(y) $(z) run fill ~-2 ~1 ~-2 ~2 ~3 ~2 minecraft:air
# solid but invisible core under the vault display (the slightly larger interaction box still catches the click)
$execute positioned $(x) $(y) $(z) run setblock ~ ~1 ~ minecraft:barrier
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~1 ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["nx.bank_zone","nx.$(team)"]}
$execute positioned $(x) $(y) $(z) align xyz positioned ~ ~1 ~ run summon minecraft:block_display ~ ~ ~ {Tags:["nx.bank_fx","nx.$(team)"],block_state:{id:"minecraft:vault",properties:{facing:"$(facing)",vault_state:"active"}},brightness:{sky:15,block:15}}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~1 ~0.5 run summon minecraft:interaction ~ ~-0.02 ~ {Tags:["nx.bank_npc","nx.$(team)"],width:1.1f,height:1.1f,response:1b}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~3.2 ~0.5 run summon minecraft:text_display ~ ~ ~ {billboard:"center",text:{text:"TEAM BANK",color:"gold",bold:true}}
