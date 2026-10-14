# with storage nonios:map lobby
$fill $(x1) $(y) $(z1) $(x2) $(y) $(z2) minecraft:smooth_quartz
$fill $(x1) $(y) $(z1) $(x2) $(y) $(z1) minecraft:quartz_bricks
$fill $(x1) $(y) $(z2) $(x2) $(y) $(z2) minecraft:quartz_bricks
$fill $(x1) $(y) $(z1) $(x1) $(y) $(z2) minecraft:quartz_bricks
$fill $(x2) $(y) $(z1) $(x2) $(y) $(z2) minecraft:quartz_bricks
$fill -3 $(y) $(z1) -1 $(y) $(z1) minecraft:white_concrete
$fill 1 $(y) $(z1) 3 $(y) $(z1) minecraft:black_concrete
kill @e[type=text_display,tag=nx.lobby_prop]
$summon minecraft:text_display $(x) 67 $(z2) {Tags:["nx.lobby_prop"],billboard:"center",background:1073741824,text:[{text:"Nonios's Map",color:"gold",bold:true},{text:"\nLobby",color:"gray"},{text:"\n\nPick a team: G > Nonios's Map > Choose team",color:"white"},{text:"\nAdmin: G > Nonios's Map > Admin panel",color:"gray"}]}
