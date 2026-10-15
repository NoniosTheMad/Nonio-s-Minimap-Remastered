# the marker (logic) + the spinning emerald core (visual; its size = level). No hologram, no click: it just spits.
summon minecraft:marker ~ ~ ~ {Tags:["nx.cgen","nx.cgen_part","nx.cgen_new"]}
summon minecraft:item_display ~ ~1.1 ~ {Tags:["nx.cgen_part","nx.cgen_core"],teleport_duration:10,item_display:"fixed",item:{id:"minecraft:emerald",count:1},brightness:{sky:15,block:15},glow_color_override:5635925,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.2f,1.2f,1.2f]}}
scoreboard players set #cgen nx.arena 1
execute as @e[type=marker,tag=nx.cgen_new,distance=..0.1,limit=1] at @s run function nonios:arena/cgen/init
