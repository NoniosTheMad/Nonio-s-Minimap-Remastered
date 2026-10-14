# #v nx.tmp = 100 + index into storage nonios:shop items
data remove storage nonios:shop sel
scoreboard players remove #v nx.tmp 100
execute store result storage nonios:shop arg.i int 1 run scoreboard players get #v nx.tmp
function nonios:shop/pick with storage nonios:shop arg
execute unless data storage nonios:shop sel run return run data modify storage nonios:shop ui.msg set value {type:"minecraft:plain_message",width:300,contents:{text:"✘ That item is no longer sold.",color:"red"}}
# classes (class/gen/shop_items): no inventory slot needed, applied instead of given
execute if data storage nonios:shop sel.class run return run function nonios:shop/buy_class with storage nonios:shop sel
execute store result score #p nx.tmp run data get storage nonios:shop sel.price
execute if score @s nx.coins < #p nx.tmp run return run function nonios:shop/broke
# enchant the held item / experience levels: no slot needed
execute if data storage nonios:shop sel{kind:"enchant"} run return run function nonios:shop/buy_enchant with storage nonios:shop sel
execute if data storage nonios:shop sel{kind:"xp"} run return run function nonios:shop/buy_xp with storage nonios:shop sel
# full inventory: refuse, take nothing (user, 2026-10-14)
execute unless function nonios:shop/has_space run return run function nonios:shop/full
scoreboard players operation @s nx.coins -= #p nx.tmp
function nonios:shop/give with storage nonios:shop sel
function nonios:shop/paid
