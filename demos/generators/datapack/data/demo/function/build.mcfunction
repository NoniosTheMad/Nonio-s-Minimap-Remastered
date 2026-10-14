# Demo arena: floor + three generators north of spawn (white Lv1, black Lv2, white Lv3).
forceload add -24 -24 24 24
fill -20 63 -20 20 63 20 minecraft:smooth_stone
fill -20 62 -20 20 62 20 minecraft:barrier
fill -20 64 -20 20 70 20 minecraft:air
kill @e[type=item]
kill @e[tag=demo.prop]
execute as @e[type=marker,tag=nx.gen] at @s run function nonios:generator/remove
execute positioned -6 65 -6 run function nonios:generator/spawn {team:"white",lvl:1}
execute positioned 0 65 -6 run function nonios:generator/spawn {team:"black",lvl:2}
execute positioned 6 65 -6 run function nonios:generator/spawn {team:"white",lvl:3}
summon minecraft:text_display 0.5 66.5 3.5 {Tags:["demo.prop"],billboard:"center",text:{text:"Resource generators\nright-click one to collect its coins and drops\nG > Demo: Generators for upgrades, time x10, coins",color:"aqua"}}
data modify storage demo:state built set value 1b
