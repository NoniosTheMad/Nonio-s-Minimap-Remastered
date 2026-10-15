# {team, Team, color}: as the player at their own vault. #b nx.eco = working copy of the team bank, written back at the end.
# #bt 3 = all, 4 = half (rounded up); #bw = a preset amount. Then the dialog is drawn again with the new balances.
$scoreboard players add #$(team) nx.bank 0
$scoreboard players operation #b nx.eco = #$(team) nx.bank
execute if score #bt nx.eco matches 3 run scoreboard players operation #bw nx.eco = #b nx.eco
execute if score #bt nx.eco matches 4 run scoreboard players operation #bw nx.eco = #b nx.eco
execute if score #bt nx.eco matches 4 run scoreboard players add #bw nx.eco 1
execute if score #bt nx.eco matches 4 run scoreboard players operation #bw nx.eco /= #2 nx.eco
execute if score #bt nx.eco matches 3..4 if score #bw nx.eco matches ..0 run scoreboard players set #bw nx.eco -1
execute unless score #bw nx.eco matches 0 run function nonios:bank/withdraw
$scoreboard players operation #$(team) nx.bank = #b nx.eco
$function nonios:bank/open {team:"$(team)",Team:"$(Team)",color:"$(color)"}
