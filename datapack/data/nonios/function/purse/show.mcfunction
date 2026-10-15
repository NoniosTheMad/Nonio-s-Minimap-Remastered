# the coin line on the actionbar: Coins <whole><.fraction in light blue> [+gain popup] [weight]
# A Barrier message owns the actionbar for ~2 s (nx.ab_hold = gametime until which the coin display pauses).
execute if score @s nx.ab_hold >= #now nx.purse run return 0
data modify storage nonios:purse hud set value {f:"",g:"",w:""}
# fraction (hundredths): .4 / .05 / .14, nothing when 0
scoreboard players add @s nx.pfrac 0
execute if score @s nx.pfrac matches 1.. run function nonios:purse/hud/num_store {src:"@s nx.pfrac"}
execute if score @s nx.pfrac matches 1.. run function nonios:purse/hud/frac with storage nonios:purse hn
# gain popup: whole part + fraction, colour by frame (bright -> gold -> dim)
execute if score @s nx.ptime matches 1.. if score @s nx.pgain matches 1.. run function nonios:purse/hud/gain_prep
# weight
execute if score @s nx.pslow matches 1.. run function nonios:purse/hud/weight_prep
execute store result storage nonios:purse hud.c int 1 run scoreboard players get @s nx.coins
function nonios:purse/hud/draw with storage nonios:purse hud
