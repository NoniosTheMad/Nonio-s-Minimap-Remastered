# with <team>.bank {team,x,y,z}: 3x3 gold pad; marker nx.bank_zone + nx.<team> (purse/tick deposits own team only)
$execute positioned $(x) $(y) $(z) run fill ~-1 ~ ~-1 ~1 ~ ~1 minecraft:gold_block
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~1 ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["nx.bank_zone","nx.$(team)"]}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~3.2 ~0.5 run summon minecraft:text_display ~ ~ ~ {billboard:"center",text:[{text:"TEAM BANK",color:"green",bold:true},{text:"\nstand on the gold to deposit your purse",color:"gray"}]}
