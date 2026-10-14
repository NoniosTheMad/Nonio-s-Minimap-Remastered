forceload add -24 -24 24 24
fill -20 63 -20 20 63 20 minecraft:smooth_stone
fill -20 62 -20 20 62 20 minecraft:barrier
function demo:mine
# bank pad (west)
fill -9 63 -1 -7 63 1 minecraft:gold_block
kill @e[tag=demo.prop]
summon minecraft:marker -7.5 64 0.5 {Tags:["nx.bank_zone","demo.prop"]}
summon minecraft:text_display -7.5 66 0.5 {Tags:["demo.prop"],billboard:"center",text:{text:"TEAM BANK\nstand on the gold to deposit",color:"green"}}
summon minecraft:text_display 5.5 71 -3.5 {Tags:["demo.prop"],billboard:"center",text:{text:"MINE\ncoal/copper 3, iron/redstone 5,\nlapis 6, gold 8, diamond 20, emerald 25\nstone/deepslate: nothing (building blocks)",color:"gold"}}
summon minecraft:text_display 0.5 66 -12.5 {Tags:["demo.prop"],billboard:"center",text:{text:"Thief arena\nG > Demo: Coin Purse > Spawn Purse Thief",color:"red"}}
data modify storage demo:state built set value 1b
