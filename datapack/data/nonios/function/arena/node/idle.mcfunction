# nobody inside: drift back to the owner's full value, or toward 0 when unowned
execute if score @s nx.ar_own matches 1 run scoreboard players operation @s nx.ar_cap += #decay nx.arena
execute if score @s nx.ar_own matches 1 run scoreboard players operation @s nx.ar_cap < #capture nx.arena
execute if score @s nx.ar_own matches 2 run scoreboard players operation @s nx.ar_cap -= #decay nx.arena
execute if score @s nx.ar_own matches 2 run scoreboard players operation @s nx.ar_cap > #ncap nx.arena
execute if score @s nx.ar_own matches 0 if score @s nx.ar_cap matches 1.. run function nonios:arena/node/decay_pos
execute if score @s nx.ar_own matches 0 if score @s nx.ar_cap matches ..-1 run function nonios:arena/node/decay_neg
execute if score @s nx.ar_own matches 1 run scoreboard players set #st nx.arena 4
execute if score @s nx.ar_own matches 2 run scoreboard players set #st nx.arena 5
