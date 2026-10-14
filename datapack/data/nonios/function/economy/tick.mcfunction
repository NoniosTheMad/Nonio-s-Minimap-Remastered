# bank dialog clicks (/trigger). Handlers reset only the triggerer; enable @a last (never 'reset @a' after this).
execute as @a[scores={nx.bankt=1..}] at @s run function nonios:bank/act
execute as @a[scores={nx.bankd=1..}] at @s run function nonios:bank/act
execute as @a[scores={nx.bankw=1..}] at @s run function nonios:bank/act
scoreboard players enable @a nx.bankt
scoreboard players enable @a nx.bankd
scoreboard players enable @a nx.bankw
# kill reward actionbar (a tick after the kill: kill reward + bounty + bonus + the purse taken, in one line)
execute as @a[tag=nx.k.show] run function nonios:economy/kill/show
# once a second: team bank sidebar (prep + battle), hidden outside a match
scoreboard players add #etick nx.eco 1
scoreboard players operation #es nx.eco = #etick nx.eco
scoreboard players operation #es nx.eco %= #20 nx.eco
execute if score #es nx.eco matches 0 run function nonios:economy/hud/second
