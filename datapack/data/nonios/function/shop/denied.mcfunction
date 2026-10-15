dialog clear @s
playsound minecraft:entity.villager.no master @s ~ ~ ~ 1 1
execute if entity @e[type=interaction,tag=nx.shop_npc,distance=..6] run return run tellraw @s {"text":"Not your shopkeeper.","color":"red"}
tellraw @s {"text":"No shopkeeper here.","color":"red"}
