# as each player, every tick
execute unless score @s coins = @s coins run scoreboard players set @s coins 0
function nonios:purse/mine/check
execute if score @s nx.died matches 1.. run function nonios:purse/death/died
execute if score @s coins matches ..-1 run scoreboard players set @s coins 0
execute unless score @s coins = @s nx.plast run return run function nonios:purse/changed
execute if score #ab nx.purse matches 0 if score @s coins matches 1.. run function nonios:purse/show
