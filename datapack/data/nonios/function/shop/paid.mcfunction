# after a purchase went through (#p nx.tmp already taken from the purse)
playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 1 1.2
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 0.6 1
function nonios:shop/msg_bought with storage nonios:shop sel
execute if data storage nonios:shop sel.chat run function nonios:shop/chat with storage nonios:shop sel
