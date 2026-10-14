# as/at a player who used /trigger nx.shop (NPC click sets it to 1). Only next to their own team's shopkeeper.
scoreboard players operation #v nx.tmp = @s nx.shop
scoreboard players reset @s nx.shop
execute unless function nonios:shop/allowed run return run function nonios:shop/denied
scoreboard players add @s nx.coins 0
data remove storage nonios:shop ui.msg
execute if score #v nx.tmp matches 100.. run function nonios:shop/buy
function nonios:shop/open
