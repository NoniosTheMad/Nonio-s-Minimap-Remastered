# as a holder: #ts nx.talis hundredths of a coin into the purse (fraction first, whole coins carried over)
scoreboard players add @s nx.pfrac 0
scoreboard players operation @s nx.pfrac += #ts nx.talis
scoreboard players operation #tw nx.talis = @s nx.pfrac
scoreboard players operation #tw nx.talis /= #100 nx.talis
scoreboard players operation @s nx.coins += #tw nx.talis
scoreboard players operation @s nx.pfrac %= #100 nx.talis
