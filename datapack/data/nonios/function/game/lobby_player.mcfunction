# as a player: back to the lobby, clean
gamemode adventure @s
function nonios:class/reset
# the shop reopens on its first page next match
scoreboard players set @s nx.shop_sec 0
scoreboard players set @s nx.shop_pg 0
clear @s
effect clear @s
scoreboard players set @s nx.coins 0
scoreboard players set @s nx.plast -1
scoreboard players set @s nx.pdebt 0
attribute @s minecraft:movement_speed modifier remove nonios:purse_weight
function nonios:game/tp_lobby with storage nonios:map lobby
