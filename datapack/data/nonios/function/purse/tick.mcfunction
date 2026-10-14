scoreboard players add #tick nx.purse 1
scoreboard players operation #ab nx.purse = #tick nx.purse
scoreboard players operation #ab nx.purse %= #ab_every nx.purse
execute store result score #now nx.purse run time query gametime
execute as @a run function nonios:purse/player
execute as @e[type=item,tag=nx.coinbag] at @s run function nonios:purse/bag/tick
# team bank: standing within 2.5 blocks of your own team's bank pad (marker nx.bank_zone + nx.<team>) deposits the whole purse
execute as @e[type=marker,tag=nx.bank_zone] at @s as @a[distance=..2.5,gamemode=!spectator,scores={nx.coins=1..}] run function nonios:purse/bank/try
