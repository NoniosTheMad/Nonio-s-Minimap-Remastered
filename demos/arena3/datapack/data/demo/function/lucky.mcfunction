function nonios:generator/lucky/toggle
execute if score #lucky nx.gen matches 1 run tellraw @s {"text":"[demo] Lucky block ON: 1 in 15 regrowths (yellow glazed terracotta).","color":"yellow"}
execute if score #lucky nx.gen matches 0 run tellraw @s {"text":"[demo] Lucky block OFF.","color":"yellow"}
