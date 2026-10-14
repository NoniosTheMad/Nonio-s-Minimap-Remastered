# overworld test pad + a portal styled after the original exit platform (end bricks, frame, purpur pillars with end rods)
forceload add -16 -16 16 16
fill -12 63 -12 12 63 12 minecraft:smooth_stone
fill -12 62 -12 12 62 12 minecraft:barrier
fill 4 63 -2 8 63 2 minecraft:end_stone_bricks
setblock 6 63 0 minecraft:end_portal_frame[eye=true]
setblock 4 64 -2 minecraft:purpur_pillar
setblock 4 64 2 minecraft:purpur_pillar
setblock 8 64 -2 minecraft:purpur_pillar
setblock 8 64 2 minecraft:purpur_pillar
setblock 4 65 -2 minecraft:end_rod
setblock 4 65 2 minecraft:end_rod
setblock 8 65 -2 minecraft:end_rod
setblock 8 65 2 minecraft:end_rod
kill @e[tag=demo.prop]
summon minecraft:text_display 6.5 66.2 0.5 {Tags:["demo.prop"],billboard:"center",text:{text:"Travel to Emerald Dream",color:"green"}}
summon minecraft:text_display 6.5 65.7 0.5 {Tags:["demo.prop"],billboard:"center",scale:[0.6f,0.6f,0.6f],text:{text:"step on the frame (or G > Demo: Emerald Dream)",color:"gray"}}
data modify storage demo:state built set value 1b
