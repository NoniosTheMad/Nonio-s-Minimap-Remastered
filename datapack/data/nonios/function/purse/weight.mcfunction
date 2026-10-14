# speed penalty (permille) = min(max(coins * 100 / S - w_free, 0) * w_num / w_den, w_cap), applied as a movement_speed
# modifier. S = the money scale of the player's team (nx.pscale, purse/scale): coins weigh less as the match goes on.
execute unless score @s nx.pscale matches 100.. run scoreboard players set @s nx.pscale 100
scoreboard players operation @s nx.pslow = @s nx.coins
scoreboard players operation @s nx.pslow *= #100 nx.purse
scoreboard players operation @s nx.pslow /= @s nx.pscale
scoreboard players operation @s nx.pslow -= #w_free nx.purse
scoreboard players operation @s nx.pslow *= #w_num nx.purse
scoreboard players operation @s nx.pslow /= #w_den nx.purse
scoreboard players operation @s nx.pslow < #w_cap nx.purse
execute if score @s nx.pslow matches ..0 run return run attribute @s minecraft:movement_speed modifier remove nonios:purse_weight
execute store result storage nonios:purse w.v double -0.001 run scoreboard players get @s nx.pslow
function nonios:purse/weight_apply with storage nonios:purse w
