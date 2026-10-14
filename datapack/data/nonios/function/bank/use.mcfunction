# {team, Team, color}: as the player at their own vault. #b nx.eco = working copy of the team bank, written back at the end.
$scoreboard players add #$(team) nx.bank 0
$scoreboard players operation #b nx.eco = #$(team) nx.bank
execute if score #bt nx.eco matches 2 run scoreboard players operation #bd nx.eco = @s nx.coins
execute if score #bt nx.eco matches 3 run scoreboard players operation #bw nx.eco = #b nx.eco
execute if score #bt nx.eco matches 2 run function nonios:bank/deposit
execute if score #bd nx.eco matches 1.. unless score #bt nx.eco matches 2 run function nonios:bank/deposit
execute if score #bt nx.eco matches 3 run function nonios:bank/withdraw
execute if score #bw nx.eco matches 1.. unless score #bt nx.eco matches 3 run function nonios:bank/withdraw
$scoreboard players operation #$(team) nx.bank = #b nx.eco
$function nonios:bank/open {team:"$(team)",Team:"$(Team)",color:"$(color)"}
