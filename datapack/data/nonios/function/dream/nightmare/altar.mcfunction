# as the altar marker (cell above the lodestone plinth)
summon minecraft:interaction ~ ~ ~ {Tags:["nx.dream","nx.dream_exodia_hit"],width:1.4f,height:1.6f,response:1b}
summon minecraft:item_display ~ ~1 ~ {Tags:["nx.dream","nx.dream_exodia_fx"],item:{id:"minecraft:nether_star",count:1},billboard:"vertical",Glowing:1b,brightness:{sky:15,block:15},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.2f,1.2f,1.2f]}}
