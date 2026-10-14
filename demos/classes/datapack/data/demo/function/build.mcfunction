# Demo arena: floor, a few walls to jump over, spawn platform.
forceload add -24 -24 24 24
fill -20 63 -20 20 63 20 minecraft:mossy_stone_bricks
fill -20 62 -20 20 62 20 minecraft:barrier
fill -20 64 -20 20 90 20 minecraft:air
fill -20 64 -20 20 66 -20 minecraft:stone_bricks
fill -20 64 20 20 66 20 minecraft:stone_bricks
fill -20 64 -20 -20 66 20 minecraft:stone_bricks
fill 20 64 -20 20 66 20 minecraft:stone_bricks
fill 6 64 -12 14 71 -10 minecraft:polished_blackstone_bricks
fill -14 63 6 -10 63 14 minecraft:water
fill -14 64 6 -10 64 14 minecraft:lily_pad
kill @e[type=item]
kill @e[tag=demo.prop]
kill @e[tag=nx.cls_dummy]
summon minecraft:text_display 0.5 66.5 3.5 {Tags:["demo.prop"],billboard:"center",text:{text:"Classes\nG > Demo: Classes to pick one\nthe wall (NE) is 8 high: try the frog's jump and broom",color:"dark_purple"}}
setworldspawn 0 64 0
data modify storage demo:state built set value 1b
