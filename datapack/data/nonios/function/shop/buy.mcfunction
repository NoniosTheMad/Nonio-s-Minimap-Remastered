# #v nx.tmp = 100 + index into storage nonios:shop items
data remove storage nonios:shop sel
scoreboard players remove #v nx.tmp 100
execute store result storage nonios:shop arg.i int 1 run scoreboard players get #v nx.tmp
function nonios:shop/pick with storage nonios:shop arg
execute unless data storage nonios:shop sel run return run data modify storage nonios:shop ui.msg set value {type:"minecraft:plain_message",width:300,contents:{text:"✘ That item is no longer sold.",color:"red"}}
execute store result score #p nx.tmp run data get storage nonios:shop sel.price
execute if score @s nx.coins < #p nx.tmp run return run function nonios:shop/broke
# full inventory: refuse, take nothing (user, 2026-10-14)
execute unless function nonios:shop/has_space run return run function nonios:shop/full
scoreboard players operation @s nx.coins -= #p nx.tmp
function nonios:shop/give with storage nonios:shop sel
playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 1 1.2
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 0.6 1
function nonios:shop/msg_bought with storage nonios:shop sel
