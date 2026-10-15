# #v nx.tmp = 100 + index into storage nonios:shop items; #again 1 = repeat the last purchase's quantity
data remove storage nonios:shop sel
scoreboard players remove #v nx.tmp 100
execute store result storage nonios:shop arg.i int 1 run scoreboard players get #v nx.tmp
function nonios:shop/pick with storage nonios:shop arg
execute unless data storage nonios:shop sel run return run function nonios:shop/msg {m:"✘ Not sold any more",c:"red"}
function nonios:shop/lots {p:"sel"}
# classes (class/gen/shop_items): no inventory slot needed, applied instead of given
execute if data storage nonios:shop sel.class run return run function nonios:shop/buy_class with storage nonios:shop sel
# specials (src/specials.json): their own charge/slot rules, then their buy function
execute if data storage nonios:shop sel{kind:"special"} run return run function nonios:shop/buy_special with storage nonios:shop sel
function nonios:shop/total
execute if score @s nx.coins < #p nx.tmp run return run function nonios:shop/broke
# enchant the held item / experience levels: no slot needed
execute if data storage nonios:shop sel{kind:"enchant"} run return run function nonios:shop/buy_enchant with storage nonios:shop sel
execute if data storage nonios:shop sel{kind:"xp"} run return run function nonios:shop/buy_xp
# items: as many lots as fit in the empty slots (stacks you already carry are not counted); none fit = nothing taken
function nonios:shop/fit
execute if score #fit nx.tmp matches ..0 run return run function nonios:shop/full
scoreboard players set #part nx.tmp 0
execute if score #lots nx.tmp > #fit nx.tmp run scoreboard players set #part nx.tmp 1
execute if score #part nx.tmp matches 1 run scoreboard players operation #lots nx.tmp = #fit nx.tmp
execute if score #part nx.tmp matches 1 run function nonios:shop/total
scoreboard players operation @s nx.coins -= #p nx.tmp
function nonios:gear/give with storage nonios:shop sel
function nonios:shop/paid
execute if score #part nx.tmp matches 1 run data modify storage nonios:shop ui.msg append value {text:" · bag full",color:"red"}
