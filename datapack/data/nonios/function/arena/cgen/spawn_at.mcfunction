summon minecraft:marker ~ ~ ~ {Tags:["nx.cgen","nx.cgen_part","nx.cgen_new"]}
summon minecraft:item_display ~ ~0.9 ~ {Tags:["nx.cgen_part","nx.cgen_core"],teleport_duration:10,item_display:"fixed",item:{id:"minecraft:iron_ingot",count:1},brightness:{sky:15,block:15},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]}}
summon minecraft:text_display ~ ~2.3 ~ {Tags:["nx.cgen_part","nx.cgen_holo"],billboard:"center",alignment:"center",line_width:220,text:""}
summon minecraft:interaction ~ ~ ~ {Tags:["nx.cgen_part","nx.cgen_click"],width:1.2f,height:1.8f,response:1b}
scoreboard players set #cgen nx.arena 1
execute as @e[type=marker,tag=nx.cgen_new,distance=..0.1,limit=1] at @s run function nonios:arena/cgen/init
