# with storage nonios:map arena: stone-brick floor, some cover, contested diamond/emerald ores in the middle
$fill $(x1) 60 $(z1) $(x2) 62 $(z2) minecraft:cobblestone
$fill $(x1) $(y) $(z1) $(x2) $(y) $(z2) minecraft:stone_bricks
$fill $(x1) $(y) $(z1) $(x1) $(y) $(z2) minecraft:mossy_stone_bricks
$fill $(x2) $(y) $(z1) $(x2) $(y) $(z2) minecraft:mossy_stone_bricks
fill -9 64 93 -6 66 93 minecraft:polished_andesite
fill 6 64 93 9 66 93 minecraft:polished_andesite
fill -9 64 107 -6 66 107 minecraft:polished_andesite
fill 6 64 107 9 66 107 minecraft:polished_andesite
fill -1 64 99 1 64 101 minecraft:deepslate_diamond_ore
setblock 0 65 100 minecraft:emerald_ore
fill -13 64 99 -12 65 101 minecraft:iron_ore
fill 12 64 99 13 65 101 minecraft:gold_ore
summon minecraft:text_display 0.5 68 100.5 {billboard:"center",text:[{text:"ARENA",color:"red",bold:true},{text:"\ndiamonds in the middle",color:"gray"}]}
