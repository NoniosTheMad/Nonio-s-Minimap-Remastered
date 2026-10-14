# only White inside: progress toward +capture, faster with more capturers (up to max_mult)
scoreboard players operation #m nx.arena = #w nx.arena
scoreboard players operation #m nx.arena < #max_mult nx.arena
scoreboard players operation #m nx.arena *= #step nx.arena
scoreboard players operation @s nx.ar_cap += #m nx.arena
scoreboard players operation @s nx.ar_cap < #capture nx.arena
scoreboard players set #st nx.arena 1
execute if score @s nx.ar_own matches 2 run scoreboard players set #st nx.arena 6
execute if score @s nx.ar_own matches 1 if score @s nx.ar_cap >= #capture nx.arena run scoreboard players set #st nx.arena 4
