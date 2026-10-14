# with <team>.label {Team,color,x,y,z}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~ ~0.5 run summon minecraft:text_display ~ ~ ~ {billboard:"center",text:{text:"$(Team) BASE",color:"$(color)",bold:true}}
