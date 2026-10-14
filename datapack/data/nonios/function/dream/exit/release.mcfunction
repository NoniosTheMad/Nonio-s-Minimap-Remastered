execute if score @s nx.dch matches 10.. run title @s actionbar {"text":"...you drift back into the dream.","color":"dark_green","italic":true}
execute if score @s nx.dch matches 1..9 run title @s actionbar ""
scoreboard players set @s nx.dch 0
