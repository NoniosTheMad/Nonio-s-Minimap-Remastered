tag @s remove nx.coinbag_new
scoreboard players operation @s coins = #drop nx.purse
execute store result storage nonios:purse bag.n int 1 run scoreboard players get @s coins
function nonios:purse/bag/name with storage nonios:purse bag
