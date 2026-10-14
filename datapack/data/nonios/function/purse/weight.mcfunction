# speed penalty (permille) = min(coins * w_num / w_den, w_cap), applied as a movement_speed modifier
scoreboard players operation @s nx.pslow = @s coins
scoreboard players operation @s nx.pslow *= #w_num nx.purse
scoreboard players operation @s nx.pslow /= #w_den nx.purse
scoreboard players operation @s nx.pslow < #w_cap nx.purse
execute if score @s nx.pslow matches ..0 run return run attribute @s minecraft:movement_speed modifier remove nonios:purse_weight
execute store result storage nonios:purse w.v double -0.001 run scoreboard players get @s nx.pslow
function nonios:purse/weight_apply with storage nonios:purse w
