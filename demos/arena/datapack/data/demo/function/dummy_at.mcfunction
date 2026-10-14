$summon minecraft:husk ~ ~ ~ {Tags:["nx.captor","demo.dummy","demo.dnew"],NoAI:1b,PersistenceRequired:1b,Silent:1b,CustomName:{text:"$(n) dummy",color:"$(c)"},CustomNameVisible:1b,Glowing:1b}
$team join $(t) @e[type=husk,tag=demo.dnew]
spreadplayers ~ ~ 0 1.8 under 66 false @e[type=husk,tag=demo.dnew]
tag @e[type=husk,tag=demo.dnew] remove demo.dnew
$tellraw @a [{text:"[demo] ",color:"aqua"},{text:"$(n) dummy",color:"$(c)"},{text:" placed on the ",color:"aqua"},{entity:"@s",nbt:"data.name",color:"yellow"},{text:" (it counts for capture; hit it to remove it)",color:"aqua"}]
