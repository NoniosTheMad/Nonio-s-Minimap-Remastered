# every interest tick (bank/interest/tick, after economy/rate): #tacc nx.talis += price x #ppm x talisman_mult, the
# talisman's own interest this tick (same units as the bank: 1 coin = #ithr). Each #tth (= #ithr / 10) in it pays every
# head-wearing holder 0.1 coin. One accumulator for all: the rate is the same for everyone.
execute store result score #tv nx.talis run data get storage nonios:shop items[{name:"Emerald Talisman"}].price
execute unless score #tv nx.talis matches 1.. run scoreboard players set #tv nx.talis 200
execute store result score #tm nx.talis run data get storage nonios:config talisman_mult
scoreboard players operation #tv nx.talis *= #tm nx.talis
scoreboard players operation #tv nx.talis *= #ppm nx.eco
scoreboard players operation #tacc nx.talis += #tv nx.talis
scoreboard players operation #ts nx.talis = #tacc nx.talis
scoreboard players operation #ts nx.talis /= #tth nx.eco
scoreboard players operation #tacc nx.talis %= #tth nx.eco
execute if score #ts nx.talis matches ..0 run return 0
scoreboard players operation #ts nx.talis *= #10 nx.talis
execute as @a[gamemode=!spectator] if items entity @s armor.head *[minecraft:custom_data~{nx_talisman:1b}] run function nonios:talisman/pay
