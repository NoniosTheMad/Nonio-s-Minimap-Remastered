# only Black inside: progress toward -capture, faster with more capturers (up to max_mult)
scoreboard players operation #m nx.arena = #b nx.arena
scoreboard players operation #m nx.arena < #max_mult nx.arena
scoreboard players operation #m nx.arena *= #step nx.arena
scoreboard players operation @s nx.ar_cap -= #m nx.arena
scoreboard players operation @s nx.ar_cap > #ncap nx.arena
scoreboard players set #st nx.arena 2
execute if score @s nx.ar_own matches 1 run scoreboard players set #st nx.arena 7
execute if score @s nx.ar_own matches 2 if score @s nx.ar_cap <= #ncap nx.arena run scoreboard players set #st nx.arena 5
