# #p = total price > purse
scoreboard players operation #need nx.tmp = #p nx.tmp
scoreboard players operation #need nx.tmp -= @s nx.coins
execute store result storage nonios:shop sel.need int 1 run scoreboard players get #need nx.tmp
function nonios:shop/msg_broke with storage nonios:shop sel
playsound minecraft:entity.villager.no master @s ~ ~ ~ 1 1
