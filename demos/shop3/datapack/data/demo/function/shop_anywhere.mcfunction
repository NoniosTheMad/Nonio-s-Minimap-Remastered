# toggle: the shop opens away from the keeper too (game check shop/allowed honours nx.shop_anywhere); opens it now
execute if entity @s[tag=nx.shop_anywhere] run return run function demo:say {m:"Shop only at your keeper again",cmd:"tag @s remove nx.shop_anywhere"}
tag @s add nx.shop_anywhere
scoreboard players set @s nx.shop 1
tellraw @s {"text":"[demo] Shop works anywhere for you (toggle again to undo).","color":"yellow"}
