# {b}: placing a coin block costs its value at the best Fortune (#place_mult nx.coinval, percent), so silk-touch an ore,
# place it and mine it again with Fortune earns nothing. Taken from nx.pfrac first, then whole coins from the purse;
# what the purse can't cover becomes debt (nx.pdebt), paid first out of the next mining income.
$scoreboard players operation #t nx.purse = @s nx.pl.$(b)
$scoreboard players operation #t nx.purse *= #$(b) nx.coinval
$scoreboard players set @s nx.pl.$(b) 0
scoreboard players operation #t nx.purse *= #place_mult nx.coinval
scoreboard players operation #t nx.purse /= #100 nx.purse
scoreboard players add @s nx.pfrac 0
scoreboard players operation @s nx.pfrac -= #t nx.purse
execute if score @s nx.pfrac matches 0.. run return 0
# whole coins to take = ceil(-pfrac / 100)
scoreboard players operation #t nx.purse = @s nx.pfrac
scoreboard players operation #t nx.purse *= #-1 nx.purse
scoreboard players add #t nx.purse 99
scoreboard players operation #t nx.purse /= #100 nx.purse
scoreboard players operation #r nx.purse = #t nx.purse
scoreboard players operation #r nx.purse *= #100 nx.purse
scoreboard players operation @s nx.pfrac += #r nx.purse
scoreboard players operation @s nx.coins -= #t nx.purse
scoreboard players operation @s nx.mined -= #t nx.purse
execute if score @s nx.coins matches 0.. run return 0
scoreboard players operation @s nx.pdebt -= @s nx.coins
scoreboard players set @s nx.coins 0
