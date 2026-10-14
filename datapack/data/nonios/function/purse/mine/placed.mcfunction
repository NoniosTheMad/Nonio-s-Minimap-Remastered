# placing a coin block costs its value back (no silk-touch place/mine farming).
# What the purse can't cover becomes debt (nx.pdebt), paid first out of the next mining income, so a broke player
# can't place + mine the same block for free coins.
$scoreboard players operation #t nx.purse = @s nx.pl.$(b)
$scoreboard players operation #t nx.purse *= #$(b) nx.coinval
scoreboard players operation @s nx.coins -= #t nx.purse
scoreboard players operation @s nx.mined -= #t nx.purse
$scoreboard players set @s nx.pl.$(b) 0
execute if score @s nx.coins matches 0.. run return 0
scoreboard players operation @s nx.pdebt -= @s nx.coins
scoreboard players set @s nx.coins 0
