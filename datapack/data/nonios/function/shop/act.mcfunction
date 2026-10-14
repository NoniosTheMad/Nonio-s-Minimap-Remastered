# as a player who used /trigger nx.shop
scoreboard players operation #v nx.tmp = @s nx.shop
scoreboard players reset @s nx.shop
scoreboard players add @s nx.coins 0
data remove storage nonios:shop ui.msg
execute if score #v nx.tmp matches 100.. run function nonios:shop/buy
function nonios:shop/open
