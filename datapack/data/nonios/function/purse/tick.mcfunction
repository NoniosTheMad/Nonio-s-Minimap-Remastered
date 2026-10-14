scoreboard players add #tick nx.purse 1
scoreboard players operation #ab nx.purse = #tick nx.purse
scoreboard players operation #ab nx.purse %= #ab_every nx.purse
execute as @a run function nonios:purse/player
execute as @e[type=item,tag=nx.coinbag] at @s run function nonios:purse/bag/tick
# bank stub: standing within 2.5 blocks of a marker tagged nx.bank_zone deposits the whole purse
execute as @e[type=marker,tag=nx.bank_zone] at @s as @e[type=player,distance=..2.5,gamemode=!spectator,scores={coins=1..}] run function nonios:purse/bank/deposit
