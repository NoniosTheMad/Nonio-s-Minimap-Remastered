# as a player: #pst nx.purse = the coin step for sounds and the gain popup (#113, #114):
# 10^floor(log10(nx.earned / 100)), at least 1: under 1000 gathered 1, 1000+ 10, 10000+ 100, ...
scoreboard players set #pst nx.purse 1
execute if score @s nx.earned matches 1000.. run scoreboard players set #pst nx.purse 10
execute if score @s nx.earned matches 10000.. run scoreboard players set #pst nx.purse 100
execute if score @s nx.earned matches 100000.. run scoreboard players set #pst nx.purse 1000
execute if score @s nx.earned matches 1000000.. run scoreboard players set #pst nx.purse 10000
