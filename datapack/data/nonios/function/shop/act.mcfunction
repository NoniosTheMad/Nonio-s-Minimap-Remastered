# as/at a player who used /trigger nx.shop (NPC click sets it to 1). Only next to their own team's shopkeeper.
scoreboard players operation #v nx.tmp = @s nx.shop
scoreboard players reset @s nx.shop
execute unless function nonios:shop/allowed run return run function nonios:shop/denied
scoreboard players add @s nx.coins 0
data remove storage nonios:shop ui.msg
scoreboard players set #noopen nx.tmp 0
execute if score #v nx.tmp matches 1 run scoreboard players set @s nx.shop_sec 0
execute if score #v nx.tmp matches 10..99 run function nonios:shop/go
execute if score #v nx.tmp matches 100.. run function nonios:shop/buy
# a purchase that opened its own dialog (class confirmation) keeps it on screen
execute if score #noopen nx.tmp matches 1 run return 0
function nonios:shop/open
