# as the buyer; sel = a special {name,label,price,fn,charge,slot} (src/specials.json via tools/build_shop.py).
# charge 0 = the shop takes nothing and fn decides everything; otherwise the usual purse + free-slot checks, then fn gives it.
$execute if data storage nonios:shop sel{charge:0} run return run function $(fn)
execute store result score #p nx.tmp run data get storage nonios:shop sel.price
execute if score @s nx.coins < #p nx.tmp run return run function nonios:shop/broke
scoreboard players set #fit nx.tmp 1
execute if data storage nonios:shop sel{slot:1} run function nonios:shop/fit
execute if score #fit nx.tmp matches ..0 run return run function nonios:shop/full
scoreboard players operation @s nx.coins -= #p nx.tmp
$function $(fn)
function nonios:shop/paid
