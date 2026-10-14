# as a player: back to the lobby, clean
gamemode adventure @s
clear @s
effect clear @s
scoreboard players set @s nx.coins 0
scoreboard players set @s nx.plast -1
attribute @s minecraft:movement_speed modifier remove nonios:purse_weight
function nonios:game/tp_lobby with storage nonios:map lobby
