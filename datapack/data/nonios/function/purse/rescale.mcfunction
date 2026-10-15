# {team}: the player's money scale changed: reweigh (and redraw the actionbar if it shows a weight)
scoreboard players set @s nx.pscale 100
$execute if score #s_$(team) nx.purse = #s_$(team) nx.purse run scoreboard players operation @s nx.pscale = #s_$(team) nx.purse
function nonios:purse/weight
execute if score @s nx.coins matches 1.. run function nonios:purse/show
