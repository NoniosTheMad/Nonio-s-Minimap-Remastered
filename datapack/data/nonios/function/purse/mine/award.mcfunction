$scoreboard players operation #t nx.purse = @s nx.mn.$(b)
$scoreboard players operation #t nx.purse *= #$(b) nx.coinval
scoreboard players operation @s nx.coins += #t nx.purse
scoreboard players operation @s nx.mined += #t nx.purse
$scoreboard players set @s nx.mn.$(b) 0
