# as/at a player who used /trigger nx.shop (codes: shop/load). Only next to their own team's shopkeeper.
scoreboard players operation #v nx.tmp = @s nx.shop
scoreboard players reset @s nx.shop
execute unless function nonios:shop/allowed run return run function nonios:shop/denied
scoreboard players add @s nx.coins 0
data remove storage nonios:shop ui.msg
scoreboard players set #noopen nx.tmp 0
scoreboard players set #again nx.tmp 0
execute if score #v nx.tmp matches 1 run function nonios:shop/nav/go {j:0,p:0}
execute if score #v nx.tmp matches 2 run function nonios:shop/again
execute if score #v nx.tmp matches 3 run scoreboard players remove @s nx.shop_pg 1
execute if score #v nx.tmp matches 4 run scoreboard players add @s nx.shop_pg 1
execute if score #v nx.tmp matches 5 run function nonios:shop/nav/up
execute if score #v nx.tmp matches 6..9 run function nonios:shop/nav/mode
execute if score #v nx.tmp matches 11..99 run function nonios:shop/nav/node
execute if score #v nx.tmp matches 100.. run function nonios:shop/buy
# a purchase that opened its own dialog (class confirmation) keeps it on screen
execute if score #noopen nx.tmp matches 1 run return 0
function nonios:shop/open
