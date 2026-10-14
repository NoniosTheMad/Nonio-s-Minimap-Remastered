# Small arena: 41x41 floor at y=63, low wall, three node pads (5x5 zone, yellow border, beacon under the centre).
forceload add -24 -24 24 24
fill -20 61 -20 20 62 20 minecraft:stone
fill -20 63 -20 20 63 20 minecraft:smooth_stone
fill -20 64 -20 20 75 20 minecraft:air
fill -20 64 -20 20 64 -20 minecraft:stone_brick_wall
fill -20 64 20 20 64 20 minecraft:stone_brick_wall
fill -20 64 -20 -20 64 20 minecraft:stone_brick_wall
fill 20 64 -20 20 64 20 minecraft:stone_brick_wall
execute positioned -11 63 -3 run function demo:pad
execute positioned 0 63 -13 run function demo:pad
execute positioned 11 63 -3 run function demo:pad
kill @e[type=item]
kill @e[tag=demo.prop]
kill @e[tag=demo.dummy]
setworldspawn 0 64 10
summon minecraft:text_display 0.5 66.2 6.5 {Tags:["demo.prop","demo.info"],billboard:"center",alignment:"center",line_width:260,text:""}
summon minecraft:text_display 0.5 65.4 6.5 {Tags:["demo.prop"],billboard:"center",alignment:"center",line_width:260,text:{text:"Stand on a pad to capture it.  G > Demo: Arena for dummies, events, lightning, x10",color:"gray"}}
data modify storage demo:arena built set value 1b
schedule function demo:build2 5t
