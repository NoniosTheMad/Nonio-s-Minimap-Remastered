# as a held node marker, macro (its data): count its bonus for the holding team
$execute if score @s nx.ar_own matches 1 run scoreboard players add #$(bonus)_white nx.arena 1
$execute if score @s nx.ar_own matches 2 run scoreboard players add #$(bonus)_black nx.arena 1
