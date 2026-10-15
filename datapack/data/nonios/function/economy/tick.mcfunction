# bank dialog clicks (/trigger). Handlers reset only the triggerer; enable @a last (never 'reset @a' after this).
execute as @a[scores={nx.bankt=1..}] at @s run function nonios:bank/act
execute as @a[scores={nx.bankw=1..}] at @s run function nonios:bank/act
scoreboard players enable @a nx.bankt
scoreboard players enable @a nx.bankw
# kill reward actionbar (a tick after the kill: kill reward + bounty + bonus + the purse taken, in one line)
execute as @a[tag=nx.k.show] run function nonios:economy/kill/show
# once a second: the team bank sidebar (hidden outside a match); #es = tick within the second
scoreboard players add #etick nx.eco 1
scoreboard players operation #es nx.eco = #etick nx.eco
scoreboard players operation #es nx.eco %= #20 nx.eco
# bank zones: entering your own team's zone (walk, jump or fly through) banks the whole purse (prep + battle)
function nonios:bank/zone/tick
# smooth interest every tick (prep + battle, bank v3 #94): +1 coin at a time, same rate per second as before
execute if score #state nx.state matches 1..2 run function nonios:bank/interest/tick
execute if score #es nx.eco matches 0 run function nonios:economy/hud/second
execute if score #hud_on nx.eco matches 1 run function nonios:economy/hud/bank {team:"white"}
execute if score #hud_on nx.eco matches 1 run function nonios:economy/hud/bank {team:"black"}
