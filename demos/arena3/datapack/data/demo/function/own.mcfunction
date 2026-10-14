$scoreboard players set @s nx.ar_own $(o)
scoreboard players operation @s nx.ar_cap = #capture nx.arena
execute if score @s nx.ar_own matches 2 run scoreboard players operation @s nx.ar_cap *= #-1 nx.arena
scoreboard players set @s nx.ar_st -1
