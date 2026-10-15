# as each player, every tick (deaths are handled by nonios:death, once the player has respawned)
execute unless score @s nx.coins = @s nx.coins run scoreboard players set @s nx.coins 0
function nonios:purse/gen/check
execute if score @s nx.coins matches ..-1 run scoreboard players set @s nx.coins 0
execute unless score @s nx.coins = @s nx.plast run return run function nonios:purse/changed
execute if score #ab nx.purse matches 0 if score @s nx.coins matches 1.. run function nonios:purse/show
