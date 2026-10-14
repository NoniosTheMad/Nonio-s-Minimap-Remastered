# from game/start: fresh streaks, interest remainders and interest clock for the new match (team banks are reset by game/start)
scoreboard players set @a nx.streak 0
scoreboard players set @a nx.krw 0
scoreboard players set @a nx.kbty 0
scoreboard players set @a nx.kbon 0
scoreboard players set @a nx.kpurse 0
tag @a remove nx.k.show
tag @a remove nx.k.done
scoreboard players set #acc_white nx.eco 0
scoreboard players set #acc_black nx.eco 0
function nonios:bank/interest/arm
# match clock (money scale + interest growth); last payouts for the sidebar
execute store result score #t0 nx.eco run time query gametime
scoreboard players set #last_white nx.eco 0
scoreboard players set #last_black nx.eco 0
scoreboard players set #capped_white nx.eco 0
scoreboard players set #capped_black nx.eco 0
