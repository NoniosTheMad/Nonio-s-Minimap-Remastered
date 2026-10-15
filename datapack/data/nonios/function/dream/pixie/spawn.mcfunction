kill @e[tag=nx.pix_me]
summon minecraft:allay ~-0.8 ~1.45 ~-0.8 {Tags:["nx.dream","nx.pixie","nx.pix_me","nx.pix_new"],NoAI:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:{text:"Pixie",color:"#7dffc8",italic:true}}
summon minecraft:interaction ~-0.8 ~1.15 ~-0.8 {Tags:["nx.dream","nx.pixie","nx.pix_me","nx.pix_new","nx.shop_npc","nx.any"],width:0.9f,height:0.9f,response:1b}
scoreboard players operation @e[tag=nx.pix_new] nx.pid = #me nx.dream
tag @e[tag=nx.pix_new] remove nx.pix_new
particle minecraft:end_rod ~-0.8 ~1.6 ~-0.8 0.2 0.2 0.2 0.03 10
playsound minecraft:entity.allay.ambient_with_item neutral @a ~ ~ ~ 0.6 1.4
