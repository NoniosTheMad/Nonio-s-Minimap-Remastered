# repeat the last purchase (same item, same quantity)
execute unless score @s nx.shop_last matches 1.. run return 0
scoreboard players operation #v nx.tmp = @s nx.shop_last
scoreboard players add #v nx.tmp 99
scoreboard players set #again nx.tmp 1
function nonios:shop/buy
