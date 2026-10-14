# placing a coin block costs its value back (no silk-touch place/mine farming)
$scoreboard players operation #t nx.purse = @s nx.pl.$(b)
$scoreboard players operation #t nx.purse *= #$(b) nx.coinval
scoreboard players operation @s nx.coins -= #t nx.purse
scoreboard players operation @s nx.mined -= #t nx.purse
$scoreboard players set @s nx.pl.$(b) 0
