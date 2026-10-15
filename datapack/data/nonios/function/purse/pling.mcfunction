# as a player whose purse just grew (purse/changed): one coin sound if it crossed a multiple of the step
# step = 10^floor(log10(gathered / 100)), at least 1 (gathered = nx.earned this match): under 1000 every coin,
# 1000-9999 every 10, 10000-99999 every 100, and so on. Every purse gain (ores, talisman, kills, bags, withdrawals) passes here.
scoreboard players set #pst nx.purse 1
execute if score @s nx.earned matches 1000.. run scoreboard players set #pst nx.purse 10
execute if score @s nx.earned matches 10000.. run scoreboard players set #pst nx.purse 100
execute if score @s nx.earned matches 100000.. run scoreboard players set #pst nx.purse 1000
execute if score @s nx.earned matches 1000000.. run scoreboard players set #pst nx.purse 10000
scoreboard players operation #pa nx.purse = @s nx.coins
scoreboard players operation #pa nx.purse /= #pst nx.purse
scoreboard players operation #pb nx.purse = @s nx.plast
scoreboard players operation #pb nx.purse /= #pst nx.purse
execute if score #pa nx.purse > #pb nx.purse at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.35 1.7
