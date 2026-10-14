$summon minecraft:marker ~ ~ ~ {Tags:["nx.gen","nx.gen.$(team)","nx.gen_new"],data:{team:"$(team)",lvl:$(lvl)}}
summon minecraft:item_display ~ ~0.9 ~ {Tags:["nx.gen_part","nx.gen_core"],teleport_duration:20,item_display:"fixed",item:{id:"minecraft:iron_ingot",count:1},brightness:{sky:15,block:15},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:text_display ~ ~2 ~ {Tags:["nx.gen_part","nx.gen_holo"],billboard:"center",alignment:"center",line_width:220,text:""}
summon minecraft:interaction ~ ~-1 ~ {Tags:["nx.gen_part","nx.gen_click"],width:1.1f,height:2.6f,response:1b}
execute as @e[type=marker,tag=nx.gen_new,distance=..0.1,limit=1] at @s run function nonios:generator/init
