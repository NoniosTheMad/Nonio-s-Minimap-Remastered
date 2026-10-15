# hud.w = the weight part of the coin line (red at the cap)
scoreboard players operation #pct nx.purse = @s nx.pslow
scoreboard players operation #pct nx.purse /= #10 nx.purse
execute store result storage nonios:purse hn.pct int 1 run scoreboard players get #pct nx.purse
execute if score @s nx.pslow >= #w_cap nx.purse run return run function nonios:purse/hud/weight with storage nonios:purse hn
function nonios:purse/hud/weight_low with storage nonios:purse hn
