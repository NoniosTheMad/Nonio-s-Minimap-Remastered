# #t nx.purse = new mining income; settle nx.pdebt from it first
scoreboard players operation #r nx.purse = #t nx.purse
scoreboard players operation #r nx.purse < @s nx.pdebt
scoreboard players operation #t nx.purse -= #r nx.purse
scoreboard players operation @s nx.pdebt -= #r nx.purse
