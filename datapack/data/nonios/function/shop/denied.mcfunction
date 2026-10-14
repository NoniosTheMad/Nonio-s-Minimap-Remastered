dialog clear @s
playsound minecraft:entity.villager.no master @s ~ ~ ~ 1 1
execute if entity @e[type=interaction,tag=nx.shop_npc,distance=..6] run return run tellraw @s {"text":"This is the other team's shopkeeper. Shop at your own base.","color":"red"}
tellraw @s {"text":"Talk to your team's shopkeeper (the villager at your base) to shop.","color":"red"}
