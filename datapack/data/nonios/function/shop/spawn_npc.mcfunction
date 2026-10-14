# Shopkeeper: a still villager (visual) inside an interaction entity (catches right-clicks -> advancement nonios:shop/npc).
# function nonios:shop/spawn_npc {team:"white"|"black"|"any",x:0,y:64,z:-4,yaw:0}
# The shop only opens for the NPC's own team (team "any" = everyone, spike demo).
$kill @e[tag=nx.shop_npc,tag=nx.$(team)]
$summon villager $(x) $(y) $(z) {Tags:["nx.shop_npc","nx.$(team)"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,Rotation:[$(yaw)f,0f],CustomName:{text:"Shop",color:"gold",bold:true},CustomNameVisible:1b,VillagerData:{profession:"minecraft:armorer",level:5,type:"minecraft:plains"},Offers:{Recipes:[]}}
$summon interaction $(x) $(y) $(z) {Tags:["nx.shop_npc","nx.$(team)"],width:1.2f,height:2.2f,response:1b}
