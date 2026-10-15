# #nonios:dream/on_enter (as the player, landed): remember which match and team their way back belongs to
scoreboard players operation @s nx.dmatch = #match nx.state
scoreboard players set @s nx.dteam 0
execute if entity @s[team=white] run scoreboard players set @s nx.dteam 1
execute if entity @s[team=black] run scoreboard players set @s nx.dteam 2
