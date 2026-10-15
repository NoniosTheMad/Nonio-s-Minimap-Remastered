# as each player, every tick (deaths are handled by nonios:death, once the player has respawned)
execute unless score @s nx.coins = @s nx.coins run scoreboard players set @s nx.coins 0
function nonios:purse/gen/check
execute if score @s nx.coins matches ..-1 run scoreboard players set @s nx.coins 0
# purse gains, fractions included (+0.1 coal): the "+N" popup on the coin line (purse/gain, nx.ptime frames)
function nonios:purse/gain
execute unless score @s nx.coins = @s nx.plast run return run function nonios:purse/changed
execute if score @s nx.ptime matches 0.. run return run function nonios:purse/show
execute if score #ab nx.purse matches 0 if score @s nx.coins matches 1.. run return run function nonios:purse/show
execute if score #ab nx.purse matches 0 if score @s nx.pfrac matches 1.. run function nonios:purse/show
