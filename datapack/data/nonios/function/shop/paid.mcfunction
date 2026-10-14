# after a purchase went through (#p taken from the purse; sel.q / sel.tot set by shop/total). Remembered for "buy again".
playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 1 1.2
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 0.6 1
execute store result score @s nx.shop_last run data get storage nonios:shop arg.i
scoreboard players add @s nx.shop_last 1
scoreboard players operation @s nx.shop_lastl = #lots nx.tmp
execute unless data storage nonios:shop sel.q run data modify storage nonios:shop sel.q set value 1
execute unless data storage nonios:shop sel.tot run data modify storage nonios:shop sel.tot set from storage nonios:shop sel.price
execute if data storage nonios:shop sel{q:1} run function nonios:shop/msg_bought1 with storage nonios:shop sel
execute unless data storage nonios:shop sel{q:1} run function nonios:shop/msg_bought with storage nonios:shop sel
execute if data storage nonios:shop sel.chat run function nonios:shop/chat with storage nonios:shop sel
