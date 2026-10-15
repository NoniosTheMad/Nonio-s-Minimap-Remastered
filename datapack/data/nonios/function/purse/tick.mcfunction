scoreboard players add #tick nx.purse 1
scoreboard players operation #ab nx.purse = #tick nx.purse
scoreboard players operation #ab nx.purse %= #ab_every nx.purse
execute store result score #now nx.purse run time query gametime
scoreboard players operation #sec nx.purse = #tick nx.purse
scoreboard players operation #sec nx.purse %= #20 nx.purse
execute if score #sec nx.purse matches 0 run function nonios:purse/scale
execute as @a run function nonios:purse/player
execute as @e[type=item,tag=nx.coinbag] at @s run function nonios:purse/bag/tick
